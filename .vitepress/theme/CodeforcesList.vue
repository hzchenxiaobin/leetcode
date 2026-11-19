<script setup lang="ts">
import { computed, ref } from 'vue'
import { withBase } from 'vitepress'
import { data } from '../data/codeforces.data'

/** 从「难度」文本里取 rating：'1000' / '未评级（500 分）' / '未评级' */
function ratingOf(p: { diff: string }): number | null {
  const m = p.diff.match(/\d{3,4}/)
  if (!m) return null
  const v = parseInt(m[0], 10)
  return v >= 500 && v <= 4000 ? v : null
}

/** 标签文本形如「构造、数学、贪心」或「dp, graphs」 */
function tagList(p: { tags: string }): string[] {
  return p.tags
    .split(/[、,，/]+/)
    .map(s => s.trim())
    .filter(Boolean)
}

const q = ref('')
const level = ref('')
const tag = ref('')

const levels = [
  { value: '', label: '全部难度' },
  { value: '800-1199', label: '800–1199' },
  { value: '1200-1599', label: '1200–1599' },
  { value: '1600-1999', label: '1600–1999' },
  { value: '2000-2399', label: '2000–2399' },
  { value: '2400-2799', label: '2400–2799' },
  { value: '2800-4000', label: '2800+' },
  { value: 'none', label: '未评级' }
]

/** 全部标签，按出现次数降序 */
const allTags = computed(() => {
  const count = new Map<string, number>()
  for (const p of data) for (const t of tagList(p)) count.set(t, (count.get(t) ?? 0) + 1)
  return [...count.entries()].sort((a, b) => b[1] - a[1]).map(([t, n]) => ({ tag: t, n }))
})

const filtered = computed(() => {
  const text = q.value.trim().toLowerCase()
  return data.filter(p => {
    if (text) {
      const hay = `cf${p.contest} ${p.contest} ${p.index} ${p.title} ${p.round} ${p.tags}`.toLowerCase()
      // 支持「4a」「2285A」「watermelon」这类混合查询
      if (!hay.includes(text) && !`${p.contest}${p.index}`.toLowerCase().includes(text)) return false
    }
    if (level.value) {
      const r = ratingOf(p)
      if (level.value === 'none') {
        if (r !== null) return false
      } else {
        const [lo, hi] = level.value.split('-').map(Number)
        if (r === null || r < lo || r > hi) return false
      }
    }
    if (tag.value && !tagList(p).includes(tag.value)) return false
    return true
  })
})

const filtering = computed(() => !!q.value.trim() || !!level.value || !!tag.value)

/** 按场次分组（loader 已按场次降序、场内题号升序排好） */
const groups = computed(() => {
  const map = new Map<number, typeof data>()
  for (const p of filtered.value) {
    const list = map.get(p.contest) ?? []
    list.push(p)
    map.set(p.contest, list)
  }
  return [...map.entries()].map(([contest, list]) => ({
    contest,
    round: list[0]?.round || `Codeforces Contest ${contest}`,
    list
  }))
})

const total = computed(() => data.length)
function reset() {
  q.value = ''
  level.value = ''
  tag.value = ''
}
</script>

