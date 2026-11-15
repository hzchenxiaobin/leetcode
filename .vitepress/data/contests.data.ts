import { createContentLoader } from 'vitepress'

export interface ContestProblem {
  url: string
  /** weekly = 周赛（contest/<场次>/），biweekly = 双周赛（contest/bw<场次>/） */
  kind: 'weekly' | 'biweekly'
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
        // 周赛：/contest/<场次>/Q<n>.<题名>；双周赛：/contest/bw<场次>/Q<n>.<题名>
        const m = page.url.match(/\/contest\/(bw)?(\d+)\/Q(\d+)\.(.+)/)
        if (!m) return null
        const src = page.src ?? ''
        const h1 = src.match(/^#\s+(.+)$/m)?.[1] ?? m[4]
        const title = h1.replace(/^LeetCode\s*/i, '').replace(/\s*题解\s*$/, '').trim()
        const tags = (src.match(/\*\*标签\*\*[：:]\s*(.+)/)?.[1] ?? '').replace(/`/g, '').trim()
        const d = src.match(/\*\*难度\*\*[：:]\s*(简单|中等|困难)/)?.[1]
        const diff = d === '简单' ? 'easy' : d === '中等' ? 'medium' : d === '困难' ? 'hard' : ''
        return {
          url: page.url,
          kind: (m[1] === 'bw' ? 'biweekly' : 'weekly') as ContestProblem['kind'],
          contest: parseInt(m[2]),
          q: parseInt(m[3]),
          title,
          diff: diff as ContestProblem['diff'],
          tags
        }
      })
      .filter((p): p is ContestProblem => p !== null)
      // 周赛在前、双周赛在后；各自按场次降序，最新在前，场内 Q 号升序
      .sort((a, b) =>
        a.kind === b.kind
          ? (b.contest - a.contest || a.q - b.q)
          : a.kind === 'weekly' ? -1 : 1)
  }
})
