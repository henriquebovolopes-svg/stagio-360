#!/usr/bin/env python3
"""Auditoria de design Stagio 360 v11 — 4 KPIs pastéis, demais painéis brancos."""
from pathlib import Path
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
PAGES=(
 "index.html","painel.html","fundamental-1/index.html",
 "admin/index.html","admin/minha-area.html","admin/segmento.html",
 "admin/infantil.html","admin/planejamento.html","admin/governanca.html",
 "admin/integracao.html","admin/coord-fii-em.html",
 "admin/pesquisas-2026.html","admin/academico.html",
 "admin/funcionarios.html","admin/sintese.html",
 "admin/pdi.html","admin/revisao.html","admin/import.html","admin/reset.html"
)
errors=[]
warnings=[]
for route in PAGES:
    fp=ROOT/route
    if not fp.is_file():
        errors.append(f"{route}: arquivo HTML ausente")
        continue
    html=fp.read_text("utf-8")
    body=re.search(r"<body\b[^>]*>",html,re.I)
    if not body or not re.search(r"\bs360-v9\b",body.group(0)):
        errors.append(f"{route}: body sem versão visual oficial v9")
    prefix="../assets/" if "/" in route else "./assets/"
    css=f'<link rel="stylesheet" href="{prefix}stagio360-visual-v9.css?v=9">'
    pastel=f'<link rel="stylesheet" href="{prefix}stagio360-pastel-v10.css?v=10">'
    white=f'<link rel="stylesheet" href="{prefix}stagio360-white-panels-v11.css?v=11">' 
    js=f'<script defer src="{prefix}stagio360-visual-v10.js?v=10"></script>'
    if html.count(css)!=1:errors.append(f"{route}: CSS v9 ausente ou duplicado")
    if html.count(pastel)!=1:errors.append(f"{route}: preenchimento pastel v10 ausente ou duplicado")
    if html.count(white)!=1:errors.append(f"{route}: refinamento branco v11 ausente ou duplicado")
    if html.count(js)!=1:errors.append(f"{route}: visual JavaScript v10 ausente ou duplicado")
    if css in html and pastel in html and html.index(css)>html.index(pastel):
        errors.append(f"{route}: a camada pastel deve ser carregada depois do design system")
    if pastel in html and white in html and html.index(pastel)>html.index(white):
        errors.append(f"{route}: a camada de painéis brancos v11 deve vir após o CSS pastel")
    if white in html and js in html and html.index(white)>html.index(js):
        errors.append(f"{route}: o script visual deve vir após os CSS de acabamento")
    if pastel in html and js in html and html.index(pastel)>html.index(js):
        errors.append(f"{route}: JavaScript visual não deve preceder o CSS pastel")
    if html.index(css)>html.index("</head>") if css in html else False:
        errors.append(f"{route}: CSS carregado após o head")
    if "stagio360-unified.css?v=8" not in html:
        errors.append(f"{route}: camada estável v8 não preservada")
    if "stagio360-logo-oficial.svg" not in html:
        errors.append(f"{route}: logotipo aprovado ausente")
    has_native_shell=('class="shell"' in html or 'class="s360-shell"' in html)
    chrome=bool(body and "s360-chrome" in body.group(0))
    if has_native_shell==chrome:
        errors.append(f"{route}: sidebar duplicada ou ausente")
    if route in ("index.html","painel.html"):
        if html.count('id="s360-v9-insights"')!=1:
            errors.append(f"{route}: os três gráficos oficiais não foram conectados")
        if 'class="s360-v9-charts"' not in html:
            errors.append(f"{route}: grid de gráficos ausente")
        for token in ('id="ano"','id="ciclo"','id="etapa"','id="nps-institucional"','id="nps-institucional-sub"','institutional.nps'):
            if token not in html:errors.append(f"{route}: indicador misto ou seletor {token} ausente")
        nav=re.search(r'<nav aria-label="Navegação institucional">([\s\S]*?)</nav>',html)
        if not nav:errors.append(f"{route}: menu lateral ausente")
        else:
            if 'Governança</a>' in nav.group(1):errors.append(f"{route}: Governança duplicada no menu")
            if nav.group(1).count('Avaliação 360</a>')!=1:errors.append(f"{route}: Avaliação 360 não é o único acesso")
            if 'Colaboradores · Privado</a>' not in nav.group(1):errors.append(f"{route}: colaboradores não renomeados")
        if 'NPS das famílias · Fundamental I</small>' in html:errors.append(f"{route}: quarto KPI não foi generalizado")
    # Segurança: não mudar autenticação ou nomes das tabelas nesta etapa visual
    if route.startswith("admin/") and route not in ("admin/reset.html",):
        if "<script" not in html:
            errors.append(f"{route}: módulo perdeu scripts de sessão")

