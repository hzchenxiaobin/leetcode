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
    onMounted(initZoom)
    watch(() => route.path, () => nextTick(initZoom))
  }
}
