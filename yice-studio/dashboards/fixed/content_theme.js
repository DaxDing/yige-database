/* 内容方向分析看板 */

registerDashboard('content_theme', {
  label: '内容方向分析',
  icon: 'category',
  iconClass: 'content_theme',
  defaultDt: 'all',
  dims: [
    { key: 'dt', label: '业务日期', w: 100 },
    { key: 'content_theme', label: '内容方向', w: 130 },
    { key: 'delivery_product', label: '产品', w: 100 },
  ],
  groups: METRIC_GROUPS_BYCONTENT,
});
