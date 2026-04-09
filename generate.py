#!/usr/bin/env python3
"""Generate index.html for Windows Icon Archive from cached file lists."""
import re
from urllib.parse import quote
import html as htmlmod
from collections import OrderedDict

# === CDN BASE URLS (jsDelivr) ===
def cdn(user, repo, branch, path):
    return f"https://cdn.jsdelivr.net/gh/{user}/{repo}@{branch}/{quote(path)}"

REPOS = {
    "trapd00r": {
        "name": "trapd00r/win95-winxp_icons",
        "url": "https://github.com/trapd00r/win95-winxp_icons",
        "cdn": lambda p: cdn("trapd00r", "win95-winxp_icons", "master", f"icons/{p}"),
    },
    "react95": {
        "name": "React95/React95",
        "url": "https://github.com/React95/React95",
        "cdn": lambda p: cdn("React95", "React95", "master", f"packages/icons/png/{p}"),
    },
    "eggy115": {
        "name": "Eggy115/Icons",
        "url": "https://github.com/Eggy115/Icons",
        "cdn": lambda p: cdn("Eggy115", "Icons", "main", p),
    },
    "alexh": {
        "name": "alexh/vintage-icons",
        "url": "https://github.com/alexh/vintage-icons",
        "cdn": lambda p: cdn("alexh", "vintage-icons", "main", p),
    },
    "bartekl1": {
        "name": "bartekl1/WindowsResources",
        "url": "https://github.com/bartekl1/WindowsResources",
        "cdn": lambda p: cdn("bartekl1", "WindowsResources", "main", p),
    },
    "visnalize": {
        "name": "visnalize/resources",
        "url": "https://github.com/Visnalize/win7-icons",
        "cdn": lambda p: cdn("visnalize", "resources", "main", p),
    },
    "xpicons": {
        "name": "softwarehistorysociety/XPIcons",
        "url": "https://github.com/softwarehistorysociety/XPIcons",
        "cdn": lambda p: cdn("softwarehistorysociety", "XPIcons", "main", p),
    },
    "gsnoopy": {
        "name": "gsnoopy/react-old-icons",
        "url": "https://github.com/gsnoopy/react-old-icons",
        "cdn": lambda p: cdn("gsnoopy", "react-old-icons", "main", f"PNG/{p}"),
    },
    "idsoftware": {
        "name": "id-Software (GPL sources)",
        "url": "https://github.com/id-Software",
        "cdn": lambda p: cdn("id-Software", p.split("/")[0], "master", "/".join(p.split("/")[1:])),
    },
    "nblood": {
        "name": "NBlood/NBlood",
        "url": "https://github.com/NBlood/NBlood",
        "cdn": lambda p: cdn("NBlood", "NBlood", "master", p),
    },
    "crispydoom": {
        "name": "fabiangreffrath/crispy-doom",
        "url": "https://github.com/fabiangreffrath/crispy-doom",
        "cdn": lambda p: cdn("fabiangreffrath", "crispy-doom", "master", p),
    },
}

# === VERSION DEFINITIONS ===
VERSIONS = OrderedDict([
    ("win95",    {"name": "Windows 95",     "year": "1995", "color": "#008080"}),
    ("win98",    {"name": "Windows 98",     "year": "1998", "color": "#000080"}),
    ("win2k",    {"name": "Windows 2000",   "year": "2000", "color": "#3a6ea5"}),
    ("winxp",    {"name": "Windows XP",     "year": "2001", "color": "#003399"}),
    ("winvista", {"name": "Windows Vista",  "year": "2007", "color": "#2b5797"}),
    ("win7",     {"name": "Windows 7",      "year": "2009", "color": "#1b78d0"}),
    ("win8",     {"name": "Windows 8.1",    "year": "2012", "color": "#00a4ef"}),
    ("win10",    {"name": "Windows 10",     "year": "2015", "color": "#0078d7"}),
    ("win11",    {"name": "Windows 11",     "year": "2021", "color": "#005fb8"}),
    # ("games",    {"name": "Classic Games",  "year": "1993-2007", "color": "#b71c1c"}),  # TODO: curate and re-add
])

