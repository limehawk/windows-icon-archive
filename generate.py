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

# Known Win95 DLLs/EXEs — anything not in this dict goes to "Miscellaneous"
DLL_NAMES = {
    # Core system
    "shell32": "shell32.dll", "user": "user.exe", "explorer": "explorer.exe",
    "progman": "progman.exe", "main": "main.cpl",
    # Common dialogs & controls
    "comdlg32": "comdlg32.dll", "comctl32": "comctl32.dll",
    # Multimedia
    "mmsys": "mmsys.cpl", "mplayer": "mplayer.exe", "mplayer_1": "mplayer.exe",
    "sndvol32": "sndvol32.exe", "sndrec32": "sndrec32.exe", "cdplayer": "cdplayer.exe",
    "quartz": "quartz.dll",
    # Accessories
    "notepad": "notepad.exe", "winfile": "winfile.exe", "pbrush": "pbrush.exe",
    "charmap": "charmap.exe", "regedit": "regedit.exe", "defrag": "defrag.exe",
    "drvspace": "drvspace.exe",
    # Games
    "sol": "sol.exe", "freecell": "freecell.exe", "mshearts": "mshearts.exe",
    "winmine": "winmine.exe",
    # Internet/networking
    "inetcpl": "inetcpl.cpl", "mshtml": "mshtml.dll", "shdocvw": "shdocvw.dll",
    "rnaapp": "rnaapp.exe", "rnaui": "rnaui.dll", "rasapi32": "rasapi32.dll",
    "directcc": "directcc.exe", "lights": "lights.exe",
    # Mail/messaging
    "mailnews": "mailnews.dll", "wab32": "wab32.dll", "wmsui32": "wmsui32.dll",
    # Control panel
    "access": "access.cpl", "appwiz": "appwiz.cpl", "desk": "desk.cpl",
    "timedate": "timedate.cpl", "joy": "joy.cpl", "powercfg": "powercfg.cpl",
    "intl": "intl.cpl", "password": "password.cpl", "confcp": "confcp.cpl",
    "msrating": "msrating.dll",
    # System utilities
    "gcdef": "gcdef.dll", "syncui": "syncui.dll", "systray": "systray.exe",
    "rsrcmtr": "rsrcmtr.exe",
    # Fax
    "awfxex32": "awfxex32.exe", "awfxcg32": "awfxcg32.dll",
    "awfext32": "awfext32.dll", "awschd32": "awschd32.exe", "awsnto32": "awsnto32.exe",
}

with open("/tmp/react95_ico_src.txt") as f:
    for line in f:
        path = line.strip()
        ico_fname = path.split("/")[-1]
        base = ico_fname.replace(".ico", "")

        # Determine DLL source — unknown sources go to Miscellaneous
        m = re.match(r'^(.+?)(?:_(\d+))?$', base)
        if not m: continue
        dll_raw = m.group(1)
        dll_name = DLL_NAMES.get(dll_raw, "Miscellaneous")

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
        "Miscellaneous": 99,
    }
    return (priority.get(name, 50), name.lower())

