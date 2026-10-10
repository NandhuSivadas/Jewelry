document.addEventListener('DOMContentLoaded', () => {
    // 1. Sticky Header Shrink & Blur Effect
    const header = document.getElementById('site-header');
    if (header) {
        const handleScroll = () => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        };
        window.addEventListener('scroll', handleScroll, { passive: true });
        handleScroll(); // Check on load
    }

    // 2. Advanced Intersection Observer for Reveals
    const revealElements = document.querySelectorAll('.reveal, .reveal-up, .reveal-left, .reveal-right, .reveal-blur');
    
    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add a slight stagger effect based on index for grouped elements
                setTimeout(() => {
                    entry.target.classList.add('active');
                }, 100); // fixed stagger
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, {
        root: null,
        rootMargin: '0px 0px -10% 0px', 
        threshold: 0.1
    });

    revealElements.forEach(el => revealObserver.observe(el));
    
    // 3. Parallax effect for Hero Video/Image
    const heroMedia = document.querySelector('.parallax-media');
    if (heroMedia) {
        window.addEventListener('scroll', () => {
            const scrollPos = window.scrollY;
            if (scrollPos < window.innerHeight) {
                heroMedia.style.transform = 'translateY(' + (scrollPos * 0.4) + 'px)';
            }
        }, { passive: true });
    }
});
