import { createContentLoader } from 'vitepress'

export interface CfProblem {
  url: string
  contest: number
  index: string
  title: string
  /** 题解里写的难度描述（rating 或 "未评级（500 分）"） */
  diff: string
  tags: string
  /** 比赛名称，如 "Codeforces Round 1135 (Div. 2)" */
  round: string
}

declare const data: CfProblem[]
export { data }

export default createContentLoader('codeforces/contests/*/*/*.md', {
  includeSrc: true,
  transform(raw): CfProblem[] {
    return raw
      .map(page => {
        // 路径形如 /codeforces/contests/2201-2300/2285/A_合数排列
        const m = page.url.match(/\/codeforces\/contests\/[\d-]+\/(\d+)\/([A-Za-z0-9]+)_(.+)/)
        if (!m) return null
        const src = page.src ?? ''
        const h1 = src.match(/^#\s+(.+)$/m)?.[1] ?? m[3]
        const title = h1.replace(/^Codeforces\s*/i, '').replace(/\s*题解\s*$/, '').trim()
        const tags = (src.match(/\*\*标签\*\*[：:]\s*(.+)/)?.[1] ?? '').replace(/`/g, '').trim()
        const diff = (src.match(/\*\*难度\*\*[：:]\s*(.+)/)?.[1] ?? '').replace(/`/g, '').trim()
        // 新模板写「**比赛来源**」，早期题解写「**来源**」，两种都要认
        const source = (src.match(/\*\*(?:比赛)?来源\*\*[：:]\s*(.+)/)?.[1] ?? '')
        const round = source.split('·')[0].trim()
        return {
          url: page.url,
          contest: parseInt(m[1]),
          index: m[2].toUpperCase(),
          title,
          diff,
          tags,
          round
        }
      })
      .filter((p): p is CfProblem => p !== null)
      // 场次降序（新的在前），场内按题号 A, B, C, … G1, G2 升序
      .sort((a, b) =>
        b.contest - a.contest ||
        a.index.localeCompare(b.index, 'en', { numeric: true }))
  }
})