total = 0
REPO_FORMATS = {
    "react95": "png", "alexh": "png", "xpicons": "png",
    "eggy115": "ico", "trapd00r": "ico", "bartekl1": "ico", "visnalize": "ico",
}

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
CSS = '''
/* === 98.css overrides — desktop metaphor === */

/* Desktop: Win2K blue */
body {
  background: #3a6ea5;
  -webkit-font-smoothing: none;
  -moz-osx-font-smoothing: grayscale;
}

/* Force pixel font on all text — 98.css only applies it to interactive elements */
* { font-family: "Pixelated MS Sans Serif", Arial; font-size: 11px; }

.page { max-width:1100px; margin:0 auto; padding:8px 16px 40px; }

/* Sticky toolbar window — "always on top" */
.toolbar-window { position:sticky; top:0; z-index:100; margin-bottom:8px; }
.toolbar-window .window-body { padding:4px 8px; }

/* Search bar layout */
.search-bar { display:flex; gap:4px; align-items:center; margin:2px 0; }
.search-bar label { white-space:nowrap; }
.search-bar input[type="text"] { flex:1; }
.search-info { font-size:11px; color:#808080; margin:1px 0; }

/* Filter row */
.filter-row { display:flex; gap:3px; flex-wrap:wrap; align-items:center; margin:3px 0; }
.filter-row label { font-weight:bold; margin-right:1px; }
.filter-row .sep { color:#808080; margin:0 3px; }

/* Pressed/active toggle button — match 98.css :active box-shadow */
button[aria-pressed="true"] {
  box-shadow: inset -1px -1px #ffffff, inset 1px 1px #0a0a0a, inset -2px -2px #dfdfdf, inset 2px 2px #808080;
  background: #dfdfdf;
}

/* Nav panel */
.nav-panel { display:flex; flex-wrap:wrap; gap:3px 10px; align-items:center; }
.nav-panel a { text-decoration:none; font-weight:bold; }
.nav-panel a:hover { text-decoration:underline; }

/* Sources detail */
.sources { font-size:11px; color:#444; line-height:1.8; margin-top:4px; }

/* Version windows — each is a real window on the desktop */
.version-window { margin-bottom:12px; }

/* Collapsible DLL sections — explorer folder-style */
.dll-header {
  background: var(--surface);
  padding:3px 8px;
  display:flex; justify-content:space-between; align-items:center;
  cursor:pointer; user-select:none;
  box-shadow: var(--border-raised-outer), var(--border-raised-inner);
  margin-top:2px;
}
.dll-header:hover { background:#d4d0c8; }
.dll-header small { color:#808080; }
.dll-header code {
  font-family: "Fixedsys", "Courier New", monospace;
  font-size: 11px;
  background: var(--button-highlight);
  padding: 0 3px;
  box-shadow: var(--border-field);
}
.dll-header .toggle { font-size:9px; margin-right:4px; display:inline-block; transition:transform .1s; }
.dll-section.collapsed .icon-grid { display:none; }
.dll-section.collapsed .dll-header .toggle { transform:rotate(-90deg); }

/* Icon grid — white sunken panel */
.icon-grid { display:flex; flex-wrap:wrap; gap:0; padding:6px; overflow:auto; }

/* Icon cells */
.icon-cell { text-align:center; padding:4px 3px; cursor:default; border:1px solid transparent; word-break:break-all; overflow:hidden; position:relative; width:80px; }
.icon-cell:hover { background:var(--dialog-blue); color:#fff; border:1px dotted #000; }
.icon-cell img { display:block; margin:0 auto 2px; image-rendering:pixelated; pointer-events:none; }
.icon-cell span { font-size:10px; line-height:1.2; display:block; max-height:2.4em; overflow:hidden; pointer-events:none; }

/* Medium density */
body.view-medium .icon-cell { width:120px; padding:8px 6px; }
body.view-medium .icon-cell img { width:48px !important; height:48px !important; }
body.view-medium .icon-cell span { max-height:3.6em; }

/* List view */
body.view-list .icon-grid { flex-direction:column; }
body.view-list .icon-cell { width:100% !important; display:flex; align-items:center; gap:8px; text-align:left; padding:2px 6px; box-sizing:border-box; }
body.view-list .icon-cell img { margin:0; flex-shrink:0; width:24px !important; height:24px !important; }
body.view-list .icon-cell span { max-height:none; flex:1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; word-break:normal; }
body.view-list .icon-cell .size-badge { flex-shrink:0; width:44px; text-align:right; }
body.view-list .icon-cell .list-meta { color:#808080; flex-shrink:0; min-width:100px; text-align:right; display:block; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
body.view-list .icon-cell:hover .list-meta { color:#c0c0c0; }
body:not(.view-list) .list-meta { display:none; }

/* Visibility */
.icon-cell.hidden { display:none; }
.version-window.hidden { display:none; }
.dll-section.hidden { display:none; }

/* Context menu — proper 98.css window */
.ctx-menu { position:fixed; z-index:9999; min-width:220px; }
.ctx-menu .title-bar { cursor:default; }
.ctx-menu .window-body { padding:2px; margin:0; }
.ctx-item { padding:4px 16px 4px 8px; cursor:pointer; white-space:nowrap; }
.ctx-item:hover { background:var(--dialog-blue); color:#fff; }
.ctx-sep { border-top:1px solid #808080; border-bottom:1px solid #fff; margin:2px 0; }

/* Toast notification */
.toast { position:fixed; bottom:20px; left:50%; transform:translateX(-50%); z-index:10000; opacity:0; transition:opacity .2s; pointer-events:none; }
.toast.show { opacity:1; }

/* Size badge */
.size-badge { font-size:9px; color:#808080; display:block; pointer-events:none; }
.icon-cell:hover .size-badge { color:#c0c0c0; }

/* Back to top link */
.back-to-top { text-align:right; font-size:11px; margin:4px 8px 0; }

@media(max-width:600px) {
  .icon-cell img { max-width:48px; }
  .page { padding:4px 8px 20px; }
}
'''