<template>
  <div class="pl-wrap">
    <h1 class="pl-title">⚔️ Codeforces 题解</h1>
    <p class="pl-desc">
      从最新已结束的比赛开始倒序整理 · 共 {{ groups.length }} 场 · {{ filtered.length }} / {{ total }} 题 ·
      <a href="https://codeforces.com/contests" target="_blank" rel="noopener noreferrer">Codeforces 赛程 →</a>
    </p>

    <div class="pl-filter">
      <input
        v-model="q"
        class="pl-input"
        type="search"
        placeholder="搜场次 / 题号 / 标题 / 标签，如 2285A、最短路、贪心"
        aria-label="搜索题解"
      />
      <select v-model="level" class="pl-select" aria-label="难度">
        <option v-for="l in levels" :key="l.value" :value="l.value">{{ l.label }}</option>
      </select>
      <select v-model="tag" class="pl-select" aria-label="标签">
        <option value="">全部标签</option>
        <option v-for="t in allTags" :key="t.tag" :value="t.tag">{{ t.tag }}（{{ t.n }}）</option>
      </select>
      <button v-if="filtering" class="pl-reset" type="button" @click="reset">清除</button>
    </div>

    <p v-if="filtering && !filtered.length" class="pl-empty">没有匹配的题解，换个关键词试试。</p>

    <div v-for="g in groups" :key="g.contest" class="pl-group">
      <h2 class="pl-contest">
        <a
          :href="`https://codeforces.com/contest/${g.contest}`"
          target="_blank"
          rel="noopener noreferrer"
        >{{ g.round }}</a>
        <span class="pl-cid">#{{ g.contest }}</span>
        <span class="pl-cid">{{ g.list.length }} 题</span>
      </h2>
      <div class="pl-list">
        <a v-for="p in g.list" :key="p.url" :href="withBase(p.url)" class="pl-card">
          <span class="pl-num">{{ p.index }}</span>
          <span class="pl-body">
            <span class="pl-name">{{ p.title }}</span>
            <span v-if="p.tags" class="pl-tags">{{ p.tags }}</span>
          </span>
          <span v-if="p.diff" class="pl-diff">{{ p.diff }}</span>
          <span class="pl-arrow">→</span>
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pl-wrap { max-width: 1024px; margin: 0 auto; padding: 48px 24px 64px; }
.pl-title { font-size: 2rem; font-weight: 700; margin: 0 0 8px; color: var(--vp-c-text-1); }
.pl-desc { color: var(--vp-c-text-2); margin: 0 0 24px; }
.pl-desc a { color: var(--vp-c-brand-1); font-weight: 600; text-decoration: none; }
.pl-desc a:hover { text-decoration: underline; }
.pl-filter {
  display: flex; flex-wrap: wrap; gap: 10px; align-items: center;
  margin: 0 0 28px;
}
.pl-input, .pl-select {
  font-size: .9rem; color: var(--vp-c-text-1);
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 8px 12px;
  outline: none;
  transition: border-color .2s;
}
.pl-input { flex: 1 1 280px; min-width: 200px; }
.pl-input:focus, .pl-select:focus { border-color: var(--vp-c-brand-1); }
.pl-reset {
  font-size: .85rem; color: var(--vp-c-text-2); cursor: pointer;
  background: transparent; border: 1px solid var(--vp-c-divider);
  border-radius: 8px; padding: 8px 12px;
}
.pl-reset:hover { color: var(--vp-c-brand-1); border-color: var(--vp-c-brand-1); }
.pl-empty { color: var(--vp-c-text-2); margin: 0 0 24px; }
.pl-group { margin-bottom: 32px; }
.pl-contest {
  font-size: 1.2rem; font-weight: 700; color: var(--vp-c-text-1);
  margin: 0 0 12px; padding-top: 0; border-top: none;
  display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap;
}
.pl-contest a { color: var(--vp-c-text-1); text-decoration: none; }
.pl-contest a:hover { color: var(--vp-c-brand-1); text-decoration: underline; }
.pl-cid { font-size: .85rem; font-weight: 500; color: var(--vp-c-text-3); }
.pl-list { display: flex; flex-direction: column; gap: 10px; }
.pl-card {
  display: flex; align-items: center; gap: 16px;
  padding: 14px 20px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  text-decoration: none;
  transition: border-color .2s, background-color .2s, transform .15s;
}
.pl-card:hover {
  border-color: var(--vp-c-brand-1);
  background-color: var(--vp-c-bg-soft);
  transform: translateX(4px);
}
.pl-num {
  flex-shrink: 0;
  font-family: var(--vp-font-family-mono);
  font-size: .95rem; font-weight: 700;
  color: var(--vp-c-brand-1);
  min-width: 32px;
}
.pl-body { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.pl-name { font-weight: 600; color: var(--vp-c-text-1); }
.pl-tags {
  font-size: .8rem; color: var(--vp-c-text-3);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.pl-diff {
  margin-left: auto; flex-shrink: 0;
  font-size: .78rem; color: var(--vp-c-text-2);
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  padding: 2px 10px;
}
.pl-arrow { color: var(--vp-c-text-3); transition: color .2s; }
.pl-card:hover .pl-arrow { color: var(--vp-c-brand-1); }
</style>
