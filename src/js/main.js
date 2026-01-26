/**
 * main.js - Main Application Entry Point
 * REXX Roofing LLC 3D Interactive Website
 *
 * Initializes and coordinates all modules:
 * - Three.js 3D Scene
 * - Camera Controller
 * - Particle System
 * - Scroll Animations
 * - UI Components
 */

import { SceneManager } from './scene.js';
import { CameraController } from './camera.js';
import { ParticleSystem } from './particles.js';
import { ScrollAnimations } from './scrollAnimations.js';
import { UIManager, FormHandler } from './ui.js';

class REXXRoofingApp {
    constructor() {
        // Core modules
        this.sceneManager = null;
        this.cameraController = null;
        this.particleSystem = null;
        this.scrollAnimations = null;
        this.uiManager = null;
        this.formHandler = null;

        // Animation state
        this.isRunning = false;
        this.lastTime = 0;
        this.animationId = null;

        // Performance
        this.performanceLevel = 'high';
        this.targetFPS = 60;
        this.frameInterval = 1000 / this.targetFPS;

        // Canvases
        this.webglCanvas = null;
        this.particleCanvas = null;

        // Bind methods
        this.animate = this.animate.bind(this);
        this.onVisibilityChange = this.onVisibilityChange.bind(this);
    }

    /**
     * Initialize the application
     */
    async init() {
        console.log('REXX Roofing - Initializing 3D Experience...');

        try {
            // Detect performance capabilities
            this.detectPerformance();

            // Get canvas elements
            this.webglCanvas = document.getElementById('webgl-canvas');
            this.particleCanvas = document.getElementById('particle-canvas');

            // Initialize modules based on performance level
            await this.initModules();

            // Setup event listeners
            this.setupEventListeners();

            // Start animation loop
            this.start();

            console.log('REXX Roofing - Initialization complete!');
            return true;
        } catch (error) {
            console.error('REXX Roofing - Initialization failed:', error);
            this.handleInitError(error);
            return false;
        }
    }

    /**
     * Detect device performance capabilities
     */
    detectPerformance() {
        // Check for reduced motion preference
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (prefersReducedMotion) {
            this.performanceLevel = 'low';
            document.body.classList.add('reduce-motion');
            return;
        }

        // Check device memory (if available)
        const memory = navigator.deviceMemory;
        if (memory && memory < 4) {
            this.performanceLevel = 'low';
        }

        // Check hardware concurrency
        const cores = navigator.hardwareConcurrency;
        if (cores && cores < 4) {
            this.performanceLevel = cores < 2 ? 'low' : 'medium';
        }

        // Check for mobile devices
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        if (isMobile) {
            this.performanceLevel = 'medium';
        }

        // Check screen resolution
        const screenArea = window.screen.width * window.screen.height;
        if (screenArea > 3000000) { // ~2K+
            if (this.performanceLevel === 'high' && !isMobile) {
                this.targetFPS = 60;
            }
        }

        // Apply performance class to body
        document.body.classList.add(`performance-${this.performanceLevel}`);

        if (this.performanceLevel === 'low') {
            document.body.classList.add('low-performance');
        }

        console.log(`Performance level: ${this.performanceLevel}`);
    }

    /**
     * Initialize all modules
     */
    async initModules() {
        // Initialize UI Manager first (handles loader)
        this.uiManager = new UIManager();
        this.uiManager.init();

        // Initialize Scroll Animations
        this.scrollAnimations = new ScrollAnimations();
        this.scrollAnimations.init();

        // Initialize Particle System
        if (this.particleCanvas && this.performanceLevel !== 'low') {
            this.particleSystem = new ParticleSystem(this.particleCanvas);
            this.particleSystem.init();

            // Adjust particle count based on performance
            if (this.performanceLevel === 'medium') {
                this.particleSystem.setParticleCount(30);
            }
        }

        // Initialize 3D Scene (only for high/medium performance)
        if (this.webglCanvas && this.performanceLevel !== 'low') {
            this.sceneManager = new SceneManager();
            const sceneInitialized = this.sceneManager.init(this.webglCanvas);

            if (sceneInitialized) {
                this.cameraController = new CameraController();
                this.cameraController.init();

                // Connect scroll to 3D scene
                this.scrollAnimations.onScroll((progress, section) => {
                    this.onScrollUpdate(progress, section);
                });
            } else {
                console.warn('WebGL not available, falling back to 2D mode');
                document.body.classList.add('no-webgl');
            }
        } else if (this.performanceLevel === 'low') {
            console.log('Low performance mode - 3D disabled');
            document.body.classList.add('no-webgl');
        }

        // Initialize Form Handler
        this.formHandler = new FormHandler('#contact-form');
        this.formHandler.init();
    }

