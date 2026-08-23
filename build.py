#!/usr/bin/env python3
"""Build the LeetCode solution website for GitHub Pages.

Adapted from ai-infra-notes/build/leetcode.py, simplified for a standalone
repository: markdown sources live at the repo root (contest/, daily/, images/)
and the site is emitted at the root of public/.

Generates:
  - public/index.html          (overview: daily + contest problem lists)
  - public/problems/<slug>.html (one page per solution markdown)
  - public/images/             (all svg/png from images/ and per-day images/)
  - public/css/, public/js/    (copied from static/)
"""

import json
import re
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent
STATIC_DIR = REPO_ROOT / "static"

# Directories never scanned for solution markdown
EXCLUDED_PARTS = {".git", ".arts", ".opencode", "build", "public", "static", "images"}

# Slug of the curated hot-interview page (hot-interview.md at repo root)
HOT_PAGE_SLUG = "hot-interview"

# Extra top-level pages that get a sidebar entry: (slug, label)
NAV_EXTRA_PAGES = [
    (HOT_PAGE_SLUG, "高频面试题"),
    ("10-week-plan", "10 周刷题计划"),
]

GITHUB_REPO_URL = "https://github.com/hzchenxiaobin/leetcode"

TOPIC_ICONS = {
    "backtracking": "🔁",
    "greedy": "💰",
    "interval-dp": "📊",
    "monotonic-stack": "📉",
}


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------

def escape_for_template_string(text: str) -> str:
    """Escape a markdown string for embedding in a JS template string."""
    text = text.replace("\\", "\\\\")
    text = text.replace("`", "\\`")
    text = text.replace("${", "\\${")
    text = text.replace("</script>", "\\x3c/script>")
    return text


def _classify(md_file: Path) -> Dict[str, Optional[str]]:
    """Classify a solution file into contest/daily/other with its path metadata."""
    rel_parts = md_file.relative_to(REPO_ROOT).parts
    if rel_parts[0] == "contest" and len(rel_parts) > 1:
        return {"category": "contest", "contest": rel_parts[1], "week": None, "day": None, "folder": rel_parts[1]}
    if rel_parts[0] == "solution" and len(rel_parts) > 1:
        return {"category": "solution", "contest": None, "week": None, "day": None, "folder": rel_parts[1]}
    if rel_parts[0] == "topics" and len(rel_parts) > 1:
        return {"category": "topics", "contest": None, "week": None, "day": None, "folder": "topics"}
    return {"category": "other", "contest": None, "week": None, "day": None, "folder": md_file.parent.name}


def _compute_slugs(md_files: List[Path]) -> Dict[Path, str]:
    """Assign each solution file its output slug (flat problems/<slug>.html).

    Collision rule: the first file keeps its bare stem; later duplicates get
    prefixed with contest / week-day / folder.
    """
    slug_by_path: Dict[Path, str] = {}
    seen_slugs: Dict[str, int] = {}
    for md_file in md_files:
        info = _classify(md_file)
        base_slug = md_file.stem
        slug = base_slug
        if slug in seen_slugs:
            seen_slugs[slug] += 1
            if info["category"] == "contest":
                slug = f"{info['contest']}-{base_slug}"
            elif info["category"] in ("daily", "solution"):
                slug = f"{info['folder']}-{base_slug}"
            else:
                slug = f"{info['folder']}-{base_slug}"
        else:
            seen_slugs[slug] = 1
        slug_by_path[md_file.resolve()] = slug
    return slug_by_path


def _rewrite_md_links_to_html(markdown_text: str, md_file: Path, slug_by_path: Dict[Path, str]) -> str:
    """Rewrite local .md links to .html for GitHub Pages deployment.

    Solution pages are emitted flat in the problems/ output directory, so a
    relative link to another solution collapses to ``./<slug>.html``.
    """

    def replace_link(match):
        url = match.group(1)
        if not url.endswith(".md"):
            return match.group(0)
        target = (md_file.parent / url).resolve()
        slug = slug_by_path.get(target)
        if slug is not None:
            return f"](./{slug}.html)"
        new_url = url[:-3] + ".html"
        if new_url.endswith("README.html"):
            new_url = new_url[: -len("README.html")] + "index.html"
        return f"]({new_url})"

    return re.sub(r"\]\((?!https?://|#)([^)]+)\)", replace_link, markdown_text)


