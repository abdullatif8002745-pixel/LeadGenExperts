/**
 * scrollAnimations.js - GSAP ScrollTrigger Animations
 * Handles scroll-based animations and 3D section transitions
 */

export class ScrollAnimations {
    constructor() {
        this.scrollProgress = 0;
        this.currentSection = 0;
        this.totalSections = 6;
        this.isScrolling = false;
        this.scrollTimeout = null;
        this.callbacks = [];
        this.triggers = [];
        this.isInitialized = false;
    }

    /**
     * Initialize scroll animations
     */
    init() {
        if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
            console.warn('GSAP or ScrollTrigger not available');
            return false;
        }

        // Register ScrollTrigger plugin
        gsap.registerPlugin(ScrollTrigger);

        // Configure ScrollTrigger defaults
        ScrollTrigger.defaults({
            toggleActions: 'play none none reverse',
            markers: false
        });

        // Setup main scroll tracking
        this.setupScrollTracking();

        // Setup section animations
        this.setupSectionAnimations();

        // Setup element animations
        this.setupElementAnimations();

        // Setup navigation scroll spy
        this.setupScrollSpy();

        // Refresh on page load complete
        window.addEventListener('load', () => {
            ScrollTrigger.refresh();
        });

        this.isInitialized = true;
        return true;
    }

    /**
     * Setup main scroll progress tracking
     */
    setupScrollTracking() {
        const scrollContainer = document.getElementById('scroll-container');
        if (!scrollContainer) return;

        // Create main scroll trigger for tracking progress
        ScrollTrigger.create({
            trigger: scrollContainer,
            start: 'top top',
            end: 'bottom bottom',
            scrub: 0.5,
            onUpdate: (self) => {
                this.scrollProgress = self.progress;
                this.currentSection = Math.floor(self.progress * this.totalSections);

                // Notify callbacks
                this.callbacks.forEach(callback => {
                    callback(this.scrollProgress, this.currentSection);
                });

                // Mark as scrolling
                this.isScrolling = true;
                clearTimeout(this.scrollTimeout);
                this.scrollTimeout = setTimeout(() => {
                    this.isScrolling = false;
                }, 150);
            }
        });
    }

    /**
     * Setup individual section animations
     */
    setupSectionAnimations() {
        const sections = document.querySelectorAll('.section');

        sections.forEach((section, index) => {
            const content = section.querySelector('.section-content');
            if (!content) return;

            // Section enter animation
            const tl = gsap.timeline({
                scrollTrigger: {
                    trigger: section,
                    start: 'top 80%',
                    end: 'top 20%',
                    scrub: 1,
                    toggleActions: 'play none none reverse'
                }
            });

            // 3D entrance effect
            tl.fromTo(content, {
                opacity: 0,
                y: 100,
                rotateX: 15,
                z: -200,
                scale: 0.9
            }, {
                opacity: 1,
                y: 0,
                rotateX: 0,
                z: 0,
                scale: 1,
                duration: 1,
                ease: 'power3.out'
            });

            // Section exit animation
            const exitTl = gsap.timeline({
                scrollTrigger: {
                    trigger: section,
                    start: 'bottom 60%',
                    end: 'bottom top',
                    scrub: 1
                }
            });

            exitTl.to(content, {
                opacity: 0,
                y: -50,
                rotateX: -10,
                z: -300,
                scale: 0.95,
                duration: 1,
                ease: 'power3.in'
            });

            this.triggers.push(tl, exitTl);
        });
    }

    /**
     * Setup element-level animations
     */
    setupElementAnimations() {
        // Hero section animations
        this.animateHeroSection();

        // Services section animations
        this.animateServicesSection();

        // About section animations
        this.animateAboutSection();

        // Projects section animations
        this.animateProjectsSection();

        // Testimonials section animations
        this.animateTestimonialsSection();

        // Contact section animations
        this.animateContactSection();

        // Animate stats counters
        this.animateCounters();
    }

    /**
     * Hero section animations
     */
    animateHeroSection() {
        const hero = document.querySelector('.section-hero');
        if (!hero) return;

        const tl = gsap.timeline({
            scrollTrigger: {
                trigger: hero,
                start: 'top top',
                end: 'bottom top',
                scrub: 1
            }
        });

        // Parallax effect on hero content
        tl.to('.hero-content', {
            y: -100,
            opacity: 0.5,
            ease: 'none'
        }, 0);

        // Fade scroll indicator
        gsap.to('.scroll-indicator', {
            scrollTrigger: {
                trigger: hero,
                start: 'top top',
                end: '20% top',
                scrub: 1
            },
            opacity: 0,
            y: 20
        });

        // Initial hero entrance animation (not scroll-based)
        const entranceTl = gsap.timeline({ delay: 0.5 });

        entranceTl.from('.hero-badge', {
            y: 30,
            opacity: 0,
            duration: 0.8,
            ease: 'power3.out'
        })
        .from('.hero-title .title-line', {
            y: 80,
            opacity: 0,
            rotateX: 30,
            stagger: 0.15,
            duration: 1,
            ease: 'power3.out'
        }, '-=0.4')
        .from('.hero-subtitle', {
            y: 30,
            opacity: 0,
            duration: 0.8,
            ease: 'power3.out'
        }, '-=0.6')
        .from('.hero-description', {
            y: 30,
            opacity: 0,
            duration: 0.8,
            ease: 'power3.out'
        }, '-=0.6')
        .from('.hero-cta-group .btn', {
            y: 30,
            opacity: 0,
            stagger: 0.1,
            duration: 0.8,
            ease: 'power3.out'
        }, '-=0.6')
        .from('.stat-item', {
            y: 30,
            opacity: 0,
            stagger: 0.1,
            duration: 0.8,
            ease: 'power3.out'
        }, '-=0.6')
        .from('.scroll-indicator', {
            y: 20,
            opacity: 0,
            duration: 0.8,
            ease: 'power3.out'
        }, '-=0.4');
    }

    /**
     * Services section animations
     */
    animateServicesSection() {
        const services = document.querySelector('.section-services');
        if (!services) return;

        // Animate section header
        gsap.from('.section-services .section-header', {
            scrollTrigger: {
                trigger: services,
                start: 'top 70%',
                toggleActions: 'play none none reverse'
            },
            y: 50,
            opacity: 0,
            duration: 1,
            ease: 'power3.out'
        });

        // Animate service cards with stagger
        gsap.from('.service-card', {
            scrollTrigger: {
                trigger: '.services-grid',
                start: 'top 70%',
                toggleActions: 'play none none reverse'
            },
            y: 80,
            opacity: 0,
            rotateY: -15,
            scale: 0.9,
            stagger: 0.15,
            duration: 1,
            ease: 'power3.out'
        });
    }

    /**
     * About section animations
     */
    animateAboutSection() {
        const about = document.querySelector('.section-about');
        if (!about) return;

        // Animate images
        gsap.from('.about-image-1', {
            scrollTrigger: {
                trigger: about,
                start: 'top 60%',
                toggleActions: 'play none none reverse'
            },
            x: -100,
            opacity: 0,
            duration: 1.2,
            ease: 'power3.out'
        });

        gsap.from('.about-image-2', {
            scrollTrigger: {
                trigger: about,
                start: 'top 50%',
                toggleActions: 'play none none reverse'
            },
            x: 100,
            opacity: 0,
            duration: 1.2,
            ease: 'power3.out'
        });

        gsap.from('.about-badge', {
            scrollTrigger: {
                trigger: about,
                start: 'top 50%',
                toggleActions: 'play none none reverse'
            },
            scale: 0,
            opacity: 0,
            duration: 0.8,
            ease: 'back.out(1.7)'
        });

        // Animate content
        gsap.from('.about-content > *', {
            scrollTrigger: {
                trigger: '.about-content',
                start: 'top 70%',
                toggleActions: 'play none none reverse'
            },
            y: 50,
            opacity: 0,
            stagger: 0.1,
            duration: 0.8,
            ease: 'power3.out'
        });
    }

    /**
     * Projects section animations
     */
    animateProjectsSection() {
        const projects = document.querySelector('.section-projects');
        if (!projects) return;

        // Animate section header
        gsap.from('.section-projects .section-header', {
            scrollTrigger: {
                trigger: projects,
                start: 'top 70%',
                toggleActions: 'play none none reverse'
            },
            y: 50,
            opacity: 0,
            duration: 1,
            ease: 'power3.out'
        });

        // Animate filter buttons
        gsap.from('.filter-btn', {
            scrollTrigger: {
                trigger: '.projects-filter',
                start: 'top 80%',
                toggleActions: 'play none none reverse'
            },
            y: 20,
            opacity: 0,
            stagger: 0.1,
            duration: 0.6,
            ease: 'power3.out'
        });

        // Animate project cards
        gsap.from('.project-card', {
            scrollTrigger: {
                trigger: '.projects-grid',
                start: 'top 70%',
                toggleActions: 'play none none reverse'
            },
            y: 100,
            opacity: 0,
            scale: 0.9,
            stagger: {
                each: 0.1,
                grid: [2, 3],
                from: 'start'
            },
            duration: 1,
            ease: 'power3.out'
        });
    }

    /**
     * Testimonials section animations
     */
    animateTestimonialsSection() {
        const testimonials = document.querySelector('.section-testimonials');
        if (!testimonials) return;

        // Animate section header
        gsap.from('.section-testimonials .section-header', {
            scrollTrigger: {
                trigger: testimonials,
                start: 'top 70%',
                toggleActions: 'play none none reverse'
            },
            y: 50,
            opacity: 0,
            duration: 1,
            ease: 'power3.out'
        });

        // Animate testimonial cards
        gsap.from('.testimonial-card', {
            scrollTrigger: {
                trigger: '.testimonials-container',
                start: 'top 70%',
                toggleActions: 'play none none reverse'
            },
            y: 80,
            opacity: 0,
            scale: 0.95,
            duration: 1.2,
            ease: 'power3.out'
        });
    }

    /**
     * Contact section animations
     */
    animateContactSection() {
        const contact = document.querySelector('.section-contact');
        if (!contact) return;

        // Animate contact info
        gsap.from('.contact-info > *', {
            scrollTrigger: {
                trigger: '.contact-info',
                start: 'top 70%',
                toggleActions: 'play none none reverse'
            },
            x: -50,
            opacity: 0,
            stagger: 0.1,
            duration: 0.8,
            ease: 'power3.out'
        });

        // Animate contact form
        gsap.from('.contact-form-container', {
            scrollTrigger: {
                trigger: '.contact-form-container',
                start: 'top 70%',
                toggleActions: 'play none none reverse'
            },
            x: 50,
            opacity: 0,
            duration: 1,
            ease: 'power3.out'
        });

        // Animate map
        gsap.from('.map-container', {
            scrollTrigger: {
                trigger: '.map-container',
                start: 'top 80%',
                toggleActions: 'play none none reverse'
            },
            y: 50,
            opacity: 0,
            duration: 1,
            ease: 'power3.out'
        });
    }

    /**
     * Animate counter numbers
     */
    animateCounters() {
        const counters = document.querySelectorAll('.stat-number');

        counters.forEach(counter => {
            const target = parseInt(counter.dataset.count) || 0;

            ScrollTrigger.create({
                trigger: counter,
                start: 'top 80%',
                onEnter: () => {
                    gsap.to(counter, {
                        innerText: target,
                        duration: 2,
                        ease: 'power2.out',
                        snap: { innerText: 1 },
                        onUpdate: function() {
                            counter.textContent = Math.round(this.targets()[0].innerText);
                        }
                    });
                },
                once: true
            });
        });
    }

    /**
     * Setup navigation scroll spy
     */
    setupScrollSpy() {
        const sections = document.querySelectorAll('.section');
        const navLinks = document.querySelectorAll('.nav-link');

        sections.forEach((section, index) => {
            ScrollTrigger.create({
                trigger: section,
                start: 'top center',
                end: 'bottom center',
                onEnter: () => this.updateActiveNav(index),
                onEnterBack: () => this.updateActiveNav(index)
            });
        });
    }

    /**
     * Update active navigation link
     */
    updateActiveNav(sectionIndex) {
        const navLinks = document.querySelectorAll('.nav-link');

        navLinks.forEach((link, index) => {
            if (index === sectionIndex) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    /**
     * Register callback for scroll updates
     */
    onScroll(callback) {
        this.callbacks.push(callback);
    }

    /**
     * Scroll to a specific section
     */
    scrollToSection(sectionIndex) {
        const sections = document.querySelectorAll('.section');
        const section = sections[sectionIndex];

        if (section) {
            gsap.to(window, {
                scrollTo: {
                    y: section,
                    offsetY: 0
                },
                duration: 1.5,
                ease: 'power3.inOut'
            });
        }
    }

    /**
     * Get current scroll progress
     */
    getProgress() {
        return this.scrollProgress;
    }

    /**
     * Get current section index
     */
    getCurrentSection() {
        return this.currentSection;
    }

    /**
     * Refresh ScrollTrigger (call after dynamic content changes)
     */
    refresh() {
        ScrollTrigger.refresh();
    }

    /**
     * Cleanup
     */
    dispose() {
        this.triggers.forEach(trigger => trigger.kill());
        ScrollTrigger.getAll().forEach(trigger => trigger.kill());
        this.callbacks = [];
        this.triggers = [];
        clearTimeout(this.scrollTimeout);
    }
}
