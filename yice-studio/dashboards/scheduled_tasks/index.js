/* 定时任务看板 */

const SCHEDULED_TASKS = [
  { id: 'cron-8a3f01', name: '每日投放日报', desc: '汇总昨日投流数据，发送至飞书群', icon: 'msg', iconName: 'send', cron: '0 9 * * *', cronLabel: '每天 09:00', enabled: true, lastRun: '2026-03-10 09:00', status: 'success', runs: [
    { time: '2026-03-10 09:00:03', status: 'success', duration: '4.2s', detail: '已推送至「投放日报群」，包含 3 个项目数据' },
    { time: '2026-03-09 09:00:02', status: 'success', duration: '3.8s', detail: '已推送至「投放日报群」，包含 3 个项目数据' },
    { time: '2026-03-08 09:00:01', status: 'success', duration: '5.1s', detail: '已推送至「投放日报群」，包含 3 个项目数据' },
    { time: '2026-03-07 09:00:04', status: 'failed', duration: '1.2s', detail: '飞书 API 超时 (HTTP 504)' },
    { time: '2026-03-06 09:00:02', status: 'success', duration: '3.5s', detail: '已推送至「投放日报群」，包含 2 个项目数据' },
  ]},
  { id: 'cron-5b7e02', name: '周度 ROI 周报', desc: '汇总本周项目 ROI，推送至飞书群', icon: 'report', iconName: 'bar_chart', cron: '0 10 * * 1', cronLabel: '每周一 10:00', enabled: true, lastRun: '2026-03-10 10:00', status: 'success', runs: [
    { time: '2026-03-10 10:00:05', status: 'success', duration: '6.7s', detail: '周报已推送，本周 ROI 均值 1.82' },
    { time: '2026-03-03 10:00:03', status: 'success', duration: '7.1s', detail: '周报已推送，本周 ROI 均值 1.65' },
    { time: '2026-02-24 10:00:02', status: 'success', duration: '5.9s', detail: '周报已推送，本周 ROI 均值 1.73' },
  ]},
  { id: 'cron-c42d03', name: '异常消费预警', desc: '检测单日消费超预算 120%，即时告警', icon: 'alert', iconName: 'warning', cron: '*/30 * * * *', cronLabel: '每 30 分钟', enabled: true, lastRun: '2026-03-10 14:30', status: 'success', runs: [
    { time: '2026-03-10 14:30:01', status: 'success', duration: '1.8s', detail: '无异常，全部账户消费在预算内' },
    { time: '2026-03-10 14:00:01', status: 'success', duration: '1.6s', detail: '无异常' },
    { time: '2026-03-10 13:30:02', status: 'success', duration: '2.1s', detail: '⚠️ 账户 7152346 消费达预算 118%，未触发阈值' },
    { time: '2026-03-10 13:00:01', status: 'success', duration: '1.5s', detail: '无异常' },
    { time: '2026-03-10 12:30:01', status: 'success', duration: '1.7s', detail: '无异常' },
    { time: '2026-03-10 12:00:02', status: 'success', duration: '1.9s', detail: '🚨 已告警：账户 7152346 消费达预算 125%' },
  ]},
  { id: 'cron-d91a04', name: '预算进度提醒', desc: '每日推送各项目预算消耗进度至飞书群', icon: 'msg', iconName: 'send', cron: '0 18 * * *', cronLabel: '每天 18:00', enabled: true, lastRun: '2026-03-10 18:00', status: 'success', runs: [
    { time: '2026-03-10 18:00:05', status: 'success', duration: '3.1s', detail: '已推送 3 个项目预算进度，春焕新颜消耗 78%' },
    { time: '2026-03-09 18:00:03', status: 'success', duration: '2.9s', detail: '已推送 3 个项目预算进度，春焕新颜消耗 72%' },
    { time: '2026-03-08 18:00:04', status: 'success', duration: '3.3s', detail: '已推送 3 个项目预算进度' },
  ]},
  { id: 'cron-e68b05', name: 'KPI 达成日报', desc: '对比当日 KPI 目标与实际完成情况', icon: 'report', iconName: 'bar_chart', cron: '0 20 * * *', cronLabel: '每天 20:00', enabled: true, lastRun: '2026-03-10 20:00', status: 'success', runs: [
    { time: '2026-03-10 20:00:06', status: 'success', duration: '5.4s', detail: '已推送 KPI 日报，GMV 达成率 92%，进店 UV 达成率 87%' },
    { time: '2026-03-09 20:00:04', status: 'success', duration: '4.8s', detail: '已推送 KPI 日报，GMV 达成率 88%，进店 UV 达成率 91%' },
    { time: '2026-03-08 20:00:03', status: 'failed', duration: '1.0s', detail: '飞书群 webhook 地址失效，请检查配置' },
  ]},
  { id: 'cron-f73c06', name: '蒲公英订单同步', desc: '同步蒲公英新增订单至飞书多维表格', icon: 'sync', iconName: 'sync_alt', cron: '0 10,16 * * *', cronLabel: '每天 10:00/16:00', enabled: false, lastRun: '2026-03-09 16:00', status: 'success', runs: [
    { time: '2026-03-09 16:00:08', status: 'success', duration: '8.2s', detail: '同步 5 条新订单，总金额 ¥42,800' },
    { time: '2026-03-09 10:00:06', status: 'success', duration: '6.5s', detail: '同步 3 条新订单，总金额 ¥28,500' },
    { time: '2026-03-08 16:00:07', status: 'success', duration: '7.1s', detail: '同步 2 条新订单，总金额 ¥15,000' },
  ]},
];

