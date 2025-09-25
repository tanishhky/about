document.addEventListener('DOMContentLoaded', () => {
    // Register GSAP plugins
    gsap.registerPlugin(ScrollTrigger);

    // --- Loading Screen ---
    const loadingScreen = document.getElementById('loading');
    window.addEventListener('load', () => {
        if (loadingScreen) {
            gsap.to(loadingScreen, {
                opacity: 0,
                duration: 0.5,
                onComplete: () => {
                    loadingScreen.style.display = 'none';
                    // Trigger Hero Animation only after loader is gone
                    animateHero();
                }
            });
        } else {
            animateHero();
        }
    });

    // --- Hero Section Staggered Animation ---
    // Replaces the old typing effect with a professional "slide-up" entry
    function animateHero() {
        const tl = gsap.timeline();

        tl.from(".hero-intro", { y: 20, opacity: 0, duration: 0.5, ease: "power2.out" })
            .from(".hero-name", { y: 20, opacity: 0, duration: 0.5, ease: "power2.out" }, "-=0.3")
            .from(".hero-tagline", { y: 20, opacity: 0, duration: 0.5, ease: "power2.out" }, "-=0.3")
            .from(".hero-subtagline", { y: 20, opacity: 0, duration: 0.5, ease: "power2.out" }, "-=0.3")
            .from(".hero-bio", { y: 20, opacity: 0, duration: 0.5, ease: "power2.out" }, "-=0.3")
            .from(".hero-socials", { y: 20, opacity: 0, duration: 0.5, ease: "power2.out" }, "-=0.3");
    }

    // --- Navbar Scroll Effect ---
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // --- Scroll Animations for Sections ---
    gsap.utils.toArray('.content-section').forEach(section => {
        gsap.from(section, {
            opacity: 0,
            y: 40,
            duration: 0.8,
            ease: 'power2.out',
            scrollTrigger: {
                trigger: section,
                start: 'top 85%',
                toggleActions: 'play none none none'
            }
        });
    });

    // --- Smooth Scrolling ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});