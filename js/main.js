document.addEventListener('DOMContentLoaded', () => {
    // Register GSAP plugins for use
    gsap.registerPlugin(ScrollTrigger);

    // --- Loading Screen Logic ---
    const loadingScreen = document.getElementById('loading');
    window.addEventListener('load', () => {
        if (loadingScreen) {
            // Fade out the loading screen
            gsap.to(loadingScreen, {
                opacity: 0,
                duration: 0.5,
                onComplete: () => {
                    loadingScreen.style.display = 'none';
                }
            });
        }
        // Trigger animations after the page is fully loaded
        animateOnLoad();
    });

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

    // --- Animation Function ---
    function animateOnLoad() {
        // Typing effect for the hero tagline
        const typingElement = document.getElementById('hero-typing-effect');
        if (typingElement) {
            const text = "NYU Masters Financial Engineering Candidate | Quantitative & Risk Analysis";
            let index = 0;
            typingElement.textContent = ''; // Clear existing text
            function type() {
                if (index < text.length) {
                    typingElement.textContent += text.charAt(index);
                    index++;
                    setTimeout(type, 50); // Typing speed
                }
            }
            type();
        }

        // On-scroll fade-in animation for content sections
        gsap.utils.toArray('.content-section').forEach(section => {
            gsap.from(section, {
                opacity: 0,
                y: 40,
                duration: 0.8,
                ease: 'power2.out',
                scrollTrigger: {
                    trigger: section,
                    start: 'top 80%',
                    toggleActions: 'play none none none'
                }
            });
        });
    }

    // --- Smooth Scrolling for Anchor Links ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            try {
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            } catch (error) {
                console.error("Error scrolling to anchor:", error);
            }
        });
    });
});