nav_links = ""
for vid, meta in active:
    vcount = sum(len(icons) for icons in data[vid].values())
    nav_links += f'      <a href="#{vid}">{meta["name"]} ({vcount:,})</a>\n'

sources_html = " &middot; ".join(
    f'<a href="{REPOS[k]["url"]}">{REPOS[k]["name"]}</a> ({c:,})'
    for k, c in sorted(repo_counts.items(), key=lambda x: -x[1])
)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Windows Icon Archive</title>
<link rel="stylesheet" href="https://unpkg.com/98.css">
<style>{CSS}</style>
</head>
<body>
<div class="page">

<!-- === About Window === -->
<div class="window">
  <div class="title-bar">
    <div class="title-bar-text">Windows Icon Archive</div>
    <div class="title-bar-controls">
      <button aria-label="Minimize"></button>
      <button aria-label="Maximize"></button>
      <button aria-label="Close"></button>
    </div>
  </div>
  <div class="window-body">
    <p>Icons extracted from Windows system files &mdash;
    <b>{total:,}</b> icons from <b>Windows 95</b> through <b>Windows 11</b>, organized by source DLL.</p>
    <fieldset>
      <legend>Navigate</legend>
      <div class="nav-panel">
{nav_links}      </div>
    </fieldset>
    <details>
      <summary>Sources ({len(repo_counts)} repositories)</summary>
      <div class="sources">{sources_html}</div>
    </details>
  </div>
  <div class="status-bar">
    <p class="status-bar-field">{total:,} icons</p>
    <p class="status-bar-field">{len(active)} versions</p>
    <p class="status-bar-field">jsDelivr CDN</p>
  </div>
</div>

<!-- === Toolbar Window (sticky) === -->
<div class="window toolbar-window" id="toolbar">
  <div class="title-bar">
    <div class="title-bar-text">Find</div>
    <div class="title-bar-controls">
      <button aria-label="Close"></button>
    </div>
  </div>
  <div class="window-body">
    <div class="search-bar">
      <label for="search">Search:</label>
      <input type="text" id="search" placeholder="{total:,} icons...">
      <button onclick="document.getElementById('search').value='';applyFilters();">Clear</button>
    </div>
    <div class="filter-row">
      <label>Size:</label>
      <button aria-pressed="true" data-size="all" onclick="setSizeFilter('all')">All</button>
      <button aria-pressed="false" data-size="16" onclick="setSizeFilter('16')">16x16</button>
      <button aria-pressed="false" data-size="32" onclick="setSizeFilter('32')">32x32</button>
      <button aria-pressed="false" data-size="48" onclick="setSizeFilter('48')">48x48</button>
      <span class="sep">|</span>
      <label>Format:</label>
      <button aria-pressed="true" data-fmt="all" onclick="setFmtFilter('all')">All</button>
      <button aria-pressed="false" data-fmt="ico" onclick="setFmtFilter('ico')">.ico</button>
      <button aria-pressed="false" data-fmt="png" onclick="setFmtFilter('png')">.png</button>
      <span class="sep">|</span>
      <label>View:</label>
      <button aria-pressed="true" data-view="small" onclick="setView('small')">Small</button>
      <button aria-pressed="false" data-view="medium" onclick="setView('medium')">Medium</button>
      <button aria-pressed="false" data-view="list" onclick="setView('list')">List</button>
    </div>
    <div class="search-info" id="search-info"></div>
  </div>
