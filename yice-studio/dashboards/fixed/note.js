/* 笔记分析看板 */

registerDashboard('note', {
  label: '笔记分析',
  icon: 'description',
  iconClass: 'note',
  defaultDt: 'last7',
  dims: [
    { key: 'dt', label: '业务日期', w: 100 },
    { key: 'kol_name', label: '博主', w: 100 },
    { key: 'note_id', label: '笔记ID', w: 120 },
  ],
  groups: METRIC_GROUPS_BYCONTENT,
});
