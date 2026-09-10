// 图片灯箱：点击正文图片后全屏预览，支持滚轮/按钮缩放、拖动平移、Esc/点击关闭。
// 点击事件委托到 document，SPA 路由切换后无需重新绑定。

const MIN_SCALE = 0.5
const MAX_SCALE = 5
const ZOOM_STEP = 0.15

let lightbox: HTMLDivElement | null = null
let lightboxImg: HTMLImageElement | null = null
let captionEl: HTMLElement | null = null

let scale = 1
let tx = 0
let ty = 0

let isDragging = false
let hasDragged = false
let dragStartX = 0
let dragStartY = 0
let dragStartTx = 0
let dragStartTy = 0

const isOpen = () => lightbox?.classList.contains('active') ?? false

function updateTransform() {
  if (!lightboxImg) return
  lightboxImg.style.transform =
    `translate(calc(-50% + ${tx}px), calc(-50% + ${ty}px)) scale(${scale})`
}

function updateScale(next: number) {
  scale = Math.max(MIN_SCALE, Math.min(MAX_SCALE, next))
  updateTransform()
}

function resetView() {
  scale = 1
  tx = 0
  ty = 0
  if (lightboxImg) lightboxImg.style.transform = ''
}

function clampPan() {
  if (!lightbox || !lightboxImg) return
  const rect = lightboxImg.getBoundingClientRect()
  const maxX = Math.max(0, rect.width / 2 + lightbox.clientWidth / 2)
  const maxY = Math.max(0, rect.height / 2 + lightbox.clientHeight / 2)
  tx = Math.max(-maxX, Math.min(maxX, tx))
  ty = Math.max(-maxY, Math.min(maxY, ty))
}

function open(img: HTMLImageElement) {
  if (!lightbox || !lightboxImg || !captionEl) return
  resetView()
  lightboxImg.src = img.currentSrc || img.src
  lightboxImg.alt = img.alt || ''
  if (img.alt) {
    captionEl.textContent = img.alt
    captionEl.style.display = 'block'
  } else {
    captionEl.style.display = 'none'
  }
  lightbox.classList.add('active')
  document.body.style.overflow = 'hidden'
}

function close() {
  if (!lightbox) return
  lightbox.classList.remove('active')
  document.body.style.overflow = ''
  resetView()
}

function startDrag(clientX: number, clientY: number) {
  isDragging = true
  hasDragged = false
  dragStartX = clientX
  dragStartY = clientY
  dragStartTx = tx
  dragStartTy = ty
  lightboxImg?.classList.add('dragging')
}

function moveDrag(clientX: number, clientY: number) {
  if (!isDragging) return
  const dx = clientX - dragStartX
  const dy = clientY - dragStartY
  if (Math.abs(dx) > 2 || Math.abs(dy) > 2) hasDragged = true
  tx = dragStartTx + dx
  ty = dragStartTy + dy
  clampPan()
  updateTransform()
}

function endDrag() {
  if (!isDragging) return
  isDragging = false
  lightboxImg?.classList.remove('dragging')
  setTimeout(() => {
    hasDragged = false
  }, 50)
}

export function initLightbox() {
  if (lightbox) return

  lightbox = document.createElement('div')
  lightbox.className = 'image-lightbox'
  lightbox.setAttribute('role', 'dialog')
  lightbox.setAttribute('aria-modal', 'true')
  lightbox.setAttribute('aria-label', '图片预览')
  lightbox.innerHTML = `
    <button class="lightbox-close" aria-label="关闭预览">&times;</button>
    <div class="lightbox-controls">
      <button class="lightbox-btn" data-action="zoom-out" aria-label="缩小">&minus;</button>
      <button class="lightbox-btn" data-action="reset" aria-label="重置缩放">重置</button>
      <button class="lightbox-btn" data-action="zoom-in" aria-label="放大">+</button>
    </div>
    <img src="" alt="">
    <div class="lightbox-caption"></div>
    <div class="lightbox-zoom-hint">滚轮缩放 / 拖动平移 / 点击关闭</div>
  `
  document.body.appendChild(lightbox)
  lightboxImg = lightbox.querySelector('img')
  captionEl = lightbox.querySelector('.lightbox-caption')

  lightbox.querySelector('.lightbox-close')!.addEventListener('click', close)

  lightbox.querySelector('.lightbox-controls')!.addEventListener('click', e => {
    e.stopPropagation()
    const action = (e.target as HTMLElement).closest('button')?.dataset.action
    if (action === 'zoom-in') updateScale(scale + ZOOM_STEP)
    else if (action === 'zoom-out') updateScale(scale - ZOOM_STEP)
    else if (action === 'reset') resetView()
  })

  document.addEventListener('click', e => {
    const img = (e.target as Element).closest?.('.vp-doc img') as HTMLImageElement | null
    if (!img || isOpen()) return
    e.preventDefault()
    open(img)
  })

  lightbox.addEventListener('click', e => {
    if (hasDragged) return
    if (e.target === lightbox || e.target === lightboxImg) close()
  })

  lightboxImg!.addEventListener('mousedown', e => {
    if (!isOpen()) return
    e.preventDefault()
    startDrag(e.clientX, e.clientY)
  })
  document.addEventListener('mousemove', e => moveDrag(e.clientX, e.clientY))
  document.addEventListener('mouseup', endDrag)

  lightboxImg!.addEventListener(
    'touchstart',
    e => {
      if (!isOpen() || e.touches.length !== 1) return
      startDrag(e.touches[0].clientX, e.touches[0].clientY)
    },
    { passive: false }
  )
  document.addEventListener(
    'touchmove',
    e => {
      if (!isDragging || e.touches.length !== 1) return
      e.preventDefault()
      moveDrag(e.touches[0].clientX, e.touches[0].clientY)
    },
    { passive: false }
  )
  document.addEventListener('touchend', endDrag)

  lightbox.addEventListener(
    'wheel',
    e => {
      if (!isOpen()) return
      e.preventDefault()
      updateScale(scale + (e.deltaY > 0 ? -ZOOM_STEP : ZOOM_STEP))
    },
    { passive: false }
  )

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && isOpen()) close()
  })
}