function renderScheduledTasks() {
  const active = SCHEDULED_TASKS.filter(t => t.enabled).length;
  let html = `<div class="task-list">
    <div class="task-list-header">
      <div>
        <div class="task-list-title">定时任务</div>
        <div class="task-list-subtitle">${active} 个运行中 / ${SCHEDULED_TASKS.length} 个任务</div>
      </div>
    </div>`;

  SCHEDULED_TASKS.forEach(t => {
    const statusIcon = t.status === 'success'
      ? '<span class="icon" style="font-size:14px;color:var(--green)">check_circle</span>'
      : '<span class="icon" style="font-size:14px;color:var(--red)">error</span>';
    html += `
      <div class="task-card" id="task-card-${t.id}" style="cursor:pointer" onclick="openTaskModal('${t.id}')">
        <div class="task-icon ${t.icon}"><span class="icon">smart_toy</span></div>
        <div class="task-info">
          <div class="task-name">${t.name} <span style="font-family:var(--mono);font-size:10px;color:var(--text-3);font-weight:400;margin-left:6px">${t.id}</span></div>
          <div class="task-detail">
            <span class="task-cron">${t.cronLabel}</span>
            <span class="task-next">上次: ${t.lastRun}</span>
            ${statusIcon}
          </div>
        </div>
        <div class="task-right">
          <button class="task-run-btn" id="run-btn-${t.id}" onclick="event.stopPropagation();runTask('${t.id}')" title="立即执行"><span class="icon">play_arrow</span></button>
          <button class="task-toggle${t.enabled ? ' on' : ''}" onclick="event.stopPropagation();toggleTask('${t.id}')" title="${t.enabled ? '运行中' : '已暂停'}"></button>
        </div>
      </div>`;
  });

  html += '</div>';
  document.getElementById('tbl-section').innerHTML = html;
}

function toggleTask(id) {
  const t = SCHEDULED_TASKS.find(t => t.id === id);
  if (t) { t.enabled = !t.enabled; renderScheduledTasks(); renderSidebar(); }
}

function runTask(id) {
  const btn = document.getElementById('run-btn-' + id);
  if (!btn || btn.classList.contains('running')) return;
  btn.classList.add('running');
  btn.innerHTML = '<span class="icon">progress_activity</span>';

  const card = document.getElementById('task-card-' + id);
  if (card) card.classList.add('running');

  const duration = (1 + Math.random() * 4).toFixed(1);
  setTimeout(() => {
    const t = SCHEDULED_TASKS.find(t => t.id === id);
    if (t) {
      const now = new Date();
      const pad = v => String(v).padStart(2, '0');
      const ts = `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;
      t.lastRun = ts.slice(0, 16);
      t.status = 'success';
      t.runs.unshift({ time: ts, status: 'success', duration: duration + 's', detail: '手动触发执行成功' });
    }
    showToast(t.name + ' 执行完成');
    renderScheduledTasks();
  }, duration * 1000);
}

function openTaskModal(id) {
  const t = SCHEDULED_TASKS.find(t => t.id === id);
  if (!t) return;
  closeTaskModal();

  const statusLabel = t.enabled
    ? '<span style="color:var(--green);font-weight:500">运行中</span>'
    : '<span style="color:var(--text-3);font-weight:500">已暂停</span>';

  let runsHtml = '';
  (t.runs || []).forEach(r => {
    runsHtml += `
      <div class="run-row">
        <div class="run-dot ${r.status}"></div>
        <div class="run-content">
          <div class="run-header">
            <span class="run-time">${r.time}</span>
            <span class="run-duration">${r.duration}</span>
          </div>
          <div class="run-detail">${r.detail}</div>
        </div>
      </div>`;
  });

  const el = document.createElement('div');
  el.className = 'task-modal-backdrop';
  el.id = 'task-modal';
  el.onclick = function(e) { if (e.target === el) closeTaskModal(); };
  el.innerHTML = `
    <div class="task-modal">
      <div class="task-modal-head">
        <div class="task-icon ${t.icon}"><span class="icon">${t.iconName}</span></div>
        <div>
          <div class="task-modal-title">${t.name}</div>
          <div class="task-modal-desc">${t.desc}</div>
        </div>
        <button class="task-modal-close" onclick="closeTaskModal()"><span class="icon">close</span></button>
      </div>
      <div class="task-modal-meta">
        <div class="task-modal-meta-item">
          <span class="task-modal-meta-label">调度频率</span>
          <span class="task-modal-meta-value">${t.cronLabel}</span>
        </div>
        <div class="task-modal-meta-item">
          <span class="task-modal-meta-label">Cron</span>
          <span class="task-modal-meta-value">${t.cron}</span>
        </div>
        <div class="task-modal-meta-item">
          <span class="task-modal-meta-label">状态</span>
          <span class="task-modal-meta-value">${statusLabel}</span>
        </div>
        <div class="task-modal-meta-item">
          <span class="task-modal-meta-label">执行次数</span>
          <span class="task-modal-meta-value">${(t.runs || []).length}</span>
        </div>
      </div>
      <div class="task-modal-body">
        <div class="task-modal-section-title">执行记录</div>
        ${runsHtml || '<div style="color:var(--text-3);font-size:12px;padding:20px 0;text-align:center">暂无记录</div>'}
      </div>
    </div>`;
  document.body.appendChild(el);
}

function closeTaskModal() {
  const el = document.getElementById('task-modal');
  if (el) el.remove();
}

registerDashboard('scheduled_tasks', {
  label: '定时任务',
  icon: 'schedule_send',
  iconClass: 'scheduled',
  section: 'system',
  badge: '<span class="icon" style="font-size:14px;color:var(--red);opacity:0.6">close</span>',
  onActivate() {
    document.getElementById('toolbar-section').innerHTML = '';
    document.getElementById('kpi-section').innerHTML = '';
    renderScheduledTasks();
  },
});