def _parse_title(markdown_text: str, filename: str = "") -> str:
    """Extract title from an explicit HTML title comment, then first H1, then filename."""
    match = re.search(r"<!--\s*title:\s*(.+?)\s*-->", markdown_text)
    if match:
        title = match.group(1).strip()
    else:
        match = re.search(r"^#\s+(.+)$", markdown_text, re.MULTILINE)
        title = match.group(1).strip() if match else "题解"

    q_match = re.match(r"^(Q\d+)\.", filename)
    if q_match:
        prefix = q_match.group(1)
        if not re.match(rf"^{prefix}\b", title):
            title = f"{prefix}. {title}"

    return title


def _extract_problem_number(markdown_text: str) -> Optional[str]:
    """Extract the LeetCode problem number from the '**链接**：[123. ...]' line."""
    match = re.search(r"\*\*链接\*\*[：:]\s*\[(?:LC\s*)?(\d+)\.", markdown_text)
    return match.group(1) if match else None


def _extract_leetcode_url(markdown_text: str) -> Optional[str]:
    match = re.search(r"https://leetcode\.cn/problems/([^/\s)]+)/?", markdown_text)
    if match:
        return f"https://leetcode.cn/problems/{match.group(1)}/"
    return None


def _range_start(name: str) -> int:
    """Sort key for a solution range folder like '0001-0100' -> 1."""
    m = re.match(r'(\d+)', name)
    return int(m.group(1)) if m else 0


def _range_label(name: str) -> str:
    """Human-friendly label for a range folder: '0001-0100' -> '1-100'."""
    m = re.match(r'0*(\d+)-0*(\d+)', name)
    return f"{m.group(1)}-{m.group(2)}" if m else name


