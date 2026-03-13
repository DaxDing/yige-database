/* 一键刷新组件
 *
 * 统一处理：服务端缓存清除 → 页面数据重载 → 跨 tab 通知 → UI 反馈
 *
 * 用法：
 *   1. <script src="widgets/refresh/index.js"></script>
 *   2. registerRefresh(async () => { await loadData(); render(); });
 *   3. <button onclick="refreshAll()">刷新</button>  (id="sync-btn")
 */

let _onRefresh = null;

window.registerRefresh = function(fn) {
  _onRefresh = fn;
};

window.showToast = function(msg, persist) {
  let el = document.getElementById('toast');
  if (!el) { el = document.createElement('div'); el.id = 'toast'; document.body.appendChild(el); }
  el.textContent = msg; el.className = 'toast show';
  clearTimeout(el._t);
  if (!persist) el._t = setTimeout(() => el.className = 'toast', 2500);
};

function _setLoading(on) {
  const shell = document.querySelector('.shell');
  if (shell) shell.classList.toggle('refreshing', on);
  const btn = document.getElementById('sync-btn');
  if (btn) { btn.disabled = on; btn.classList.toggle('spinning', on); }
}

const _bc = new BroadcastChannel('yice_refresh');
_bc.onmessage = async () => {
  showToast('其他页面触发刷新…', true);
  if (_onRefresh) await _onRefresh(true);
  showToast('刷新完成');
};

window.refreshAll = async function() {
  _setLoading(true);
  showToast('正在刷新数据…', true);
  const t0 = Date.now();
  if (_onRefresh) await _onRefresh(true);
  _bc.postMessage('refresh');
  _setLoading(false);
  const sec = ((Date.now() - t0) / 1000).toFixed(1);
  showToast('刷新完成 ' + sec + 's');
};
