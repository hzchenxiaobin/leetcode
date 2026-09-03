import { defineConfig } from 'vitepress'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import katex from '@traptitech/markdown-it-katex'

const root = path.dirname(fileURLToPath(import.meta.url))

/** 去掉 H1 的「LeetCode」前缀与「题解」后缀，得到纯标题 */
function cleanTitle(h1: string) {
  return h1.replace(/^LeetCode\s*/i, '').replace(/\s*题解\s*$/, '').trim()
}

/** 从 solution/<区间>/ 目录读取题目列表：题号排序，标题取自每篇 H1 */
function loadSolutions() {
  const base = path.resolve(root, '../solution')
  if (!fs.existsSync(base)) return []
  return fs.readdirSync(base)
    .filter(d => /^\d{4}-\d{4}$/.test(d))
    .flatMap(d => {
      const abs = path.join(base, d)
      return fs.readdirSync(abs)
        .filter(f => f.endsWith('.md'))
        .map(f => {
          const num = f.match(/^(\d+)_/)?.[1] ?? ''
          const h1 = fs.readFileSync(path.join(abs, f), 'utf-8').match(/^#\s+(.+)$/m)?.[1] ?? f
          return {
            num: parseInt(num) || 0,
            text: `#${num} ${cleanTitle(h1)}`,
            link: `/solution/${d}/${f.replace(/\.md$/, '')}`
          }
        })
    })
    .sort((a, b) => a.num - b.num)
}

/** 从 contest/<场次>/ 目录读取周赛题目列表：场次升序、场内 Q 号升序 */
function loadContests() {
  const base = path.resolve(root, '../contest')
  if (!fs.existsSync(base)) return []
  return fs.readdirSync(base)
    .filter(d => /^\d+$/.test(d))
    .flatMap(d => {
      const abs = path.join(base, d)
      return fs.readdirSync(abs)
        .filter(f => f.endsWith('.md'))
        .map(f => {
          const q = f.match(/^Q(\d+)/)?.[1] ?? ''
          const h1 = fs.readFileSync(path.join(abs, f), 'utf-8').match(/^#\s+(.+)$/m)?.[1] ?? f
          return {
            contest: parseInt(d),
            q: parseInt(q) || 0,
            text: `第${d}场 Q${q} ${cleanTitle(h1)}`,
            link: `/contest/${d}/${f.replace(/\.md$/, '')}`
          }
        })
    })
    .sort((a, b) => a.contest - b.contest || a.q - b.q)
}

// 全局题目顺序（每日一题按题号；周赛按场次 → Q 号），用于生成 上一题/下一题
const solutionOrder = loadSolutions()
const contestOrder = loadContests()

export default defineConfig({
  title: 'LeetCode 题解',
  description: 'LeetCode 题解 · 面试高频 · 周赛实战',
  lang: 'zh-CN',
  base: '/leetcode/',
  // 旧版 Python 生成器与文档不纳入站点构建（保留在仓库中作存档）
  srcExclude: [
    'README.md', '**/SKILL.md', '**/INDEX.md',
    'build/**', 'static/**', 'public/**', 'dist/**'
  ],
  outDir: './dist',
  ignoreDeadLinks: true, // 正文里有指向仓库内非页面文件的相对链接
  lastUpdated: false,
  // 4100+ 页 SSR 渲染默认 64 并发会把 Node 内存打爆，限制并发
  buildConcurrency: 8,

  vite: {
    plugins: [
      {
        // 部分题解引用了从未生成的插图（旧站上是 404 占位），
        // 这里把缺失的图片解析为透明占位图，避免 Rollup 因无法解析资源而中断构建
        name: 'tolerate-missing-images',
        enforce: 'pre',
        resolveId(id, importer) {
          if (!importer || !/\.(svg|png|jpe?g|gif|webp)$/i.test(id)) return null
          let abs: string | null = null
          if (id.startsWith('/')) abs = path.resolve(root, '..' + id)
          else if (id.startsWith('./') || id.startsWith('../'))
            abs = path.resolve(path.dirname(importer.split('?')[0]), id)
          if (abs && !fs.existsSync(abs)) return '\0missing-image'
          return null
        },
        load(id) {
          if (id === '\0missing-image')
            return 'export default "data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'1\' height=\'1\'/%3E"'
        }
      }
    ]
  },

  head: [
    ['link', { rel: 'icon', href: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="0.9em" font-size="90">📝</text></svg>' }]
  ],

  markdown: {
    config: (md) => {
      // output: 'html'：不输出 MathML——annotation 里的 TeX 源码（如 \mathrel{{+}{=}}）
      // 含 {{，会被 Vue 误认为插值语法导致编译失败
      md.use(katex, { output: 'html', strict: 'ignore' })
      // KaTeX 可见输出里也可能含字面花括号（如集合套集合 $\{\{1\},…\}$ 渲染为 <span>{{</span>），
      // 转义为 HTML 实体，避免被 Vue 当作插值语法
      for (const name of ['math_inline', 'math_block']) {
        const orig = md.renderer.rules[name]
        if (orig) {
          md.renderer.rules[name] = (...args) =>
            orig(...args).replace(/\{/g, '&#123;').replace(/\}/g, '&#125;')
        }
      }
      // VitePress 自带的行尾 {…} 属性语法会把正文里的集合记号（如 {i love you:5, …}、{0, 1, 2}）
      // 误解析成 HTML 属性，禁用之（本站内容不使用该语法）
      md.core.ruler.disable('curly_attributes', true)
      // 周赛题解中的 images/xxx.svg 是仓库根 images/ 目录的引用，改写为根绝对路径
      const defaultImage = md.renderer.rules.image!
      md.renderer.rules.image = (tokens, idx, options, env, self) => {
        const src = tokens[idx].attrGet('src')
        if (src && src.startsWith('images/')) tokens[idx].attrSet('src', '/' + src)
        return defaultImage(tokens, idx, options, env, self)
      }
      // 题解里的 `{{3,"Fizz"},…}`（C++ 初始化列表）会被 Vue 误认为插值语法：
      // 行内代码加 v-pre，正文中的 {{ 拆成实体转义
      md.core.ruler.after('inline', 'escape-mustache', (state) => {
        for (const tok of state.tokens) {
          if (tok.type !== 'inline' || !tok.children) continue
          const children: typeof tok.children = []
          for (const child of tok.children) {
            if (child.type === 'code_inline') {
              if (child.content.includes('{{')) child.attrPush(['v-pre', ''])
              children.push(child)
            } else if (child.type === 'text' && child.content.includes('{{')) {
              child.content.split('{{').forEach((part, i) => {
                if (i > 0) {
                  const t = new state.Token('html_inline', '', 0)
                  t.content = '&#123;&#123;'
                  children.push(t)
                }
                if (part) {
                  const t = new state.Token('text', '', 0)
                  t.content = part
                  children.push(t)
                }
              })
            } else {
              children.push(child)
            }
          }
          tok.children = children
        }
      })
    },
    lineNumbers: true
  },

  // 无侧边栏：题解页为 正文 + 右侧本页目录；按题号顺序自动推导 上一题/下一题
  transformPageData(pageData) {
    for (const order of [solutionOrder, contestOrder]) {
      const idx = order.findIndex(o => pageData.relativePath === o.link.slice(1) + '.md')
      if (idx >= 0) {
        const prev = order[idx - 1]
        const next = order[idx + 1]
        pageData.frontmatter.prev = prev ? { text: prev.text, link: prev.link } : false
        pageData.frontmatter.next = next ? { text: next.text, link: next.link } : false
        return
      }
    }
  },

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '题解', link: '/solutions.html' },
      { text: '周赛', link: '/contests.html' },
      { text: '专题', link: '/topics.html' },
      { text: 'GitHub', link: 'https://github.com/hzchenxiaobin/leetcode' }
    ],

    sidebar: false,

    outline: { level: [2, 3], label: '本页目录' },

    search: {
      provider: 'local',
      options: {
        // 4100+ 页全量索引：剔除代码块，显著降低索引体积与构建内存
        _render(src: string, env: any, md: any) {
          const html: string = md.render(src, env)
          if (env.frontmatter?.search === false) return ''
          return html
            .replace(/<pre[\s\S]*?<\/pre>/g, ' ')
            .replace(/<code>[\s\S]*?<\/code>/g, ' ')
        },
        miniSearch: {
          options: {
            // 默认分词对中文整句不切分，会产生海量超长唯一词导致 OOM；
            // 中文按二元组（bigram）切分，英文/数字整词索引
            tokenize: (str: string): string[] => {
              const tokens: string[] = []
              for (const word of str.toLowerCase().split(/[^\p{L}\p{N}]+/u)) {
                if (!word) continue
                if (/^[\x00-\x7f]+$/.test(word)) { tokens.push(word); continue }
                const chars = [...word]
                if (chars.length === 1) { tokens.push(chars[0]); continue }
                for (let i = 0; i < chars.length - 1; i++) tokens.push(chars[i] + chars[i + 1])
              }
              return tokens
            }
          }
        },
        translations: {
          button: { buttonText: '搜索', buttonAriaLabel: '搜索' },
          modal: {
            displayDetails: '显示详细列表',
            noResultsText: '无法找到相关结果',
            resetButtonTitle: '清除查询条件',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' }
          }
        }
      }
    },

    docFooter: { prev: '上一题', next: '下一题' },
    darkModeSwitchLabel: '外观',
    sidebarMenuLabel: '菜单',
    returnToTopLabel: '回到顶部'
  }
})
