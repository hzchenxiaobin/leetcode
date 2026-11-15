<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, withBase } from 'vitepress'

const route = useRoute()
const target = computed(() => {
  // 双周赛页（/contest/bw…）返回双周赛列表，周赛页（/contest/<数字>…）返回周赛列表
  if (/^\/contest\/bw/.test(route.path))
    return { label: '双周赛', link: '/biweekly.html' }
  const targets: Record<string, { label: string; link: string }> = {
    solution: { label: '题解', link: '/solutions.html' },
    contest: { label: '周赛', link: '/contests.html' },
    topics: { label: '专题', link: '/topics.html' }
  }
  return targets[route.path.match(/^\/(solution|contest|topics)\//)?.[1] ?? '']
})
</script>

<template>
  <nav v-if="target" class="back-nav">
    <a :href="withBase(target.link)">← 返回 {{ target.label }} 列表</a>
  </nav>
</template>

<style scoped>
.back-nav { margin-bottom: 20px; }
.back-nav a {
  font-size: .88rem;
  color: var(--vp-c-text-2);
  text-decoration: none;
  transition: color .2s;
}
.back-nav a:hover { color: var(--vp-c-brand-1); }
</style>
