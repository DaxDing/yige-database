"""填充飞书复合指标表的「中文公式」列"""

import json
import re
import os
import sys
import urllib.request

BASE_URL = "https://open.feishu.cn/open-apis"
APP_TOKEN = "EnH2bAwmnavrI8spt2Ac1kJUnbg"
TABLE_ID = "tblQQhfnQQGWex4E"

# 从 fields.json 中不存在但公式中出现的字段，手动补充映射
EXTRA_MAPPING = {
    "finish_cnt": "完播数",
    "conversion_cnt": "转化数",
    "total_platform_cnt": "平台服务数",
    "search_revisit_user": "搜索回访用户数",
    "new_customer_uv": "新客UV",
    "shop_visit_uv": "进店UV",
    "offsite_active_uv": "站外活跃UV",
    "task_period_read_uv": "任务周期阅读UV",
    "task_period_cost": "任务周期消费",
    "actual_budget": "实际预算",
    "execution_detail_cnt": "执行细项数",
    "kol_cnt": "达人数",
    "view_time": "浏览时长",
    "read_3s_cnt": "3s阅读数",
}


def load_field_mapping(fields_path):
    """从 fields.json 构建 name -> label 映射"""
    with open(fields_path, "r") as f:
        fields = json.load(f)

    mapping = {}
    for field in fields:
        name = field.get("name")
        label = field.get("label")
        if name and label:
            # 第一个出现的优先（避免重复 name 覆盖）
            if name not in mapping:
                mapping[name] = label.strip()

    # 补充缺失映射
    mapping.update(EXTRA_MAPPING)
    return mapping


def formula_to_chinese(formula, mapping):
    """将英文公式转换为中文公式"""
    if not formula:
        return ""

    # 用正则找出公式中的所有英文标识符（字母+下划线+数字组成的词）
    # 保留运算符、数字、括号、函数名
    def replace_token(match):
        token = match.group(0)
        # 跳过纯数字
        if token.isdigit():
            return token
        # 跳过 SQL 函数名（sum, count, avg 等）
        if token.lower() in ("sum", "count", "avg", "max", "min"):
            return token
        # 查找映射
        return mapping.get(token, token)

    result = re.sub(r'[a-zA-Z_][a-zA-Z0-9_]*', replace_token, formula)
    return result


def get_access_token():
    """获取飞书 tenant_access_token"""
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")

    url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(url, data=data,
                                 headers={"Content-Type": "application/json; charset=utf-8"},
                                 method="POST")
    with urllib.request.urlopen(req) as resp:
        result = json.load(resp)
        return result["tenant_access_token"]


def update_record(token, record_id, cn_formula):
    """更新单条记录的中文公式"""
    url = f"{BASE_URL}/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}"
    data = json.dumps({"fields": {"中文公式": cn_formula}}).encode()
    req = urllib.request.Request(url, data=data,
                                 headers={
                                     "Content-Type": "application/json; charset=utf-8",
                                     "Authorization": f"Bearer {token}"
                                 },
                                 method="PUT")
    with urllib.request.urlopen(req) as resp:
        result = json.load(resp)
        if result.get("code") != 0:
            print(f"  更新失败: {result.get('msg')}", file=sys.stderr)
            return False
    return True


def main():
    fields_path = os.path.join(os.path.dirname(__file__), "../../data/xhs_openapi/fields.json")
    fields_path = os.path.normpath(fields_path)

    # 1. 构建映射
    mapping = load_field_mapping(fields_path)
    print(f"映射表: {len(mapping)} 个字段")

    # 2. 读取记录（从 stdin 或直接调用 API）
    records_path = os.path.join(os.path.dirname(__file__), "records.json")
    if os.path.exists(records_path):
        with open(records_path, "r") as f:
            data = json.load(f)
            records = data.get("records", data) if isinstance(data, dict) else data
    else:
        print("请先将 bitable 记录保存到 out/code/records.json")
        sys.exit(1)

    # 3. 生成中文公式
    updates = []
    unmapped = set()
    for rec in records:
        record_id = rec["record_id"]
        fields = rec["fields"]
        formula = fields.get("公式", "")
        cn_name = fields.get("中文名", "")
        en_name = fields.get("英文名", "")

        if not formula:
            continue

        cn_formula = formula_to_chinese(formula, mapping)

        # 检查是否还有未映射的英文字段
        remaining = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', cn_formula)
        for token in remaining:
            if token.lower() not in ("sum", "count", "avg", "max", "min"):
                unmapped.add(token)

        updates.append({
            "record_id": record_id,
            "en_name": en_name,
            "cn_name": cn_name,
            "formula": formula,
            "cn_formula": cn_formula,
        })
        print(f"  {en_name}: {formula} → {cn_formula}")

    if unmapped:
        print(f"\n未映射字段: {unmapped}")

    # 4. 回写飞书
    print(f"\n准备更新 {len(updates)} 条记录...")
    token = get_access_token()
    success = 0
    for item in updates:
        if update_record(token, item["record_id"], item["cn_formula"]):
            success += 1
    print(f"完成: {success}/{len(updates)} 条更新成功")


if __name__ == "__main__":
    main()
