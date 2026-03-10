---
name: crawl_xh_data
type: tool
description: 采集星河平台任务数据，输出本地 JSON。Use when user says 采集、更新星河、crawl xh, or mentions adstar/星河 data collection.
trigger: /crawl-xh
---

# crawl_xh_data

采集阿里妈妈星河平台（adstar.alimama.com）小红书任务数据。
所有 API 请求在浏览器内发起（绕过 TLS 指纹反爬），结果通过本地 HTTP 服务保存。

## 执行规则

- **严格按 Step 1→6 顺序执行，禁止跳步、合并、并行**
- **每个 Step 必须成功后才能进入下一步**
- **每次触发都必须完整执行全流程**，包括 reset，不能因为"刚跑过"而跳过
- **全程自动执行，无需用户确认**，包括登录确认、采集启动等所有步骤

## 前置条件

- Python 3.9+
- Chrome 已登录 adstar.alimama.com

## 增量逻辑

- **新任务**（无已有数据）：全量拉取，startTime = 任务开始日期，状态标 ★
- **老任务**（有已有数据）：**按表独立增量**，startTime = 该表实际 max(theDate) + 1 天，状态标 △
- **所有 cycle 统一逻辑**：有数据则增量，无数据则全量，不区分 cycle=15/30
- **去重规则**：event 数据按 `theDate`，content 数据按 `contentId` + `theDate`，新数据覆盖旧数据
- **判断依据**：HTTP 服务扫描 out/xh_data/ 目录下实际文件的 max_date

## 工作流

### Step 1: 启动 HTTP 服务

```bash
# 检查是否已运行
lsof -i :18008
# 未运行则后台启动
nohup python3 .claude/skills/crawl_xh_data/scripts/http_service.py >/dev/null 2>&1 &
```

验证：`curl -s http://127.0.0.1:18008/health` 返回 `{"status":"ok"}`

### Step 2: 重置完成列表

每次采集前必须清除 completed，确保所有任务都会被执行：

```bash
curl -s -X POST http://127.0.0.1:18008/api/reset
```

### Step 3: 获取浏览器 tab

```
tabs_context_mcp(createIfEmpty=true) → 获取 tabId
```

### Step 4: 登录确认（自动）

1. 导航到 `https://adstar.alimama.com`
2. 等待 3s 页面加载
3. 截图检查页面状态：
   - **已登录**（能看到导航栏和用户菜单）→ 直接进入 Step 5
   - **确认登录页**（显示「快速进入」按钮）→ 自动点击「快速进入」→ 等待 3s → 截图确认进入主页
   - **未登录**（需要扫码/输入密码）→ 提示用户手动登录 → **停止后续步骤**

### Step 5: 注入 JS 采集

分三步注入（避免超时）：

**第一步：注入滑块检测器**

```javascript
// javascript_tool 注入到 adstar.alimama.com 页面
// 仅检测滑块并报告坐标，实际拖拽由 Claude 浏览器工具执行
(function(){
if(window.__xh_slider)return'EXISTS';
const S=window.__xh_slider={detected:false,btn:null,track:null,ok:0,log:m=>console.log('[SL] '+m)};
function findBtn(root){root=root||document;const sels=['[id$="_n1z"]','.btn_slide','.slide-btn','.nc-lang-cnt [class*="btn"]','[data-nc-type="slide"]'];for(const s of sels){try{const e=root.querySelector(s);if(e&&e.offsetWidth>0)return e}catch(x){}}return null}
function findTrack(btn,root){root=root||document;const sels=['.nc-lang-cnt','.nc_scale','.nc-container','.slide-track'];for(const s of sels){try{const e=root.querySelector(s);if(e&&e.offsetWidth>0)return e}catch(x){}}return btn.parentElement}
function rect(el){const r=el.getBoundingClientRect();return{x:~~r.left,y:~~r.top,w:~~r.width,h:~~r.height}}
function check(){let btn=findBtn();if(btn){const track=findTrack(btn);S.detected=true;S.btn=rect(btn);S.track=rect(track);if(!S._l){S.log('DETECTED btn='+JSON.stringify(S.btn)+' track='+JSON.stringify(S.track));S._l=true}return}for(const f of document.querySelectorAll('iframe')){try{const d=f.contentDocument;if(!d)continue;btn=findBtn(d);if(btn){const track=findTrack(btn,d);const fr=f.getBoundingClientRect(),br=btn.getBoundingClientRect(),tr=track.getBoundingClientRect();S.detected=true;S.btn={x:~~(fr.left+br.left),y:~~(fr.top+br.top),w:~~br.width,h:~~br.height};S.track={x:~~(fr.left+tr.left),y:~~(fr.top+tr.top),w:~~tr.width,h:~~tr.height};if(!S._l){S.log('DETECTED in iframe');S._l=true}return}}catch(e){}}if(S.detected){S.detected=false;S.btn=null;S.track=null;S._l=false;S.ok++;S.log('CLEARED #'+S.ok)}}
new MutationObserver(()=>setTimeout(check,300)).observe(document.body,{childList:true,subtree:true});setInterval(check,2000);S.log('detector active');
})();'SLIDER_OK'
```

