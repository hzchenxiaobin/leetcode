document.addEventListener('DOMContentLoaded', function() {
    // Scroll the active day pill into view inside the top nav (mobile)
    const activePill = document.querySelector('.landing-nav-pills .day-pill-active');
    if (activePill) {
        activePill.scrollIntoView({ inline: 'center', block: 'nearest' });
    }

    // Navigation drawer (opened from the top-bar menu button)
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const navOverlay = document.querySelector('.nav-overlay');

    function closeDrawer() {
        sidebar.classList.remove('open');
        if (navOverlay) navOverlay.classList.remove('visible');
    }

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            const willOpen = !sidebar.classList.contains('open');
            sidebar.classList.toggle('open');
            if (navOverlay) navOverlay.classList.toggle('visible', willOpen);
            if (willOpen) {
                // Bring the active page link into view inside the drawer
                const active = sidebar.querySelector('.nav-link.active');
                if (active) {
                    active.scrollIntoView({ block: 'center' });
                }
            }
        });

        if (navOverlay) {
            navOverlay.addEventListener('click', closeDrawer);
        }

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && sidebar.classList.contains('open')) {
                closeDrawer();
            }
        });

        // Close drawer after navigating
        sidebar.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', closeDrawer);
        });
    }

    // Right-hand table of contents
    initToc();

    // Accordion navigation in sidebar
    function toggleAccordionItem(item) {
        if (!item) return;
        const willExpand = !item.classList.contains('is-expanded');
        item.classList.toggle('is-expanded');
        const isExpanded = item.classList.contains('is-expanded');
        const button = item.querySelector('.nav-accordion-toggle');
        if (button) {
            button.setAttribute('aria-expanded', isExpanded ? 'true' : 'false');
        }
        // Animate max-height with real measurements so long lists are never
        // clipped by a fixed cap. After the expand transition finishes, the
        // inline style is cleared and the CSS `max-height: none` rule applies.
        const content = item.querySelector(':scope > .nav-accordion-content');
        if (content) {
            if (isExpanded) {
                content.style.maxHeight = content.scrollHeight + 'px';
                content.addEventListener('transitionend', function handler(e) {
                    if (e.propertyName !== 'max-height') return;
                    content.removeEventListener('transitionend', handler);
                    if (item.classList.contains('is-expanded')) {
                        content.style.maxHeight = '';
                    }
                });
            } else {
                content.style.maxHeight = content.scrollHeight + 'px';
                void content.offsetHeight; // force reflow so the collapse animates
                content.style.maxHeight = '0px';
            }
        }
        // When manually expanding a level, collapse its descendants so that
        // each level requires its own click to expand.
        if (willExpand) {
            item.querySelectorAll('.nav-accordion-item.is-expanded').forEach(child => {
                child.classList.remove('is-expanded');
                const childButton = child.querySelector('.nav-accordion-toggle');
                if (childButton) {
                    childButton.setAttribute('aria-expanded', 'false');
                }
                const childContent = child.querySelector(':scope > .nav-accordion-content');
                if (childContent) {
                    childContent.style.maxHeight = '';
                }
            });
        }
    }

    document.querySelectorAll('.nav-accordion-toggle').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleAccordionItem(button.closest('.nav-accordion-item'));
        });
    });

    // Clicking a week header toggles the accordion; week links don't navigate.
    document.querySelectorAll('.nav-accordion-header').forEach(header => {
        header.addEventListener('click', function(e) {
            const link = e.target.closest('.week-link');
            if (link) {
                e.preventDefault();
                e.stopPropagation();
            }
            // Don't toggle if the click was on a day-link inside the header (future-proofing)
            if (e.target.closest('.day-link')) {
                return;
            }
            toggleAccordionItem(header.closest('.nav-accordion-item'));
            // Prevent nested accordion clicks from toggling parent accordions
            e.stopPropagation();
        });
    });

    // Add language-label header + copy button to code blocks
    const CODE_LANG_LABELS = {
        cpp: 'C++', c: 'C', python: 'Python', py: 'Python', text: 'text',
        sql: 'SQL', bash: 'Bash', shell: 'Shell', javascript: 'JavaScript',
        js: 'JavaScript', typescript: 'TypeScript', ts: 'TypeScript',
        java: 'Java', xml: 'XML', json: 'JSON', go: 'Go', rust: 'Rust',
    };
    document.querySelectorAll('.content pre').forEach(pre => {
        const wrapper = document.createElement('div');
        wrapper.className = 'code-block-wrapper';
        pre.parentNode.insertBefore(wrapper, pre);

        const code = pre.querySelector('code');
        const classNames = ((code && code.className) || '') + ' ' + (pre.className || '');
        const langMatch = classNames.match(/language-([a-z+-]+)/i);
        const langKey = langMatch ? langMatch[1].toLowerCase() : '';
        const langLabel = CODE_LANG_LABELS[langKey] || langKey || 'code';

        const header = document.createElement('div');
        header.className = 'code-header';
        const langSpan = document.createElement('span');
        langSpan.className = 'code-lang';
        langSpan.textContent = langLabel;
        header.appendChild(langSpan);

        const button = document.createElement('button');
        button.className = 'copy-button';
        button.textContent = 'Copy';
        button.addEventListener('click', async function() {
            const text = code ? code.textContent : pre.textContent;
            try {
                await navigator.clipboard.writeText(text);
                button.textContent = 'Copied!';
                button.classList.add('copied');
                setTimeout(() => {
                    button.textContent = 'Copy';
                    button.classList.remove('copied');
                }, 2000);
            } catch (err) {
                button.textContent = 'Failed';
                setTimeout(() => {
                    button.textContent = 'Copy';
                }, 2000);
            }
        });
        header.appendChild(button);

        wrapper.appendChild(header);
        wrapper.appendChild(pre);
    });

    // Back to top button
    const backToTop = document.querySelector('.back-to-top');
    if (backToTop) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        });

        backToTop.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Problem list: collapsible groups + live search + state persistence
    initProblemListControls();

    // Random LeetGPU problem picker on overview page
    const randomPickBtn = document.getElementById('random-pick-btn');
    if (randomPickBtn) {
        randomPickBtn.addEventListener('click', function() {
            try {
                const problems = JSON.parse(randomPickBtn.dataset.problems || '[]');
                if (!problems.length) return;
                const p = problems[Math.floor(Math.random() * problems.length)];
                if (p.url) {
                    window.open(p.url, '_blank', 'noopener,noreferrer');
                } else if (p.slug) {
                    window.open('https://leetgpu.com/challenges/' + encodeURIComponent(p.slug), '_blank',
                                'noopener,noreferrer');
                }
            } catch (e) {
                // Ignore malformed data attribute
            }
        });
    }

    // Image lightbox zoom
    initImageLightbox();

    // Enhance interview Q&A section into styled cards
    enhanceInterviewQA();

    // Open external links in new tab; on non-landing pages, open all non-sidebar
    // links in new tab (existing behavior). On the landing page, only external
    // links get target="_blank" so internal navigation stays in-tab.
    document.querySelectorAll('a').forEach(link => {
        if (link.closest('.sidebar') || link.closest('.top-nav')) {
            return;
        }
        if (document.body.classList.contains('landing')) {
            const href = link.getAttribute('href') || '';
            if (href.startsWith('http://') || href.startsWith('https://')) {
                try {
                    if (new URL(href).origin !== window.location.origin) {
                        link.setAttribute('target', '_blank');
                        link.setAttribute('rel', 'noopener noreferrer');
                    }
                } catch (e) {}
            }
        } else {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });
});

