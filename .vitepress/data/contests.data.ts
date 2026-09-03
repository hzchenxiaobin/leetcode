import { createContentLoader } from 'vitepress'

export interface ContestProblem {
  url: string
  contest: number
  q: number
  title: string
  diff: 'easy' | 'medium' | 'hard' | ''
  tags: string
}

declare const data: ContestProblem[]
export { data }

export default createContentLoader('contest/*/*.md', {
  includeSrc: true,
  transform(raw): ContestProblem[] {
    return raw
      .map(page => {
        const m = page.url.match(/\/contest\/(\d+)\/Q(\d+)\.(.+)/)
        if (!m) return null
        const src = page.src ?? ''
        const h1 = src.match(/^#\s+(.+)$/m)?.[1] ?? m[3]
        const title = h1.replace(/^LeetCode\s*/i, '').replace(/\s*题解\s*$/, '').trim()
        const tags = (src.match(/\*\*标签\*\*[：:]\s*(.+)/)?.[1] ?? '').replace(/`/g, '').trim()
        const d = src.match(/\*\*难度\*\*[：:]\s*(简单|中等|困难)/)?.[1]
        const diff = d === '简单' ? 'easy' : d === '中等' ? 'medium' : d === '困难' ? 'hard' : ''
        return {
          url: page.url,
          contest: parseInt(m[1]),
          q: parseInt(m[2]),
          title,
          diff: diff as ContestProblem['diff'],
          tags
        }
      })
      .filter((p): p is ContestProblem => p !== null)
      .sort((a, b) => b.contest - a.contest || a.q - b.q) // 场次降序，最新在前
  }
})
