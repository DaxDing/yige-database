#!/usr/bin/env bash
set -euo pipefail

# ─── Config ──────────────────────────────────────────────
REGION="cn-hangzhou"
CURRENT_MONTH=$(date +%Y-%m)
YESTERDAY=$(date -v-1d +%Y-%m-%d)
YESTERDAY_MONTH=$(date -v-1d +%Y-%m)

# ─── Auth check ──────────────────────────────────────────
if [[ -z "${ALIYUN_ACCESS_KEY_ID:-}" || -z "${ALIYUN_ACCESS_KEY_SECRET:-}" ]]; then
    echo "ERROR: ALIYUN_ACCESS_KEY_ID and ALIYUN_ACCESS_KEY_SECRET must be set"
    exit 1
fi

AUTH="--access-key-id ${ALIYUN_ACCESS_KEY_ID} --access-key-secret ${ALIYUN_ACCESS_KEY_SECRET} --region ${REGION}"

# ─── Helpers ─────────────────────────────────────────────
aliyun_call() {
    local result
    result=$(aliyun bssopenapi "$@" $AUTH 2>&1)
    local success
    success=$(echo "$result" | jq -r '.Success // empty' 2>/dev/null)
    if [[ "$success" == "false" ]]; then
        local code msg
        code=$(echo "$result" | jq -r '.Code // empty')
        msg=$(echo "$result" | jq -r '.Message // empty')
        echo "ERROR: [$code] $msg" >&2
        exit 1
    fi
    echo "$result"
}

# ─── balance ─────────────────────────────────────────────
cmd_balance() {
    local result
    result=$(aliyun_call QueryAccountBalance)

    local available currency
    available=$(echo "$result" | jq -r '.Data.AvailableAmount // "N/A"')
    currency=$(echo "$result" | jq -r '.Data.Currency // "CNY"')

    echo ""
    echo "=== 阿里云账户余额 ==="
    echo "可用余额: ¥${available}"
    echo "币种: ${currency}"
    echo ""
}

# ─── overview ────────────────────────────────────────────
cmd_overview() {
    local cycle="${1:-$CURRENT_MONTH}"
    local result
    result=$(aliyun_call QueryBillOverview --BillingCycle "$cycle")

    echo ""
    echo "=== 阿里云账单总览 (${cycle}) ==="
    echo ""

    # Extract items and format as table
    local items
    items=$(echo "$result" | jq -r '.Data.Items.Item // []')
    local count
    count=$(echo "$items" | jq 'length')

    if [[ "$count" -eq 0 ]]; then
        echo "无账单数据"
        return
    fi

    # Header
    printf "| %-30s | %12s | %12s | %-10s |\n" "产品" "应付金额" "现金支付" "付费方式"
    printf "|%-32s|%14s|%14s|%-12s|\n" "$(printf '%0.s-' {1..32})" "$(printf '%0.s-' {1..14})" "$(printf '%0.s-' {1..14})" "$(printf '%0.s-' {1..12})"

    # Rows sorted by PretaxAmount descending
    echo "$items" | jq -r '
        sort_by(-.PretaxAmount) |
        .[] |
        select(.PretaxAmount != 0) |
        [
            .ProductName,
            (.PretaxAmount | tostring),
            (.CashAmount | tostring),
            (if .SubscriptionType == "PayAsYouGo" then "按量付费"
             elif .SubscriptionType == "Subscription" then "包年包月"
             else .SubscriptionType end)
        ] | @tsv
    ' | while IFS=$'\t' read -r name amount cash sub_type; do
        printf "| %-30s | %12s | %12s | %-10s |\n" \
            "$name" "¥${amount}" "¥${cash}" "$sub_type"
    done

    # Total
    local total
    total=$(echo "$items" | jq '[.[].PretaxAmount] | add // 0')
    echo ""
    echo "合计: ¥${total}"
    echo ""
}

