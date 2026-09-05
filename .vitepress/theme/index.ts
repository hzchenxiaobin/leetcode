import DefaultTheme from 'vitepress/theme'
import { h, onMounted, watch, nextTick } from 'vue'
import { useRoute } from 'vitepress'
import mediumZoom from 'medium-zoom'
import SolutionList from './SolutionList.vue'
import ContestList from './ContestList.vue'
import BackLink from './BackLink.vue'
import 'katex/dist/katex.min.css'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('SolutionList', SolutionList)
    app.component('ContestList', ContestList)
  },
  Layout() {
    return h(DefaultTheme.Layout, null, {
      'doc-before': () => h(BackLink)
    })
  },
  setup() {
    const route = useRoute()
    let zoom: ReturnType<typeof mediumZoom> | null = null
    const initZoom = () => {
      zoom?.detach()
      zoom = mediumZoom('.vp-doc img', {
        background: 'rgba(0, 0, 0, 0.75)',
        margin: 24
      })
    }
    onMounted(() => {
      initZoom()
      // Open every link in a new tab. VitePress intercepts clicks on internal
      // links for SPA routing, so we capture the click first, stop the router,
      // and open the URL ourselves. Same-page anchors keep default behavior.
      document.addEventListener(
        'click',
        (e) => {
          if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return
          const link = (e.target as HTMLElement).closest?.('a')
          if (!link) return
          const rawHref = link.getAttribute('href') || ''
          if (!rawHref || rawHref.startsWith('#')) return
          e.preventDefault()
          e.stopImmediatePropagation()
          window.open(link.href, '_blank', 'noopener,noreferrer')
        },
        true
      )
    })
    watch(() => route.path, () => nextTick(initZoom))
  }
}