# version_id -> { section_name -> [(repo_key, url, label, fname, size_px)] }
data = {vid: {} for vid in VERSIONS}

def add(vid, section, repo_key, url, label, fname, size_px=None):
    if section not in data[vid]:
        data[vid][section] = []
    data[vid][section].append((repo_key, url, label, fname, size_px))

def make_label(fname):
    """Preserve original filename as label — just strip extension."""
    for ext in [".ico", ".png", ".svg", ".icl", ".ani", ".webp"]:
        if fname.endswith(ext):
            return fname[:-len(ext)]
    return fname

# ============================================================
# REACT95 Win95 icons (all sizes, organized by DLL)
# ============================================================
# Build PNG index: lowercase_stripped -> [(priority, filename, size_str, size_px)]
r95_index = {}
with open("/tmp/react95_icons.txt") as f:
    for line in f:
        png = line.strip().replace("packages/icons/png/", "")
        m = re.match(r'^(.+?)_(\d+)x(\d+)_(\d+)\.png$', png)
        if not m: continue
        base = m.group(1)
        w, h = int(m.group(2)), int(m.group(3))
        depth = m.group(4)
        key = base.lower()
        if key not in r95_index:
            r95_index[key] = []
        r95_index[key].append((png, f"{w}x{h}", w, depth))

# DLL display names for React95 ICO sources
DLL_NAMES = {
    "shell32": "shell32.dll", "progman": "progman.exe", "mmsys": "mmsys.cpl",
    "explorer": "explorer.exe", "user": "user.exe", "main": "main.cpl",
    "comdlg32": "comdlg32.dll", "comctl32": "comctl32.dll", "regedit": "regedit.exe",
    "mplayer": "mplayer.exe", "mplayer_1": "mplayer.exe",
    "notepad": "notepad.exe", "winfile": "winfile.exe",
    "sndvol32": "sndvol32.exe", "sndrec32": "sndrec32.exe",
    "sol": "sol.exe", "freecell": "freecell.exe", "mshearts": "mshearts.exe",
    "winmine": "winmine.exe", "cdplayer": "cdplayer.exe",
    "inetcpl": "inetcpl.cpl", "mshtml": "mshtml.dll", "shdocvw": "shdocvw.dll",
    "syncui": "syncui.dll", "systray": "systray.exe", "access": "access.cpl",
    "gcdef": "gcdef.dll", "mailnews": "mailnews.dll", "wmsui32": "wmsui32.dll",
    "rsrcmtr": "rsrcmtr.exe", "wab32": "wab32.dll", "quartz": "quartz.dll",
    "defrag": "defrag.exe", "drvspace": "drvspace.exe", "rnaapp": "rnaapp.exe",
    "rnaui": "rnaui.dll", "rasapi32": "rasapi32.dll", "directcc": "directcc.exe",
    "confcp": "confcp.cpl", "lights": "lights.exe", "msrating": "msrating.dll",
    "pbrush": "pbrush.exe", "charmap": "charmap.exe", "calc": "calc.exe",
    "appwiz": "appwiz.cpl", "desk": "desk.cpl", "timedate": "timedate.cpl",
    "joy": "joy.cpl", "powercfg": "powercfg.cpl", "intl": "intl.cpl",
    "password": "password.cpl", "awfxex32": "awfxex32.exe", "awfxcg32": "awfxcg32.dll",
    "awfext32": "awfext32.dll", "awschd32": "awschd32.exe", "awsnto32": "awsnto32.exe",
}

with open("/tmp/react95_ico_src.txt") as f:
    for line in f:
        path = line.strip()
        ico_fname = path.split("/")[-1]
        base = ico_fname.replace(".ico", "")

        # Determine DLL source
        m = re.match(r'^(.+?)(?:_(\d+))?$', base)
        if not m: continue
        dll_raw = m.group(1)
        dll_name = DLL_NAMES.get(dll_raw, dll_raw)

        # Build PNG lookup key
        png_base = base[0].upper() + base[1:]
        png_base = re.sub(r'_(\d+)$', r'\1', png_base)
        png_base = png_base.replace("_", "")
        key = png_base.lower()

        if key not in r95_index:
            continue

        # Add ALL size variants
        for png_fname, size_str, size_px, depth in r95_index[key]:
            url = REPOS["react95"]["cdn"](png_fname)
            add("win95", dll_name, "react95", url, png_fname, png_fname, size_px)