</div>

'''

# Build version windows — each version is its own window on the desktop
for vid, meta in active:
    secs = data[vid]
    if not secs: continue
    vcount = sum(len(icons) for icons in secs.values())
    sorted_secs = sorted(secs.keys(), key=dll_sort_key)

    html += f'''
<!-- === {meta['name']} Window === -->
<div id="{vid}" class="window version-window">
  <div class="title-bar">
    <div class="title-bar-text">{meta['name']} &mdash; {vcount:,} icons &mdash; {meta['year']}</div>
    <div class="title-bar-controls">
      <button aria-label="Minimize"></button>
      <button aria-label="Maximize"></button>
      <button aria-label="Close"></button>
    </div>
  </div>
  <div class="window-body">
'''
    for sec in sorted_secs:
        icons = secs[sec]
        sec_id = f"{vid}-{re.sub(r'[^a-z0-9]', '-', sec.lower())}"
        html += f'''    <div class="dll-section" id="{sec_id}">
      <div class="dll-header" onclick="this.parentElement.classList.toggle('collapsed')">
        <span><span class="toggle">&#9660;</span> <code>{htmlmod.escape(sec)}</code></span>
        <small>{len(icons)} icons</small>
      </div>
      <div class="sunken-panel icon-grid">
'''
        for repo_key, url, label, fname, size_px in icons:
            esc_label = htmlmod.escape(make_label(label), quote=True)
            esc_url = htmlmod.escape(url, quote=True)
            esc_fname = htmlmod.escape(fname, quote=True)
            esc_sec = htmlmod.escape(sec, quote=True)

            if size_px and size_px > 0:
                w = h = size_px
                size_attr = f'width="{w}" height="{h}"'
                cell_width = max(w + 16, 80)
                size_badge = f'<span class="size-badge">{w}x{h}</span>'
            else:
                size_attr = 'width="32" height="32"'
                cell_width = 80
                size_badge = ''

            fmt = REPO_FORMATS.get(repo_key, "ico")
            list_meta = f'<span class="list-meta">{esc_sec}</span>'
            html += f'        <div class="icon-cell" style="width:{cell_width}px" data-repo="{repo_key}" data-url="{esc_url}" data-fname="{esc_fname}" data-dll="{esc_sec}" data-size="{size_px or 0}" data-fmt="{fmt}" onclick="showMenu(event,this)"><img src="{esc_url}" alt="{esc_label}" {size_attr} loading="lazy"><span class="icon-label">{esc_label}</span>{size_badge}{list_meta}</div>\n'

        html += '      </div>\n    </div>\n'

    html += f'''  </div>
  <div class="status-bar">
    <p class="status-bar-field">{vcount:,} object(s) in {len(sorted_secs)} source(s)</p>
    <p class="status-bar-field">{meta['name']}</p>
  </div>
</div>
<div class="back-to-top"><a href="#{active[0][0]}">&#9650; Back to top</a></div>
'''

html += f'''
</div>

<!-- Toast (styled as a tiny 98.css window) -->
<div class="window toast" id="toast">
  <div class="window-body" style="margin:4px;padding:4px 12px;">
    <span id="toast-text"></span>
  </div>
</div>

<script>
var repoUrls={repo_urls_js};
var repoNames={repo_names_js};
var activeMenu=null;
var currentSizeFilter='all';
var currentFmtFilter='all';
var totalIcons={total};

