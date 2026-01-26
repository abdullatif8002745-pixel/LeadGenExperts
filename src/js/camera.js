/**
 * camera.js - Camera Controller
 * Handles camera positioning, movement, and scroll-based transitions
 */

export class CameraController {
    constructor() {
        this.camera = null;
        this.targetPosition = { x: 0, y: 0, z: 10 };
        this.targetRotation = { x: 0, y: 0, z: 0 };
        this.currentPosition = { x: 0, y: 0, z: 10 };
        this.currentRotation = { x: 0, y: 0, z: 0 };
        this.parallaxOffset = { x: 0, y: 0 };
        this.smoothness = 0.08;
        this.sectionCameraPositions = [];
        this.currentSection = 0;
        this.fov = 60;
    }

    /**
     * Initialize the camera
     */
    init() {
        this.camera = new THREE.PerspectiveCamera(
            this.fov,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );

        this.camera.position.set(0, 0, 10);
        this.camera.lookAt(0, 0, 0);

        // Define camera positions for each section
        this.sectionCameraPositions = [
            { // Hero
                position: { x: 0, y: 1, z: 12 },
                rotation: { x: -0.05, y: 0, z: 0 },
                lookAt: { x: 3, y: 0, z: -5 }
            },
            { // Services
                position: { x: 0, y: 0.5, z: 10 },
                rotation: { x: 0, y: 0, z: 0 },
                lookAt: { x: 0, y: 0, z: -50 }
            },
            { // About
                position: { x: -1, y: 0.5, z: 10 },
                rotation: { x: 0, y: 0.1, z: 0 },
                lookAt: { x: 2, y: 0, z: -100 }
            },
            { // Projects
                position: { x: 1, y: 0, z: 10 },
                rotation: { x: 0, y: -0.1, z: 0 },
                lookAt: { x: -1, y: 0, z: -150 }
            },
            { // Testimonials
                position: { x: 0, y: 0.5, z: 10 },
                rotation: { x: 0, y: 0, z: 0 },
                lookAt: { x: 0, y: 0, z: -200 }
            },
            { // Contact
                position: { x: 0, y: 1, z: 12 },
                rotation: { x: -0.05, y: 0, z: 0 },
                lookAt: { x: 2, y: 0, z: -250 }
            }
        ];

        // Handle window resize
        window.addEventListener('resize', () => this.onResize());

        // Handle mouse movement for parallax
        window.addEventListener('mousemove', (e) => this.onMouseMove(e));

        return this.camera;
    }

    /**
     * Update camera position based on scroll
     */
    updateFromScroll(scrollProgress, deltaTime) {
        const sectionCount = this.sectionCameraPositions.length;
        const sectionIndex = Math.min(
            Math.floor(scrollProgress * sectionCount),
            sectionCount - 1
        );
        const sectionProgress = (scrollProgress * sectionCount) % 1;

        // Get current and next section camera settings
        const currentSettings = this.sectionCameraPositions[sectionIndex];
        const nextSettings = this.sectionCameraPositions[Math.min(sectionIndex + 1, sectionCount - 1)];

        // Interpolate between sections
        this.targetPosition = {
            x: this.lerp(currentSettings.position.x, nextSettings.position.x, sectionProgress),
            y: this.lerp(currentSettings.position.y, nextSettings.position.y, sectionProgress),
            z: this.lerp(currentSettings.position.z, nextSettings.position.z, sectionProgress)
        };

        this.targetRotation = {
            x: this.lerp(currentSettings.rotation.x, nextSettings.rotation.x, sectionProgress),
            y: this.lerp(currentSettings.rotation.y, nextSettings.rotation.y, sectionProgress),
            z: this.lerp(currentSettings.rotation.z, nextSettings.rotation.z, sectionProgress)
        };

        // Apply parallax offset from mouse
        const parallaxStrength = 0.5;
        this.targetPosition.x += this.parallaxOffset.x * parallaxStrength;
        this.targetPosition.y += this.parallaxOffset.y * parallaxStrength * 0.5;

        // Smooth camera movement
        this.currentPosition.x += (this.targetPosition.x - this.currentPosition.x) * this.smoothness;
        this.currentPosition.y += (this.targetPosition.y - this.currentPosition.y) * this.smoothness;
        this.currentPosition.z += (this.targetPosition.z - this.currentPosition.z) * this.smoothness;

        this.currentRotation.x += (this.targetRotation.x - this.currentRotation.x) * this.smoothness;
        this.currentRotation.y += (this.targetRotation.y - this.currentRotation.y) * this.smoothness;
        this.currentRotation.z += (this.targetRotation.z - this.currentRotation.z) * this.smoothness;

        // Apply to camera
        if (this.camera) {
            this.camera.position.set(
                this.currentPosition.x,
                this.currentPosition.y,
                this.currentPosition.z
            );

            this.camera.rotation.set(
                this.currentRotation.x,
                this.currentRotation.y,
                this.currentRotation.z
            );

            // Calculate look-at target based on scroll
            const lookAtZ = -scrollProgress * 50 * 6;
            this.camera.lookAt(0, 0, lookAtZ);
        }

        this.currentSection = sectionIndex;
    }