    /**
     * Setup global event listeners
     */
    setupEventListeners() {
        // Visibility change (pause when tab is hidden)
        document.addEventListener('visibilitychange', this.onVisibilityChange);

        // Window resize
        window.addEventListener('resize', this.onResize.bind(this));

        // Error handling
        window.addEventListener('error', (e) => {
            console.error('Application error:', e.error);
        });
    }

    /**
     * Handle scroll updates
     */
    onScrollUpdate(progress, section) {
        if (this.sceneManager) {
            this.sceneManager.updateSections(progress, 0.016);
        }

        if (this.cameraController) {
            this.cameraController.updateFromScroll(progress, 0.016);
        }
    }

    /**
     * Main animation loop
     */
    animate(currentTime) {
        if (!this.isRunning) return;

        // Calculate delta time
        const deltaTime = currentTime - this.lastTime;

        // Limit frame rate if needed
        if (deltaTime >= this.frameInterval) {
            this.lastTime = currentTime - (deltaTime % this.frameInterval);
            const dt = Math.min(deltaTime / 1000, 0.1); // Convert to seconds, cap at 100ms

            // Update 3D scene
            if (this.sceneManager && this.cameraController) {
                const camera = this.cameraController.getCamera();

                // Update camera based on current scroll progress
                const progress = this.scrollAnimations ? this.scrollAnimations.getProgress() : 0;
                this.cameraController.updateFromScroll(progress, dt);
                this.sceneManager.updateSections(progress, dt);

                // Render
                this.sceneManager.render(camera);
            }
        }

        this.animationId = requestAnimationFrame(this.animate);
    }

    /**
     * Start the animation loop
     */
    start() {
        if (this.isRunning) return;

        this.isRunning = true;
        this.lastTime = performance.now();
        this.animationId = requestAnimationFrame(this.animate);

        // Start particle system
        if (this.particleSystem) {
            this.particleSystem.start();
        }
    }

    /**
     * Stop the animation loop
     */
    stop() {
        this.isRunning = false;

        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }

        // Stop particle system
        if (this.particleSystem) {
            this.particleSystem.stop();
        }
    }

    /**
     * Handle visibility change
     */
    onVisibilityChange() {
        if (document.hidden) {
            this.stop();
        } else {
            this.start();
        }
    }

    /**
     * Handle window resize
     */
    onResize() {
        // Scene manager and camera controller handle their own resize
        // This is for any additional resize handling
    }

    /**
     * Handle initialization errors
     */
    handleInitError(error) {
        // Hide loader
        const loader = document.getElementById('loader');
        if (loader) {
            loader.classList.add('hidden');
        }

        // Enable fallback mode
        document.body.classList.add('no-webgl');
        document.body.classList.add('low-performance');

        // Still initialize UI
        if (!this.uiManager) {
            this.uiManager = new UIManager();
            this.uiManager.init();
        }

        if (!this.formHandler) {
            this.formHandler = new FormHandler('#contact-form');
            this.formHandler.init();
        }
    }

    /**
     * Cleanup all resources
     */
    dispose() {
        this.stop();

        if (this.sceneManager) {
            this.sceneManager.dispose();
        }

        if (this.cameraController) {
            this.cameraController.dispose();
        }

        if (this.particleSystem) {
            this.particleSystem.dispose();
        }

        if (this.scrollAnimations) {
            this.scrollAnimations.dispose();
        }

        if (this.uiManager) {
            this.uiManager.dispose();
        }

        document.removeEventListener('visibilitychange', this.onVisibilityChange);
    }
}

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const app = new REXXRoofingApp();
    app.init();

    // Expose to global scope for debugging
    window.REXXApp = app;
});

// Handle page unload
window.addEventListener('beforeunload', () => {
    if (window.REXXApp) {
        window.REXXApp.dispose();
    }
});