// === TOAST ===
function showToast(m){{
  var t=document.getElementById('toast'),tx=document.getElementById('toast-text');
  tx.textContent=m;t.classList.add('show');
  setTimeout(function(){{t.classList.remove('show')}},1500);
}}

// === CONTEXT MENU (proper 98.css window) ===
function closeMenu(){{if(activeMenu){{activeMenu.remove();activeMenu=null}}}}
function showMenu(e,cell){{
  e.stopPropagation();closeMenu();
  var url=cell.getAttribute('data-url'),repo=cell.getAttribute('data-repo'),
      fname=cell.getAttribute('data-fname'),dll=cell.getAttribute('data-dll'),
      label=(cell.querySelector('.icon-label')||cell.querySelector('span')).textContent;

  // Build a proper 98.css window
  var win=document.createElement('div');
  win.className='window ctx-menu';

  // Title bar with close button
  var tb=document.createElement('div');tb.className='title-bar';
  var tbt=document.createElement('div');tbt.className='title-bar-text';
  tbt.textContent=(label||fname)+(dll?' \\u2014 '+dll:'');
  var tbc=document.createElement('div');tbc.className='title-bar-controls';
  var closeBtn=document.createElement('button');
  closeBtn.setAttribute('aria-label','Close');
  closeBtn.addEventListener('click',function(ev){{ev.stopPropagation();closeMenu()}});
  tbc.appendChild(closeBtn);
  tb.appendChild(tbt);tb.appendChild(tbc);
  win.appendChild(tb);

  // Window body with menu items
  var body=document.createElement('div');body.className='window-body';
  body.style.margin='2px';body.style.padding='2px';

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
    if(it.sep){{var s=document.createElement('div');s.className='ctx-sep';body.appendChild(s);return}}
    var r=document.createElement('div');r.className='ctx-item';r.innerHTML=it.text;
    r.addEventListener('click',function(ev){{ev.stopPropagation();closeMenu();it.action()}});body.appendChild(r);
  }});
  win.appendChild(body);

  win.style.visibility='hidden';win.style.left='0';win.style.top='0';
  document.body.appendChild(win);activeMenu=win;
  var cx=e.clientX,cy=e.clientY;
  requestAnimationFrame(function(){{
    var rect=win.getBoundingClientRect(),x=cx,y=cy;
    if(x+rect.width>window.innerWidth)x=window.innerWidth-rect.width-4;
    if(y+rect.height>window.innerHeight)y=window.innerHeight-rect.height-4;
    if(x<0)x=0;if(y<0)y=0;
    win.style.left=x+'px';win.style.top=y+'px';win.style.visibility='';
  }});
}}
document.addEventListener('click',closeMenu);
document.addEventListener('keydown',function(e){{if(e.key==='Escape')closeMenu()}});

// === FUZZY SEARCH ===
function fuzzyMatch(q,t){{q=q.toLowerCase();t=t.toLowerCase();if(!q.length)return true;var qi=0;for(var ti=0;ti<t.length&&qi<q.length;ti++){{if(t[ti]===q[qi])qi++}}return qi===q.length}}

// === TOGGLE HELPERS (aria-pressed) ===
function toggleGroup(attr,val){{
  document.querySelectorAll('['+attr+']').forEach(function(b){{
    if(b.tagName==='BUTTON')b.setAttribute('aria-pressed',b.getAttribute(attr)===val?'true':'false');
  }});
}}

// === SIZE FILTER ===
function setSizeFilter(size){{
  currentSizeFilter=size;
  toggleGroup('data-size',size);
  applyFilters();updateHash();
}}

// === FORMAT FILTER ===
function setFmtFilter(fmt){{
  currentFmtFilter=fmt;
  toggleGroup('data-fmt',fmt);
  applyFilters();updateHash();
}}

