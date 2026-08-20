#!/usr/bin/env python3
import json, html, shutil, os
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_site"
CONTENT = ROOT / "content"
RES_DIR = CONTENT / "resources"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    return html.escape(str(s), quote=True)


def icon_svg(name):
    icons = {
        "headphones": '<path d="M4 13a8 8 0 0 1 16 0"/><path d="M4 13v5a2 2 0 0 0 2 2h2v-7H4z"/><path d="M20 13v5a2 2 0 0 1-2 2h-2v-7h4z"/>',
        "audio": '<path d="M4 10v4"/><path d="M8 7v10"/><path d="M12 4v16"/><path d="M16 7v10"/><path d="M20 10v4"/>',
        "news": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M7 9h5M7 13h10M7 16h10M15 9h2"/>',
        "community": '<path d="M8 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM16 10a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/><path d="M3 19c0-3 2.2-5 5-5s5 2 5 5M13 14c.8-.7 1.8-1 3-1 2.7 0 5 1.8 5 4.5"/>',
        "puzzle": '<path d="M8 3h5a2 2 0 1 1 4 0h4v6a2 2 0 1 0 0 4v8h-7a2 2 0 1 0-4 0H3v-7a2 2 0 1 0 0-4V3h5z"/>',
        "computer": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
        "book": '<path d="M3 5a9 9 0 0 1 9 2v13a9 9 0 0 0-9-2z"/><path d="M21 5a9 9 0 0 0-9 2v13a9 9 0 0 1 9-2z"/>',
        "graduation": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 3 9 3 12 0v-5"/><path d="M22 9v6"/>',
        "pen": '<path d="M4 20h4L19 9l-4-4L4 16v4z"/><path d="M13.5 6.5l4 4"/>',
        "mic": '<path d="M12 3a4 4 0 0 0-4 4v5a4 4 0 0 0 8 0V7a4 4 0 0 0-4-4z"/><path d="M5 11v1a7 7 0 0 0 14 0v-1"/><path d="M12 19v3M9 22h6"/>',
        "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
    }
    body = icons.get(name, icons["book"])
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{body}</svg>'


def nav(current=""):
    items = [
        ("Home", "index.html", "home"),
        ("English Resources", "english-learning-resources.html", "resources"),
        ("Academic English", "academic-english.html", "academic"),
        ("Dictionaries", "dictionaries.html", "dictionaries"),
        ("Communities", "communities.html", "communities"),
        ("About", "about.html", "about"),
        ("Contact", "contact.html", "contact"),
    ]
    links = ''.join(f'<a href="{href}" class="{"active" if key==current else ""}">{label}</a>' for label, href, key in items)
    return f'''<header class="site-header"><div class="nav-wrap"><a class="brand" href="index.html"><span class="brand-mark">SH</span><span>Samira’s English Hub</span></a><button class="nav-toggle" type="button" aria-expanded="false" aria-label="Open menu">Menu</button><nav class="main-nav" aria-label="Main navigation">{links}</nav></div></header>'''


