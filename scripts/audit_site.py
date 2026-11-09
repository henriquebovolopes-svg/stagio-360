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
PAGES = [ROOT / "index.html", *sorted((ROOT / "admin").glob("*.html")), ROOT / "fundamental-1" / "index.html"]

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
    if not re.search("stagio360-logo-oficial.svg", code):
        WARNINGS.append(f"{path.relative_to(ROOT)}: não usa o logotipo oficial")

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

if not (ROOT/"assets/stagio360-logo-oficial.svg").exists():
    ERRORS.append("Logotipo oficial ausente")
print(f"Auditoria: {len(PAGES)} páginas; {len(ERRORS)} erros; {len(WARNINGS)} avisos")
for issue in WARNINGS:
    print("AVISO:",issue)
for issue in ERRORS:
    print("ERRO:",issue)
sys.exit(1 if ERRORS else 0)