# ============================================================
# EGGY115 moricons + pifmgr (Win95)
# ============================================================
with open("/tmp/eggy115_win95.txt") as f:
    for line in f:
        path = line.strip()
        if not path: continue
        parts = path.split("/")
        dll_name = parts[0] + ".dll"
        fname = parts[-1]
        url = REPOS["eggy115"]["cdn"](path)
        add("win95", dll_name, "eggy115", url, fname, fname)

# ============================================================
# TRAPD00R Win98/2K
# ============================================================
with open("/tmp/winicons_clean.txt") as f:
    for line in f:
        fname = line.strip()
        if not fname: continue
        for pfx, vid in [("w98", "win98"), ("w2k", "win2k")]:
            if fname.startswith(pfx):
                url = REPOS["trapd00r"]["cdn"](fname)
                add(vid, "System Icons", "trapd00r", url, fname, fname)
                break

# ============================================================
# ALEXH/vintage-icons (Win98 PNGs)
# ============================================================
with open("/tmp/alexh_all.txt") as f:
    for line in f:
        path = line.strip()
        if not path: continue
        fname = path.split("/")[-1]
        url = REPOS["alexh"]["cdn"](path)
        add("win98", "System Icons (PNG)", "alexh", url, fname, fname)

# ============================================================
# BARTEKL1 (XP→11 by DLL)
# ============================================================
BARTEKL1_MAP = {
    "Windows XP": "winxp", "Windows Vista": "winvista", "Windows 7": "win7",
    "Windows 8.1": "win8", "Windows 10": "win10", "Windows 11": "win11",
}
with open("/tmp/bartekl1_all.txt") as f:
    for line in f:
        path = line.strip()
        if not path: continue
        parts = path.split("/")
        if len(parts) < 5: continue
        vid = BARTEKL1_MAP.get(parts[1])
        if not vid: continue
        dll = parts[3]
        fname = parts[-1]
        url = REPOS["bartekl1"]["cdn"](path)
        add(vid, dll, "bartekl1", url, fname, fname)

# ============================================================
# XPICONS (XP + Longhorn + Whistler)
# ============================================================
with open("/tmp/xpicons_all.txt") as f:
    for line in f:
        path = line.strip()
        if not path: continue
        parts = path.split("/")
        category = parts[0]  # "XP", "Longhorn Icons", "Whistler", "Service Pack 2 Beta"
        fname = parts[-1]
        url = REPOS["xpicons"]["cdn"](path)
        add("winxp", category, "xpicons", url, fname, fname)

# ============================================================
# VISNALIZE (Win7 by source)
# ============================================================
with open("/tmp/visnalize_all.txt") as f:
    for line in f:
        path = line.strip()
        if not path: continue
        parts = path.split("/")
        if len(parts) < 4: continue
        source = parts[2]
        fname = parts[-1]
        url = REPOS["visnalize"]["cdn"](path)
        add("win7", source, "visnalize", url, fname, fname)

# ============================================================
# CLASSIC GAMES - disabled until curated
# TODO: deduplicate, organize by game title, verify original sizes
# ============================================================

# ============================================================
# SORT & COUNT
# ============================================================
def sort_key(item):
    _, _, label, _, _ = item
    clean = make_label(label)
    if re.match(r'^(ICON\s*)?\d+', clean):
        nums = re.findall(r'\d+', clean)
        return (1, int(nums[0]) if nums else 0, clean.lower())
    return (0, 0, clean.lower())