def page_shell(title, description, body, current="", extra_head="", extra_js=""):
    site = load_json(CONTENT / "site.json")
    full_title = f'{title} | {site["site_title"]}' if title != site["site_title"] else site["site_title"]
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(full_title)}</title><meta name="description" content="{esc(description)}"><meta name="theme-color" content="#c9894b"><link rel="stylesheet" href="assets/styles.css">{extra_head}</head><body><a class="skip-link" href="#main">Skip to content</a>{nav(current)}<main id="main">{body}</main><footer class="site-footer"><div><strong>Samira’s English Hub</strong><p>Practical English for everyday life, work and academic success.</p></div><div class="footer-links"><a href="about.html">About</a><a href="contact.html">Contact</a><a href="admin/">Site editor</a></div><p class="footer-note">External learning resources remain the property of their respective publishers.</p></footer><script src="assets/app.js"></script>{extra_js}</body></html>'''


def skill_icon(skill):
    names = {"listen":"headphones", "speak":"mic", "read":"book", "write":"pen", "academic":"graduation", "practise":"puzzle"}
    return icon_svg(names.get(skill,"book"))


def resource_card(r):
    badges = ''.join(f'<span class="tag">{esc(t)}</span>' for t in r.get("tags", [])[:3])
    skills = ' '.join(r.get('skills', [])); levels = ' '.join(r.get('levels', []))
    search_text = ' '.join([r.get('title',''), r.get('description',''), *r.get('tags',[]), *r.get('skills',[]), *r.get('levels',[])]).lower()
    host = urlparse(r['url']).netloc.replace('www.', '')
    favicon = f"https://www.google.com/s2/favicons?sz=128&domain={host}"
    initials = ''.join(word[0] for word in r['title'].split() if word and word[0].isalnum())[:3].upper()
    return f'''<article class="resource-card" data-skills="{esc(skills)}" data-levels="{esc(levels)}" data-collection="{esc(r.get('collection','english'))}" data-australian="{str(bool(r.get('australian'))).lower()}" data-search="{esc(search_text)}"><div class="resource-brand"><div class="brand-logo-wrap"><img class="brand-logo" src="{esc(favicon)}" alt="{esc(r['title'])} logo" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='grid'"><span class="brand-fallback">{esc(initials)}</span></div><div class="brand-site-name">{esc(r['title'])}</div><div class="brand-domain">{esc(host)}</div></div><div class="resource-body"><div class="resource-content"><div class="tags">{badges}</div><h3>{esc(r['title'])}</h3><p>{esc(r['description'])}</p></div><a class="card-link" href="{esc(r['url'])}" target="_blank" rel="noopener noreferrer" aria-label="Visit {esc(r['title'])}">Visit resource <span aria-hidden="true">→</span></a></div></article>'''


def cards(resources): return '<div class="resource-grid">' + ''.join(resource_card(r) for r in resources) + '</div>'
def load_resources(): return [load_json(p) for p in sorted(RES_DIR.glob("*.json"))]


def hero(site):
    return f'''<section class="hero"><div class="hero-copy"><span class="eyebrow">A learning hub for adult English learners</span><h1>{esc(site['site_title'])}</h1><p class="hero-tagline">{esc(site['tagline'])}</p><p class="hero-intro">{esc(site['hero_intro'])}</p><div class="hero-actions"><a class="btn primary" href="english-learning-resources.html">Start learning</a><a class="btn secondary" href="academic-english.html">Academic English</a></div><div class="welcome-notes"><span>Adult learners</span><span>Learn at your own pace</span><span>Life in Australia</span></div></div><div class="hero-visual"><div class="hero-photo-card"><span class="photo-label">Study • Work • Life</span><div class="photo-art"><div class="art-bubble art-one">{icon_svg('book')}</div><div class="art-bubble art-two">{icon_svg('mic')}</div><div class="art-bubble art-three">{icon_svg('community')}</div></div><p class="photo-copy">A friendly place to find trusted resources without feeling overwhelmed.</p></div></div></section>'''


def home_page(site, resources):
    skill_info=[("listen","Listen","Podcasts, videos and real-world listening practice."),("speak","Speak","Pronunciation, conversation and spoken English."),("read","Read","Stories, news and reading comprehension."),("write","Write","Writing, grammar and sentence-building practice."),("academic","Academic English","Study skills, assignments and academic writing."),("practise","Practise","Interactive worksheets, quizzes and games.")]
    tiles=[]
    for key,label,desc in skill_info:
        href='academic-english.html' if key=='academic' else f'english-learning-resources.html?skill={key}#{key}'
        tiles.append(f'''<a class="skill-tile" href="{href}"><div class="skill-icon">{skill_icon(key)}</div><h3>{label}</h3><p>{desc}</p><span>Explore →</span></a>''')
    featured=[r for r in resources if r.get('featured')][:6]; australian=[r for r in resources if r.get('australian') and r.get('collection')=='english'][:3]
    body=hero(site)+f'''<section class="section"><div class="section-heading"><span class="eyebrow">Start here</span><h2>What would you like to practise today?</h2><p>Choose a skill and go straight to resources that match your goal.</p></div><div class="skill-grid">{''.join(tiles)}</div></section>'''
    if australian: body+=f'''<section class="section soft"><div class="section-heading"><span class="eyebrow">English in context</span><h2>English for life in Australia</h2><p>Build practical English while learning about Australian life, news and communication.</p></div>{cards(australian)}</section>'''
    body+=f'''<section class="section"><div class="section-heading split"><div><span class="eyebrow">Handpicked</span><h2>Featured resources</h2><p>Useful starting points with short summaries so you know what each site offers.</p></div><a class="text-link" href="english-learning-resources.html">View all resources →</a></div>{cards(featured)}</section><section class="section soft try-today"><div><span class="eyebrow">A small step</span><h2>Try something today</h2><p>Listen to one short item, learn five useful words, or complete one interactive activity.</p></div><a class="btn primary" href="english-learning-resources.html?skill=practise#practise">Find an activity</a></section>'''
    return page_shell(site['site_title'],site['tagline'],body,'home')