验证：返回 `SLIDER_OK`

**第二步：注入工具函数**

```javascript
// ag 函数在滑块出现时自动暂停，等待 Claude 拖拽完成后继续
window.__xh={F:'http://127.0.0.1:18008',sl:ms=>new Promise(r=>setTimeout(r,ms)),rn:(a,b)=>Math.floor(Math.random()*(b-a+1))+a,nd:s=>{const d=new Date(s);d.setDate(d.getDate()+1);return d.toISOString().slice(0,10)},tk:()=>{const t=document.cookie.split(';').map(p=>p.trim()).find(p=>p.startsWith('_tb_token_='));return t?t.split('=')[1]:''},po:async(p,b)=>(await fetch(window.__xh.F+p,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)})).json(),ag:async u=>{while(window.__xh_slider&&window.__xh_slider.detected)await window.__xh.sl(1000);try{const r=await fetch(u,{headers:{'_tb_token_':window.__xh.tk(),'x-requested-with':'XMLHttpRequest'},credentials:'include'});return JSON.parse(await r.text())}catch{return null}},fp:async(e,s,t,b,c)=>{let a=[],p=1;while(true){const u=`/openapi/param2/1/gateway.unionpub/union.adstar.effect.data.detail.json?bizCode=adstar&_tb_token_=${window.__xh.tk()}&eventId=${e}&mediaType=RED_BOOK&startTime=${encodeURIComponent(s)}&endTime=${encodeURIComponent(t)}&dataBatch=${b}&pageNo=${p}&pageSize=50&contentId&subEventId&dataType&cycle=${c}`;const d=await window.__xh.ag(u);if(!d||!d.data||!d.data.result)break;a=a.concat(d.data.result);if(p>=(d.data.totalPages||1))break;p++;await window.__xh.sl(window.__xh.rn(1000,2000))}return a}};
'OK'
```

验证：返回 `OK`

**第三步：启动采集（非阻塞，自动判断全量/增量）**

```javascript
(async()=>{const X=window.__xh;X.s='START';const r=await fetch(X.F+'/api/tasks').then(r=>r.json());if(r.code!==0){X.s='ERR';return}const dn=new Set(r.completed),dd=r.data_dates||{},pd=r.tasks.filter(t=>!dn.has(t.eventId));if(!pd.length){X.s='ALL_DONE';return}let ok=0;for(let i=0;i<pd.length;i++){const t=pd[i],e=t.eventId,n=t.name||e,ed=dd[String(e)]||{},nw=!Object.keys(ed).length;X.s=`${n}(${i+1}/${pd.length})${nw?'★':'△'}`;const b=await X.ag(`/api/cpa/event/info/detail?bizCode=adstar&_tb_token_=${X.tk()}&eventId=${e}`);if(!b)continue;if(b.code===601){X.s='COOKIE_EXPIRED';return}await X.po('/api/save',{eventId:e,type:'base',data:b});const bi=(b.model||{}).basicInfo||{};if(!bi.startTime||!bi.endTime){await X.po('/api/complete',{eventId:e});ok++;continue}const fst=bi.startTime+' 00:00:00',et=bi.endTime+' 23:59:59';for(const d of[{b:'EVENT',c:15,f:'event_15'},{b:'EVENT',c:30,f:'event_30'},{b:'EVENT_CONTENT',c:15,f:'content_15'},{b:'EVENT_CONTENT',c:30,f:'content_30'}]){const md=ed[d.f],st=md?X.nd(md)+' 00:00:00':fst,mg=!!md;X.s=`${n}(${i+1}/${pd.length})${nw?'★':'△'} ${d.f}`;let data=await X.fp(e,st,et,d.b,d.c);if(!data.length&&nw){for(let rt=0;rt<2;rt++){X.s=`${n}(${i+1}/${pd.length})★ retry${d.f}#${rt+1}`;await X.sl(3000);data=await X.fp(e,st,et,d.b,d.c);if(data.length)break}}if(data.length||nw){await X.po('/api/save',{eventId:e,type:d.f,data:data,merge:mg})}}await X.po('/api/complete',{eventId:e});ok++;if(i<pd.length-1)await X.sl(X.rn(1000,10000))}X.s=`DONE:${ok}/${pd.length}`})();
'LAUNCHED'
```

验证：返回 `LAUNCHED`

### Step 6: 轮询进度 + 滑块处理

每 15s 用 `javascript_tool` 查状态（进度 + 滑块一次查完）：

```javascript
JSON.stringify({s:window.__xh.s, sl:window.__xh_slider?{d:window.__xh_slider.detected,b:window.__xh_slider.btn,t:window.__xh_slider.track,ok:window.__xh_slider.ok}:null})
```

**进度状态**（`s` 字段）：
- `任务名(1/5)★` = 全量采集中
- `任务名(2/5)△` = 增量采集中
- `DONE:5/5` = 全部完成
- `COOKIE_EXPIRED` = Cookie 过期，提示用户重新登录

**滑块处理**（`sl.d === true` 时）：

1. 通过飞书 webhook 发送通知：
   ```bash
   curl -s -X POST -H "Content-Type: application/json" \
     -d '{"msg_type":"text","content":{"text":"⚠️ 星河采集：滑块验证触发，请手动处理\n当前任务：'${TASK_STATUS}'"}}' \
     https://open.feishu.cn/open-apis/bot/v2/hook/ea7d3a63-61e7-4423-9b27-356784619eb0
   ```
2. **同一次滑块只通知一次**，记录已通知的 `sl.ok` 值，避免重复发送
3. **不自动执行滑块操作**，等待 3 分钟让用户手动处理，期间每 30s 轮询一次滑块状态，若滑块已消失则立即继续
4. 3 分钟后若滑块仍在，刷新页面（导航回 `https://adstar.alimama.com`），等待 3s
5. 重新注入 Step 5 三段 JS（已完成任务自动跳过），继续轮询