# ─── detail ──────────────────────────────────────────────
cmd_detail() {
    local cycle="${1:-$YESTERDAY_MONTH}"
    shift 2>/dev/null || true

    local billing_date="" product_code=""

    # Parse optional flags
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --date)
                billing_date="$2"
                shift 2
                ;;
            --product)
                product_code="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done

    # Default to yesterday if no --date specified
    if [[ -z "$billing_date" ]]; then
        billing_date="$YESTERDAY"
    fi

    # Build CLI args
    local args="--BillingCycle ${cycle} --MaxResults 300 --IsHideZeroCharge true"
    args="$args --Granularity DAILY --BillingDate ${billing_date}"

    if [[ -n "$product_code" ]]; then
        args="$args --ProductCode ${product_code}"
    fi

    # Paginated fetch
    local all_items="[]"
    local next_token=""
    local page=0

    while true; do
        page=$((page + 1))
        local page_args="$args"
        if [[ -n "$next_token" ]]; then
            page_args="$page_args --NextToken ${next_token}"
        fi

        local result
        result=$(aliyun_call DescribeInstanceBill $page_args)

        # Merge items
        local page_items
        page_items=$(echo "$result" | jq '.Data.Items // []')
        all_items=$(echo "$all_items $page_items" | jq -s '.[0] + .[1]')

        # Check pagination
        next_token=$(echo "$result" | jq -r '.Data.NextToken // empty')
        if [[ -z "$next_token" || "$next_token" == "null" ]]; then
            break
        fi
        echo "  fetching page ${page}..." >&2
    done

    local count
    count=$(echo "$all_items" | jq 'length')

    local title="${cycle}"
    if [[ -n "$billing_date" ]]; then
        title="${billing_date}"
    fi
    if [[ -n "$product_code" ]]; then
        title="${title} [${product_code}]"
    fi

    echo ""
    echo "=== 阿里云账单明细 (${title}) === [${count} 条]"
    echo ""

    if [[ "$count" -eq 0 ]]; then
        echo "无账单数据"
        return
    fi

    # Header
    printf "| %-24s | %-20s | %12s | %-10s | %-10s |\n" \
        "产品" "实例ID" "应付金额" "日期" "付费方式"
    printf "|%-26s|%-22s|%14s|%-12s|%-12s|\n" \
        "$(printf '%0.s-' {1..26})" "$(printf '%0.s-' {1..22})" \
        "$(printf '%0.s-' {1..14})" "$(printf '%0.s-' {1..12})" "$(printf '%0.s-' {1..12})"

    # Rows sorted by PretaxAmount descending
    echo "$all_items" | jq -r '
        sort_by(-.PretaxAmount) |
        .[] |
        [
            .ProductName,
            (.InstanceID // "-"),
            (.PretaxAmount | tostring),
            (.BillingDate // .BillingItemCode // "-"),
            (if .SubscriptionType == "PayAsYouGo" then "按量付费"
             elif .SubscriptionType == "Subscription" then "包年包月"
             else (.SubscriptionType // "-") end)
        ] | @tsv
    ' | while IFS=$'\t' read -r name instance amount date sub_type; do
        # Truncate long instance IDs
        if [[ ${#instance} -gt 20 ]]; then
            instance="${instance:0:17}..."
        fi
        printf "| %-24s | %-20s | %12s | %-10s | %-10s |\n" \
            "$name" "$instance" "¥${amount}" "$date" "$sub_type"
    done

    # Total
    local total
    total=$(echo "$all_items" | jq '[.[].PretaxAmount] | add // 0')
    echo ""
    echo "合计: ¥${total} (${count} 条记录)"
    echo ""
}

# ─── Main ────────────────────────────────────────────────
cmd="${1:-help}"
shift 2>/dev/null || true

case "$cmd" in
    balance)
        cmd_balance
        ;;
    overview)
        cmd_overview "$@"
        ;;
    detail)
        cmd_detail "$@"
        ;;
    help|*)
        echo ""
        echo "Usage: query_billing.sh <command> [options]"
        echo ""
        echo "Commands:"
        echo "  balance                      查询账户余额"
        echo "  overview [YYYY-MM]           月度账单总览（默认当月）"
        echo "  detail [YYYY-MM] [options]   实例账单明细（默认当月）"
        echo ""
        echo "Options (detail):"
        echo "  --date YYYY-MM-DD            指定日期"
        echo "  --product <code>             按产品过滤 (odps/ecs/rds/oss)"
        echo ""
        ;;
esac
