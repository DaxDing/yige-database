/* 设置菜单组件
 *
 * 统一渲染：资源配置 / 组织配置 入口
 *
 * 用法：
 *   1. <script src="widgets/settings-menu/index.js"></script>
 *   2. 菜单容器 <div class="hdr-menu" id="settings-menu"></div>
 *      — 空容器：自动填充全部菜单项
 *      — 有子元素：追加到 #settings-menu-extra（如 ad-studio）
 */

const SETTINGS_MENU_ITEMS = [
  { label: '资源配置', icon: 'key', page: 'accounts' },
  { label: '组织配置', icon: 'apartment', page: 'enterprise' },
];

function _buildMenuHtml() {
  const isProjectPage = location.pathname.includes('project-management');
  return SETTINGS_MENU_ITEMS.map(item => {
    if (isProjectPage) {
      return `<button class="hdr-menu-item" onclick="openResPage('${item.page}')"><span class="icon">${item.icon}</span>${item.label}</button>`;
    }
    return `<a class="hdr-menu-item" href="project-management.html?page=${item.page}"><span class="icon">${item.icon}</span>${item.label}</a>`;
  }).join('');
}

window.renderSettingsMenu = function() {
  const extra = document.getElementById('settings-menu-extra');
  if (extra) { extra.innerHTML = _buildMenuHtml(); return; }
  const slot = document.getElementById('settings-menu');
  if (slot) slot.innerHTML = _buildMenuHtml();
};

document.addEventListener('DOMContentLoaded', () => renderSettingsMenu());
