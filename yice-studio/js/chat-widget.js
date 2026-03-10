/**
 * YICE Chat Widget — 自注入式共享聊天组件
 * 所有页面（HTML / React）引用同一个文件
 */
(function () {
  'use strict';

  /* ═══ CSS ═══ */
  const style = document.createElement('style');
  style.textContent = `
.chat-fab {
  position: fixed; bottom: 24px; right: 24px;
  width: 48px; height: 48px; border-radius: 50%;
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  color: #fff; border: none; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 16px rgba(37,99,235,0.35);
  transition: all 0.2s; z-index: 100;
}
.chat-fab:hover { transform: scale(1.08); box-shadow: 0 6px 20px rgba(37,99,235,0.45); }
.chat-fab .icon { font-size: 22px; transition: transform 0.2s; }
.chat-fab.open .icon { transform: rotate(90deg); }

.chat-panel {
  position: fixed; bottom: 84px; right: 24px;
  width: 380px; height: 680px;
  background: var(--surface, #fff);
  border: 1px solid var(--border, #e5e7eb);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.12);
  display: none; flex-direction: column;
  z-index: 99; overflow: hidden;
}
.chat-panel.open { display: flex; animation: chat-enter 0.2s ease-out; }

@keyframes chat-enter {
  from { opacity: 0; transform: translateY(12px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.chat-header {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border, #e5e7eb);
  background: var(--surface-alt, #f9fafb);
}
.chat-header-avatar {
  width: 28px; height: 28px; border-radius: 50%;
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  display: flex; align-items: center; justify-content: center;
  font-family: var(--mono, monospace); font-size: 10px; font-weight: 700; color: #fff;
}
.chat-header-title { font-size: 13px; font-weight: 600; color: var(--text-1, #111827); flex: 1; }
.chat-header-status { font-size: 11px; color: var(--green, #10b981); }

.chat-messages {
  flex: 1; overflow-y: auto; padding: 16px;
  display: flex; flex-direction: column; gap: 12px;
}
.chat-msg {
  max-width: 85%; padding: 10px 14px;
  border-radius: 12px; font-size: 13px; line-height: 1.5;
  white-space: pre-wrap;
}
.chat-msg.bot {
  align-self: flex-start;
  background: var(--surface-alt, #f9fafb); border: 1px solid var(--border-light, #f3f4f6);
  color: var(--text-1, #111827); border-bottom-left-radius: 4px;
}
.chat-msg.user {
  align-self: flex-end;
  background: var(--blue, #2563eb); color: #fff;
  border-bottom-right-radius: 4px;
}
.chat-input-area {
  display: flex; align-items: center; gap: 8px;
  padding: 12px 16px;
  border-top: 1px solid var(--border, #e5e7eb);
}
.chat-input {
  flex: 1; font-family: var(--ui, system-ui); font-size: 13px;
  color: var(--text-1, #111827); background: var(--surface-alt, #f9fafb);
  border: 1px solid var(--border, #e5e7eb); border-radius: 20px;
  padding: 8px 14px; outline: none; transition: border-color 0.15s;
}
.chat-input:focus { border-color: var(--blue, #2563eb); }
.chat-input::placeholder { color: var(--text-3, #9ca3af); }
.chat-send {
  width: 32px; height: 32px; border-radius: 50%;
  background: var(--blue, #2563eb); color: #fff; border: none; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.15s; flex-shrink: 0;
}
.chat-send:hover { background: #1d4ed8; }
.chat-send:disabled { opacity: 0.4; cursor: not-allowed; }
.chat-send .icon { font-size: 16px; }
.chat-upload {
  width: 32px; height: 32px; border-radius: 50%;
  background: none; color: var(--text-3, #9ca3af); border: 1px solid var(--border, #e5e7eb);
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: all 0.15s; flex-shrink: 0;
}
.chat-upload:hover { color: var(--blue, #2563eb); border-color: var(--blue-border, #93c5fd); }
.chat-upload .icon { font-size: 16px; }
.chat-file-tag {
  display: flex; align-items: center; gap: 4px;
  padding: 4px 10px; margin: 0 16px 4px;
  background: var(--surface-alt, #f9fafb); border: 1px solid var(--border, #e5e7eb);
  border-radius: 6px; font-size: 11px; color: var(--text-2, #6b7280);
}
.chat-file-tag .icon { font-size: 14px; cursor: pointer; }
.chat-file-tag .icon:hover { color: var(--red, #ef4444); }
.chat-msg.bot .typing-dot { display: inline-block; animation: blink 1.2s infinite; }
.chat-msg.bot .typing-dot:nth-child(2) { animation-delay: 0.2s; }
.chat-msg.bot .typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink { 0%,80% { opacity: 0.2; } 40% { opacity: 1; } }
.thinking-anim { color: var(--text-3, #9ca3af); font-size: 12px; animation: pulse 1.5s ease-in-out infinite; }
@keyframes pulse { 0%,100% { opacity: 0.5; } 50% { opacity: 1; } }
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
    <div class="chat-header-avatar">YC</div>
    <span class="chat-header-title">YICE 助手</span>
    <span class="chat-header-status">● 在线</span>
  </div>
  <div class="chat-messages" id="chat-messages">
    <div class="chat-msg bot">你好！我是 YICE 助手，有什么想了解的？</div>
  </div>
  <div id="chat-file-area"></div>
  <div class="chat-input-area">
    <button class="chat-upload" onclick="document.getElementById('chat-file').click()" title="上传文件"><span class="icon">attach_file</span></button>
    <input type="file" id="chat-file" style="display:none" accept=".csv,.json,.xlsx,.txt,.png,.jpg" onchange="window.__chatWidget.handleFile(this)">
    <input class="chat-input" id="chat-input" type="text" placeholder="输入消息..." onkeydown="if(event.key==='Enter')window.__chatWidget.send()">
    <button class="chat-send" onclick="window.__chatWidget.send()"><span class="icon">send</span></button>
  </div>
</div>`;
  document.body.appendChild(wrapper);

  /* ═══ State ═══ */
  let chatBusy = false;
  let chatFile = null;

  function escHtml(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  /* ═══ Toggle ═══ */
  document.getElementById('chat-fab').addEventListener('click', function () {
    const panel = document.getElementById('chat-panel');
    const fab = this;
    const isOpen = panel.classList.toggle('open');
    fab.classList.toggle('open', isOpen);
    if (isOpen) document.getElementById('chat-input').focus();
  });

  document.addEventListener('click', function (e) {
    const panel = document.getElementById('chat-panel');
    const fab = document.getElementById('chat-fab');
    if (panel.classList.contains('open') && !panel.contains(e.target) && !fab.contains(e.target)) {
      panel.classList.remove('open');
      fab.classList.remove('open');
    }
  });

  /* ═══ File ═══ */
  function handleFile(input) {
    var file = input.files[0];
    if (!file) return;
    chatFile = file;
    document.getElementById('chat-file-area').innerHTML =
      '<div class="chat-file-tag"><span class="icon" style="font-size:14px;color:var(--blue,#2563eb)">description</span>' +
      escHtml(file.name) +
      '<span class="icon" onclick="window.__chatWidget.removeFile()">close</span></div>';
    input.value = '';
  }

  function removeFile() {
    chatFile = null;
    document.getElementById('chat-file-area').innerHTML = '';
  }

  /* ═══ Chat State ═══ */
  var chatHistory = [{ role: 'system', content: '你是 YICE 助手，一个专业的小红书营销数据分析助手。简洁、专业地回答问题。' }];

  /* ═══ Send ═══ */
  async function send() {
    var input = document.getElementById('chat-input');
    var msg = input.value.trim();
    if (!msg || chatBusy) return;
    chatBusy = true;

    var area = document.getElementById('chat-messages');
    var sendBtn = document.querySelector('.chat-send');
    sendBtn.disabled = true;

    var userHtml = escHtml(msg);
    var contentMsg = msg;
    if (chatFile) {
      userHtml = '<div style="font-size:11px;color:rgba(255,255,255,0.7);margin-bottom:4px">📎 ' + escHtml(chatFile.name) + '</div>' + userHtml;
      try {
        var text = await chatFile.text();
        var preview = text.slice(0, 3000);
        contentMsg = '[用户上传文件: ' + chatFile.name + ']\n```\n' + preview + '\n```\n\n' + msg;
      } catch (_) {}
      removeFile();
    }
    area.innerHTML += '<div class="chat-msg user">' + userHtml + '</div>';
    input.value = '';

    chatHistory.push({ role: 'user', content: contentMsg });

    var botEl = document.createElement('div');
    botEl.className = 'chat-msg bot';
    botEl.innerHTML = '<span class="thinking-anim"><span class="typing-dot">●</span><span class="typing-dot">●</span><span class="typing-dot">●</span> 思考中</span>';
    area.appendChild(botEl);
    area.scrollTop = area.scrollHeight;

    try {
      var res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: chatHistory.slice(-20) })
      });

      if (!res.ok) throw new Error('API ' + res.status);

      var reader = res.body.getReader();
      var decoder = new TextDecoder();
      var full = '', reasoning = '', buf = '';
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
            var delta = evt.choices && evt.choices[0] && evt.choices[0].delta;
            if (!delta) continue;
            if (delta.reasoning_content) {
              reasoning += delta.reasoning_content;
              if (!cleared) { cleared = true; botEl.textContent = ''; }
              botEl.textContent = '💭 ' + reasoning;
              area.scrollTop = area.scrollHeight;
            }
            if (delta.content) {
              if (!cleared) { cleared = true; botEl.textContent = ''; }
              full += delta.content;
              botEl.textContent = full;
              area.scrollTop = area.scrollHeight;
            }
          } catch (e) { if (e instanceof SyntaxError) continue; throw e; }
        }
      }

      if (!full && reasoning) full = reasoning;
      if (!full) full = '(无响应)';
      chatHistory.push({ role: 'assistant', content: full });
    } catch (e) {
      botEl.textContent = '请求失败: ' + e.message;
    }

    chatBusy = false;
    sendBtn.disabled = false;
    area.scrollTop = area.scrollHeight;
    input.focus();
  }

  /* ═══ Public API ═══ */
  window.__chatWidget = { send: send, handleFile: handleFile, removeFile: removeFile };
})();
