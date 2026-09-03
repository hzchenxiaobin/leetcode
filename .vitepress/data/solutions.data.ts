import { createContentLoader } from 'vitepress'

export interface Problem {
  url: string
  range: string
  num: number
  title: string
  diff: 'easy' | 'medium' | 'hard' | ''
  tags: string
}

declare const data: Problem[]
export { data }

export default createContentLoader('solution/*/*.md', {
  includeSrc: true,
  transform(raw): Problem[] {
    return raw
      .map(page => {
        const m = page.url.match(/\/solution\/(\d{4}-\d{4})\/(\d+)_(.+)/)
        if (!m) return null
        const src = page.src ?? ''
        const h1 = src.match(/^#\s+(.+)$/m)?.[1] ?? m[3]
        const title = h1.replace(/^LeetCode\s*/i, '').replace(/\s*题解\s*$/, '').trim()
        const tags = (src.match(/\*\*标签\*\*[：:]\s*(.+)/)?.[1] ?? '').replace(/`/g, '').trim()
        const d = src.match(/\*\*难度\*\*[：:]\s*(简单|中等|困难)/)?.[1]
        const diff = d === '简单' ? 'easy' : d === '中等' ? 'medium' : d === '困难' ? 'hard' : ''
        return {
          url: page.url,
          range: m[1],
          num: parseInt(m[2]),
          title,
          diff: diff as Problem['diff'],
          tags
        }
      })
      .filter((p): p is Problem => p !== null)
      .sort((a, b) => a.num - b.num)
  }
})
