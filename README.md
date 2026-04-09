<div align="center">

# Windows Icon Archive

**Every icon extracted from Windows system files — Win95 through Win11**

[**Browse the Archive →**](https://limehawk.github.io/windows-icon-archive/)

---

`shell32.dll` · `imageres.dll` · `progman.exe` · `moricons.dll` · `pifmgr.dll` · and 360+ more

</div>

---

### What is this?

A single-page archive of **8,780 icons** extracted from Windows system DLLs and executables, spanning 9 versions of Windows over 26 years. Every icon is displayed at its native pixel-perfect resolution, organized by Windows version and source file.

Icons are served via [jsDelivr CDN](https://www.jsdelivr.com/) from their original open-source repositories — nothing is modified or re-encoded.

### Coverage

| Version | Icons | Sources | Year |
|---------|------:|---------|------|
| **Windows 95** | 1,687 | `shell32.dll`, `progman.exe`, `moricons.dll`, `pifmgr.dll`, +363 more | 1995 |
| **Windows 98** | 2,398 | System Icons, System Icons (PNG) | 1998 |
| **Windows 2000** | 275 | System Icons | 2000 |
| **Windows XP** | 794 | `shell32.dll`, XP, Longhorn, Whistler, SP2 Beta | 2001 |
| **Windows Vista** | 463 | `shell32.dll`, `imageres.dll` | 2007 |
| **Windows 7** | 1,086 | `shell32.dll`, `imageres.dll`, +28 app sources | 2009 |
| **Windows 8.1** | 721 | `shell32.dll`, `imageres.dll` | 2012 |
| **Windows 10** | 663 | `shell32.dll.mun`, `imageres.dll.mun` | 2015 |
| **Windows 11** | 693 | `shell32.dll.mun`, `imageres.dll.mun` | 2021 |

### Features

- **Fuzzy search** across all 8,780 icons — filenames, labels, and DLL sources
- **Size filter** — toggle between All / 16×16 / 32×32 / 48×48
- **Three view modes** — Small grid, Medium grid, List (with full metadata)
- **Collapsible sections** — click any DLL header to fold/unfold
- **Click any icon** for a context menu: copy URL, download, copy as HTML/Markdown, link to source repo
- **URL hash routing** — search state persists in the URL for bookmarking and sharing
- **Sticky toolbar** — search and filters stay pinned while you scroll

### Upstream Sources

All icons are sourced from these open-source repositories:

| Repository | Icons | Coverage |
|------------|------:|----------|
| [React95/React95](https://github.com/React95/React95) | 1,536 | Win95 icons from 180+ DLLs/EXEs, all sizes |
| [alexh/vintage-icons](https://github.com/alexh/vintage-icons) | 1,763 | Win98 system icons as PNG |
| [trapd00r/win95-winxp_icons](https://github.com/trapd00r/win95-winxp_icons) | 910 | Win98/2K system icons |
| [softwarehistorysociety/XPIcons](https://github.com/softwarehistorysociety/XPIcons) | 556 | WinXP + Longhorn + Whistler |
| [bartekl1/WindowsResources](https://github.com/bartekl1/WindowsResources) | 3,303 | XP→11 extracted from shell32/imageres DLLs |
| [visnalize/resources](https://github.com/Visnalize/win7-icons) | 561 | Win7 icons from 29 system sources |
| [Eggy115/Icons](https://github.com/Eggy115/Icons) | 151 | Win95 moricons.dll + pifmgr.dll |

### Roadmap

- [ ] **Self-hosted archive** — migrate all icons into this repo with original DLLs + extracted files, organized like [bartekl1/windows-ui-assets](https://github.com/bartekl1/windows-ui-assets)
- [ ] **Original filenames preserved** — no renaming, no sanitizing
- [ ] **Classic game icons** — curated section with authentic exe-extracted icons (Doom, Quake, etc.)
- [ ] **Icon size variants** — serve all sizes from multi-resolution .ico containers

### Tech

One `index.html` file (4.6 MB). No framework, no build step, no dependencies. A `generate.py` script builds it from cached file lists. Icons served via jsDelivr CDN from upstream GitHub repos.

### License

This project aggregates icons from multiple upstream repositories, each with their own licenses. The website code itself is MIT. Windows icons are property of Microsoft Corporation.

---

<div align="center">

**[limehawk.github.io/windows-icon-archive](https://limehawk.github.io/windows-icon-archive/)**

Best viewed in Netscape Navigator 4.0

</div>
