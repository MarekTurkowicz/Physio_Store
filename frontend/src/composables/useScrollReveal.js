import { onMounted, onUnmounted } from 'vue'

/**
 * Composable that sets up IntersectionObserver for scroll-reveal animations.
 * Elements with `data-reveal` attribute will get `is-visible` class when they enter viewport.
 * 
 * Add `data-reveal` to any element to enable scroll-triggered animation.
 * Add `data-reveal-delay="N"` where N is ms delay (optional).
 * Add `data-reveal-distance="N"` where N is px offset (optional, default 40).
 */
export function useScrollReveal(rootRef) {
  let observer = null

  const setupObserver = () => {
    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const el = entry.target
            const delay = parseInt(el.dataset.revealDelay || '0', 10)
            if (delay > 0) {
              setTimeout(() => el.classList.add('is-visible'), delay)
            } else {
              el.classList.add('is-visible')
            }
            observer.unobserve(el)
          }
        })
      },
      {
        threshold: 0.08,
        rootMargin: '0px 0px -20px 0px'
      }
    )

    // Observe all data-reveal elements within root (or document)
    const root = rootRef?.value || document
    const elements = root.querySelectorAll('[data-reveal]')
    elements.forEach((el) => observer.observe(el))
  }

  onMounted(() => {
    // Slight delay to ensure DOM is rendered
    requestAnimationFrame(setupObserver)
  })

  onUnmounted(() => {
    if (observer) {
      observer.disconnect()
      observer = null
    }
  })

  return { setupObserver }
}
