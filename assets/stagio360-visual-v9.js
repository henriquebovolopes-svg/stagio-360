/* STAGIO 360 | UX visual v9. Nenhuma credencial, dado individual ou acesso ao Supabase. */
(function(){
'use strict';
var palette={
 blue:'#2f73d9',cyan:'#35c4e8',violet:'#7c5cfa',
 green:'#27ae60',amber:'#e1a32f',orange:'#eb9248',
 red:'#dc5959',sky:'#5ea6ff'
};
var ordered=[palette.blue,palette.cyan,palette.violet,palette.green,palette.orange,palette.sky];
var script=document.currentScript;
var base=script&&script.src?script.src:'';
var aggUrl=new URL('./stagio360-2026-agregados.json',base).href;
var historyUrl=new URL('./stagio360-historico.json',base).href;
function node(tag,text,cls){
 var e=document.createElement(tag);
 if(text!==undefined&&text!==null)e.textContent=String(text);
 if(cls)e.className=cls;
 return e;
}
function appendChildren(parent,children){children.forEach(function(x){parent.appendChild(x)});return parent}
function getRoot(){return location.pathname.indexOf('/admin/')!==-1?'../':'./'}
function buildSidebar(){
 if(!document.body.classList.contains('s360-chrome'))return;
 if(document.querySelector('.s360-global-sidebar'))return;
 var root=getRoot();
 var sidebar=node('aside',null,'s360-global-sidebar');
 sidebar.id='s360-global-sidebar';
 var brand=node('a',null,'s360-global-brand');brand.href=root+'painel.html';brand.setAttribute('aria-label','Stagio Academy · Visão institucional');
 var brandImage=node('img');brandImage.src=root+'assets/stagio-academy-logo.svg';brandImage.alt='Stagio Academy · Ensinar, aprender e transformar';brand.appendChild(brandImage);sidebar.appendChild(brand);
 var nav=node('nav',null,'s360-global-nav');nav.setAttribute('aria-label','Navegação institucional');
 var links=[
  {label:'Governança',href:root+'painel.html',icon:'▦',page:'painel.html'},
  {label:'Avaliação 360',href:root+'admin/governanca.html',icon:'◎',page:'governanca.html'},
  {label:'Planejamento docente',href:root+'admin/planejamento.html',icon:'▥',page:'planejamento.html'},
  {label:'Funcionários · privado',href:root+'admin/funcionarios.html',icon:'♧',page:'funcionarios.html'},
  {label:'Minha área',href:root+'admin/minha-area.html',icon:'⌂',page:'minha-area.html'},
  {label:'Painel administrativo',href:root+'admin/index.html',icon:'▣',page:'index.html'},
  {label:'Pesquisas 2026',href:root+'admin/pesquisas-2026.html',icon:'◉',page:'pesquisas-2026.html'},
  {label:'Resultados acadêmicos',href:root+'admin/academico.html',icon:'▤',page:'academico.html'},
  {label:'Integração de dados',href:root+'admin/integracao.html',icon:'◇',page:'integracao.html'}
 ];
 var current=location.pathname.split('/').pop()||'';
 var logicalPage=({'segmento.html':'governanca.html','infantil.html':'governanca.html','coord-fii-em.html':'governanca.html'})[current]||current;
 links.forEach(function(item){
  var a=node('a');a.href=item.href;
  var glyph=node('span',item.icon,'s360-nav-icon');glyph.setAttribute('aria-hidden','true');
  appendChildren(a,[glyph,node('span',item.label)]);
  if(logicalPage===item.page)a.setAttribute('aria-current','page');
  nav.appendChild(a);
 });
 sidebar.appendChild(nav);
 var foot=node('div',null,'s360-global-footer');
 appendChildren(foot,[node('strong','Inteligência pedagógica'),node('span','Stagio 360 · Governança e avaliação institucional')]);
 sidebar.appendChild(foot);
 var toggle=node('button','☰','s360-menu-toggle');toggle.type='button';toggle.setAttribute('aria-label','Abrir menu institucional');toggle.setAttribute('aria-controls',sidebar.id);toggle.setAttribute('aria-expanded','false');
 function close(){
  document.body.classList.remove('s360-menu-open');toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','Abrir menu institucional');
 }
 toggle.addEventListener('click',function(){
  var open=document.body.classList.toggle('s360-menu-open');
  toggle.setAttribute('aria-expanded',String(open));
  toggle.setAttribute('aria-label',open?'Fechar menu institucional':'Abrir menu institucional');
 });
 nav.addEventListener('click',function(event){if(event.target.closest('a'))close()});
 document.addEventListener('keydown',function(event){if(event.key==='Escape')close()});
 document.addEventListener('click',function(event){
  if(document.body.classList.contains('s360-menu-open')&&!sidebar.contains(event.target)&&!toggle.contains(event.target))close();
 });
 document.body.insertBefore(sidebar,document.body.firstChild);
 document.body.insertBefore(toggle,sidebar.nextSibling);
}
function paletteBars(){
 /* Colore apenas o preenchimento: tamanho e valores seguem controlados pela página. */
 var fills=document.querySelectorAll('.score .fill,.row-score .fill,.track .fill,.bar > .fill,.progress-fill');
 for(var i=0;i<fills.length;i++){
  var f=fills[i];
  var context=f.closest('.score,.row-score,.barrow,.bar,.detail,.card')||f.parentElement;
  if(!context)continue;
  var lower=String(context.textContent||'').toLowerCase();
  var color=ordered[i%ordered.length];
  if(context.matches('[data-low="true"]'))color=palette.orange;
  if(f.classList.contains('auto'))color=palette.violet;
  if(lower.indexOf('detrator')>=0)color=palette.red;
  if(lower.indexOf('promotor')>=0)color=palette.green;
  if(lower.indexOf('neutro')>=0)color=palette.amber;
  if(f.dataset.s360Colored===color)continue;
  f.style.setProperty('--s360-chart-accent',color);
  f.dataset.s360Colored=color;
 }
}
function observeGraphs(){
 paletteBars();
 var pending=false;
 var watcher=new MutationObserver(function(records){
  var should=false;
  for(var i=0;i<records.length;i++){
   if(records[i].addedNodes&&records[i].addedNodes.length){should=true;break}
  }
  if(!should||pending)return;
  pending=true;
  requestAnimationFrame(function(){pending=false;paletteBars()});
 });
 watcher.observe(document.body,{childList:true,subtree:true});
}
function fmt(x){
 return Number(x).toLocaleString('pt-BR',{minimumFractionDigits:0,maximumFractionDigits:2});
}
function legendItem(label,color,value){
 var row=node('div');
 var dot=node('span',null,'s360-v9-dot');dot.style.background=color;dot.setAttribute('aria-hidden','true');
 appendChildren(row,[dot,node('span',label+' · '+fmt(value))]);return row;
}
function infoCard(title,sub){
 var card=node('section',null,'s360-v9-chart-card');
 appendChildren(card,[node('h3',title),node('p',sub,'s360-v9-chart-note')]);
 return card;
}
function donutChart(record){
 var card=infoCard('Composição do NPS · famílias','2026 · '+fmt(record.respondents)+' respostas válidas');
 var counts=[record.promoters,record.passives,record.detractors],n=record.respondents;
 var a=100*counts[0]/n,b=100*(counts[0]+counts[1])/n;
 var donut=node('div',null,'s360-v9-donut');
 donut.style.background='conic-gradient('+palette.green+' 0% '+a+'%, '+palette.amber+' '+a+'% '+b+'%, '+palette.red+' '+b+'% 100%)';
 donut.setAttribute('role','img');
 donut.setAttribute('aria-label','Promotores: '+counts[0]+', neutros: '+counts[1]+', detratores: '+counts[2]);
 donut.appendChild(node('strong',fmt(record.nps)));
 var legend=node('div',null,'s360-v9-chart-legend');
 appendChildren(legend,[legendItem('Promotores',palette.green,counts[0]),legendItem('Neutros',palette.amber,counts[1]),legendItem('Detratores',palette.red,counts[2])]);
 appendChildren(card,[appendChildren(node('div',null,'s360-v9-donut-layout'),[donut,legend]),node('p','NPS = % promotores − % detratores. O centro indica o índice, não a nota média.','s360-v9-chart-foot')]);
 return card;
}
function stageBars(groups){
 var card=infoCard('NPS das famílias por etapa','2026 · uma atribuição exclusiva por família');
 var stages=[['infantil','Infantil',palette.sky],['fundamental1','Fundamental I',palette.cyan],['fundamental2','Fundamental II',palette.blue],['medio','Ensino Médio',palette.violet]];
 stages.forEach(function(item){
  var g=groups.find(function(x){return x.id===item[0]});
  if(!g)return;
  var holder=node('div',null,'s360-v9-hbar-item');
  var caption=node('div',null,'s360-v9-hbar-caption');
  appendChildren(caption,[node('span',item[1]),node('b',(g.nps>0?'+':'')+fmt(g.nps))]);
  var bar=node('div',null,'s360-v9-hbar-track');
  bar.setAttribute('role','img');
  bar.setAttribute('aria-label',item[1]+': NPS '+fmt(g.nps)+'; '+g.respondents+' respostas');
  var fill=node('div',null,'s360-v9-hbar-fill');
  /* Barra está em escala -100..+100: comprimento = (NPS+100)/2, não valor absoluto. */
  fill.style.width=Math.max(0,Math.min(100,(g.nps+100)/2))+'%';fill.style.background=item[2];
  bar.append(fill);appendChildren(holder,[caption,bar]);card.append(holder);
 });
 card.appendChild(node('p','Comprimento em escala NPS de −100 a +100. Os denominadores variam por etapa.','s360-v9-chart-foot'));
 return card;
}
function createSVG(name){
 return document.createElementNS('http://www.w3.org/2000/svg',name);
}
function setAttrs(el,attr){Object.keys(attr).forEach(function(k){el.setAttribute(k,String(attr[k]))});return el}
function lineHistory(segment,stage){
 var card=infoCard('Evolução histórica · famílias','2023–2025 · série histórica disponível');
 var svg=setAttrs(createSVG('svg'),{viewBox:'0 0 366 215',role:'img','aria-label':'Série histórica NPS das famílias de 2023 a 2025 para '+stage});
 svg.classList.add('s360-v9-chart-svg');
 var points=segment.points||[];
 [0,50,100].forEach(function(t){
  var y=185-t*1.5;
  var line=setAttrs(createSVG('line'),{x1:42,y1:y,x2:344,y2:y,stroke:'#dce8f5','stroke-width':1});
  svg.append(line);
  var label=setAttrs(createSVG('text'),{x:34,y:y+4,'text-anchor':'end',fill:'#6c83a0','font-size':11});
  label.textContent=String(t);svg.append(label);
 });
 var coords=points.map(function(p,i){return {x:65+i*126,y:185-Number(p.nps)*1.5,val:p.nps,year:p.year}});
 var curve=setAttrs(createSVG('polyline'),{points:coords.map(function(p){return p.x+','+p.y}).join(' '),fill:'none',stroke:palette.violet,'stroke-width':4,'stroke-linecap':'round','stroke-linejoin':'round'});
 svg.append(curve);
 coords.forEach(function(p){
  svg.append(setAttrs(createSVG('circle'),{cx:p.x,cy:p.y,r:5,fill:palette.violet,stroke:'#fff','stroke-width':2}));
  var value=setAttrs(createSVG('text'),{x:p.x,y:p.y-12,'text-anchor':'middle',fill:'#254f93','font-size':12,'font-weight':800});
  value.textContent=fmt(p.val);svg.append(value);
  var year=setAttrs(createSVG('text'),{x:p.x,y:205,'text-anchor':'middle',fill:'#617a9e','font-size':11});
  year.textContent=p.year;svg.append(year);
 });
 card.appendChild(svg);
 card.appendChild(node('p','Os históricos de famílias não representam ciclos M1/M2/M3. Em Infantil, 2023–2025 incluíam o 1º ano.','s360-v9-chart-foot'));
 return card;
}
async function buildInsights(){
 var container=document.getElementById('s360-v9-insights');
 if(!container)return;
 try{
  var responses=await Promise.all([fetch(aggUrl,{cache:'no-store'}),fetch(historyUrl,{cache:'no-store'})]);
  if(responses.some(function(r){return !r.ok}))throw Error('Arquivos agregados indisponíveis');
  var docs=await Promise.all(responses.map(function(r){return r.json()}));
  var groups=docs[0].groups,history=docs[1].segments;
  function render(){
   var year=document.getElementById('ano'),cycle=document.getElementById('ciclo'),stageSel=document.getElementById('etapa');
   var y=year?String(year.value):'2026';
   var cy=cycle?String(cycle.value):'M1';
   if(y!=='2026'||cy!=='M1'){container.hidden=true;return}
   var stage=stageSel?String(stageSel.value):'institutional';
   var key=(stage==='institutional'?'familias':stage);
   var selected=groups.find(function(g){return g.id===key});
   var hist=history.find(function(h){return h.id===(stage==='institutional'?'total':stage)});
   if(!selected||!hist){container.hidden=true;return}
   container.hidden=false;
   var target=container.querySelector('.s360-v9-charts');
   if(!target)return;
   target.replaceChildren();
   appendChildren(target,[donutChart(selected),stageBars(groups),lineHistory(hist,stage)]);
  }
  document.addEventListener('change',function(event){
   if(event.target&&['ano','ciclo','etapa'].indexOf(event.target.id)!==-1)render();
  });
  render();
 }catch(err){
  container.hidden=true;
  /* Widgets decorativos não devem interromper indicadores existentes. */
 }
}
function init(){
 buildSidebar();observeGraphs();buildInsights();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});
else init();
})();