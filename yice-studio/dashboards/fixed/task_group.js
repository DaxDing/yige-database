/* 任务组分析看板 */

registerDashboard('task_group', {
  label: '任务组分析',
  icon: 'assignment',
  iconClass: 'task_group',
  defaultDt: 'all',
  dims: [
    { key: 'dt', label: '业务日期', w: 100 },
    { key: 'task_group_name', label: '任务组', w: 140 },
    { key: 'ad_product_name', label: '产品', w: 100 },
  ],
  groups: [
    { label: '投入', tint: 'blue', cols: [
      { key: 'fee', label: '总消费', fmt: 'currency' },
      { key: 'ad_fee', label: '投流金额', fmt: 'currency' },
      { key: 'kols_fee', label: '蒲公英金额', fmt: 'currency' },
    ]},
    { label: '流量', tint: 'green', cols: [
      { key: 'read_uv', label: '阅读UV', fmt: 'int' },
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
      { key: 'shop_order_gmv', label: '成交GMV', fmt: 'currency' },
      { key: 'task_product_gmv', label: '任务商品GMV', fmt: 'currency' },
      { key: 'collect_rate', label: '收加率', fmt: 'pct' },
      { key: 'rpv', label: 'UV价值', fmt: 'dec2' },
      { key: 'roi', label: 'ROI', fmt: 'dec2', cond: 'roi' },
    ]},
  ],
  getKPIs(rows) {
    const sum = k => rows.reduce((s, r) => s + (Number(r[k]) || 0), 0);
    const fee = sum('fee'), gmv = sum('shop_order_gmv');
    const roi = fee > 0 ? gmv / fee : 0;
    const roiClass = roi >= 2 ? 'good' : roi < 1 ? 'bad' : roi < 1.5 ? 'warn' : '';
    return [
      { label: '总消费', value: fee, fmt: 'currency', color: 'blue' },
      { label: '阅读UV', value: sum('read_uv'), fmt: 'int', color: 'blue' },
      { label: '进店UV', value: sum('enter_shop_uv'), fmt: 'int', color: 'green' },
      { label: '成交GMV', value: gmv, fmt: 'currency', color: 'green' },
      { label: 'ROI', value: roi, fmt: 'dec2', color: 'amber', valClass: roiClass },
    ];
  },
});