css=(ROOT/"assets/stagio360-visual-v9.css").read_text("utf-8")
js=(ROOT/"assets/stagio360-visual-v10.js").read_text("utf-8")
pastel_css=(ROOT/"assets/stagio360-pastel-v10.css").read_text("utf-8")
white_css=(ROOT/"assets/stagio360-white-panels-v11.css").read_text("utf-8")
for name,color in (
 ("deep","#081e43"),("blue","#2f73d9"),("cyan","#35c4e8"),
 ("violet","#7c5cfa"),("green","#27ae60"),("amber","#e1a32f"),
 ("red","#dc5959"),
):
    if color not in css or (name!="deep" and color not in js):
        errors.append("Cor oficial v9 ausente da stylesheet/script: "+name)
for token in (
 ".s360-global-sidebar",".s360-menu-toggle",".s360-v9-charts",
 ".s360-v9-donut",".s360-v9-hbar-fill",".s360-v9-chart-svg",
 "#signin","#denied","prefers-reduced-motion","focus-visible",
 "@media(max-width:900px)","@media(max-width:500px)"
):
    if token not in css:errors.append("Componente visual não estilizado: "+token)
for token in (
 "buildSidebar()","paletteBars()","buildInsights()",
 "conic-gradient(","createElementNS(","stageBars(groups)","lineHistory(",
 "'2026'","'M1'","getRoot()"
):
    if token not in js:errors.append("Implementação gráfica ou adaptativa ausente: "+token)
for token in ("#avaliacao > .card.kpi:nth-child(1)","#avaliacao > .card.kpi:nth-child(4)","--s360-pastel-blue","--s360-pastel-green","--s360-pastel-lavender","--s360-pastel-peach",".year-control","color:#fff","background:var(--s360-v10-card-bg) !important","button[type=\"submit\"]"):
    if token not in pastel_css:errors.append("Pastel v10 sem componente cromático: "+token)
for token in ('#avaliacao > .card.kpi:nth-child(1)', '#avaliacao > .card.kpi:nth-child(2)', '#avaliacao > .card.kpi:nth-child(3)', '#avaliacao > .card.kpi:nth-child(4)', '.eval-path', '.stage-access', '.s360-v9-charts > .s360-v9-chart-card:nth-child(n)', '#pesquisas-agregadas,#historico,#fontes', 'background:#fff !important', 'background-color:#fff !important'):
    if token not in white_css:errors.append("Refinamento v11 incompleto: "+token)
if "label:'Governança'" in js or "label:'Colaboradores · Privado'" not in js:
    errors.append("Sidebar global não reflete Avaliação 360 / Colaboradores")
if "label:'Avaliação 360'" not in js:errors.append("Avaliação 360 ausente da sidebar global")
if any(t in js.lower() for t in ("service_role","sb_secret_","auth.signin","createclient(","supabase.auth")):
    errors.append("O script visual deve ficar completamente alheio a Auth/Supabase")
# Evita conclusões visuais com dados inventados
data=json.loads((ROOT/"assets/stagio360-2026-agregados.json").read_text("utf-8"))
groups={g["id"]:g for g in data["groups"]}
for key in ("familias","infantil","fundamental1","fundamental2","medio"):
    g=groups[key]
    if g["respondents"]!=g["promoters"]+g["passives"]+g["detractors"]:
        errors.append(f"NPS {key}: grupos não reconciliados")
    if abs(round(100*(g["promoters"]-g["detractors"])/g["respondents"],2)-g["nps"])>.02:
        errors.append(f"NPS {key}: índice incompatível com a composição")
historical=json.loads((ROOT/"assets/stagio360-historico.json").read_text("utf-8"))
historical_ids={x["id"] for x in historical["segments"]}
if not {"total","infantil","fundamental1","fundamental2","medio"}.issubset(historical_ids):
    errors.append("Gráfico de histórico sem segmentos disponíveis")
print(f"Auditoria visual v11: {len(PAGES)} páginas, {len(errors)} erros, {len(warnings)} avisos.")
for e in errors:print("ERRO:",e)
for w in warnings:print("AVISO:",w)
sys.exit(1 if errors else 0)
