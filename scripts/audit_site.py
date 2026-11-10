#!/usr/bin/env python3
"""Auditoria estática do STAGIO 360. Executar com: python3 scripts/audit_site.py"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json
import math
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []
WARNINGS = []
PAGES = [ROOT / "index.html", ROOT / "painel.html", *sorted((ROOT / "admin").glob("*.html")), ROOT / "fundamental-1" / "index.html"]

class AuditHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []
        self.ids = set()
        self.duplicates = set()
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if d.get("id"):
            if d["id"] in self.ids:
                self.duplicates.add(d["id"])
            self.ids.add(d["id"])
        if tag in ("img", "script", "link", "a", "iframe"):
            ref = d.get("src") or d.get("href")
            if ref:
                self.refs.append((tag, ref))
    handle_startendtag = handle_starttag

def is_local(ref):
    target = urlsplit(ref)
    return not target.scheme and not target.netloc and bool(target.path)

def verify_html(path):
    if not path.exists():
        ERRORS.append(f"Arquivo HTML ausente: {path.relative_to(ROOT)}")
        return
    code = path.read_text(encoding="utf-8")
    parser = AuditHTML()
    parser.feed(code)
    for duplicate in parser.duplicates:
        ERRORS.append(f"{path.relative_to(ROOT)}: id duplicado {duplicate!r}")
    for tag, ref in parser.refs:
        if not is_local(ref):
            continue
        local = unquote(urlsplit(ref).path)
        target = (path.parent / local).resolve()
        try:
            target.relative_to(ROOT)
        except ValueError:
            ERRORS.append(f"{path.relative_to(ROOT)}: referência fora do repositório: {ref}")
            continue
        if target.is_dir():
            target /= "index.html"
        if not target.is_file():
            ERRORS.append(f"{path.relative_to(ROOT)}: referência quebrada: {ref}")
    if re.search(r"sb_secret_|service_role|sk_live_", code, re.I):
        ERRORS.append(f"{path.relative_to(ROOT)}: token/identificador de credencial privilegiada")
    body = re.search(r'<body\b[^>]*>', code, re.I)
    theme_classes = re.findall(r'\bs360-harmonized\b', body.group(0)) if body else []
    if len(theme_classes) != 1:
        ERRORS.append(f"{path.relative_to(ROOT)}: a classe do tema deve aparecer exatamente uma vez no body")
    if not re.search("stagio360-logo-oficial.svg", code):
        ERRORS.append(f"{path.relative_to(ROOT)}: logotipo oficial ausente")

def check_navigation_step3():
    """Mantém o menu principal enxuto e preserva o caminho protegido por etapa."""
    expected = [
        ('#segmentos', 'Avaliação 360'),
        ('./admin/planejamento.html', 'Planejamento docente'),
        ('./admin/funcionarios.html', 'Colaboradores · Privado'),
        ('./admin/integracao.html', 'Painel Administrativo')
    ]
    for rel in ("index.html", "painel.html"):
        html = (ROOT / rel).read_text(encoding="utf-8")
        nav_match = re.search(r'<nav aria-label="Navegação institucional">(.*?)</nav>', html, re.S)
        if not nav_match:
            ERRORS.append(f"{rel}: menu institucional ausente")
            continue
        nav = nav_match.group(1)
        entries = re.findall(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>', nav, re.S)
        actual = [(href, re.sub(r'<[^>]+>', '', label).strip().lstrip('◫◎▥♧').strip()) for href, label in entries]
        if actual != expected:
            ERRORS.append(f"{rel}: barra lateral não possui exatamente os quatro acessos principais")
        if "Gestão restrita" in nav or "Educação Infantil · restrito" in nav or "Acessos complementares" in nav:
            ERRORS.append(f"{rel}: barra lateral contém itens redundantes")
        for token in ('id="historico"', 'id="fontes"', 'id="stage-access-link"', "updateContextualAccess(stage)", "fundamental1:{href:'./admin/segmento.html?etapa=fundamental1'", "infantil:{href:'./admin/segmento.html?etapa=infantil'"):
            if token not in html:
                ERRORS.append(f"{rel}: destino preservado da etapa ou histórico ausente ({token})")

def check_planning_stage_panel_link():
    """O atalho de planejamento acompanha a etapa e não fica preso ao Infantil."""
    page = ROOT / "admin/planejamento.html"
    if not page.is_file():
        ERRORS.append("Planejamento não encontrado para validar o painel contextual")
        return
    html = page.read_text(encoding="utf-8")
    for token in (
        'id="stage-panel-link"',
        'function updateStagePanelLink(stage)',
        "updateStagePanelLink(stage);",
        "infantil:{label:'Painel Infantil',href:'./infantil.html'}",
        "fundamental1:{label:'Painel Fundamental I',href:'./segmento.html?etapa=fundamental1'}",
        "fundamental2:{label:'Painel Fundamental II',href:'./segmento.html?etapa=fundamental2'}",
        "medio:{label:'Painel Ensino Médio',href:'./segmento.html?etapa=medio'}",
        "link.hidden=!target;",
    ):
        if token not in html:
            ERRORS.append("Atalho contextual de planejamento sem requisito: " + token)
    if '<a class="btn alt" href="./infantil.html">Painel Infantil</a>' in html:
        ERRORS.append("Planejamento ainda possui atalho Infantil estático")


def check_stage_access_step4():
    """A entrada protegida deve autenticar por perfil e etapa, sem expor dados individuais no portal."""
    page = ROOT / "admin/segmento.html"
    if not page.exists():
        ERRORS.append("Portal autenticado por segmento ausente")
        return
    code = page.read_text(encoding="utf-8")
    required = (
        "stg_members", "stg_scope_access", "signInWithPassword",
        "fundamental1", "fundamental2", "medio", "infantil",
        "stg_stage_rubric_aggregates", "stg_infantil_indicators",
        "stg_teachers", "stg_pdi_plans",
        "stages[scope]", "Acesso não autorizado para este segmento",
        "./index.html?tab=teachers", "./index.html?tab=search",
        "./pdi.html", "./governanca.html?etapa="
    )
    for token in required:
        if token not in code:
            ERRORS.append(f"Área da coordenação sem requisito: {token}")
    for route in ("fundamental1", "fundamental2", "medio", "infantil"):
        for public in ("index.html", "painel.html"):
            page_text = (ROOT / public).read_text(encoding="utf-8")
            if f"./admin/segmento.html?etapa={route}" not in page_text:
                ERRORS.append(f"{public}: não direciona acesso protegido a {route}")

def check_navigation_step5():
    """As quatro seções devem ser navegáveis sem publicar dados individuais."""
    for rel in ("index.html", "painel.html"):
        html = (ROOT / rel).read_text(encoding="utf-8")
        for token in (
            'aria-label="Seções da Avaliação 360"',
            'id="pesquisas-agregadas"',
            'id="eval-professores"',
            'id="eval-pdis"',
            "admin/segmento.html?etapa=",
            "'&aba='+section",
            "const eligible=['infantil','fundamental1','fundamental2','medio'].includes(stage)",
        ):
            if token not in html:
                ERRORS.append(f"{rel}: navegação da Avaliação 360 incompleta ({token})")
    hub = ROOT / "admin/segmento.html"
    if not hub.exists():
        ERRORS.append("Área de coordenação ausente no passo 5")
        return
    source = hub.read_text(encoding="utf-8")
    for tab in ("visao", "pesquisas", "professores", "pdis"):
        for token in (f'id="tab-{tab}"', f'id="panel-{tab}"', f'id="actions-{tab}"' if tab != "visao" else 'id="indicators"'):
            if token not in source:
                ERRORS.append(f"Hub da coordenação sem navegação {tab}: {token}")
    for token in ("role=\"tablist\"", "aria-selected", "activateTab(", "history.replaceState", "show('app')"):
        if token not in source:
            ERRORS.append(f"Hub sem recurso de navegação acessível: {token}")
    workflow = (ROOT / ".github/workflows/deploy-pages.yml").read_text(encoding="utf-8")
    if "test -s _site/admin/segmento.html" not in workflow:
        ERRORS.append("GitHub Pages não valida a inclusão do hub da coordenação")

def check_permissions_step6():
    """Previne regressoes nas verificacoes de perfil, etapa e revogacao de acesso."""
    fi = (ROOT / "admin/index.html").read_text(encoding="utf-8")
    segment = (ROOT / "admin/segmento.html").read_text(encoding="utf-8")
    migration = ROOT / "supabase/migrations/20261109_stagio360_step6_permissions.sql"
    for token in (
        'id="denied" hidden',
        "'stg_scope_access'",
        ".eq('stage','fundamental1')",
        "if(!permitted){show('denied');return}",
        "role==='admin'||role==='master'",
        "id=\"switch-account\"",
    ):
        if token not in fi:
            ERRORS.append(f"Passo 6: painel FI sem isolamento de perfil ({token})")
    for token in ("stg_members", "stg_scope_access", "stages[scope]", "show('denied')"):
        if token not in segment:
            ERRORS.append(f"Passo 6: portal por etapa sem bloqueio ({token})")
    if not migration.exists():
        ERRORS.append("Passo 6: regras SQL de perfis nao versionadas")
        return
    sql = migration.read_text(encoding="utf-8")
    for token in ("m.active is true", "a.active is true",
                  "m.role in ('admin', 'master')",
                  "stg_pdi_institutional_reviews_reviewer_role_check",
                  "reviewer_role in ('admin', 'master', 'coordenacao')"):
        if token not in sql:
            ERRORS.append(f"Passo 6: migracao sem protecao ({token})")


def check_contextual_step7():
    """Minha área depende de Auth e RLS, e nunca mostra links restritos por texto de nome."""
    path = ROOT / "admin/minha-area.html"
    if not path.exists():
        ERRORS.append("Passo 7: página Minha área ausente")
        return
    code = path.read_text(encoding="utf-8")
    required = (
        'id="dashboard" hidden', 'id="stage-cards"', 'id="institutional-section"',
        "auth.getUser()", "signInWithPassword", "stg_members", "stg_scope_access",
        "member?.active", "Object.hasOwn(ROLE_NAMES,member.role)",
        "const privileged=member.role==='admin'||member.role==='master'",
        "stg_staff_survey_cycles", "if(!staff.error&&(staff.count||0)>0)",
        "./segmento.html?etapa=infantil", "./segmento.html?etapa=fundamental1",
        "./segmento.html?etapa=fundamental2", "./segmento.html?etapa=medio",
        "./planejamento.html#fundamental1",
    )
    for token in required:
        if token not in code:
            ERRORS.append(f"Passo 7: Minha área sem requisito ({token})")
    for rel in ("index.html", "painel.html"):
        public = (ROOT / rel).read_text(encoding="utf-8")
        if 'id="my-area-link"' not in public or 'href="./admin/minha-area.html"' not in public:
            ERRORS.append(f"Passo 7: {rel} sem acesso a Minha área")
    segment = (ROOT / "admin/segmento.html").read_text(encoding="utf-8")
    if 'href="./minha-area.html"' not in segment:
        ERRORS.append("Passo 7: coordenação sem retorno à Minha área")
    for rel in ("admin/pdi.html", "admin/revisao.html", "admin/sintese.html"):
        fi = (ROOT / rel).read_text(encoding="utf-8")
        variable = "members[0].role" if rel != "admin/sintese.html" else "member[0].role"
        if f"!['admin','master','coordenacao'].includes({variable})" not in fi:
            ERRORS.append(f"Passo 7: {rel} não reconhece a direção master")
    workflow = (ROOT / ".github/workflows/deploy-pages.yml").read_text(encoding="utf-8")
    if "test -s _site/admin/minha-area.html" not in workflow:
        ERRORS.append("Passo 7: GitHub Pages não valida a Minha área")


def check_visual_step8():
    """Verifica o mesmo design system nas rotas sem interferir no Auth/RLS."""
    css_path = ROOT / "assets/stagio360-unified.css"
    if not css_path.exists():
        ERRORS.append("Passo 8: folha visual compartilhada ausente")
        return
    css = css_path.read_text(encoding="utf-8")
    for token in ("--s360ui-blue", "--s360ui-cyan", "body.s360-harmonized",
                  ".s360-quick-nav", "prefers-reduced-motion", "@media(max-width:580px)"):
        if token not in css:
            ERRORS.append(f"Passo 8: estilo sem requisito ({token})")
    if any(x in css.lower() for x in ("url(http", "service_role", "api_key", "data:image")):
        ERRORS.append("Passo 8: estilos não devem incluir recursos remotos ou segredos")
    main_pages = ("index.html", "painel.html", "fundamental-1/index.html")
    admin_pages = ("index.html", "sintese.html", "pdi.html", "revisao.html",
                   "segmento.html", "infantil.html", "planejamento.html",
                   "governanca.html", "integracao.html", "funcionarios.html",
                   "minha-area.html", "reset.html", "import.html", "coord-fii-em.html", "pesquisas-2026.html", "academico.html")
    for rel in main_pages + tuple("admin/" + x for x in admin_pages):
        source = (ROOT / rel).read_text(encoding="utf-8")
        href = "../assets/stagio360-unified.css?v=8" if "/" in rel else "./assets/stagio360-unified.css?v=8"
        if f'href="{href}"' not in source:
            ERRORS.append(f"Passo 8: visual não carregado em {rel}")
        if not re.search(r'<body[^>]*class="[^"]*s360-harmonized', source):
            ERRORS.append(f"Passo 8: {rel} não adota o design system")
    for rel in ("infantil.html", "planejamento.html", "governanca.html",
                "integracao.html", "funcionarios.html"):
        source = (ROOT / "admin" / rel).read_text(encoding="utf-8")
        for token in ('class="s360-quick-nav"', 'href="./minha-area.html"',
                      'href="../painel.html"'):
            if token not in source:
                ERRORS.append(f"Passo 8: navegação não padronizada em admin/{rel}")
    for rel in ("index.html", "painel.html", "admin/minha-area.html",
                "admin/sintese.html", "admin/pdi.html", "admin/revisao.html"):
        source = (ROOT / rel).read_text(encoding="utf-8")
        if "stagio360-logo-oficial.svg" not in source:
            ERRORS.append(f"Passo 8: marca aprovada ausente de {rel}")
    for rel in ("admin/sintese.html", "admin/pdi.html", "admin/revisao.html",
                "admin/import.html", "admin/reset.html", "fundamental-1/index.html"):
        source = (ROOT / rel).read_text(encoding="utf-8")
        href = '../admin/minha-area.html' if rel.startswith("fundamental-1/") else './minha-area.html'
        if f'href="{href}"' not in source:
            ERRORS.append(f"Passo 8: {rel} sem acesso lateral à Minha área")


def check_coord_fiiem_granular():
    """O detalhe confidencial deve ser por sessão master/admin e nunca integrar o portal público."""
    path = ROOT / "admin/coord-fii-em.html"
    if not path.is_file():
        ERRORS.append("Rubrica detalhada FII/EM não publicada")
        return
    code = path.read_text(encoding="utf-8")
    for token in ("stg_members", "'admin','master'", "stg_360_coord_fiiem_items",
                  "source_teacher_id", "response_text", "declared_stage",
                  "renderRows()", 'id="signin"', 'id="denied"',
                  "stagio360-logo-oficial.svg"):
        if token not in code:
            ERRORS.append(f"Rubrica confidencial FII/EM sem requisito: {token}")
    if "service_role" in code or "sb_secret_" in code:
        ERRORS.append("Rubrica FII/EM com credencial privilegiada")
    for rel in ("admin/minha-area.html", "admin/integracao.html"):
        if "./coord-fii-em.html" not in (ROOT / rel).read_text(encoding="utf-8"):
            ERRORS.append(f"Link da rubrica FII/EM ausente em {rel}")


def check_2026_survey_reconciliation():
    """Os NPS agregados publicos devem refletir os formularios brutos: NPS ausente != 0."""
    import json
    data = json.loads((ROOT / "assets/stagio360-2026-agregados.json").read_text(encoding="utf-8"))
    by = {g["id"]:g for g in data["groups"]}
    expected = {
       "fii6a8":(96,41,35,20,21.88),
       "medio_alunos":(36,13,16,7,16.67),
       "alunos":(172,60,77,35,14.53),
       "institucional":(408,219,136,53,40.69),
    }
    for key,(n,p,pa,d,nps) in expected.items():
        rec=by.get(key,{})
        if any(rec.get(col)!=value for col,value in
           (("respondents",n),("promoters",p),("passives",pa),
            ("detractors",d),("nps",nps))):
            ERRORS.append("NPS 2026 sem a conciliacao dos formularios brutos: "+key)
    page=ROOT / "admin/pesquisas-2026.html"
    if not page.exists():
        ERRORS.append("Consulta protegida de pesquisas 2026 ausente")
        return
    html=page.read_text(encoding="utf-8")
    for token in ("stg_360_survey_forms","stg_360_survey_teacher_blocks","stg_members","['admin','master']",
                  "nps_value","declared_segments","rating_categorical","teacher_source_label",
                  "textContent", 'id="dashboard"','id="signin"','id="denied"',
                  'href="./minha-area.html"'):
        if token not in html: ERRORS.append("Pesquisa 2026 sem recurso de seguranca: "+token)
    for file in ("admin/minha-area.html","admin/integracao.html"):
        if "./pesquisas-2026.html" not in (ROOT / file).read_text(encoding="utf-8"):
            ERRORS.append("Atalho da pesquisa 2026 ausente em "+file)
    for rel in ("supabase/migrations/20261109_stagio360_survey_forms_2026_secure.sql",
                "supabase/migrations/20261109_stagio360_survey_teacher_source_blocks.sql"):
        if not (ROOT / rel).is_file():
            ERRORS.append("Migracao protegida das pesquisas 2026 ausente: "+rel)
    public = json.loads((ROOT / "assets/stagio360-nps-publico-2023-2026.json").read_text(encoding="utf-8"))
    values = {(r["year"],r["stage"],r["audience"],r["population"]):(r["n"],r["nps"]) for r in public["rows"]}
    required = {
       (2026,"fundamental2","alunos","fii_6a8"):(96,21.88),
       (2026,"medio","alunos","medio_alunos"):(36,16.67),
       (2026,"institutional","alunos","alunos_escola"):(172,14.53),
       (2026,"institutional","misto","escola_familias_e_alunos"):(408,40.69)
    }
    for k,v in required.items():
        if values.get(k)!=v:ERRORS.append("JSON publico NPS desatualizado: "+str(k))
    print("NPS 2026: denominadores corrigidos e painel privado vinculado")


def check_academic_history_and_family_partition():
    """Audita o isolamento das series historicas e duas leituras de familia (exclusiva/inclusiva)."""
    academic=ROOT/"admin/academico.html"
    if not academic.exists():
        ERRORS.append("Acervo academico protegido ausente")
        return
    source=academic.read_text(encoding="utf-8")
    for token in ("stg_360_academic_results","stg_members","['admin','master']",
                  "reference_mean","grade_label","academic_area",
                  "stagio360-logo-oficial.svg",'id="dashboard"',
                  'id="signin"','id="denied"'):
        if token not in source:ERRORS.append("Acervo academico sem requisito: "+token)
    for path in ("admin/minha-area.html","admin/integracao.html"):
        if "./academico.html" not in (ROOT/path).read_text(encoding="utf-8"):
            ERRORS.append("Link do acervo academico ausente em "+path)
    for rel in ("supabase/migrations/20261109_stagio360_academic_history_secure.sql",
                "supabase/migrations/20261109_stagio360_family_stage_coverage_invoker.sql"):
        if not (ROOT/rel).exists():ERRORS.append("Migracao de governanca ausente: "+rel)
    survey=(ROOT/"admin/pesquisas-2026.html").read_text(encoding="utf-8")
    for token in ("stg_360_family_stage_coverage","nps_exclusive_value","nps_inclusive_value",
                  "family-stage-coverage"):
        if token not in survey:ERRORS.append("Painel de familias sem comparativo seguro: "+token)


def check_shared_dashboard():
    """O acesso comum deve ser só de agregados e não depender de identidade docente."""
    path = ROOT / "painel.html"
    datafile = ROOT / "assets/stagio360-nps-publico-2023-2026.json"
    workflow = (ROOT / ".github/workflows/deploy-pages.yml").read_text(encoding="utf-8")
    if "cp painel.html _site/painel.html" not in workflow:
        ERRORS.append("Fluxo de publicação não inclui painel.html no pacote do GitHub Pages")
    if not path.exists() or not datafile.exists():
        ERRORS.append("Painel geral compartilhável ou dataset agregado ausente")
        return
    html = path.read_text(encoding="utf-8")
    data = json.loads(datafile.read_text(encoding="utf-8"))
    for token in ("Indicadores gerais da escola", "assets/stagio360-nps-publico-2023-2026.json", 'id="etapa"', 'id="ano"', 'id="ciclo"', 'class="shell"', 'class="sidebar-brand"', 'class="hero"', 'class="hero-logo"', 'class="year-control"'):
        if token not in html: ERRORS.append(f"Painel geral sem requisito: {token}")
    for risky in ("service_role", "stg_teacher_scores", "stg_students", "stg_families", "stg_staff_survey_comments", "signInWithPassword"):
        if risky in html: ERRORS.append(f"Painel geral com dado privado/integração proibida: {risky}")
    rows = data.get("rows", [])
    if len(rows) != 25: ERRORS.append("O dataset público não possui 25 registros agregados de NPS auditados")
    for item in rows:
        if set(item) != {"year","stage","audience","population","n","nps","comparable"}:
            ERRORS.append("Dataset público contém chaves não homologadas para divulgação")
            break

def check_integration_routes():
    """Preflight: authenticated modules must ship together with config and integrations."""
    routes = {
        "admin/integracao.html": (
            "stg_360_integrate_autoeval",
            "stg_360_teacher_registry_pending",
            "stg_360_autoeval_reconciliation",
            "stg_360_teacher_profile",
            "stg_360_operational_readiness",
            "stg_360_audience_coverage",
            "stg_360_fi_class_context",
            "stg_360_fi_grade_context",
        ),
        "admin/planejamento.html": (
            "stg_planning_entries",
            "stg_360_planning_crosswalk",
        ),
        "admin/infantil.html": (
            "stg_planning_entries",
        ),
    }
    for rel, required in routes.items():
        path = ROOT / rel
        if not path.exists():
            ERRORS.append(f"Rota essencial de integração ausente: {rel}")
            continue
        code = path.read_text(encoding="utf-8")
        for token in required:
            if token not in code:
                ERRORS.append(f"{rel}: integração obrigatória ausente ({token})")
        if '<script src="./config.js">' not in code:
            ERRORS.append(f"{rel}: cliente Supabase sem configuração autenticada")
    config = ROOT / "admin/config.js"
    if not config.exists():
        ERRORS.append("Configuração pública do cliente Supabase ausente")
    else:
        code = config.read_text(encoding="utf-8")
        if "publishableKey" not in code or "STAGIO_AUTH" not in code:
            ERRORS.append("Configuração pública do Supabase inválida")
        if re.search(r"sb_secret_|service_role|sk_live_", code, re.I):
            ERRORS.append("Credencial privilegiada em configuração pública")

def check_nps(path):
    doc = json.loads(path.read_text(encoding="utf-8"))
    groups = []
    for seg in doc.get("segments", []):
        groups.extend(seg["points"])
    groups.extend(doc.get("groups", []))
    assert groups, f"Sem pontos: {path}"
    for item in groups:
        n = item["respondents"]
        if n <= 0 or sum(item[k] for k in ("promoters","passives","detractors")) != n:
            ERRORS.append(f"{path.name}: contagem de classes inválida em {item}")
            continue
        calc = (item["promoters"]-item["detractors"])*100/n
        if abs(item["nps"]-calc)>0.06:
            ERRORS.append(f"{path.name}: NPS inconsistente ({calc:.2f} versus {item['nps']})")
    print(f"{path.relative_to(ROOT)}: {len(groups)} recortes NPS reconciliados")

def check_2026_reconciliation(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    groups = {g["id"]: g for g in data["groups"]}
    expected = {
        "institucional": ["familias", "alunos"],
        "familias": ["infantil", "fundamental1", "fundamental2", "medio"],
        "alunos": ["fii6a8", "nono", "medio_alunos"],
    }
    for parent, children in expected.items():
        for key in ("respondents", "promoters", "passives", "detractors"):
            observed = sum(groups[child][key] for child in children)
            if observed != groups[parent][key]:
                ERRORS.append(f"{path.name}: {parent}.{key}: {observed} nas etapas, {groups[parent][key]} no total")
    if data.get("year") != 2026:
        ERRORS.append("Base 2026 com ano incorreto")
    if groups["medio"]["respondents"] < 30:
        WARNINGS.append("Ensino Médio: NPS de famílias com amostra pequena (n<30); manter ressalva")
    print("Reconciliação institucional 2026: famílias + alunos, etapas e classes verificadas")

for page in PAGES:
    verify_html(page)
for path in (ROOT/"assets/stagio360-historico.json", ROOT/"assets/stagio360-2026-agregados.json"):
    check_nps(path)
check_2026_reconciliation(ROOT/"assets/stagio360-2026-agregados.json")
check_integration_routes()
check_shared_dashboard()
check_navigation_step3()
check_planning_stage_panel_link()
check_stage_access_step4()
check_navigation_step5()
check_permissions_step6()
check_contextual_step7()
check_visual_step8()
check_coord_fiiem_granular()
check_2026_survey_reconciliation()
check_academic_history_and_family_partition()

if not (ROOT/"assets/stagio360-logo-oficial.svg").exists():
    ERRORS.append("Logotipo oficial ausente")
print(f"Auditoria: {len(PAGES)} páginas; {len(ERRORS)} erros; {len(WARNINGS)} avisos")
for issue in WARNINGS:
    print("AVISO:",issue)
for issue in ERRORS:
    print("ERRO:",issue)
sys.exit(1 if ERRORS else 0)