function initProblemListControls() {
    const overview = document.querySelector('.leetcode-overview-row');
    if (!overview) return;

    const sections = Array.from(overview.querySelectorAll('details.leetcode-section'));
    const links = Array.from(overview.querySelectorAll('.leetcode-problem-link'));
    const searchInput = document.getElementById('problem-search');
    const countEl = document.getElementById('problem-search-count');
    const emptyEl = document.getElementById('problem-list-empty');
    const expandBtn = document.getElementById('expand-all-btn');
    const collapseBtn = document.getElementById('collapse-all-btn');
    const STORAGE_KEY = 'leetcode-open-sections';

    links.forEach(link => {
        link._searchText = link.textContent.toLowerCase();
    });

    // Restore previously expanded groups (falls back to the server-rendered
    // default: only the newest contest is open).
    let savedIds = null;
    try {
        savedIds = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
    } catch (e) {}
    if (Array.isArray(savedIds)) {
        sections.forEach(sec => { sec.open = savedIds.indexOf(sec.id) !== -1; });
    }

    function persistOpenState() {
        if (searchInput && searchInput.value.trim()) return; // don't persist search state
        const openIds = sections.filter(s => s.open).map(s => s.id);
        try { localStorage.setItem(STORAGE_KEY, JSON.stringify(openIds)); } catch (e) {}
    }
    sections.forEach(sec => sec.addEventListener('toggle', persistOpenState));

    if (expandBtn) {
        expandBtn.addEventListener('click', () => sections.forEach(s => { s.open = true; }));
    }
    if (collapseBtn) {
        collapseBtn.addEventListener('click', () => sections.forEach(s => { s.open = false; }));
    }

    if (!searchInput) return;

    function escapeHtml(text) {
        return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    function highlight(link, query) {
        link.querySelectorAll('.leetcode-problem-num, .leetcode-problem-title').forEach(span => {
            if (span._origHtml === undefined) span._origHtml = span.innerHTML;
            const text = span.textContent;
            const idx = text.toLowerCase().indexOf(query);
            if (idx === -1) {
                span.innerHTML = span._origHtml;
            } else {
                span.innerHTML =
                    escapeHtml(text.slice(0, idx)) +
                    '<mark class="list-hl">' + escapeHtml(text.slice(idx, idx + query.length)) + '</mark>' +
                    escapeHtml(text.slice(idx + query.length));
            }
        });
    }

    function clearHighlight(link) {
        link.querySelectorAll('.leetcode-problem-num, .leetcode-problem-title').forEach(span => {
            if (span._origHtml !== undefined) {
                span.innerHTML = span._origHtml;
                span._origHtml = undefined;
            }
        });
    }

    searchInput.addEventListener('input', () => {
        const query = searchInput.value.trim().toLowerCase();

        if (!query) {
            // Restore pre-search open state and visibility
            sections.forEach(sec => {
                sec.style.display = '';
                if (sec._preSearchOpen !== undefined) {
                    sec.open = sec._preSearchOpen;
                    sec._preSearchOpen = undefined;
                }
            });
            links.forEach(link => {
                link.style.display = '';
                clearHighlight(link);
            });
            if (countEl) countEl.textContent = '';
            if (emptyEl) emptyEl.hidden = true;
            overview.style.display = '';
            return;
        }

        // Snapshot open state the first time a search begins
        sections.forEach(sec => {
            if (sec._preSearchOpen === undefined) sec._preSearchOpen = sec.open;
        });

        let matched = 0;
        sections.forEach(sec => {
            const secLinks = Array.from(sec.querySelectorAll('.leetcode-problem-link'));
            let secMatched = 0;
            secLinks.forEach(link => {
                const hit = link._searchText.indexOf(query) !== -1;
                link.style.display = hit ? '' : 'none';
                if (hit) {
                    secMatched++;
                    highlight(link, query);
                } else {
                    clearHighlight(link);
                }
            });
            if (secMatched > 0) {
                sec.style.display = '';
                sec.open = true;
                matched += secMatched;
            } else {
                sec.style.display = 'none';
            }
        });

        if (countEl) countEl.textContent = '匹配 ' + matched + ' 题';
        if (emptyEl) emptyEl.hidden = matched > 0;
        overview.style.display = matched > 0 ? '' : 'none';
    });
}

function enhanceInterviewQA() {
    const content = document.querySelector('.content');
    if (!content) return;

    content.querySelectorAll('h4').forEach(heading => {
        const details = heading.nextElementSibling;
        if (!details || details.tagName !== 'DETAILS') return;

        // Avoid re-processing
        if (heading.closest('.qa-card')) return;

        const card = document.createElement('div');
        card.className = 'qa-card';

        heading.classList.add('qa-question');
        details.classList.add('qa-answer');

        const summary = details.querySelector('summary');
        if (summary) {
            summary.classList.add('qa-answer-toggle');
        }

        heading.parentNode.insertBefore(card, heading);
        card.appendChild(heading);
        card.appendChild(details);
    });
}

function initImageLightbox() {
    const content = document.querySelector('.content');
    if (!content) return;

    const images = content.querySelectorAll('img');
    if (images.length === 0) return;

    const lightbox = document.createElement('div');
    lightbox.className = 'image-lightbox';
    lightbox.setAttribute('role', 'dialog');
    lightbox.setAttribute('aria-modal', 'true');
    lightbox.setAttribute('aria-label', 'Image preview');
    lightbox.innerHTML = `
        <button class="lightbox-close" aria-label="Close image preview">&times;</button>
        <img src="" alt="">
        <div class="lightbox-caption"></div>
        <div class="lightbox-zoom-hint">滚轮缩放 / 点击关闭</div>
    `;
    document.body.appendChild(lightbox);

    const lightboxImg = lightbox.querySelector('img');
    const lightboxCaption = lightbox.querySelector('.lightbox-caption');
    const closeButton = lightbox.querySelector('.lightbox-close');
    const zoomHint = lightbox.querySelector('.lightbox-zoom-hint');

    let currentScale = 1;
    let currentTranslateX = 0;
    let currentTranslateY = 0;
    const MIN_SCALE = 0.5;
    const MAX_SCALE = 5;
    const ZOOM_STEP = 0.15;

    function updateTransform() {
        lightboxImg.style.transform = `translate(calc(-50% + ${currentTranslateX}px), calc(-50% + ${currentTranslateY}px)) scale(${currentScale})`;
    }

    function updateScale(scale) {
        currentScale = Math.max(MIN_SCALE, Math.min(MAX_SCALE, scale));
        updateTransform();
    }

    function resetScale() {
        currentScale = 1;
        currentTranslateX = 0;
        currentTranslateY = 0;
        lightboxImg.style.transform = '';
    }

    function openLightbox(img) {
        resetScale();
        lightboxImg.src = img.src;
        lightboxImg.alt = img.alt || '';
        if (img.alt) {
            lightboxCaption.textContent = img.alt;
            lightboxCaption.style.display = 'block';
        } else {
            lightboxCaption.style.display = 'none';
        }
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
        resetScale();
    }

    images.forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function(e) {
            e.preventDefault();
            openLightbox(img);
        });
    });

    lightbox.addEventListener('click', function(e) {
        if (hasDragged) return;
        if (e.target === lightbox || e.target === lightboxImg) {
            closeLightbox();
        }
    });

    closeButton.addEventListener('click', closeLightbox);

    // Drag to pan the zoomed image
    let isDragging = false;
    let hasDragged = false;
    let dragStartX = 0;
    let dragStartY = 0;
    let dragStartTranslateX = 0;
    let dragStartTranslateY = 0;

    function clampPan() {
        const rect = lightboxImg.getBoundingClientRect();
        const viewportWidth = lightbox.clientWidth;
        const viewportHeight = lightbox.clientHeight;
        const halfWidth = rect.width / 2;
        const halfHeight = rect.height / 2;

        // Allow the image center to move within the viewport plus half its size,
        // so users can drag any part of the image into view.
        const maxX = Math.max(0, halfWidth + viewportWidth / 2);
        const maxY = Math.max(0, halfHeight + viewportHeight / 2);

        currentTranslateX = Math.max(-maxX, Math.min(maxX, currentTranslateX));
        currentTranslateY = Math.max(-maxY, Math.min(maxY, currentTranslateY));
    }

    lightboxImg.addEventListener('mousedown', function(e) {
        if (!lightbox.classList.contains('active')) return;
        isDragging = true;
        hasDragged = false;
        dragStartX = e.clientX;
        dragStartY = e.clientY;
        dragStartTranslateX = currentTranslateX;
        dragStartTranslateY = currentTranslateY;
        lightboxImg.classList.add('dragging');
        e.preventDefault();
    });

    document.addEventListener('mousemove', function(e) {
        if (!isDragging) return;
        const dx = e.clientX - dragStartX;
        const dy = e.clientY - dragStartY;
        if (Math.abs(dx) > 2 || Math.abs(dy) > 2) {
            hasDragged = true;
        }
        currentTranslateX = dragStartTranslateX + dx;
        currentTranslateY = dragStartTranslateY + dy;
        clampPan();
        updateTransform();
    });

    document.addEventListener('mouseup', function() {
        if (!isDragging) return;
        isDragging = false;
        lightboxImg.classList.remove('dragging');
        setTimeout(() => { hasDragged = false; }, 50);
    });

    // Touch support for mobile
    lightboxImg.addEventListener('touchstart', function(e) {
        if (!lightbox.classList.contains('active')) return;
        if (e.touches.length !== 1) return;
        isDragging = true;
        hasDragged = false;
        dragStartX = e.touches[0].clientX;
        dragStartY = e.touches[0].clientY;
        dragStartTranslateX = currentTranslateX;
        dragStartTranslateY = currentTranslateY;
        lightboxImg.classList.add('dragging');
    }, { passive: false });

    document.addEventListener('touchmove', function(e) {
        if (!isDragging) return;
        if (e.touches.length !== 1) return;
        const dx = e.touches[0].clientX - dragStartX;
        const dy = e.touches[0].clientY - dragStartY;
        if (Math.abs(dx) > 2 || Math.abs(dy) > 2) {
            hasDragged = true;
        }
        currentTranslateX = dragStartTranslateX + dx;
        currentTranslateY = dragStartTranslateY + dy;
        clampPan();
        updateTransform();
        e.preventDefault();
    }, { passive: false });

    document.addEventListener('touchend', function() {
        if (!isDragging) return;
        isDragging = false;
        lightboxImg.classList.remove('dragging');
        setTimeout(() => { hasDragged = false; }, 50);
    });

    // Mouse wheel zoom
    lightbox.addEventListener('wheel', function(e) {
        if (!lightbox.classList.contains('active')) return;
        e.preventDefault();
        const delta = e.deltaY > 0 ? -ZOOM_STEP : ZOOM_STEP;
        updateScale(currentScale + delta);
    }, { passive: false });

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && lightbox.classList.contains('active')) {
            closeLightbox();
        }
    });
}


function initToc() {
    const content = document.querySelector('.content');
    const toc = document.getElementById('toc');
    if (!content || !toc) return;

    const headings = Array.from(content.querySelectorAll('h2, h3'));
    if (headings.length < 2) {
        const shell = toc.closest('.content-shell');
        if (shell) shell.classList.add('no-toc');
        toc.style.display = 'none';
        return;
    }

    const title = document.createElement('div');
    title.className = 'toc-title';
    title.textContent = '本页目录';
    toc.appendChild(title);

    const tocLinks = [];
    headings.forEach((heading, i) => {
        if (!heading.id) {
            heading.id = 'section-' + i;
        }
        const link = document.createElement('a');
        link.className = heading.tagName === 'H3' ? 'toc-h3' : 'toc-h2';
        link.href = '#' + heading.id;
        link.textContent = heading.textContent;
        toc.appendChild(link);
        tocLinks.push(link);
    });

    // Scroll-spy: highlight the section currently in view
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            tocLinks.forEach(link => {
                link.classList.toggle('toc-active', link.hash === '#' + entry.target.id);
            });
        });
    }, { rootMargin: '-80px 0px -70% 0px' });

    headings.forEach(heading => observer.observe(heading));
}