def dll_sort_key(name):
    priority = {
        "shell32.dll": 0, "shell32.dll.mun": 0,
        "imageres.dll": 1, "imageres.dll.mun": 1,
        "progman.exe": 2, "moricons.dll": 3, "pifmgr.dll": 4,
        "System Icons": 5, "System Icons (PNG)": 6,
        "XP": 7, "Longhorn Icons": 8, "Whistler": 9, "Service Pack 2 Beta": 10,
        "Classic Software & Games": 0,
    }
    return (priority.get(name, 50), name.lower())

total = 0
repo_counts = {}
for vid in data:
    for sec in data[vid]:
        data[vid][sec].sort(key=sort_key)
        total += len(data[vid][sec])
        for rk, _, _, _, _ in data[vid][sec]:
            repo_counts[rk] = repo_counts.get(rk, 0) + 1

active = [(vid, meta) for vid, meta in VERSIONS.items() if data[vid]]

# Repo JS maps
repo_urls_js = "{" + ",".join(f'"{k}":"{v["url"]}"' for k, v in REPOS.items()) + "}"
repo_names_js = "{" + ",".join(f'"{k}":"{v["name"]}"' for k, v in REPOS.items()) + "}"

# ============================================================
# BUILD HTML
# ============================================================
# Read CSS and JS from template parts if they exist, otherwise inline
CSS = '''body {
  background: #c0c0c0; color: #000;
  font-family: "MS Sans Serif","Microsoft Sans Serif",Tahoma,Geneva,sans-serif;
  font-size: 13px; margin: 0; padding: 0;
}
a { color: #00007f; } a:visited { color: #551a8b; } a:hover { color: #f00; }
hr { border:none; border-top:1px solid #808080; border-bottom:1px solid #fff; margin:12px 0; }
.page { max-width:1100px; margin:0 auto; padding:8px 16px 40px; }
.titlebar { background:linear-gradient(90deg,#000080,#1084d0); color:#fff; font-weight:bold; font-size:14px; padding:3px 6px; display:flex; justify-content:space-between; align-items:center; }
.titlebar-buttons { display:flex; gap:2px; }
.titlebar-btn { background:#c0c0c0; border:1px outset #fff; width:16px; height:14px; font-size:9px; line-height:14px; text-align:center; color:#000; cursor:default; }
.window { border:2px outset #dfdfdf; background:#c0c0c0; margin-bottom:16px; }
.window-body { padding:8px 12px; border:2px inset #808080; margin:2px; }
h1 { font-size:22px; margin:0 0 4px; font-weight:bold; }
.search-bar { display:flex; gap:4px; align-items:center; margin:8px 0; }
.search-bar label { font-weight:bold; white-space:nowrap; }
.search-bar input { flex:1; font-family:inherit; font-size:13px; padding:3px 4px; border:2px inset #808080; background:#fff; outline:none; }
.search-bar button { font-family:inherit; font-size:12px; padding:3px 12px; border:2px outset #dfdfdf; background:#c0c0c0; cursor:pointer; }
.search-bar button:active { border-style:inset; }
.search-info { font-size:11px; color:#808080; margin:2px 0 4px; }
.filters { margin:6px 0; font-size:12px; display:flex; gap:4px; flex-wrap:wrap; align-items:center; }
.filters label { font-weight:bold; }
.filters button { font-family:inherit; font-size:11px; padding:2px 8px; border:2px outset #dfdfdf; background:#c0c0c0; cursor:pointer; }
.filters button:active,.filters button.active { border-style:inset; background:#a0a0a0; }
.nav { background:#fff; border:2px inset #808080; padding:6px 10px; margin:8px 0; display:flex; flex-wrap:wrap; gap:3px 12px; align-items:center; }
.nav a { font-weight:bold; text-decoration:none; padding:1px 4px; font-size:12px; }
.nav a:hover { text-decoration:underline; }
.sources { font-size:11px; color:#444; margin:6px 0; line-height:1.6; }
.sources a { font-size:11px; }
.version-header { padding:4px 8px; color:#fff; font-weight:bold; font-size:15px; margin-top:20px; display:flex; justify-content:space-between; align-items:center; }
.version-header small { font-weight:normal; font-size:12px; opacity:0.85; }
.dll-header { background:#e8e8e8; border:1px solid #808080; border-bottom:none; padding:3px 8px; font-size:12px; font-weight:bold; color:#333; display:flex; justify-content:space-between; align-items:center; margin-top:4px; }
.dll-header small { font-weight:normal; color:#808080; font-size:11px; }
.dll-header code { background:#fff; border:1px solid #aaa; padding:0 4px; font-size:11px; font-family:"Fixedsys","Courier New",monospace; }
.icon-grid { display:flex; flex-wrap:wrap; gap:0; background:#fff; border:2px inset #808080; padding:8px; }
.icon-cell { text-align:center; padding:6px 4px; cursor:default; border:1px solid transparent; word-break:break-all; overflow:hidden; position:relative; }
.icon-cell:hover { background:#000080; color:#fff; border:1px dotted #000; }
.icon-cell img { display:block; margin:0 auto 3px; image-rendering:pixelated; pointer-events:none; }
.icon-cell span { font-size:10px; line-height:1.2; display:block; max-height:2.4em; overflow:hidden; pointer-events:none; }
.statusbar { background:#c0c0c0; border-top:1px solid #808080; padding:3px 8px; font-size:12px; display:flex; justify-content:space-between; }
.statusbar-cell { border:1px inset #808080; padding:1px 6px; background:#c0c0c0; }
.center { text-align:center; }
.back-to-top { text-align:right; font-size:11px; margin:4px 0 0; }
.icon-cell.hidden { display:none; }
.version-section.hidden { display:none; }
.dll-section.hidden { display:none; }
.ctx-menu { position:fixed; background:#c0c0c0; border:2px outset #dfdfdf; padding:2px; z-index:9999; min-width:200px; box-shadow:2px 2px 0 rgba(0,0,0,.3); font-size:12px; }
.ctx-menu .ctx-header { background:#000080; color:#fff; padding:3px 6px; font-weight:bold; font-size:11px; margin-bottom:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:280px; }
.ctx-menu .ctx-item { padding:4px 20px 4px 8px; cursor:pointer; white-space:nowrap; }
.ctx-menu .ctx-item:hover { background:#000080; color:#fff; }
.ctx-menu .ctx-sep { border-top:1px solid #808080; border-bottom:1px solid #fff; margin:2px 0; }
.toast { position:fixed; bottom:20px; left:50%; transform:translateX(-50%); background:#000080; color:#fff; padding:6px 16px; border:2px outset #4040c0; font-family:inherit; font-size:12px; z-index:10000; opacity:0; transition:opacity .2s; pointer-events:none; }
.toast.show { opacity:1; }
.size-badge { font-size:9px; color:#808080; display:block; }
.icon-cell:hover .size-badge { color:#c0c0c0; }
@media(max-width:600px) { .icon-cell img { max-width:48px; } .page { padding:4px 8px 20px; } }
'''

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Windows Icon Archive - System Icons from Win95 to Win11</title>
<style>{CSS}</style>
</head>
<body>
<div class="page">
<div class="window">
  <div class="titlebar">
    <span>&#128193; Windows Icon Archive</span>
    <div class="titlebar-buttons">
      <div class="titlebar-btn">_</div>
      <div class="titlebar-btn">&#9633;</div>
      <div class="titlebar-btn">&#10005;</div>
    </div>
  </div>
  <div class="window-body">
    <h1>Windows Icon Archive</h1>
    <p>Icons extracted from Windows system files and classic software.<br>
    {total:,} icons from <b>Windows 95</b> through <b>Windows 11</b>, organized by source DLL. Served via jsDelivr CDN.</p>

    <div class="search-bar">
      <label for="search">Find:</label>
      <input type="text" id="search" placeholder="Search {total:,} icons..." autofocus>
      <button onclick="document.getElementById('search').value='';filterIcons('');">Clear</button>
    </div>
    <div class="search-info" id="search-info"></div>

    <div class="nav">
      <span>Go&nbsp;to:</span>