// === VIEW MODE ===
function setView(mode){{
  document.body.classList.remove('view-small','view-medium','view-list');
  if(mode!=='small')document.body.classList.add('view-'+mode);
  toggleGroup('data-view',mode);
  updateHash();
}}

// === COMBINED FILTER ===
function applyFilters(){{
  var q=document.getElementById('search').value.trim();
  var sf=currentSizeFilter;
  var ff=currentFmtFilter;
  var tv=0;
  document.querySelectorAll('.version-window').forEach(function(sec){{
    var sv=0;
    sec.querySelectorAll('.dll-section').forEach(function(ds){{
      var dv=0;
      ds.querySelectorAll('.icon-cell').forEach(function(c){{
        var text=c.querySelector('span').textContent+' '+c.querySelector('img').alt+' '+(c.getAttribute('data-dll')||'');
        var matchText=!q||fuzzyMatch(q,text);
        var sz=c.getAttribute('data-size')||'0';
        var matchSize=(sf==='all')||(sz===sf)||(sf==='32'&&sz==='0');
        var ft=c.getAttribute('data-fmt')||'ico';
        var matchFmt=(ff==='all')||(ft===ff);
        if(matchText&&matchSize&&matchFmt){{c.classList.remove('hidden');dv++}}else{{c.classList.add('hidden')}}
      }});
      var anyFilter=q||sf!=='all'||ff!=='all';
      if(dv===0&&anyFilter)ds.classList.add('hidden');else ds.classList.remove('hidden');
      sv+=dv;
    }});
    tv+=sv;
    var sb=sec.querySelector('.status-bar-field');if(sb)sb.textContent=sv.toLocaleString()+' object(s)';
    var anyFilter=q||sf!=='all'||ff!=='all';
    if(sv===0&&anyFilter)sec.classList.add('hidden');else sec.classList.remove('hidden');
  }});
  var info=document.getElementById('search-info');
  var parts=[];
  if(q)parts.push('"'+q+'"');
  if(sf!=='all')parts.push(sf+'x'+sf);
  if(ff!=='all')parts.push('.'+ff);
  info.textContent=parts.length?tv.toLocaleString()+' of '+totalIcons.toLocaleString()+' icons'+(parts.length?' matching '+parts.join(', '):''):'';
}}

// === URL HASH ROUTING ===
function updateHash(){{
  var q=document.getElementById('search').value.trim();
  var sf=currentSizeFilter;
  var ff=currentFmtFilter;
  var view='small';
  if(document.body.classList.contains('view-medium'))view='medium';
  if(document.body.classList.contains('view-list'))view='list';
  var parts=[];
  if(q)parts.push('q='+encodeURIComponent(q));
  if(sf!=='all')parts.push('size='+sf);
  if(ff!=='all')parts.push('fmt='+ff);
  if(view!=='small')parts.push('view='+view);
  var hash=parts.length?'#'+parts.join('&'):'';
  if(window.location.hash!==hash)history.replaceState(null,null,hash||window.location.pathname);
}}

function loadFromHash(){{
  var h=window.location.hash.replace('#','');
  if(!h||h.indexOf('=')===-1)return; // plain anchor, not filter state
  var params={{}};
  h.split('&').forEach(function(p){{var kv=p.split('=');if(kv.length===2)params[kv[0]]=decodeURIComponent(kv[1])}});
  if(params.q)document.getElementById('search').value=params.q;
  if(params.size){{currentSizeFilter=params.size;toggleGroup('data-size',params.size)}}
  if(params.fmt){{currentFmtFilter=params.fmt;toggleGroup('data-fmt',params.fmt)}}
  if(params.view){{
    if(params.view!=='small')document.body.classList.add('view-'+params.view);
    toggleGroup('data-view',params.view);
  }}
  applyFilters();
}}

// === INIT ===
var dt;
document.getElementById('search').addEventListener('input',function(){{clearTimeout(dt);var v=this;dt=setTimeout(function(){{applyFilters();updateHash()}},200)}});
window.addEventListener('hashchange',loadFromHash);
loadFromHash();
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