def filter_bar():
    return f'''<div class="filters"><label class="search-field"><span>Search</span><div class="search-box">{icon_svg('search')}<input id="resourceSearch" type="search" placeholder="Search resources..."></div></label><label><span>Skill</span><select id="skillFilter"><option value="all">All skills</option><option value="listen">Listening</option><option value="speak">Speaking</option><option value="read">Reading</option><option value="write">Writing</option><option value="practise">Interactive practice</option></select></label><label><span>Level</span><select id="levelFilter"><option value="all">All levels</option><option value="beginner">Beginner</option><option value="intermediate">Intermediate</option><option value="advanced">Advanced</option></select></label><label class="check-row"><input id="australianFilter" type="checkbox"><span>Australian English</span></label></div><p class="result-count" id="resultCount"></p>'''


def resources_page(resources):
    rs=[r for r in resources if r.get('collection')=='english']
    anchors='''<div class="anchor-nav"><a href="#listen">Listen</a><a href="#speak">Speak</a><a href="#read">Read</a><a href="#write">Write</a><a href="academic-english.html">Academic English</a><a href="#practise">Practise</a></div>'''
    body='''<section class="page-hero"><span class="eyebrow">Resource library</span><h1>English Learning Resources</h1><p>Each resource includes a quick visual identity and a short description to help you choose.</p></section>'''+anchors+'<section class="section compact">'+filter_bar()+cards(rs)+'</section>'
    return page_shell('English Learning Resources','Handpicked English-learning resources.',body,'resources')


def collection_page(title,intro,resources,kind,current): return page_shell(title,intro,f'''<section class="page-hero"><span class="eyebrow">Curated resources</span><h1>{esc(title)}</h1><p>{esc(intro)}</p></section><section class="section compact">{cards([r for r in resources if r.get('collection')==kind])}</section>''',current)
def about_page(site): return page_shell('About','About Samira’s English Hub.',f'''<section class="page-hero narrow"><span class="eyebrow">About</span><h1>About Samira’s English Hub</h1><p>{esc(site['about_short'])}</p></section><section class="section prose"><h2>Why I created this site</h2><p>{esc(site['about_long'])}</p></section>''','about')
def contact_page(site): return page_shell('Contact','Contact Samira’s English Hub.',f'''<section class="page-hero narrow"><span class="eyebrow">Contact</span><h1>Questions or suggestions?</h1><p>Suggest a useful English-learning resource or get in touch.</p><a class="btn primary" href="{esc(site.get('contact_url','#'))}" target="_blank" rel="noopener">Open contact form</a></section>''','contact')
def write(path,text): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text,encoding='utf-8')
def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(); site=load_json(CONTENT/'site.json'); resources=load_resources()
    write(OUT/'index.html',home_page(site,resources)); write(OUT/'english-learning-resources.html',resources_page(resources)); write(OUT/'academic-english.html',collection_page('Academic English','Build academic writing, study and university communication skills with carefully selected resources.',resources,'academic','academic')); write(OUT/'dictionaries.html',collection_page('Dictionaries & Vocabulary','Use learner-friendly dictionaries and vocabulary tools to understand words, pronunciation and natural usage.',resources,'dictionary','dictionaries')); write(OUT/'communities.html',collection_page('English Learning Communities','Practise English with other learners through discussions, peer interaction and language exchange.',resources,'community','communities')); write(OUT/'about.html',about_page(site)); write(OUT/'contact.html',contact_page(site)); shutil.copytree(ROOT/'assets',OUT/'assets'); shutil.copytree(ROOT/'admin',OUT/'admin'); write(OUT/'.nojekyll',''); print(f'Built {len(resources)} resources')
if __name__=='__main__': build()