'''

for vid, meta in active:
    vcount = sum(len(icons) for icons in data[vid].values())
    html += f'      <a href="#{vid}">&#9654; {meta["name"]} ({vcount:,})</a>\n'

html += '    </div>\n    <div class="sources"><b>Sources:</b> '
html += " &middot; ".join(
    f'<a href="{REPOS[k]["url"]}">{REPOS[k]["name"]}</a> ({c:,})'
    for k, c in sorted(repo_counts.items(), key=lambda x: -x[1])
)
html += '</div>\n  </div>\n</div>\n<hr>\n'

# Build sections
for vid, meta in active:
    secs = data[vid]
    if not secs: continue
    vcount = sum(len(icons) for icons in secs.values())
    sorted_secs = sorted(secs.keys(), key=dll_sort_key)

    html += f'''
<div id="{vid}" class="version-section">
  <div class="version-header" style="background:{meta['color']};">
    <span>{meta['name']}</span>
    <small>{vcount:,} icons &middot; {meta['year']}</small>
  </div>
'''
    for sec in sorted_secs:
        icons = secs[sec]
        sec_id = f"{vid}-{re.sub(r'[^a-z0-9]', '-', sec.lower())}"
        html += f'''  <div class="dll-section" id="{sec_id}">
    <div class="dll-header">
      <span><code>{htmlmod.escape(sec)}</code></span>
      <small>{len(icons)} icons</small>
    </div>
    <div class="icon-grid">
