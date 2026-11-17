<script setup lang="ts">
import { computed } from 'vue'
import { withBase } from 'vitepress'
import { data } from '../data/codeforces.data'

/** 按场次分组（loader 已按场次降序、场内题号升序排好） */
const groups = computed(() => {
  const map = new Map<number, typeof data>()
  for (const p of data) {
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
</script>

<template>
  <div class="pl-wrap">
    <h1 class="pl-title">⚔️ Codeforces 题解</h1>
    <p class="pl-desc">
      从最新已结束的比赛开始倒序整理 · 共 {{ groups.length }} 场 · {{ total }} 题 ·
      <a href="https://codeforces.com/contests" target="_blank" rel="noopener noreferrer">Codeforces 赛程 →</a>
    </p>
    <div v-for="g in groups" :key="g.contest" class="pl-group">
      <h2 class="pl-contest">
        <a
          :href="`https://codeforces.com/contest/${g.contest}`"
          target="_blank"
          rel="noopener noreferrer"
        >{{ g.round }}</a>
        <span class="pl-cid">#{{ g.contest }}</span>
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
.pl-desc { color: var(--vp-c-text-2); margin: 0 0 32px; }
.pl-desc a { color: var(--vp-c-brand-1); font-weight: 600; text-decoration: none; }
.pl-desc a:hover { text-decoration: underline; }
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
