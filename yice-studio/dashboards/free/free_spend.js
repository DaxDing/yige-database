/* 消费趋势看板 */

function renderFreeSpendChart() {
  const rows = DATA.project || [];
  if (!rows.length) {
    document.getElementById('tbl-section').innerHTML =
      '<div style="text-align:center;padding:80px 0;color:var(--text-3)">暂无数据</div>';
    return;
  }

  const map = {};
  rows.forEach(r => {
    const dt = String(r.dt);
    if (!map[dt]) map[dt] = { fee: 0, ad_fee: 0 };
    map[dt].fee += Number(r.fee) || 0;
    map[dt].ad_fee += Number(r.ad_fee) || 0;
  });
  const dates = Object.keys(map).sort();
  const fees = dates.map(d => map[d].fee);
  const adFees = dates.map(d => map[d].ad_fee);
  const labels = dates.map(d => d.length === 8 ? d.slice(4,6) + '.' + d.slice(6) : d);

  document.getElementById('tbl-section').innerHTML = `
    <div class="chart-card">
      <div class="chart-title">每日消费趋势</div>
      <div class="chart-subtitle">数据来源：项目分析 · 按日期汇总</div>
      <canvas id="spend-chart" height="480"></canvas>
      <div class="chart-legend">
        <span><span class="chart-legend-dot" style="background:#2563eb"></span>总消费</span>
        <span><span class="chart-legend-dot" style="background:#f59e0b"></span>投流消费</span>
      </div>
    </div>`;

  const canvas = document.getElementById('spend-chart');
  const ctx = canvas.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  canvas.width = rect.width * dpr;
  canvas.height = 480 * dpr;
  ctx.scale(dpr, dpr);
  canvas.style.width = rect.width + 'px';
  canvas.style.height = '480px';

  const W = rect.width, H = 480;
  const pad = { t: 20, r: 20, b: 40, l: 60 };
  const cw = W - pad.l - pad.r, ch = H - pad.t - pad.b;

  const allVals = [...fees, ...adFees];
  const maxV = Math.max(...allVals) * 1.15 || 1;
  const minV = 0;

  const x = i => pad.l + (i / (dates.length - 1 || 1)) * cw;
  const y = v => pad.t + ch - ((v - minV) / (maxV - minV)) * ch;

  ctx.strokeStyle = '#e5e7eb'; ctx.lineWidth = 0.5;
  for (let i = 0; i <= 4; i++) {
    const yy = pad.t + ch * i / 4;
    ctx.beginPath(); ctx.moveTo(pad.l, yy); ctx.lineTo(W - pad.r, yy); ctx.stroke();
    const val = maxV - (maxV * i / 4);
    ctx.fillStyle = '#9ca3af'; ctx.font = '10px system-ui';
    ctx.textAlign = 'right'; ctx.fillText(val >= 1000 ? (val/1000).toFixed(1) + 'k' : val.toFixed(0), pad.l - 8, yy + 3);
  }

  ctx.fillStyle = '#9ca3af'; ctx.font = '10px system-ui'; ctx.textAlign = 'center';
  const step = Math.max(1, Math.floor(dates.length / 10));
  dates.forEach((_, i) => {
    if (i % step === 0 || i === dates.length - 1) {
      ctx.fillText(labels[i], x(i), H - pad.b + 18);
    }
  });

  function drawLine(data, color, fill) {
    if (data.length < 2) return;
    ctx.beginPath();
    data.forEach((v, i) => { i === 0 ? ctx.moveTo(x(i), y(v)) : ctx.lineTo(x(i), y(v)); });
    ctx.strokeStyle = color; ctx.lineWidth = 2; ctx.lineJoin = 'round'; ctx.stroke();

    ctx.beginPath();
    data.forEach((v, i) => { i === 0 ? ctx.moveTo(x(i), y(v)) : ctx.lineTo(x(i), y(v)); });
    ctx.lineTo(x(data.length - 1), pad.t + ch);
    ctx.lineTo(x(0), pad.t + ch);
    ctx.closePath();
    ctx.fillStyle = fill; ctx.fill();

    data.forEach((v, i) => {
      ctx.beginPath(); ctx.arc(x(i), y(v), 3, 0, Math.PI * 2);
      ctx.fillStyle = color; ctx.fill();
      ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke();
    });
  }

  drawLine(fees, '#2563eb', 'rgba(37,99,235,0.08)');
  drawLine(adFees, '#f59e0b', 'rgba(245,158,11,0.08)');
}

registerDashboard('free_spend', {
  label: '消费趋势',
  icon: 'show_chart',
  iconClass: 'free_spend',
  section: 'free',
  badge: '<span class="icon" style="font-size:14px;color:var(--red);opacity:0.6">close</span>',
  onActivate() {
    document.getElementById('toolbar-section').innerHTML = '';
    setTimeout(() => renderFreeSpendChart(), 300);
  },
});
