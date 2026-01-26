/**
 * ui.js - UI Components & Interactions
 * Handles navigation, forms, testimonials slider, project filtering, and more
 */

export class UIManager {
    constructor() {
        this.nav = null;
        this.navToggle = null;
        this.navMenu = null;
        this.isNavOpen = false;
        this.lastScrollY = 0;
        this.testimonialSlider = null;
        this.currentTestimonial = 0;
        this.testimonialAutoplay = null;
    }

    /**
     * Initialize all UI components
     */
    init() {
        this.initNavigation();
        this.initTestimonialsSlider();
        this.initProjectsFilter();
        this.initServiceCards();
        this.initSmoothScroll();
        this.initFooterYear();
        this.initLoader();

        return true;
    }

    /**
     * Initialize navigation
     */
    initNavigation() {
        this.nav = document.querySelector('.main-nav');
        this.navToggle = document.querySelector('.nav-toggle');
        this.navMenu = document.querySelector('.nav-menu');

        if (!this.nav) return;

        // Mobile menu toggle
        if (this.navToggle) {
            this.navToggle.addEventListener('click', () => this.toggleMobileMenu());
        }

        // Close menu when clicking nav links
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (this.isNavOpen) {
                    this.toggleMobileMenu();
                }
            });
        });

        // Handle scroll for nav background
        window.addEventListener('scroll', () => this.handleNavScroll());

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isNavOpen) {
                this.toggleMobileMenu();
            }
        });
    }

    /**
     * Toggle mobile menu
     */
    toggleMobileMenu() {
        this.isNavOpen = !this.isNavOpen;
        this.navToggle.setAttribute('aria-expanded', this.isNavOpen);
        this.navMenu.classList.toggle('active', this.isNavOpen);
        document.body.style.overflow = this.isNavOpen ? 'hidden' : '';
    }

    /**
     * Handle navigation scroll effects
     */
    handleNavScroll() {
        const scrollY = window.scrollY;

        // Add/remove scrolled class
        if (scrollY > 50) {
            this.nav.classList.add('scrolled');
        } else {
            this.nav.classList.remove('scrolled');
        }

        this.lastScrollY = scrollY;
    }

    /**
     * Initialize testimonials slider
     */
    initTestimonialsSlider() {
        const track = document.querySelector('.testimonials-track');
        const cards = document.querySelectorAll('.testimonial-card');
        const prevBtn = document.querySelector('.nav-prev');
        const nextBtn = document.querySelector('.nav-next');
        const dotsContainer = document.querySelector('.testimonials-dots');

        if (!track || cards.length === 0) return;

        // Create dots
        cards.forEach((_, index) => {
            const dot = document.createElement('button');
            dot.classList.add('dot');
            if (index === 0) dot.classList.add('active');
            dot.setAttribute('aria-label', `Go to testimonial ${index + 1}`);
            dot.addEventListener('click', () => this.goToTestimonial(index));
            dotsContainer.appendChild(dot);
        });

        // Navigation buttons
        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.prevTestimonial());
        }
        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextTestimonial());
        }

        // Touch/swipe support
        let startX = 0;
        let currentX = 0;
        let isDragging = false;

        track.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            isDragging = true;
        }, { passive: true });

        track.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            currentX = e.touches[0].clientX;
        }, { passive: true });

        track.addEventListener('touchend', () => {
            if (!isDragging) return;
            const diff = startX - currentX;

            if (Math.abs(diff) > 50) {
                if (diff > 0) {
                    this.nextTestimonial();
                } else {
                    this.prevTestimonial();
                }
            }
            isDragging = false;
        });

        // Auto-play
        this.startTestimonialAutoplay();

        // Pause on hover
        track.addEventListener('mouseenter', () => this.stopTestimonialAutoplay());
        track.addEventListener('mouseleave', () => this.startTestimonialAutoplay());
    }

    /**
     * Go to specific testimonial
     */
    goToTestimonial(index) {
        const cards = document.querySelectorAll('.testimonial-card');
        const dots = document.querySelectorAll('.testimonials-dots .dot');
        const track = document.querySelector('.testimonials-track');

        if (index < 0) index = cards.length - 1;
        if (index >= cards.length) index = 0;

        this.currentTestimonial = index;

        // Scroll to card
        const cardWidth = cards[0].offsetWidth;
        const gap = 24; // gap from CSS
        const scrollPosition = index * (cardWidth + gap);

        track.scrollTo({
            left: scrollPosition,
            behavior: 'smooth'
        });

        // Update dots
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
    }

    /**
     * Previous testimonial
     */
    prevTestimonial() {
        this.goToTestimonial(this.currentTestimonial - 1);
    }

    /**
     * Next testimonial
     */
    nextTestimonial() {
        this.goToTestimonial(this.currentTestimonial + 1);
    }

    /**
     * Start testimonial autoplay
     */
    startTestimonialAutoplay() {
        this.stopTestimonialAutoplay();
        this.testimonialAutoplay = setInterval(() => {
            this.nextTestimonial();
        }, 5000);
    }

    /**
     * Stop testimonial autoplay
     */
    stopTestimonialAutoplay() {
        if (this.testimonialAutoplay) {
            clearInterval(this.testimonialAutoplay);
            this.testimonialAutoplay = null;
        }
    }

    /**
     * Initialize projects filter
     */
    initProjectsFilter() {
        const filterBtns = document.querySelectorAll('.filter-btn');
        const projectCards = document.querySelectorAll('.project-card');

        if (filterBtns.length === 0 || projectCards.length === 0) return;

        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Update active button
                filterBtns.forEach(b => {
                    b.classList.remove('active');
                    b.setAttribute('aria-selected', 'false');
                });
                btn.classList.add('active');
                btn.setAttribute('aria-selected', 'true');

                // Filter projects
                const filter = btn.dataset.filter;

                projectCards.forEach(card => {
                    const category = card.dataset.category;
                    const shouldShow = filter === 'all' || category === filter;

                    if (shouldShow) {
                        card.style.display = '';
                        gsap.to(card, {
                            opacity: 1,
                            scale: 1,
                            duration: 0.3,
                            ease: 'power2.out'
                        });
                    } else {
                        gsap.to(card, {
                            opacity: 0,
                            scale: 0.9,
                            duration: 0.3,
                            ease: 'power2.in',
                            onComplete: () => {
                                card.style.display = 'none';
                            }
                        });
                    }
                });
            });
        });
    }

    /**
     * Initialize service cards 3D tilt effect
     */
    initServiceCards() {
        const cards = document.querySelectorAll('.service-card');

        cards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const centerX = rect.width / 2;
                const centerY = rect.height / 2;

                const rotateX = (y - centerY) / centerY * -10;
                const rotateY = (x - centerX) / centerX * 10;

                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0)';
            });
        });
    }

    /**
     * Initialize smooth scroll for anchor links
     */
    initSmoothScroll() {
        const links = document.querySelectorAll('a[href^="#"]');

        links.forEach(link => {
            link.addEventListener('click', (e) => {
                const href = link.getAttribute('href');
                if (href === '#') return;

                const target = document.querySelector(href);
                if (!target) return;

                e.preventDefault();

                const headerHeight = document.querySelector('.main-nav').offsetHeight;
                const targetPosition = target.offsetTop - headerHeight;

                if (typeof gsap !== 'undefined' && typeof ScrollToPlugin !== 'undefined') {
                    gsap.to(window, {
                        scrollTo: { y: targetPosition, autoKill: true },
                        duration: 1,
                        ease: 'power3.inOut'
                    });
                } else {
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    /**
     * Initialize footer year
     */
    initFooterYear() {
        const yearElement = document.getElementById('current-year');
        if (yearElement) {
            yearElement.textContent = new Date().getFullYear();
        }
    }

    /**
     * Initialize loading screen
     */
    initLoader() {
        const loader = document.getElementById('loader');
        const progressBar = document.querySelector('.loader-progress');

        if (!loader) return;

        // Simulate loading progress
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 100) progress = 100;

            if (progressBar) {
                progressBar.style.width = `${progress}%`;
            }

            if (progress === 100) {
                clearInterval(interval);
                setTimeout(() => {
                    loader.classList.add('hidden');
                    document.body.style.overflow = '';
                }, 500);
            }
        }, 100);

        // Ensure loader is hidden after max time
        setTimeout(() => {
            clearInterval(interval);
            loader.classList.add('hidden');
            document.body.style.overflow = '';
        }, 3000);
    }

    /**
     * Show notification toast
     */
    showToast(message, type = 'success', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;

        toast.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 16px 24px;
            background: ${type === 'success' ? '#10B981' : type === 'error' ? '#EF4444' : '#FFD400'};
            color: ${type === 'warning' ? '#000' : '#fff'};
            border-radius: 8px;
            font-weight: 500;
            z-index: 9999;
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.3s ease;
        `;

        document.body.appendChild(toast);

        // Animate in
        requestAnimationFrame(() => {
            toast.style.transform = 'translateY(0)';
            toast.style.opacity = '1';
        });

        // Animate out
        setTimeout(() => {
            toast.style.transform = 'translateY(100px)';
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    /**
     * Cleanup
     */
    dispose() {
        this.stopTestimonialAutoplay();
    }
}

/**
 * Form Handler - Contact form validation and submission
 */
export class FormHandler {
    constructor(formSelector) {
        this.form = document.querySelector(formSelector);
        this.submitBtn = null;
        this.successMessage = null;
        this.isSubmitting = false;
    }

    /**
     * Initialize form handling
     */
    init() {
        if (!this.form) return false;

        this.submitBtn = this.form.querySelector('.btn-submit');
        this.successMessage = this.form.querySelector('.form-success');

        // Form submission
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));

        // Real-time validation
        const inputs = this.form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearError(input));
        });

        // Phone number formatting
        const phoneInput = this.form.querySelector('#phone');
        if (phoneInput) {
            phoneInput.addEventListener('input', (e) => this.formatPhoneNumber(e));
        }

        return true;
    }

    /**
     * Handle form submission
     */
    async handleSubmit(e) {
        e.preventDefault();

        if (this.isSubmitting) return;

        // Validate all fields
        const isValid = this.validateForm();
        if (!isValid) return;

        // Show loading state
        this.isSubmitting = true;
        this.submitBtn.classList.add('loading');
        this.submitBtn.disabled = true;

        try {
            // Simulate API call
            await this.simulateSubmission();

            // Show success message
            this.showSuccess();
        } catch (error) {
            // Show error
            this.showError('Something went wrong. Please try again.');
        } finally {
            this.isSubmitting = false;
            this.submitBtn.classList.remove('loading');
            this.submitBtn.disabled = false;
        }
    }

    /**
     * Validate entire form
     */
    validateForm() {
        const inputs = this.form.querySelectorAll('[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });

        return isValid;
    }

    /**
     * Validate individual field
     */
    validateField(input) {
        const value = input.value.trim();
        const type = input.type;
        const name = input.name;
        let errorMessage = '';

        // Required check
        if (input.required && !value) {
            errorMessage = 'This field is required';
        }
        // Email validation
        else if (type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                errorMessage = 'Please enter a valid email address';
            }
        }
        // Phone validation
        else if (type === 'tel' && value) {
            const phoneRegex = /^[\d\s\-\(\)]{10,}$/;
            if (!phoneRegex.test(value)) {
                errorMessage = 'Please enter a valid phone number';
            }
        }
        // Checkbox validation
        else if (type === 'checkbox' && input.required && !input.checked) {
            errorMessage = 'Please check this box to continue';
        }
        // Select validation
        else if (input.tagName === 'SELECT' && input.required && !value) {
            errorMessage = 'Please select an option';
        }

        // Show/hide error
        if (errorMessage) {
            this.showFieldError(input, errorMessage);
            return false;
        } else {
            this.clearError(input);
            return true;
        }
    }

    /**
     * Show field error
     */
    showFieldError(input, message) {
        const formGroup = input.closest('.form-group') || input.parentElement;
        const errorSpan = formGroup.querySelector('.form-error');

        input.classList.add('error');

        if (errorSpan) {
            errorSpan.textContent = message;
        }
    }

    /**
     * Clear field error
     */
    clearError(input) {
        const formGroup = input.closest('.form-group') || input.parentElement;
        const errorSpan = formGroup.querySelector('.form-error');

        input.classList.remove('error');

        if (errorSpan) {
            errorSpan.textContent = '';
        }
    }

    /**
     * Format phone number as user types
     */
    formatPhoneNumber(e) {
        let value = e.target.value.replace(/\D/g, '');

        if (value.length > 10) {
            value = value.slice(0, 10);
        }

        if (value.length >= 6) {
            value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6)}`;
        } else if (value.length >= 3) {
            value = `(${value.slice(0, 3)}) ${value.slice(3)}`;
        }

        e.target.value = value;
    }

    /**
     * Simulate form submission (replace with actual API call)
     */
    simulateSubmission() {
        return new Promise((resolve) => {
            setTimeout(resolve, 2000);
        });
    }

    /**
     * Show success state
     */
    showSuccess() {
        // Hide form fields
        const formElements = this.form.querySelectorAll('.form-row, .form-group, .btn-submit, .form-title');
        formElements.forEach(el => {
            el.style.display = 'none';
        });

        // Show success message
        if (this.successMessage) {
            this.successMessage.hidden = false;
            gsap.from(this.successMessage, {
                opacity: 0,
                scale: 0.9,
                duration: 0.5,
                ease: 'back.out(1.7)'
            });
        }

        // Reset form after delay
        setTimeout(() => {
            this.resetForm();
        }, 5000);
    }

    /**
     * Show error message
     */
    showError(message) {
        // Create or update error message
        let errorElement = this.form.querySelector('.form-submit-error');

        if (!errorElement) {
            errorElement = document.createElement('p');
            errorElement.className = 'form-submit-error';
            errorElement.style.cssText = `
                color: #EF4444;
                text-align: center;
                margin-top: 16px;
                font-size: 14px;
            `;
            this.form.appendChild(errorElement);
        }

        errorElement.textContent = message;

        // Auto-hide after delay
        setTimeout(() => {
            errorElement.textContent = '';
        }, 5000);
    }

    /**
     * Reset form to initial state
     */
    resetForm() {
        this.form.reset();

        // Clear all errors
        const inputs = this.form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => this.clearError(input));

        // Show form fields
        const formElements = this.form.querySelectorAll('.form-row, .form-group, .btn-submit, .form-title');
        formElements.forEach(el => {
            el.style.display = '';
        });

        // Hide success message
        if (this.successMessage) {
            this.successMessage.hidden = true;
        }
    }

    /**
     * Get form data as object
     */
    getFormData() {
        const formData = new FormData(this.form);
        const data = {};

        formData.forEach((value, key) => {
            data[key] = value;
        });

        return data;
    }
}