def _thousand_range_key(folder: str) -> str:
    """1000-range key for a 100-range folder: '0001-0100' -> '0001-1000'."""
    start = _range_start(folder)
    t_start = ((start - 1) // 1000) * 1000 + 1
    return f"{t_start:04d}-{t_start + 999:04d}"


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------

def _build_nav(current_slug: Optional[str], problems: List[Dict], root_prefix: str) -> str:
    """Build sidebar navigation — contest accordion + solution flat list by difficulty."""
    lines = []

    overview_class = "nav-link active" if current_slug is None else "nav-link"
    lines.append(f'<a class="{overview_class}" href="{root_prefix}index.html">题解列表</a>')

    slugs = {p["slug"] for p in problems}
    for slug, label in NAV_EXTRA_PAGES:
        if slug in slugs:
            cls = "nav-link active" if current_slug == slug else "nav-link"
            lines.append(f'<a class="{cls}" href="{root_prefix}problems/{slug}.html">{label}</a>')

    topic_problems = [p for p in problems if p["category"] == "topics"]

    current_path: List[str] = []
    if current_slug is not None:
        for p in problems:
            if p["slug"] == current_slug:
                if p["category"] == "contest":
                    current_path = ["contest", p["contest"]]
                elif p["category"] == "solution":
                    current_path = ["solution", _thousand_range_key(p["folder"]), p["folder"]]
                elif p["category"] == "topics":
                    current_path = ["topics"]
                break

    tree: Dict[str, Dict] = {
        "contest": {"title": "周赛", "children": {}, "problems": []},
        "solution": {"title": "每日一题", "children": {}, "problems": []},
    }

    for p in problems:
        if p["category"] == "contest":
            contest = p["contest"]
            if contest not in tree["contest"]["children"]:
                tree["contest"]["children"][contest] = {
                    "title": contest, "children": {}, "problems": []
                }
            tree["contest"]["children"][contest]["problems"].append(p)
        elif p["category"] == "solution":
            folder = p["folder"]
            t_key = _thousand_range_key(folder)
            if t_key not in tree["solution"]["children"]:
                tree["solution"]["children"][t_key] = {
                    "title": _range_label(t_key), "children": {}, "problems": []
                }
            if folder not in tree["solution"]["children"][t_key]["children"]:
                tree["solution"]["children"][t_key]["children"][folder] = {
                    "title": _range_label(folder), "children": {}, "problems": []
                }
            tree["solution"]["children"][t_key]["children"][folder]["problems"].append(p)

    def sort_key_numeric(name: str) -> int:
        match = re.search(r'(\d+)$', name)
        return int(match.group(1)) if match else 0

    def render_accordion(node: Dict, path: List[str], level: int) -> List[str]:
        result: List[str] = []
        title = node["title"]

        is_expanded = bool(current_path and current_path[:len(path)] == path)
        expanded_cls = " is-expanded" if is_expanded else ""
        aria_expanded = "true" if is_expanded else "false"
        toggle_icon = "▸"
        level_cls = f" level-{level}"

        result.append(f'<div class="nav-accordion-item{level_cls}{expanded_cls}">')
        result.append('  <div class="nav-accordion-header">')
        result.append(
            f'    <span class="nav-link week-link">{title}</span>'
            f'<button class="nav-accordion-toggle" aria-label="收起/展开 {title}" aria-expanded="{aria_expanded}">{toggle_icon}</button>'
        )
        result.append('  </div>')
        result.append('  <div class="nav-accordion-content">')
        result.append('    <div class="nav-section">')

        children = node.get("children", {})
        if children:
            child_items = list(children.items())
            if path == ["contest"]:
                child_items.sort(key=lambda x: sort_key_numeric(x[0]), reverse=True)
            else:
                child_items.sort(key=lambda x: x[0])
            for key, child in child_items:
                child_path = path + [key]
                result.extend(render_accordion(child, child_path, level + 1))

        for p in node.get("problems", []):
            cls = "nav-link active" if current_slug == p["slug"] else "nav-link"
            label = p["title"]
            if p.get("number"):
                label = f'{p["number"]}. {label}'
            result.append(
                f'<a class="{cls}" href="{root_prefix}problems/{p["slug"]}.html">{label}</a>'
            )

        result.append('    </div>')
        result.append('  </div>')
        result.append('</div>')
        return result

    if topic_problems:
        topic_node = {"title": "专题", "children": {}, "problems": topic_problems}
        lines.extend(render_accordion(topic_node, ["topics"], 1))

    lines.append('<div class="nav-section-title">题目</div>')

    for key in ["contest", "solution"]:
        if tree[key]["children"] or tree[key]["problems"]:
            lines.extend(render_accordion(tree[key], [key], 1))

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Page template
# ---------------------------------------------------------------------------

def page_template(
    title: str,
    nav_html: str,
    markdown: str,
    *,
    root_prefix: str = "",
    page_title: Optional[str] = None,
    sidebar_title: str = "LeetCode 题解",
    sidebar_title_style: str = "font-size: 1.5rem; margin-bottom: 0;",
) -> str:
    """Generate a standard HTML page with sidebar navigation and markdown content."""
    escaped_markdown = escape_for_template_string(markdown)
    if page_title is None:
        page_title = title

    title_style_attr = f' style="{sidebar_title_style}"' if sidebar_title_style else ""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <link rel="stylesheet" href="{root_prefix}css/style.css?v=10">
    <!-- Marked.js for Markdown rendering -->
    <script src="{root_prefix}js/marked.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script src="{root_prefix}js/markdown-math.js"></script>
    <!-- Prism.js for syntax highlighting -->
    <link href="{root_prefix}css/prism-tomorrow.min.css" rel="stylesheet">
    <script src="{root_prefix}js/prism.min.js"></script>
    <script src="{root_prefix}js/prism-c.min.js"></script>
    <script src="{root_prefix}js/prism-cpp.min.js"></script>
    <script src="{root_prefix}js/prism-bash.min.js"></script>
    <script src="{root_prefix}js/prism-python.min.js"></script>
</head>
<body>
    <header class="top-nav">
        <div class="top-nav-inner">
            <button class="menu-toggle" aria-label="打开导航菜单">☰</button>
            <a class="top-nav-brand" href="{root_prefix}index.html">LeetCode <span>题解</span></a>
            <nav class="top-nav-links">
                <a href="{root_prefix}index.html">题解列表</a>
                <a href="{GITHUB_REPO_URL}">GitHub ↗</a>
            </nav>
        </div>
    </header>

    <div class="nav-overlay"></div>
    <aside class="sidebar">
        <div class="sidebar-header">
            <a href="{root_prefix}index.html" style="text-decoration: none;">
                <h1 class="sidebar-title"{title_style_attr}>{sidebar_title}</h1>
            </a>
        </div>
        <nav class="sidebar-nav">
{nav_html}
        </nav>
    </aside>

    <main class="main-content">
        <div class="page-header">
            <h1 class="page-title">{title}</h1>
        </div>
        <div class="content-shell">
            <article class="content" id="content"></article>
            <aside class="toc" id="toc" aria-label="本页目录"></aside>
        </div>
    </main>

    <button class="back-to-top" aria-label="Back to top">↑</button>

    <script>
        const markdown = `{escaped_markdown}`;

        const renderer = new marked.Renderer();
        marked.setOptions({{
            renderer: renderer,
            headerIds: false,
            gfm: true,
            breaks: false,
            sanitize: false
        }});

        try {{
            if (typeof marked === 'undefined') {{
                throw new Error('marked.js failed to load. Please check js/marked.min.js exists.');
            }}
            document.getElementById('content').innerHTML = marked.parse(markdown);

            if (window.Prism) {{
                Prism.highlightAll();
            }}
        }} catch (err) {{
            document.getElementById('content').innerHTML = '<div style="padding: 20px; color: #ff7b72; background: #2d1515; border-radius: 8px;">' +
                '<h2>⚠️ 页面渲染失败</h2>' +
                '<p>' + err.message + '</p>' +
                '<p>请打开浏览器控制台（Cmd + Option + J）查看详细错误。</p>' +
                '</div>';
            console.error('Markdown render error:', err);
        }}
    </script>
    <script src="{root_prefix}js/main.js?v=10"></script>
</body>
</html>
"""


def landing_template(
    *,
    stats_html: str,
    topic_cards_html: str,
    resource_cards_html: str,
    problem_list_html: str,
    random_picker_html: str,
    hot_href: Optional[str] = None,
    plan_href: Optional[str] = None,
    root_prefix: str = "",
) -> str:
    """Generate the landing-style index.html (no sidebar, hero + card sections)."""

    hero_actions_parts = []
    if hot_href:
        hero_actions_parts.append(
            f'<a class="btn btn-primary" href="{hot_href}">高频面试题</a>'
        )
    if plan_href:
        hero_actions_parts.append(
            f'<a class="btn btn-secondary" href="{plan_href}">10 周刷题计划</a>'
        )
    hero_actions = (
        f'<div class="hero-actions">{"".join(hero_actions_parts)}</div>'
        if hero_actions_parts
        else ""
    )

    nav_links_parts = [
        f'<a href="#problems">题解列表</a>',
        f'<a href="#topics">算法专题</a>',
    ]
    if hot_href:
        nav_links_parts.append(f'<a href="{hot_href}">高频面试题</a>')
    if plan_href:
        nav_links_parts.append(f'<a href="{plan_href}">10 周计划</a>')
    nav_links_parts.append(
        f'<a class="landing-nav-github" href="{GITHUB_REPO_URL}">GitHub ↗</a>'
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LeetCode 题解</title>
    <meta name="description" content="面试高频题与周赛题的中文题解集合，配套手绘 SVG 图解、复杂度分析与面试 Q&A。">
    <link rel="stylesheet" href="{root_prefix}css/style.css?v=10">
    <script src="{root_prefix}js/main.js?v=10" defer></script>
</head>
<body class="landing">
    <header class="landing-nav">
        <a class="landing-nav-brand" href="{root_prefix}index.html">LeetCode <span>题解</span></a>
        <nav class="landing-nav-links">
            {"".join(nav_links_parts)}
        </nav>
    </header>

    <section class="hero">
        <div class="hero-inner">
            <div class="hero-eyebrow">面试高频 · 周赛实战</div>
            <h1 class="hero-title">LeetCode <span class="hero-title-accent">题解</span></h1>
            <p class="hero-subtitle">从「暴力递归」进阶到「最优解 + 面试讲清楚」</p>
            <p class="hero-meta">涵盖 Hot 100 / 面试经典 150 / 剑指 Offer 高频题，配套手绘 SVG 图解、复杂度分析与面试 Q&A</p>
            {hero_actions}
        </div>
    </section>

    <section class="stats-strip">
        {stats_html}
    </section>

    <main class="landing-main">
        <section class="landing-section" id="topics">
            <h2 class="section-title">算法专题</h2>
            <p class="section-subtitle">按算法类别沉淀的专题笔记：核心思想 + 模板 + 剪枝/去重技巧 + 例题精讲 + 课后练习。</p>
            <div class="topic-grid">
                {topic_cards_html}
            </div>
        </section>

        <section class="landing-section">
            <h2 class="section-title">更多资源</h2>
            <div class="resource-grid">
                {resource_cards_html}
            </div>
        </section>

        <section class="landing-section" id="problems">
            <h2 class="section-title">题解列表</h2>
            <p class="section-subtitle">每日一题按题号区间分组 + 周赛按场次降序，点击题目进入题解。</p>
            {random_picker_html}
            {problem_list_html}
        </section>
    </main>

    <footer class="landing-footer">
        <span>LeetCode 题解 · 由 <a href="{GITHUB_REPO_URL}">GitHub</a> 驱动 · Deployed on GitHub Pages</span>
    </footer>

    <button class="back-to-top" aria-label="Back to top">↑</button>
</body>
</html>
"""


def copy_static_assets(public_dir: Path) -> None:
    """Copy shared css/js from static/ to public/css/ and public/js/."""
    for sub in ("css", "js"):
        src = STATIC_DIR / sub
        if src.exists():
            dst = public_dir / sub
            dst.mkdir(parents=True, exist_ok=True)
            for item in src.iterdir():
                if item.is_file():
                    shutil.copy2(item, dst / item.name)


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def main() -> None:
    public_dir = REPO_ROOT / "public"
    if public_dir.exists():
        shutil.rmtree(public_dir)
    public_dir.mkdir()

    print("Copying static assets (css/js)...")
    copy_static_assets(public_dir)

    problems_dir = public_dir / "problems"
    problems_dir.mkdir(parents=True, exist_ok=True)

    images_dir = public_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    top_level_images = REPO_ROOT / "images"
    if top_level_images.exists():
        shutil.copytree(top_level_images, images_dir, dirs_exist_ok=True)

    solution_images = REPO_ROOT / "solution" / "images"
    if solution_images.exists():
        shutil.copytree(solution_images, images_dir, dirs_exist_ok=True)

    md_files = sorted([
        f for f in REPO_ROOT.rglob("*.md")
        if f.is_file()
        and not (set(f.relative_to(REPO_ROOT).parts) & EXCLUDED_PARTS)
        and f.name != "SKILL.md"
    ])

    for md_file in md_files:
        local_images = md_file.parent / "images"
        if local_images.exists() and local_images.is_dir():
            shutil.copytree(local_images, images_dir, dirs_exist_ok=True)

    slug_by_path = _compute_slugs(md_files)

    problems = []
    for md_file in md_files:
        markdown_text = md_file.read_text(encoding="utf-8")
        markdown_text = _rewrite_md_links_to_html(markdown_text, md_file, slug_by_path)

        title = _parse_title(markdown_text, filename=md_file.name)
        info = _classify(md_file)

        num_match = re.match(r"(\d+)_", md_file.stem)
        number = num_match.group(1) if num_match else _extract_problem_number(markdown_text)

        problems.append({
            "slug": slug_by_path[md_file.resolve()],
            "title": title,
            "number": number,
            "leetcode_url": _extract_leetcode_url(markdown_text),
            "category": info["category"],
            "contest": info["contest"],
            "week": info["week"],
            "day": info["day"],
            "folder": info["folder"],
            "markdown": markdown_text,
        })

    contest_groups: Dict[str, List[Dict]] = {}
    solution_groups: Dict[str, List[Dict]] = defaultdict(list)
    for p in problems:
        if p["category"] == "contest":
            contest_groups.setdefault(p["contest"], []).append(p)
        elif p["category"] == "solution":
            solution_groups[p["folder"]].append(p)

    def sort_key_numeric(name: str) -> int:
        match = re.search(r'(\d+)$', name)
        return int(match.group(1)) if match else 0

    daily_markdown = ""
    for folder in sorted(solution_groups.keys(), key=_range_start):
        label = _range_label(folder)
        group_problems = solution_groups.get(folder, [])
        group_problems.sort(key=lambda x: x["slug"])
        daily_markdown += f'<div class="leetcode-section">\n'
        daily_markdown += f'  <div class="leetcode-section-title">{label}</div>\n'
        daily_markdown += f'  <div class="leetcode-problem-list">\n'
        for p in group_problems:
            daily_markdown += (
                f'    <a class="leetcode-problem-link" href="./problems/{p["slug"]}.html">'
                f'<span class="leetcode-problem-title">{p["title"]}</span>'
                f'</a>\n'
            )
        daily_markdown += '  </div>\n'
        daily_markdown += '</div>\n\n'

    contest_markdown = ""
    for contest in sorted(contest_groups.keys(), key=sort_key_numeric, reverse=True):
        contest_markdown += f'<div class="leetcode-section">\n'
        contest_markdown += f'  <div class="leetcode-section-title">周赛 {contest}</div>\n'
        contest_markdown += f'  <div class="leetcode-problem-list">\n'
        for p in contest_groups[contest]:
            contest_markdown += (
                f'    <a class="leetcode-problem-link" href="./problems/{p["slug"]}.html">'
                f'{p["title"]}'
                f'</a>\n'
            )
        contest_markdown += '  </div>\n'
        contest_markdown += '</div>\n\n'

    picker_problems = []
    seen_slugs = set()
    for p in problems:
        if p.get("leetcode_url") and p["slug"] not in seen_slugs:
            seen_slugs.add(p["slug"])
            picker_problems.append({"title": p["title"], "url": p["leetcode_url"]})
    problems_json = json.dumps(picker_problems, ensure_ascii=False)

    random_picker_html = f"""<div class="random-pick">
  <button id="random-pick-btn" class="random-btn" data-problems='{problems_json}'>随机选一道题练习</button>
</div>

"""

    hot_href = f"./problems/{HOT_PAGE_SLUG}.html" if any(p["slug"] == HOT_PAGE_SLUG for p in problems) else None
    plan_href = "./problems/10-week-plan.html" if any(p["slug"] == "10-week-plan" for p in problems) else None

    topic_problems = [p for p in problems if p["category"] == "topics"]
    topic_cards_html = ""
    for p in topic_problems:
        icon = TOPIC_ICONS.get(p["slug"], "📘")
        topic_cards_html += (
            f'<a class="topic-card" href="./problems/{p["slug"]}.html">'
            f'<span class="topic-card-icon">{icon}</span>'
            f'<span class="topic-card-name">{p["title"]}</span>'
            f'<span class="topic-card-arrow">→</span>'
            f'</a>\n'
        )

    resource_items = []
    if hot_href:
        resource_items.append(("🔥", "高频面试题", "Hot 100 / CodeTop / 剑指 Offer 高频题汇总", hot_href))
    if plan_href:
        resource_items.append(("📅", "10 周刷题计划", "按类别组织 198 道高频题的递进式路线", plan_href))
    resource_items.append(("🧠", "AI Infra Notes", "CUDA / 推理系统 / 分布式并行学习笔记", "https://hzchenxiaobin.github.io/ai-infra-notes/"))
    resource_items.append(("💻", "GitHub 仓库", "本站全部源码与 Markdown 原文", GITHUB_REPO_URL))

    resource_cards_html = ""
    for icon, name, desc, href in resource_items:
        resource_cards_html += (
            f'<a class="resource-card" href="{href}">'
            f'<span class="resource-card-icon">{icon}</span>'
            f'<span class="resource-card-body">'
            f'<span class="resource-card-name">{name}</span>'
            f'<span class="resource-card-desc">{desc}</span>'
            f'</span>'
            f'</a>\n'
        )

    total_solutions = len([p for p in problems if p["category"] in ("solution", "contest")])
    stats = [
        (str(total_solutions), "道题解"),
        (str(len(contest_groups)), "场周赛"),
        (str(len(topic_problems)), "算法专题"),
        ("∞", "持续更新"),
    ]
    stats_html = ""
    for value, label in stats:
        stats_html += (
            f'<div class="stat-item">'
            f'<span class="stat-value">{value}</span>'
            f'<span class="stat-label">{label}</span>'
            f'</div>\n'
        )

    problem_list_html = (
        '<div class="leetcode-overview-row">\n'
        '  <div class="leetcode-col leetcode-col-daily">\n'
        f'{daily_markdown}'
        '  </div>\n'
        '  <div class="leetcode-col leetcode-col-contest">\n'
        f'{contest_markdown}'
        '  </div>\n'
        '</div>\n'
    )

    landing_html = landing_template(
        stats_html=stats_html,
        topic_cards_html=topic_cards_html,
        resource_cards_html=resource_cards_html,
        problem_list_html=problem_list_html,
        random_picker_html=random_picker_html,
        hot_href=hot_href,
        plan_href=plan_href,
        root_prefix="",
    )
    (public_dir / "index.html").write_text(landing_html, encoding="utf-8")
    print(f"Generated: {public_dir / 'index.html'}")

    for p in problems:
        problem_markdown = p["markdown"].replace("](images/", "](../images/")
        html = page_template(
            title=p["title"],
            nav_html=_build_nav(current_slug=p["slug"], problems=problems, root_prefix="../"),
            markdown=problem_markdown,
            root_prefix="../",
        )
        slug_html = f"{p['slug']}.html"
        (problems_dir / slug_html).write_text(html, encoding="utf-8")
        print(f"Generated: {problems_dir / slug_html}")

    print(f"\nWebsite built successfully in public/ ({len(problems)} problem pages)")


if __name__ == "__main__":
    main()
