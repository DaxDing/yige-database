/**
 * YICE Chat Widget — 驱动本地 Claude Code CLI
 * 所有页面（HTML / React）引用同一个文件
 */
(function () {
  'use strict';

  /* ═══ CSS ═══ */
  const style = document.createElement('style');
  style.textContent = `
.chat-fab {
  position: fixed; bottom: 24px; right: 24px;
  width: 52px; height: 52px; border-radius: 16px;
  background: linear-gradient(135deg, #d97706, #f59e0b);
  color: #fff; border: none; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 20px rgba(0,0,0,0.25);
  transition: all 0.25s cubic-bezier(0.4,0,0.2,1); z-index: 100;
}
.chat-fab:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(0,0,0,0.3); }
.chat-fab .icon { font-size: 22px; transition: transform 0.25s; }
.chat-fab.open .icon { transform: rotate(90deg); }

.chat-panel {
  position: fixed; bottom: 84px; right: 24px;
  width: 760px; height: 85vh;
  background: #f7f7f8;
  border: none;
  border-radius: 20px;
  box-shadow: 0 12px 48px rgba(0,0,0,0.15), 0 0 0 1px rgba(0,0,0,0.05);
  display: none; flex-direction: column;
  z-index: 99; overflow: hidden;
}
.chat-panel.open { display: flex; animation: chat-enter 0.25s cubic-bezier(0.4,0,0.2,1); }

@keyframes chat-enter {
  from { opacity: 0; transform: translateY(16px) scale(0.97); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.chat-header {
  display: flex; align-items: center; gap: 12px;
  padding: 16px 20px;
  background: #fff;
  border-bottom: 1px solid #eee;
}
.chat-header-avatar {
  width: 32px; height: 32px; border-radius: 10px;
  background: linear-gradient(135deg, #d97706, #f59e0b);
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; font-weight: 700; color: #fff;
  box-shadow: 0 2px 8px rgba(217,119,6,0.3);
}
.chat-header-title { font-size: 14px; font-weight: 600; color: #1a1a2e; flex: 1; letter-spacing: -0.01em; }
.chat-header-status { font-size: 11px; color: #10b981; font-weight: 500; }
.chat-hdr-btn {
  width: 28px; height: 28px; border-radius: 8px;
  background: #f0f0f3; border: none;
  color: #9ca3af; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s;
}
.chat-hdr-btn:hover { background: #e5e5ea; color: #374151; }
.chat-hdr-btn .icon { font-size: 16px; }

.chat-messages {
  flex: 1; overflow-y: auto; padding: 20px;
  display: flex; flex-direction: column; gap: 14px;
  background: #f7f7f8;
}
.chat-messages::-webkit-scrollbar { width: 5px; }
.chat-messages::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 10px; }
.chat-messages::-webkit-scrollbar-track { background: transparent; }
.chat-msg {
  max-width: 88%; padding: 12px 16px;
  border-radius: 16px; font-size: 13.5px; line-height: 1.6;
  white-space: pre-wrap;
}
.chat-msg.bot {
  align-self: flex-start;
  background: #fff;
  border: none;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  color: #1a1a2e; border-bottom-left-radius: 6px;
}
.chat-msg.user {
  align-self: flex-end;
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  color: #fff; border-bottom-right-radius: 6px;
  box-shadow: 0 2px 8px rgba(37,99,235,0.25);
}
.chat-msg.divider {
  align-self: center; max-width: 100%;
  font-size: 11px; color: #9ca3af;
  border: none; background: none; box-shadow: none;
  padding: 4px 0;
}
.chat-input-area {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 20px;
  background: #fff;
  border-top: 1px solid #eee;
}
.chat-input {
  flex: 1; font-family: var(--ui, system-ui); font-size: 13.5px;
  color: #1a1a2e; background: #f0f0f3;
  border: none; border-radius: 22px;
  padding: 10px 16px; outline: none; transition: all 0.2s;
}
.chat-input:focus { background: #e8e8ee; box-shadow: 0 0 0 2px rgba(37,99,235,0.15); }
.chat-input::placeholder { color: #9ca3af; }
.chat-send {
  width: 36px; height: 36px; border-radius: 12px;
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  color: #fff; border: none; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s; flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(37,99,235,0.3);
}
.chat-send:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(37,99,235,0.4); }
.chat-send:disabled { opacity: 0.35; cursor: not-allowed; transform: none; box-shadow: none; }
.chat-send .icon { font-size: 16px; }
.chat-upload, .chat-mic, .chat-ctx {
  width: 36px; height: 36px; border-radius: 12px;
  background: #f0f0f3; color: #9ca3af; border: none;
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: all 0.2s; flex-shrink: 0;
}
.chat-upload:hover, .chat-mic:hover, .chat-ctx:hover { background: #e5e5ea; color: #374151; }
.chat-upload .icon, .chat-mic .icon, .chat-ctx .icon { font-size: 16px; }
.chat-ctx.active {
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
  color: #fff; box-shadow: 0 2px 8px rgba(139,92,246,0.3);
}
.chat-ctx.active .icon { animation: ctx-blink 2s ease-in-out infinite; }
@keyframes ctx-blink { 0%,100% { opacity: 1; } 50% { opacity: 0.6; } }
.chat-mic.recording {
  background: linear-gradient(135deg, #ef4444, #f87171);
  color: #fff; animation: mic-glow 1.5s ease-in-out infinite;
  box-shadow: 0 0 0 0 rgba(239,68,68,0.4);
}
.chat-mic.recording .icon { animation: mic-icon-pulse 0.8s ease-in-out infinite alternate; }
@keyframes mic-glow {
  0% { box-shadow: 0 0 0 0 rgba(239,68,68,0.5); }
  50% { box-shadow: 0 0 0 10px rgba(239,68,68,0), 0 0 20px rgba(239,68,68,0.15); }
  100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.5); }
}
@keyframes mic-icon-pulse { 0% { transform: scale(1); } 100% { transform: scale(1.2); } }

/* 录音中：输入栏变为波形动画 */
.chat-input-area.recording { border-top-color: #fecaca; }
.chat-input-area.recording .chat-input {
  background: linear-gradient(90deg, #fef2f2, #fee2e2, #fef2f2);
  background-size: 200% 100%;
  animation: input-wave 2s ease-in-out infinite;
  color: #ef4444; font-weight: 500;
}
@keyframes input-wave { 0% { background-position: 0% 50%; } 100% { background-position: 200% 50%; } }

/* 识别中状态 */
.chat-input-area.recognizing .chat-input {
  background: linear-gradient(90deg, #eff6ff, #dbeafe, #eff6ff);
  background-size: 200% 100%;
  animation: input-wave 1.5s ease-in-out infinite;
  color: #2563eb; font-weight: 500;
}
.chat-mic.recognizing {
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  color: #fff; animation: mic-glow-blue 1.5s ease-in-out infinite;
}
@keyframes mic-glow-blue {
  0%,100% { box-shadow: 0 0 0 0 rgba(37,99,235,0.4); }
  50% { box-shadow: 0 0 0 8px rgba(37,99,235,0); }
}
.chat-file-tag {
  display: flex; align-items: center; gap: 6px;
  padding: 6px 12px; margin: 0 20px 4px;
  background: #fff; border: 1px solid #eee;
  border-radius: 8px; font-size: 11px; color: #6b7280;
}
.chat-file-tag .icon { font-size: 14px; cursor: pointer; }
.chat-file-tag .icon:hover { color: #ef4444; }
.chat-msg.bot .typing-dot { display: inline-block; animation: blink 1.2s infinite; }
.chat-msg.bot .typing-dot:nth-child(2) { animation-delay: 0.2s; }
.chat-msg.bot .typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink { 0%,80% { opacity: 0.2; } 40% { opacity: 1; } }
.thinking-anim { color: var(--text-3, #9ca3af); font-size: 12px; animation: pulse 1.5s ease-in-out infinite; }
@keyframes pulse { 0%,100% { opacity: 0.5; } 50% { opacity: 1; } }

/* History Panel */
.chat-history {
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background: #f7f7f8; z-index: 10;
  display: none; flex-direction: column;
}
.chat-history.open { display: flex; animation: chat-enter 0.15s ease-out; }
.chat-history-hdr {
  display: flex; align-items: center; gap: 10px;
  padding: 16px 20px;
  background: #fff;
  border-bottom: 1px solid #eee;
}
.chat-history-hdr .icon { font-size: 18px; color: #d97706; }
.chat-history-hdr-title { font-size: 14px; font-weight: 600; color: #1a1a2e; flex: 1; letter-spacing: -0.01em; }
.chat-history-list {
  flex: 1; overflow-y: auto; padding: 12px 16px;
}
.chat-history-list::-webkit-scrollbar { width: 5px; }
.chat-history-list::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 10px; }
.chat-history-group {
  font-size: 11px; font-weight: 600; color: #9ca3af;
  text-transform: uppercase; letter-spacing: 0.04em;
  padding: 12px 4px 6px; margin-top: 4px;
}
.chat-history-group:first-child { padding-top: 4px; margin-top: 0; }
.chat-history-item {
  display: flex; align-items: flex-start; gap: 12px;
  padding: 12px 14px; border-radius: 12px;
  cursor: pointer; transition: all 0.15s;
  margin-bottom: 2px;
  background: #fff;
  border: 1px solid transparent;
  box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}
.chat-history-item:hover { border-color: #e5e5ea; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.chat-history-item.active { background: #eff6ff; border-color: #bfdbfe; box-shadow: 0 2px 8px rgba(37,99,235,0.1); }
.chat-history-item-icon {
  width: 34px; height: 34px; border-radius: 10px; flex-shrink: 0;
  background: #f0f0f3; color: #9ca3af;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; margin-top: 1px;
}
.chat-history-item.active .chat-history-item-icon { background: #dbeafe; color: #2563eb; }
.chat-history-item-edit {
  width: 28px; height: 28px; border-radius: 8px; flex-shrink: 0;
  background: transparent; border: none; color: #c0c5cf;
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  opacity: 0; transition: all 0.15s; margin-top: 2px;
}
.chat-history-item-edit .icon { font-size: 15px; }
.chat-history-item:hover .chat-history-item-edit { opacity: 1; }
.chat-history-item-edit:hover { background: #f0f0f3; color: #374151; }
.chat-history-item-body { flex: 1; min-width: 0; }
.chat-history-item-preview {
  font-size: 13px; color: #1a1a2e; font-weight: 500; line-height: 1.4;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  display: flex; align-items: center; gap: 6px;
}
.chat-history-item-meta {
  font-size: 11px; color: #b0b5bf; margin-top: 3px;
  display: flex; align-items: center; gap: 4px;
}
.chat-history-item-meta .icon { font-size: 12px; }
.chat-history-item-meta .sep { margin: 0 4px; opacity: 0.4; }
.chat-history-badge {
  font-size: 10px; color: #2563eb; background: #dbeafe;
  padding: 1px 7px; border-radius: 4px; font-weight: 600;
  flex-shrink: 0; letter-spacing: 0.02em;
}
.chat-history-empty {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  flex: 1; color: #b0b5bf; font-size: 13px; gap: 8px;
}
.chat-history-empty .icon { font-size: 40px; opacity: 0.3; }

/* Context chip in user message */
.chat-ctx-chip {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 10px; margin-bottom: 6px;
  background: rgba(255,255,255,0.15); border-radius: 6px;
  font-size: 11px; color: rgba(255,255,255,0.8);
  cursor: pointer; transition: all 0.15s;
  max-width: 100%;
}
.chat-ctx-chip:hover { background: rgba(255,255,255,0.25); }
.chat-ctx-chip .icon { font-size: 13px; }
.chat-ctx-chip-detail {
  display: none; margin-top: 6px; padding: 8px 10px;
  background: rgba(0,0,0,0.15); border-radius: 8px;
  font-size: 11px; line-height: 1.5; color: rgba(255,255,255,0.75);
  white-space: pre-wrap; word-break: break-all;
  max-height: 200px; overflow-y: auto;
}
.chat-ctx-chip-detail.open { display: block; }
`;
  document.head.appendChild(style);

  /* ═══ HTML ═══ */
  const wrapper = document.createElement('div');
  wrapper.id = 'yice-chat-widget';
  wrapper.innerHTML = `
<button class="chat-fab" id="chat-fab">
  <span class="icon">chat</span>
</button>
<div class="chat-panel" id="chat-panel">
  <div class="chat-header">
    <div class="chat-header-avatar">✦</div>
    <span class="chat-header-title">YICE 助手</span>
    <span class="chat-header-status">● local</span>
    <button class="chat-hdr-btn" id="btn-history" title="历史对话"><span class="icon">history</span></button>
    <button class="chat-hdr-btn" id="btn-new" title="新对话"><span class="icon">add</span></button>
  </div>
  <div class="chat-messages" id="chat-messages">
    <div class="chat-msg bot">你好！我是 YICE 助手，有什么想了解的？</div>
  </div>
  <div id="chat-file-area"></div>
  <div class="chat-input-area">
    <button class="chat-ctx" id="chat-ctx" onclick="window.__chatWidget.toggleCtx()" title="携带当前页面信息"><span class="icon">screen_share</span></button>
    <button class="chat-upload" onclick="document.getElementById('chat-file').click()" title="上传文件"><span class="icon">attach_file</span></button>
    <input type="file" id="chat-file" style="display:none" accept=".csv,.json,.xlsx,.txt,.png,.jpg,.jpeg,.gif,.webp,.pdf" multiple onchange="window.__chatWidget.handleFile(this)">
    <button class="chat-mic" id="chat-mic" onclick="window.__chatWidget.toggleMic()" title="语音输入"><span class="icon">mic</span></button>
    <input class="chat-input" id="chat-input" type="text" placeholder="输入消息..." onkeydown="if(event.key==='Enter')window.__chatWidget.send()">
    <button class="chat-send" onclick="window.__chatWidget.send()"><span class="icon">send</span></button>
  </div>
  <div class="chat-history" id="chat-history">
    <div class="chat-history-hdr">
      <span class="icon">history</span>
      <span class="chat-history-hdr-title">历史对话</span>
      <button class="chat-hdr-btn" id="btn-history-close"><span class="icon">close</span></button>
    </div>
    <div class="chat-history-list" id="chat-history-list"></div>
  </div>
</div>`;
  document.body.appendChild(wrapper);

  /* ═══ State ═══ */
  var chatBusy = false;
  var chatFiles = [];
  var ctxActive = false;

  function toggleCtx() {
    ctxActive = !ctxActive;
    document.getElementById('chat-ctx').classList.toggle('active', ctxActive);
  }

  function gatherPageContext() {
    var ctx = { page: document.title, url: location.pathname };
    // 当前页面的筛选状态
    var selects = document.querySelectorAll('select:not(#yice-chat-widget select)');
    var filters = {};
    selects.forEach(function (s) {
      if (s.id && s.value) filters[s.id || s.name || s.className] = s.selectedOptions[0]?.textContent || s.value;
    });
    if (Object.keys(filters).length) ctx.filters = filters;
    // 活跃 tab
    var activeTab = document.querySelector('.tab-btn.active, .tab.active, [data-active="true"]');
    if (activeTab) ctx.active_tab = activeTab.textContent.trim();
    // KPI 卡片数据
    var kpis = document.querySelectorAll('.kpi-card, .stat-card, .metric-card');
    if (kpis.length) {
      ctx.kpis = [];
      kpis.forEach(function (k) {
        var label = k.querySelector('.kpi-label, .stat-label, .metric-label, h4, h3');
        var value = k.querySelector('.kpi-value, .stat-value, .metric-value, .value');
        if (label && value) ctx.kpis.push({ label: label.textContent.trim(), value: value.textContent.trim() });
      });
    }
    // 表格摘要（取前 3 行）
    var table = document.querySelector('table:not(#yice-chat-widget table)');
    if (table) {
      var headers = Array.from(table.querySelectorAll('th')).map(function (th) { return th.textContent.trim(); });
      var rows = [];
      table.querySelectorAll('tbody tr').forEach(function (tr, i) {
        if (i >= 3) return;
        var cells = Array.from(tr.querySelectorAll('td')).map(function (td) { return td.textContent.trim(); });
        rows.push(cells);
      });
      if (headers.length) ctx.table_preview = { headers: headers, rows: rows, total_rows: table.querySelectorAll('tbody tr').length };
    }
    return ctx;
  }
  var currentSessionId = null;
  var STORAGE_KEY = 'yice_chat_history';

  function saveHistory() {
    var area = document.getElementById('chat-messages');
    localStorage.setItem(STORAGE_KEY, area.innerHTML);
    if (currentSessionId) {
      localStorage.setItem(STORAGE_KEY + '_sid', currentSessionId);
    }
  }

  function loadHistory() {
    var saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      document.getElementById('chat-messages').innerHTML = saved;
    }
    currentSessionId = localStorage.getItem(STORAGE_KEY + '_sid') || null;
  }

  loadHistory();

  function escHtml(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function renderMd(s) {
    var esc = escHtml(s);
    esc = esc.replace(/```(\w*)\n([\s\S]*?)```/g, function (_, lang, code) {
      return '<pre style="background:rgba(0,0,0,0.06);padding:8px 10px;border-radius:6px;overflow-x:auto;font-size:12px;margin:4px 0"><code>' + code.trimEnd() + '</code></pre>';
    });
    var lines = esc.split('\n');
    var html = '', inTable = false, tableRow = 0;
    for (var i = 0; i < lines.length; i++) {
      var ln = lines[i];
      if (/^\|[\s\-:|]+\|$/.test(ln)) { continue; }
      if (/^\|(.+)\|$/.test(ln)) {
        var cells = ln.slice(1, -1).split('|').map(function (c) { return c.trim(); });
        if (!inTable) { inTable = true; tableRow = 0; html += '<table style="border-collapse:collapse;font-size:12px;margin:4px 0;width:100%">'; }
        var rowBg = tableRow === 0 ? 'background:#f5f5f7;font-weight:600;' : '';
        html += '<tr style="' + rowBg + '">' + cells.map(function (c) { return '<td style="padding:3px 8px;border:1px solid rgba(0,0,0,0.1)">' + c + '</td>'; }).join('') + '</tr>';
        tableRow++;
        continue;
      }
      if (inTable) { inTable = false; html += '</table>'; }
      if (/^### (.+)/.test(ln)) { html += '<div style="font-weight:600;font-size:13px;margin:8px 0 4px">' + ln.slice(4) + '</div>'; continue; }
      if (/^## (.+)/.test(ln)) { html += '<div style="font-weight:700;font-size:14px;margin:8px 0 4px">' + ln.slice(3) + '</div>'; continue; }
      if (/^[-*] (.+)/.test(ln)) { html += '<div style="padding-left:12px">• ' + ln.slice(2) + '</div>'; continue; }
      if (/^\d+\. (.+)/.test(ln)) { html += '<div style="padding-left:12px">' + ln + '</div>'; continue; }
      if (ln.trim() === '') { html += '<div style="height:6px"></div>'; continue; }
      html += ln + '<br>';
    }
    if (inTable) html += '</table>';
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/`([^`]+)`/g, '<code style="background:rgba(0,0,0,0.06);padding:1px 4px;border-radius:3px;font-size:12px">$1</code>');
    return html;
  }

  function formatTime(ts) {
    var d = new Date(ts * 1000);
    var now = new Date();
    var hhmm = String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0');
    if (d.toDateString() === now.toDateString()) return '今天 ' + hhmm;
    var yesterday = new Date(now); yesterday.setDate(yesterday.getDate() - 1);
    if (d.toDateString() === yesterday.toDateString()) return '昨天 ' + hhmm;
    return (d.getMonth() + 1) + '/' + d.getDate() + ' ' + hhmm;
  }

  /* ═══ Toggle ═══ */
  document.getElementById('chat-fab').addEventListener('click', function () {
    var panel = document.getElementById('chat-panel');
    var fab = this;
    var isOpen = panel.classList.toggle('open');
    fab.classList.toggle('open', isOpen);
    if (!isOpen) {
      document.getElementById('chat-history').classList.remove('open');
    }
    if (isOpen) {
      var msgs = document.getElementById('chat-messages');
      msgs.scrollTop = msgs.scrollHeight;
      document.getElementById('chat-input').focus();
    }
  });

  document.addEventListener('click', function (e) {
    var panel = document.getElementById('chat-panel');
    var fab = document.getElementById('chat-fab');
    if (panel.classList.contains('open') && !panel.contains(e.target) && !fab.contains(e.target)) {
      panel.classList.remove('open');
      fab.classList.remove('open');
      document.getElementById('chat-history').classList.remove('open');
    }
  });

  /* ═══ History Panel ═══ */
  document.getElementById('btn-history').addEventListener('click', function () {
    var hp = document.getElementById('chat-history');
    hp.classList.add('open');
    loadHistoryList();
  });

  document.getElementById('btn-history-close').addEventListener('click', function () {
    document.getElementById('chat-history').classList.remove('open');
  });

  function dateGroup(ts) {
    var d = new Date(ts * 1000), now = new Date();
    if (d.toDateString() === now.toDateString()) return '今天';
    var y = new Date(now); y.setDate(y.getDate() - 1);
    if (d.toDateString() === y.toDateString()) return '昨天';
    var diff = Math.floor((now - d) / 86400000);
    if (diff < 7) return '近 7 天';
    if (diff < 30) return '近 30 天';
    return '更早';
  }

  async function loadHistoryList() {
    var list = document.getElementById('chat-history-list');
    list.innerHTML = '<div class="chat-history-empty"><span class="icon">hourglass_empty</span>加载中...</div>';
    try {
      var res = await fetch('/api/chat/history');
      var data = await res.json();
      var sessions = data.sessions || [];
      if (!sessions.length) {
        list.innerHTML = '<div class="chat-history-empty"><span class="icon">chat_bubble_outline</span>暂无历史对话</div>';
        return;
      }
      var html = '', lastGroup = '';
      sessions.forEach(function (s) {
        var group = dateGroup(s.last_ts);
        if (group !== lastGroup) {
          html += '<div class="chat-history-group">' + group + '</div>';
          lastGroup = group;
        }
        var isCurrent = currentSessionId && s.session_id === currentSessionId;
        var cls = 'chat-history-item' + (isCurrent ? ' active' : '');
        var badge = isCurrent ? '<span class="chat-history-badge">当前</span>' : '';
        var iconName = isCurrent ? 'chat' : 'chat_bubble_outline';
        var displayName = escHtml(s.name || s.preview || '(空)');
        html += '<div class="' + cls + '" data-sid="' + escHtml(s.session_id) + '">' +
          '<div class="chat-history-item-icon"><span class="icon">' + iconName + '</span></div>' +
          '<div class="chat-history-item-body">' +
            '<div class="chat-history-item-preview">' + displayName + ' ' + badge + '</div>' +
            '<div class="chat-history-item-meta">' +
              '<span class="icon">schedule</span>' + formatTime(s.last_ts) +
              '<span class="sep">·</span>' +
              '<span class="icon">forum</span>' + s.msg_count + ' 条' +
            '</div>' +
          '</div>' +
          '<button class="chat-history-item-edit" data-sid="' + escHtml(s.session_id) + '" data-name="' + escHtml(s.name || s.preview || '') + '" title="重命名"><span class="icon">edit</span></button>' +
          '</div>';
      });
      list.innerHTML = html;
    } catch (e) {
      list.innerHTML = '<div class="chat-history-empty"><span class="icon">error_outline</span>加载失败</div>';
    }
  }

  document.getElementById('chat-history-list').addEventListener('click', function (e) {
    var editBtn = e.target.closest('.chat-history-item-edit');
    if (editBtn) {
      e.stopPropagation();
      var sid = editBtn.getAttribute('data-sid');
      var oldName = editBtn.getAttribute('data-name') || '';
      var newName = prompt('重命名对话', oldName);
      if (newName !== null && newName.trim() && newName.trim() !== oldName) {
        fetch('/api/chat/rename', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ session_id: sid, name: newName.trim() })
        }).then(function () { loadHistoryList(); });
      }
      return;
    }
    var item = e.target.closest('.chat-history-item');
    if (!item) return;
    var sid = item.getAttribute('data-sid');
    if (!sid) return;
    if (currentSessionId && sid === currentSessionId) {
      document.getElementById('chat-history').classList.remove('open');
      return;
    }
    loadSession(sid);
  });

  async function loadSession(sid) {
    document.getElementById('chat-history').classList.remove('open');
    var area = document.getElementById('chat-messages');
    area.innerHTML = '<div class="chat-msg bot" style="color:#9ca3af;font-size:12px">加载中...</div>';
    try {
      var res = await fetch('/api/chat/history?session_id=' + encodeURIComponent(sid));
      var data = await res.json();
      var msgs = data.messages || [];
      area.innerHTML = '';
      msgs.forEach(function (m) {
        if (m.role === 'system') {
          area.innerHTML += '<div class="chat-msg divider">— ' + escHtml(m.text) + ' —</div>';
        } else if (m.role === 'user') {
          area.innerHTML += '<div class="chat-msg user">' + escHtml(m.text) + '</div>';
        } else {
          area.innerHTML += '<div class="chat-msg bot">' + renderMd(m.text) + '</div>';
        }
      });
      if (!msgs.length) {
        area.innerHTML = '<div class="chat-msg bot">你好！我是 YICE 助手，有什么想了解的？</div>';
      }
      currentSessionId = sid;
      saveHistory();
      area.scrollTop = area.scrollHeight;
    } catch (e) {
      area.innerHTML = '<div class="chat-msg bot">加载历史失败: ' + escHtml(e.message) + '</div>';
    }
  }

  /* ═══ File ═══ */
  function renderFileTags() {
    var area = document.getElementById('chat-file-area');
    if (!chatFiles.length) { area.innerHTML = ''; return; }
    area.innerHTML = chatFiles.map(function (f, i) {
      var icon = f.type.startsWith('image/') ? 'image' : 'description';
      return '<div class="chat-file-tag"><span class="icon" style="font-size:14px;color:#d97706">' + icon + '</span>' +
        escHtml(f.name) +
        '<span class="icon" onclick="window.__chatWidget.removeFile(' + i + ')">close</span></div>';
    }).join('');
  }

  function attachFile(file) {
    if (!file) return;
    chatFiles.push(file);
    renderFileTags();
    document.getElementById('chat-input').focus();
  }

  function handleFile(input) {
    for (var i = 0; i < input.files.length; i++) {
      chatFiles.push(input.files[i]);
    }
    renderFileTags();
    document.getElementById('chat-input').focus();
    input.value = '';
  }

  document.getElementById('chat-input').addEventListener('paste', function (e) {
    var items = e.clipboardData && e.clipboardData.items;
    if (!items) return;
    for (var i = 0; i < items.length; i++) {
      if (items[i].kind === 'file') {
        e.preventDefault();
        var file = items[i].getAsFile();
        if (file) attachFile(file);
        return;
      }
    }
  });

  var panel = document.getElementById('chat-panel');
  panel.addEventListener('dragover', function (e) { e.preventDefault(); e.dataTransfer.dropEffect = 'copy'; });
  panel.addEventListener('drop', function (e) {
    e.preventDefault();
    var files = e.dataTransfer.files;
    if (files) for (var i = 0; i < files.length; i++) attachFile(files[i]);
  });

  function removeFile(idx) {
    if (idx === undefined) { chatFiles = []; } else { chatFiles.splice(idx, 1); }
    renderFileTags();
  }

  /* ═══ New Chat ═══ */
  document.getElementById('btn-new').addEventListener('click', newChat);

  function newChat() {
    fetch('/api/chat/reset', { method: 'POST' });
    currentSessionId = null;
    localStorage.removeItem(STORAGE_KEY + '_sid');
    var area = document.getElementById('chat-messages');
    area.innerHTML = '<div class="chat-msg bot">你好！我是 YICE 助手，有什么想了解的？</div>';
    saveHistory();
  }

  /* ═══ Send ═══ */
  async function send() {
    var input = document.getElementById('chat-input');
    var msg = input.value.trim();
    if (!msg || chatBusy) return;
    chatBusy = true;

    var area = document.getElementById('chat-messages');
    var sendBtn = document.querySelector('.chat-send');
    sendBtn.disabled = true;

    var userHtml = '';
    var contentMsg = msg;

    // 页面上下文：收集并生成 chip + 实际内容
    var ctxJson = '';
    if (ctxActive) {
      var pageCtx = gatherPageContext();
      ctxJson = JSON.stringify(pageCtx, null, 2);
      contentMsg = '[当前页面上下文]\n```json\n' + ctxJson + '\n```\n\n' + contentMsg;
      var ctxId = 'ctx-' + Date.now();
      userHtml += '<div class="chat-ctx-chip" onclick="var d=document.getElementById(\'' + ctxId + '\');d.classList.toggle(\'open\')">' +
        '<span class="icon">screen_share</span>已携带页面上下文' +
        '</div>' +
        '<div class="chat-ctx-chip-detail" id="' + ctxId + '">' + escHtml(ctxJson) + '</div>';
    }

    // 文件附件
    if (chatFiles.length) {
      var names = chatFiles.map(function (f) { return f.name; });
      userHtml += '<div style="font-size:11px;color:rgba(255,255,255,0.7);margin-bottom:4px">\u{1F4CE} ' + names.map(escHtml).join(', ') + '</div>';
      var fileParts = [];
      for (var fi = 0; fi < chatFiles.length; fi++) {
        var cf = chatFiles[fi];
        try {
          var isText = /\.(csv|json|txt|md|sql|js|py|html|css|xml|yml|yaml|log|sh)$/i.test(cf.name);
          if (isText) {
            var text = await cf.text();
            fileParts.push('[文件: ' + cf.name + ']\n```\n' + text.slice(0, 3000) + '\n```');
          } else {
            var b64 = await new Promise(function (resolve) {
              var reader = new FileReader();
              reader.onload = function () { resolve(reader.result); };
              reader.readAsDataURL(cf);
            });
            var upRes = await fetch('/api/chat/upload', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ name: cf.name, data: b64 })
            });
            var upData = await upRes.json();
            if (upData.path) {
              fileParts.push('[文件: ' + cf.name + '，已保存到 ' + upData.path + '，请用 Read 工具查看]');
            }
          }
        } catch (_) {}
      }
      contentMsg = fileParts.join('\n\n') + '\n\n' + contentMsg;
      removeFile();
    }

    if (ctxJson || chatFiles.length) userHtml += '<div style="margin-top:6px"></div>';
    userHtml += escHtml(msg);
    area.innerHTML += '<div class="chat-msg user">' + userHtml + '</div>';
    input.value = '';

    var botEl = document.createElement('div');
    botEl.className = 'chat-msg bot';
    botEl.innerHTML = '<span class="thinking-anim"><span class="typing-dot">\u25CF</span><span class="typing-dot">\u25CF</span><span class="typing-dot">\u25CF</span> 思考中</span>';
    area.appendChild(botEl);
    area.scrollTop = area.scrollHeight;
    var payload = { message: contentMsg };
    if (currentSessionId) payload.session_id = currentSessionId;

    try {
      var res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('API ' + res.status);

      var reader = res.body.getReader();
      var decoder = new TextDecoder();
      var full = '', buf = '';
      var cleared = false;

      while (true) {
        var chunk = await reader.read();
        if (chunk.done) break;
        buf += decoder.decode(chunk.value, { stream: true });
        var lines = buf.split('\n');
        buf = lines.pop();
        for (var i = 0; i < lines.length; i++) {
          if (!lines[i].startsWith('data:')) continue;
          var data = lines[i].slice(5).trim();
          if (data === '[DONE]') continue;
          try {
            var evt = JSON.parse(data);
            if (evt.type === 'timeout') {
              area.insertBefore(makeDivider('会话已超时，自动开启新对话'), botEl);
              currentSessionId = null;
            } else if (evt.type === 'init') {
              currentSessionId = evt.session_id || currentSessionId;
            } else if (evt.type === 'delta') {
              if (!cleared) { cleared = true; botEl.textContent = ''; }
              full += evt.text;
              botEl.textContent = full;
              area.scrollTop = area.scrollHeight;
            } else if (evt.type === 'thinking') {
              /* 思考过程不显示 */
            } else if (evt.type === 'done') {
              if (evt.session_id) currentSessionId = evt.session_id;
            }
          } catch (e) { if (e instanceof SyntaxError) continue; throw e; }
        }
      }

      if (full) {
        botEl.innerHTML = renderMd(full);
      } else {
        botEl.textContent = '(无响应)';
      }
      saveHistory();
    } catch (e) {
      botEl.textContent = '请求失败: ' + e.message;
      saveHistory();
    }

    chatBusy = false;
    sendBtn.disabled = false;
    area.scrollTop = area.scrollHeight;
    input.focus();
  }

  function makeDivider(text) {
    var el = document.createElement('div');
    el.className = 'chat-msg divider';
    el.textContent = '\u2014 ' + text + ' \u2014';
    return el;
  }

  /* ═══ Voice ═══ */
  var micStream = null, micCtx = null, micProcessor = null, micChunks = [];
  var micRecording = false;

  function toggleMic() {
    if (micRecording) stopMic(); else startMic();
  }

  async function startMic() {
    try {
      micStream = await navigator.mediaDevices.getUserMedia({ audio: { sampleRate: 16000, channelCount: 1, echoCancellation: true } });
    } catch (e) {
      console.error('mic access denied', e);
      return;
    }
    micRecording = true;
    micChunks = [];
    document.getElementById('chat-mic').classList.add('recording');
    document.querySelector('.chat-input-area').classList.add('recording');
    document.getElementById('chat-input').placeholder = '🎙 录音中，再次点击结束...';

    micCtx = new (window.AudioContext || window.webkitAudioContext)();
    var source = micCtx.createMediaStreamSource(micStream);
    micProcessor = micCtx.createScriptProcessor(4096, 1, 1);
    micProcessor.onaudioprocess = function (e) {
      var float32 = e.inputBuffer.getChannelData(0);
      var targetLen = Math.round(float32.length * 16000 / micCtx.sampleRate);
      var resampled = new Float32Array(targetLen);
      var ratio = micCtx.sampleRate / 16000;
      for (var i = 0; i < targetLen; i++) {
        var srcIdx = i * ratio;
        var lo = Math.floor(srcIdx), hi = Math.min(lo + 1, float32.length - 1);
        var frac = srcIdx - lo;
        resampled[i] = float32[lo] * (1 - frac) + float32[hi] * frac;
      }
      var int16 = new Int16Array(resampled.length);
      for (var j = 0; j < resampled.length; j++) {
        var s = Math.max(-1, Math.min(1, resampled[j]));
        int16[j] = s < 0 ? s * 0x8000 : s * 0x7FFF;
      }
      micChunks.push(new Uint8Array(int16.buffer));
    };
    source.connect(micProcessor);
    micProcessor.connect(micCtx.destination);
  }

  async function stopMic() {
    micRecording = false;
    var micBtn = document.getElementById('chat-mic');
    var inputArea = document.querySelector('.chat-input-area');
    micBtn.classList.remove('recording');
    inputArea.classList.remove('recording');

    if (micProcessor) { micProcessor.disconnect(); micProcessor = null; }
    if (micCtx) { micCtx.close(); micCtx = null; }
    if (micStream) { micStream.getTracks().forEach(function (t) { t.stop(); }); micStream = null; }

    if (!micChunks.length) {
      document.getElementById('chat-input').placeholder = '输入消息...';
      return;
    }

    var totalLen = micChunks.reduce(function (s, c) { return s + c.length; }, 0);
    var merged = new Uint8Array(totalLen);
    var offset = 0;
    for (var i = 0; i < micChunks.length; i++) {
      merged.set(micChunks[i], offset);
      offset += micChunks[i].length;
    }
    micChunks = [];

    var binary = '';
    for (var b = 0; b < merged.length; b++) {
      binary += String.fromCharCode(merged[b]);
    }
    var b64 = btoa(binary);

    var input = document.getElementById('chat-input');
    input.placeholder = '✨ 识别中...';
    micBtn.classList.add('recognizing');
    inputArea.classList.add('recognizing');
    try {
      var res = await fetch('/api/chat/asr', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ audio: b64 })
      });
      var data = await res.json();
      console.log('[ASR] response:', JSON.stringify(data));
      if (data.text) {
        input.value = (input.value ? input.value + ' ' : '') + data.text;
      } else {
        console.warn('[ASR] empty text, full response:', data);
      }
    } catch (e) {
      console.error('[ASR] failed', e);
    }
    micBtn.classList.remove('recognizing');
    inputArea.classList.remove('recognizing');
    input.placeholder = '输入消息...';
    input.focus();
  }

  /* ═══ Public API ═══ */
  window.__chatWidget = { send: send, handleFile: handleFile, removeFile: removeFile, newChat: newChat, toggleMic: toggleMic, toggleCtx: toggleCtx };
})();