**每 5 个任务刷新页面**（防止 TMD 反爬累积）：

轮询时记录 `done` 数，每累计完成 5 个任务刷新一次（即 done 达到 5, 10, 15...时）：
1. 导航回 `https://adstar.alimama.com` 刷新页面
2. 等待 3s 页面加载
3. 重新注入 Step 5 三段 JS（已完成任务自动跳过）
4. 继续轮询

也可用 HTTP 服务查进度：

```bash
curl -s http://127.0.0.1:18008/api/progress
```

### Step 7: T+2 校验

平台数据有 2 天延迟，采集完成后校验数据时效性：

1. 扫描每个任务 out/xh_data/{eventId}/ 下所有表的 max_date
2. 跳过已结束任务（base.json 中 endTime < today - 2）和空数据任务
3. 若有任务 max_date < today - 2：重新执行 Step 2 → 6（增量重跑）
4. 重试后仍无新数据 → 平台确实未更新，正常结束

### Cookie 过期处理

`window.__xh.s === 'COOKIE_EXPIRED'` 时：

1. 提示用户在浏览器中重新登录
2. 确认登录后从 Step 5 重新注入（已完成的任务自动跳过）

## tasks.json 格式

位于 `out/xh_data/tasks.json`：

```json
[
  {"eventId": 113152481, "name": "大厨-双11-小白马"},
  {"eventId": 116228750, "name": "大厨-双12-烟机kol"}
]
```

## 输出

```
out/xh_data/
├── tasks.json          # [{eventId, name}]
├── {eventId}/
│   ├── base.json        # 任务基础信息
│   ├── event_15.json    # 任务维度 15 天（按 theDate 去重合并）
│   ├── event_30.json    # 任务维度 30 天
│   ├── content_15.json  # 内容维度 15 天（按 contentId+theDate 去重合并）
│   └── content_30.json  # 内容维度 30 天
└── progress.json        # history + 当日完成列表
```

## 频率控制

- 任务内 API：无延迟（连续请求）
- 翻页间隔：1-2s 随机
- 任务间隔：1-10s 随机

## 采集报告

Workflow 完成后（Step 7 之后）输出标准报告：

```
══════════════════════════════════════════════════════
  📊 星河数据采集报告 | {YYYY-MM-DD HH:MM}
══════════════════════════════════════════════════════

  任务总数: {N} | 进行中: {N} | 已结束: {N}
  数据总量: {N} 条 | 耗时: {N}分{N}秒

──────────────────────────────────────────────────────
🟢 {任务名}                              ← 进行中
   eventId: {id} | {startTime} ~ {endTime}
   数据最新: {max_date} | {total} 条
     event_15    {count} 条  最新 {date}
     event_30    {count} 条  最新 {date}
     content_15  {count} 条  最新 {date}
     content_30  {count} 条  最新 {date}

⚪ {任务名}                              ← 已结束
   ...同上...

══════════════════════════════════════════════════════
```

规则：
- 🟢 进行中 / ⚪ 已结束
- 空数据任务标注「无数据」，不展开表明细
- 按任务名排序
