#!/usr/bin/env python3
"""构建脚本：从模板 + 计算器定义生成静态 HTML 页面"""
import json, os, shutil
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
TEMPLATES = ROOT / "templates"
CALCULATORS = ROOT / "calculators"
STATIC = ROOT / "static"

def load_template(name):
    return (TEMPLATES / name).read_text(encoding="utf-8")

def render(template, ctx):
    """简单模板渲染，替换 {{key}}"""
    result = template
    for k, v in ctx.items():
        result = result.replace(f"{{{{{k}}}}}", str(v))
    return result

def build_calculator(calc_dir, lang, base_template):
    """构建单个计算器页面"""
    meta_file = calc_dir / f"{lang}.json"
    if not meta_file.exists():
        return None
    
    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    logic_file = calc_dir / "logic.html"
    logic = logic_file.read_text(encoding="utf-8") if logic_file.exists() else ""
    
    # 结构化数据 (Schema.org)
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": meta["title"],
        "description": meta["description"],
        "url": meta.get("canonical", ""),
        "applicationCategory": "UtilityApplication",
        "operatingSystem": "Any",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }, ensure_ascii=False)
    
    ctx = {
        "title": meta["title"],
        "description": meta["description"],
        "keywords": meta.get("keywords", ""),
        "canonical": meta.get("canonical", ""),
        "lang": lang,
        "h1": meta.get("h1", meta["title"]),
        "intro": meta.get("intro", ""),
        "calculator_body": logic,
        "schema_json": schema,
        "slug": calc_dir.name,
        "faq_html": build_faq(meta.get("faq", [])),
    }
    return render(base_template, ctx)

def build_faq(faq_list):
    if not faq_list:
        return ""
    items = ""
    for item in faq_list:
        items += f'<details><summary>{item["q"]}</summary><p>{item["a"]}</p></details>\n'
    return f'<section class="faq"><h2>FAQ</h2>\n{items}</section>'

def build_index(lang, base_template, calculators_meta):
    """构建首页"""
    cards = ""
    for m in calculators_meta:
        cards += f'<a href="/{lang}/{m["slug"]}/" class="calc-card"><h3>{m["title"]}</h3><p>{m["desc"]}</p></a>\n'
    
    index_meta = {
        "en": {"title": "Free Online Calculators - CalcTools", "description": "Free online calculators for math, finance, health, and everyday use.", "h1": "Free Online Calculators"},
        "zh": {"title": "免费在线计算器 - CalcTools", "description": "免费在线计算器：数学、金融、健康、日常工具。", "h1": "免费在线计算器"},
    }
    m = index_meta.get(lang, index_meta["en"])
    
    ctx = {
        "title": m["title"],
        "description": m["description"],
        "keywords": "online calculator, free calculator, math tools",
        "canonical": f"https://calc.tools/{lang}/",
        "lang": lang,
        "h1": m["h1"],
        "intro": "",
        "calculator_body": f'<div class="calc-grid">{cards}</div>',
        "schema_json": "{}",
        "slug": "index",
        "faq_html": "",
    }
    return render(base_template, ctx)

def main():
    # 清理输出
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    
    # 复制静态资源
    if STATIC.exists():
        shutil.copytree(STATIC, DIST / "static")
    
    base_template = load_template("base.html")
    langs = ["en", "zh"]
    
    # 遍历计算器目录
    calc_dirs = sorted([d for d in CALCULATORS.iterdir() if d.is_dir()])
    
    for lang in langs:
        lang_dir = DIST / lang
        lang_dir.mkdir(parents=True, exist_ok=True)
        
        calculators_meta = []
        
        for calc_dir in calc_dirs:
            meta_file = calc_dir / f"{lang}.json"
            if not meta_file.exists():
                continue
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            
            # 生成页面
            html = build_calculator(calc_dir, lang, base_template)
            if html:
                out_dir = lang_dir / calc_dir.name
                out_dir.mkdir(parents=True, exist_ok=True)
                (out_dir / "index.html").write_text(html, encoding="utf-8")
                calculators_meta.append({"slug": calc_dir.name, "title": meta["title"], "desc": meta["description"][:60]})
        
        # 生成首页
        index_html = build_index(lang, base_template, calculators_meta)
        (lang_dir / "index.html").write_text(index_html, encoding="utf-8")
    
    # 根目录 index.html 重定向到英文
    (DIST / "index.html").write_text('<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0;url=/en/"><link rel="canonical" href="/en/"></head></html>', encoding="utf-8")
    
    # 生成 sitemap
    build_sitemap(calc_dirs, langs)
    
    # 生成 robots.txt
    (DIST / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://calc.tools/sitemap.xml\n", encoding="utf-8")
    
    print(f"✓ Built {sum(1 for _ in DIST.rglob('index.html'))} pages")

def build_sitemap(calc_dirs, langs):
    urls = []
    base = "https://calc.tools"
    for lang in langs:
        urls.append(f"{base}/{lang}/")
        for calc_dir in calc_dirs:
            if (calc_dir / f"{lang}.json").exists():
                urls.append(f"{base}/{lang}/{calc_dir.name}/")
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += f"  <url><loc>{url}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>\n"
    xml += "</urlset>"
    (DIST / "sitemap.xml").write_text(xml, encoding="utf-8")

if __name__ == "__main__":
    main()
