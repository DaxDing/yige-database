/* 看板注册系统 + 共享配置 */

window.DASHBOARDS = {};
window.DASHBOARD_SECTIONS = { system: [], fixed: [], free: [] };

window.registerDashboard = function(key, config) {
  DASHBOARDS[key] = config;
  const section = config.section || 'fixed';
  if (DASHBOARD_SECTIONS[section]) {
    DASHBOARD_SECTIONS[section].push(key);
  }
};

/* 默认 KPI 卡片（bycontent 看板通用） */
window.defaultGetKPIs = function(rows) {
  const sum = k => rows.reduce((s, r) => s + (Number(r[k]) || 0), 0);
  const fee = sum('fee'), gmv = sum('shop_order_gmv');
  const roi = fee > 0 ? gmv / fee : 0;
  const roiClass = roi >= 2 ? 'good' : roi < 1 ? 'bad' : roi < 1.5 ? 'warn' : '';
  return [
    { label: '总消费', value: fee, fmt: 'currency', color: 'blue' },
    { label: '曝光量', value: sum('impression'), fmt: 'int', color: 'blue' },
    { label: '阅读量', value: sum('read_uv'), fmt: 'int', color: 'blue' },
    { label: '进店UV', value: sum('enter_shop_uv'), fmt: 'int', color: 'green' },
    { label: '全店GMV', value: gmv, fmt: 'currency', color: 'green' },
    { label: 'ROI', value: roi, fmt: 'dec2', color: 'amber', valClass: roiClass },
  ];
};

/* 共享指标分组（bycontent 看板通用） */
window.METRIC_GROUPS_BYCONTENT = [
  { label: '投入', tint: 'blue', cols: [
    { key: 'fee', label: '总消费', fmt: 'currency' },
    { key: 'ad_fee', label: '投流金额', fmt: 'currency' },
    { key: 'kols_fee', label: '蒲公英金额', fmt: 'currency' },
  ]},
  { label: '流量', tint: 'green', cols: [
    { key: 'note_count', label: '笔记数', fmt: 'int' },
    { key: 'impression', label: '曝光', fmt: 'int' },
    { key: 'read_uv', label: '阅读', fmt: 'int' },
    { key: 'interaction', label: '互动', fmt: 'int' },
  ]},
  { label: '效率', tint: 'amber', cols: [
    { key: 'cpm', label: 'CPM', fmt: 'dec2' },
    { key: 'cpc', label: 'CPC', fmt: 'dec2' },
    { key: 'cpe', label: 'CPE', fmt: 'dec2' },
    { key: 'ctr', label: 'CTR', fmt: 'pct' },
  ]},
  { label: '搜索', tint: 'pink', cols: [
    { key: 'search_cmt_impression', label: '组件曝光', fmt: 'int' },
    { key: 'search_cmt_click', label: '组件点击', fmt: 'int' },
    { key: 'search_cmt_click_ctr', label: '组件CTR', fmt: 'pct' },
  ]},
  { label: '转化', tint: 'purple', cols: [
    { key: 'enter_shop_uv', label: '进店UV', fmt: 'int' },
    { key: 'enter_shop_rate', label: '进店率', fmt: 'pct' },
    { key: 'cpuv', label: 'CPUV', fmt: 'dec2' },
    { key: 'shop_order_uv', label: '成交UV', fmt: 'int' },
    { key: 'conversion_rate', label: '转化率', fmt: 'pct' },
    { key: 'average_order_value', label: '客单价', fmt: 'currency' },
  ]},
  { label: '价值', tint: 'orange', cols: [
    { key: 'shop_order_gmv', label: '全店GMV', fmt: 'currency' },
    { key: 'task_product_gmv', label: '单品GMV', fmt: 'currency' },
    { key: 'rpv', label: 'UV价值', fmt: 'dec2' },
    { key: 'roi', label: 'ROI', fmt: 'dec2', cond: 'roi' },
    { key: 'single_product_roi', label: '单品ROI', fmt: 'dec2', cond: 'roi' },
  ]},
  { label: '新客', tint: 'teal', cols: [
    { key: 'shop_new_visitor_uv', label: '新访客', fmt: 'int' },
    { key: 'new_visitor_rate', label: '新访客率', fmt: 'pct' },
    { key: 'shop_new_customer_uv', label: '新客UV', fmt: 'int' },
    { key: 'new_customer_rate', label: '新客率', fmt: 'pct' },
    { key: 'cac', label: '新客成本', fmt: 'currency' },
  ]},
];