    /**
     * Handle mouse movement for parallax effect
     */
    onMouseMove(event) {
        // Normalize mouse position to -1 to 1
        const x = (event.clientX / window.innerWidth) * 2 - 1;
        const y = -(event.clientY / window.innerHeight) * 2 + 1;

        // Smooth parallax offset
        this.parallaxOffset.x += (x - this.parallaxOffset.x) * 0.05;
        this.parallaxOffset.y += (y - this.parallaxOffset.y) * 0.05;
    }

    /**
     * Linear interpolation
     */
    lerp(start, end, t) {
        return start + (end - start) * this.easeInOutCubic(t);
    }

    /**
     * Easing function for smooth transitions
     */
    easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    /**
     * Handle window resize
     */
    onResize() {
        if (this.camera) {
            this.camera.aspect = window.innerWidth / window.innerHeight;
            this.camera.updateProjectionMatrix();
        }
    }

    /**
     * Get current camera
     */
    getCamera() {
        return this.camera;
    }

    /**
     * Set camera FOV
     */
    setFOV(fov) {
        this.fov = fov;
        if (this.camera) {
            this.camera.fov = fov;
            this.camera.updateProjectionMatrix();
        }
    }

    /**
     * Animate to a specific section
     */
    animateToSection(sectionIndex, duration = 1) {
        const settings = this.sectionCameraPositions[sectionIndex];
        if (!settings) return;

        // Use GSAP if available for smooth animation
        if (window.gsap) {
            gsap.to(this.targetPosition, {
                x: settings.position.x,
                y: settings.position.y,
                z: settings.position.z,
                duration: duration,
                ease: 'power3.out'
            });

            gsap.to(this.targetRotation, {
                x: settings.rotation.x,
                y: settings.rotation.y,
                z: settings.rotation.z,
                duration: duration,
                ease: 'power3.out'
            });
        }

        this.currentSection = sectionIndex;
    }

    /**
     * Add camera shake effect
     */
    shake(intensity = 0.1, duration = 0.5) {
        if (!window.gsap) return;

        const originalPosition = { ...this.currentPosition };

        gsap.to(this.currentPosition, {
            x: originalPosition.x + (Math.random() - 0.5) * intensity,
            y: originalPosition.y + (Math.random() - 0.5) * intensity,
            duration: 0.05,
            repeat: Math.floor(duration / 0.05),
            yoyo: true,
            ease: 'power1.inOut',
            onComplete: () => {
                this.currentPosition = { ...originalPosition };
            }
        });
    }

    /**
     * Cleanup
     */
    dispose() {
        window.removeEventListener('resize', this.onResize);
        window.removeEventListener('mousemove', this.onMouseMove);
    }
}
