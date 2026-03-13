/* 项目分析看板 */

registerDashboard('project', {
  label: '项目分析',
  icon: 'folder',
  iconClass: 'project',
  defaultDt: 'all',
  dims: [
    { key: 'dt', label: '业务日期', w: 100 },
  ],
  groups: METRIC_GROUPS_BYCONTENT,
});