'''
        for repo_key, url, label, fname, size_px in icons:
            esc_label = htmlmod.escape(make_label(label), quote=True)
            esc_url = htmlmod.escape(url, quote=True)
            esc_fname = htmlmod.escape(fname, quote=True)
            esc_sec = htmlmod.escape(sec, quote=True)

            # Native size display
            if size_px and size_px > 0:
                w = h = size_px
                size_attr = f'width="{w}" height="{h}"'
                cell_width = max(w + 16, 80)
                size_badge = f'<span class="size-badge">{w}x{h}</span>'
            else:
                size_attr = 'width="32" height="32"'
                cell_width = 80
                size_badge = ''

            html += f'      <div class="icon-cell" style="width:{cell_width}px" data-repo="{repo_key}" data-url="{esc_url}" data-fname="{esc_fname}" data-dll="{esc_sec}" data-size="{size_px or 0}" onclick="showMenu(event,this)"><img src="{esc_url}" alt="{esc_label}" {size_attr} loading="lazy"><span>{esc_label}</span>{size_badge}</div>\n'

        html += '    </div>\n  </div>\n'

    html += f'''  <div class="statusbar">
    <span class="statusbar-cell">{vcount:,} object(s) in {len(sorted_secs)} source(s)</span>
    <span class="statusbar-cell">{meta['name']}</span>
  </div>
  <div class="back-to-top"><a href="#{active[0][0]}">&#9650; Back to top</a></div>
</div>
<hr>
'''

html += f'''
<div class="center">
  <p style="font-size:11px;color:#808080;">
    {total:,} icons served via jsDelivr CDN &middot; Best viewed in Netscape Navigator 4.0
  </p>
