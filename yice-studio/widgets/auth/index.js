/* 认证守卫
 *
 * 所有需要登录的页面引入此脚本（login.html 除外）。
 * 1. 请求 /api/me 验证会话
 * 2. 未登录 → 跳转 login.html
 * 3. 已登录 → 设置 window.YICE_USER，渲染用户菜单
 */

(async function () {
  try {
    const resp = await fetch('/api/me');
    if (!resp.ok) throw new Error();
    window.YICE_USER = await resp.json();
    _renderUserMenu(window.YICE_USER);
  } catch {
    location.href = '/login.html';
  }
})();

function _renderUserMenu(user) {
  // 头像按钮
  const avatarBtn = document.querySelector('.user-avatar-btn');
  if (avatarBtn) {
    const img = avatarBtn.querySelector('img');
    if (img && user.avatar) {
      img.src = user.avatar;
      img.alt = user.name;
    } else if (img && !user.avatar) {
      img.replaceWith(_makeInitial(user.name, 28));
    }
    avatarBtn.title = user.name;
  }

  // 用户菜单面板
  const panel = document.getElementById('user-menu');
  if (!panel) return;

  const avatarHtml = user.avatar
    ? `<img src="${user.avatar}" style="width:48px;height:48px;border-radius:50%;object-fit:cover;border:2px solid #f3f4f6">`
    : _makeInitial(user.name, 48).outerHTML;

  const roleLabel = user.role === 'root' ? 'root' : 'member';
  const roleBg = user.role === 'root' ? 'linear-gradient(135deg,#2563eb,#3b82f6)' : 'linear-gradient(135deg,#059669,#10b981)';

  panel.innerHTML = `
    <div style="padding:20px 20px 14px;display:flex;flex-direction:column;align-items:center;gap:8px;border-bottom:1px solid var(--border)">
      ${avatarHtml}
      <div style="text-align:center">
        <div style="display:flex;align-items:center;justify-content:center;gap:6px;margin-bottom:2px">
          <span style="font-size:14px;font-weight:600;color:var(--text-1)">${user.name}</span>
          <span style="font-size:10px;padding:1px 8px;border-radius:10px;background:${roleBg};color:#fff;font-weight:500;letter-spacing:0.5px">${roleLabel}</span>
        </div>
        ${user.department ? `<div style="display:flex;align-items:center;justify-content:center;gap:4px;font-size:11px;color:var(--text-3)"><span class="icon" style="font-size:13px">corporate_fare</span>${user.department}</div>` : ''}
      </div>
    </div>
    <div style="padding:4px">
      <button class="hdr-menu-item" onclick="yiceLogout()"><span class="icon">logout</span>退出登录</button>
    </div>`;
}

function _makeInitial(name, size) {
  const span = document.createElement('span');
  span.textContent = (name || '?')[0];
  span.style.cssText = `display:inline-flex;align-items:center;justify-content:center;width:${size}px;height:${size}px;border-radius:50%;background:linear-gradient(135deg,#2563eb,#3b82f6);color:#fff;font-size:${Math.round(size*0.45)}px;font-weight:600`;
  return span;
}

async function yiceLogout() {
  try {
    await fetch('/api/logout', { method: 'POST' });
  } catch { /* ignore */ }
  location.href = '/login.html';
}
