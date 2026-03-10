#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""浏览器端采集 JS — 由 Claude 注入 adstar.alimama.com 页面执行。
API 请求在浏览器内发起（绕过 TLS 指纹反爬），结果 POST 到本地 Flask 保存。
注入顺序：1) 滑块检测  2) 工具函数  3) 启动采集（非阻塞）

滑块处理：
- JS 仅负责检测滑块出现并报告坐标（window.__xh_slider）
- Claude 通过浏览器工具 left_click_drag 执行真实鼠标拖拽（isTrusted=true）
- ag 函数在滑块出现期间自动暂停，等待 Claude 处理完后继续

增量逻辑：
- 新任务（history 中无记录）：全量采集，startTime=任务开始日期
- 老任务（history 中有记录）：增量采集，startTime=上次采集日期，数据合并去重
- 状态标识：★=全量 △=增量"""

# Step 0: 滑块检测器（仅检测+报坐标，不做拖拽）
INJECT_SLIDER = r"""(function(){
if(window.__xh_slider)return'EXISTS';
const S=window.__xh_slider={detected:false,btn:null,track:null,ok:0,log:m=>console.log('[SL] '+m)};

function findBtn(root){
  root=root||document;
  const sels=['[id$="_n1z"]','.btn_slide','.slide-btn','.nc-lang-cnt [class*="btn"]','[data-nc-type="slide"]'];
  for(const s of sels){try{const e=root.querySelector(s);if(e&&e.offsetWidth>0)return e}catch(x){}}
  return null;
}
function findTrack(btn,root){
  root=root||document;
  const sels=['.nc-lang-cnt','.nc_scale','.nc-container','.slide-track'];
  for(const s of sels){try{const e=root.querySelector(s);if(e&&e.offsetWidth>0)return e}catch(x){}}
  return btn.parentElement;
}
function rect(el){const r=el.getBoundingClientRect();return{x:~~r.left,y:~~r.top,w:~~r.width,h:~~r.height}}

function check(){
  let btn=findBtn();
  if(btn){
    const track=findTrack(btn);
    S.detected=true;S.btn=rect(btn);S.track=rect(track);
    if(!S._l){S.log('DETECTED btn='+JSON.stringify(S.btn)+' track='+JSON.stringify(S.track));S._l=true}
    return;
  }
  for(const f of document.querySelectorAll('iframe')){
    try{
      const d=f.contentDocument;if(!d)continue;
      btn=findBtn(d);
      if(btn){
        const track=findTrack(btn,d);
        const fr=f.getBoundingClientRect(),br=btn.getBoundingClientRect(),tr=track.getBoundingClientRect();
        S.detected=true;
        S.btn={x:~~(fr.left+br.left),y:~~(fr.top+br.top),w:~~br.width,h:~~br.height};
        S.track={x:~~(fr.left+tr.left),y:~~(fr.top+tr.top),w:~~tr.width,h:~~tr.height};
        if(!S._l){S.log('DETECTED in iframe');S._l=true}
        return;
      }
    }catch(e){}
  }
  if(S.detected){S.detected=false;S.btn=null;S.track=null;S._l=false;S.ok++;S.log('CLEARED #'+S.ok)}
}

new MutationObserver(()=>setTimeout(check,300)).observe(document.body,{childList:true,subtree:true});
setInterval(check,2000);
S.log('detector active');
})();'SLIDER_OK'"""

# Step 1: 工具函数（ag 在滑块出现时暂停等待）
INJECT_FUNCTIONS = r"""window.__xh={F:'http://127.0.0.1:18008',D:2000,sl:ms=>new Promise(r=>setTimeout(r,ms)),rn:(a,b)=>Math.floor(Math.random()*(b-a+1))+a,tk:()=>{const t=document.cookie.split(';').map(p=>p.trim()).find(p=>p.startsWith('_tb_token_='));return t?t.split('=')[1]:''},po:async(p,b)=>(await fetch(window.__xh.F+p,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)})).json(),ag:async u=>{while(window.__xh_slider&&window.__xh_slider.detected)await window.__xh.sl(1000);try{const r=await fetch(u,{headers:{'_tb_token_':window.__xh.tk(),'x-requested-with':'XMLHttpRequest'},credentials:'include'});return JSON.parse(await r.text())}catch{return null}},fp:async(e,s,t,b,c)=>{let a=[],p=1;while(true){const u=`/openapi/param2/1/gateway.unionpub/union.adstar.effect.data.detail.json?bizCode=adstar&_tb_token_=${window.__xh.tk()}&eventId=${e}&mediaType=RED_BOOK&startTime=${encodeURIComponent(s)}&endTime=${encodeURIComponent(t)}&dataBatch=${b}&pageNo=${p}&pageSize=50&contentId&subEventId&dataType&cycle=${c}`;const d=await window.__xh.ag(u);if(!d||!d.data||!d.data.result)break;a=a.concat(d.data.result);if(p>=(d.data.totalPages||1))break;p++;await window.__xh.sl(window.__xh.D)}return a}};'OK'"""

# Step 2: 启动采集（增量逻辑）
# ★=全量（新任务） △=增量（老任务，从 last_crawl 开始，merge 合并）
INJECT_CRAWL = r"""(async()=>{const X=window.__xh;X.s='START';const r=await fetch(X.F+'/api/tasks').then(r=>r.json());if(r.code!==0){X.s='ERR';return}const dn=new Set(r.completed),hi=r.history||{},pd=r.tasks.filter(t=>!dn.has(t.eventId));if(!pd.length){X.s='ALL_DONE';return}let ok=0;for(let i=0;i<pd.length;i++){const t=pd[i],e=t.eventId,n=t.name||e,nw=!(String(e) in hi);X.s=`${n}(${i+1}/${pd.length})${nw?'★':'△'}`;const b=await X.ag(`/api/cpa/event/info/detail?bizCode=adstar&_tb_token_=${X.tk()}&eventId=${e}`);if(!b)continue;if(b.code===601){X.s='COOKIE_EXPIRED';return}await X.po('/api/save',{eventId:e,type:'base',data:b});const bi=(b.model||{}).basicInfo||{};if(!bi.startTime||!bi.endTime){await X.po('/api/complete',{eventId:e});ok++;continue}const st=nw?bi.startTime+' 00:00:00':hi[String(e)].last_crawl+' 00:00:00',et=bi.endTime+' 23:59:59',mg=!nw;for(const d of[{b:'EVENT',c:15,f:'event_15'},{b:'EVENT',c:30,f:'event_30'},{b:'EVENT_CONTENT',c:15,f:'content_15'},{b:'EVENT_CONTENT',c:30,f:'content_30'}]){const data=await X.fp(e,st,et,d.b,d.c);await X.po('/api/save',{eventId:e,type:d.f,data:data,merge:mg})}await X.po('/api/complete',{eventId:e});ok++;if(i<pd.length-1)await X.sl(X.rn(1000,10000))}X.s=`DONE:${ok}/${pd.length}`})();'LAUNCHED'"""

if __name__ == '__main__':
    print("=== 浏览器采集 JS ===\n")
    print("Step 0 — 注入滑块检测器:")
    print(INJECT_SLIDER)
    print("\nStep 1 — 注入工具函数:")
    print(INJECT_FUNCTIONS)
    print("\nStep 2 — 启动采集:")
    print(INJECT_CRAWL)