</div>
</div>
<div class="toast" id="toast"></div>
<script>
var repoUrls={repo_urls_js};
var repoNames={repo_names_js};
var activeMenu=null;
function showToast(m){{var t=document.getElementById('toast');t.textContent=m;t.classList.add('show');setTimeout(function(){{t.classList.remove('show')}},1500)}}
function closeMenu(){{if(activeMenu){{activeMenu.remove();activeMenu=null}}}}
function showMenu(e,cell){{
  e.stopPropagation();closeMenu();
  var url=cell.getAttribute('data-url'),repo=cell.getAttribute('data-repo'),fname=cell.getAttribute('data-fname'),dll=cell.getAttribute('data-dll'),label=cell.querySelector('span').textContent;
  var menu=document.createElement('div');menu.className='ctx-menu';
  var h=document.createElement('div');h.className='ctx-header';h.textContent=(label||fname)+(dll?' \\u2014 '+dll:'');menu.appendChild(h);
  var items=[
    {{text:'Copy image URL',action:function(){{navigator.clipboard.writeText(url).then(function(){{showToast('URL copied!')}})}} }},
    {{text:'Open image in new tab',action:function(){{window.open(url,'_blank')}}}},
    {{text:'Download icon',action:function(){{var a=document.createElement('a');a.href=url;a.download=fname;a.click()}}}},
    {{sep:true}},
    {{text:'Copy filename',action:function(){{navigator.clipboard.writeText(fname).then(function(){{showToast('Filename copied!')}})}} }},
    {{text:'Copy as HTML &lt;img&gt;',action:function(){{navigator.clipboard.writeText('<img src="'+url+'" alt="'+(label||fname)+'">'  ).then(function(){{showToast('HTML copied!')}})}} }},
    {{text:'Copy as Markdown',action:function(){{navigator.clipboard.writeText('!['+(label||fname)+']('+url+')').then(function(){{showToast('Markdown copied!')}})}} }},
    {{sep:true}},
    {{text:'Source: '+repoNames[repo],action:function(){{window.open(repoUrls[repo],'_blank')}}}},
  ];
  items.forEach(function(it){{
    if(it.sep){{var s=document.createElement('div');s.className='ctx-sep';menu.appendChild(s);return}}
    var r=document.createElement('div');r.className='ctx-item';r.innerHTML=it.text;
    r.addEventListener('click',function(ev){{ev.stopPropagation();closeMenu();it.action()}});menu.appendChild(r);
  }});
  document.body.appendChild(menu);activeMenu=menu;
  var rect=menu.getBoundingClientRect(),x=e.clientX,y=e.clientY;
  if(x+rect.width>window.innerWidth)x=window.innerWidth-rect.width-4;
  if(y+rect.height>window.innerHeight)y=window.innerHeight-rect.height-4;
  if(x<0)x=0;if(y<0)y=0;
  menu.style.left=x+'px';menu.style.top=y+'px';
}}
document.addEventListener('click',closeMenu);
document.addEventListener('keydown',function(e){{if(e.key==='Escape')closeMenu()}});
function fuzzyMatch(q,t){{q=q.toLowerCase();t=t.toLowerCase();if(!q.length)return true;var qi=0;for(var ti=0;ti<t.length&&qi<q.length;ti++){{if(t[ti]===q[qi])qi++}}return qi===q.length}}
var searchInput=document.getElementById('search'),searchInfo=document.getElementById('search-info'),totalIcons={total};
function filterIcons(q){{
  q=q.trim();var tv=0;
  document.querySelectorAll('.version-section').forEach(function(sec){{
    var sv=0;
    sec.querySelectorAll('.dll-section').forEach(function(ds){{
      var dv=0;
      ds.querySelectorAll('.icon-cell').forEach(function(c){{
        var t=c.querySelector('span').textContent+' '+c.querySelector('img').alt+' '+(c.getAttribute('data-dll')||'');
        if(!q||fuzzyMatch(q,t)){{c.classList.remove('hidden');dv++}}else{{c.classList.add('hidden')}}
      }});
      if(dv===0&&q)ds.classList.add('hidden');else ds.classList.remove('hidden');
      sv+=dv;
    }});
    tv+=sv;
    var sb=sec.querySelector('.statusbar-cell');if(sb)sb.textContent=sv.toLocaleString()+' object(s)';
    if(sv===0&&q)sec.classList.add('hidden');else sec.classList.remove('hidden');
  }});
  searchInfo.textContent=q?tv.toLocaleString()+' of '+totalIcons.toLocaleString()+' icons match "'+q+'"':'';
}}
var dt;searchInput.addEventListener('input',function(){{clearTimeout(dt);var v=this.value;dt=setTimeout(function(){{filterIcons(v)}},200)}});
</script>
</body>
</html>
'''

with open("/home/limehawk/dev/windows-icon-archive/index.html", "w") as f:
    f.write(html)

print(f"Generated index.html: {total:,} icons, {len(html):,} bytes ({len(html)/1024/1024:.1f} MB)")
print()
for vid, meta in active:
    secs = data[vid]
    vcount = sum(len(i) for i in secs.values())
    print(f"  {meta['name']:20s} {vcount:>6,} icons  [{len(secs)} sections]")
