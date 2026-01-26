/**
 * particles.js - Particle System
 * Creates floating white bubble particles in the background
 * Uses Canvas API for performance, with optional Three.js integration
 */

export class ParticleSystem {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = null;
        this.particles = [];
        this.particleCount = 50;
        this.animationId = null;
        this.isRunning = false;
        this.lastTime = 0;
        this.mousePosition = { x: 0, y: 0 };
        this.mouseInfluence = 0.05;

        // Performance settings
        this.targetFPS = 60;
        this.frameInterval = 1000 / this.targetFPS;
        this.useReducedMotion = false;

        // Bind methods
        this.animate = this.animate.bind(this);
        this.onResize = this.onResize.bind(this);
        this.onMouseMove = this.onMouseMove.bind(this);
    }

    /**
     * Initialize the particle system
     */
    init() {
        if (!this.canvas) {
            console.warn('Particle canvas not found');
            return false;
        }

        this.ctx = this.canvas.getContext('2d');
        if (!this.ctx) {
            console.warn('Canvas 2D context not available');
            return false;
        }

        // Check for reduced motion preference
        this.useReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (this.useReducedMotion) {
            this.particleCount = 20;
        }

        // Adjust particle count based on screen size
        this.adjustParticleCount();

        // Set canvas size
        this.onResize();

        // Create particles
        this.createParticles();

        // Event listeners
        window.addEventListener('resize', this.onResize);
        window.addEventListener('mousemove', this.onMouseMove);

        // Start animation
        this.start();

        return true;
    }

    /**
     * Adjust particle count based on screen size and device capability
     */
    adjustParticleCount() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        const area = width * height;

        // Base count on screen area
        let count = Math.floor(area / 40000);

        // Clamp between min and max
        count = Math.max(20, Math.min(count, 100));

        // Reduce for mobile devices
        if (width < 768) {
            count = Math.floor(count * 0.5);
        }

        // Further reduce if reduced motion is preferred
        if (this.useReducedMotion) {
            count = Math.floor(count * 0.5);
        }

        this.particleCount = count;
    }

    /**
     * Create particle instances
     */
    createParticles() {
        this.particles = [];

        for (let i = 0; i < this.particleCount; i++) {
            this.particles.push(this.createParticle());
        }
    }

    /**
     * Create a single particle
     */
    createParticle(startFromBottom = false) {
        const size = Math.random() * 4 + 2; // 2-6px
        const opacity = Math.random() * 0.3 + 0.1; // 0.1-0.4

        return {
            x: Math.random() * this.canvas.width,
            y: startFromBottom ? this.canvas.height + size : Math.random() * this.canvas.height,
            size: size,
            originalSize: size,
            opacity: opacity,
            originalOpacity: opacity,
            speedY: -(Math.random() * 0.5 + 0.2), // Upward movement
            speedX: (Math.random() - 0.5) * 0.3, // Slight horizontal drift
            wobbleSpeed: Math.random() * 0.02 + 0.01,
            wobbleAmount: Math.random() * 30 + 10,
            wobbleOffset: Math.random() * Math.PI * 2,
            pulseSpeed: Math.random() * 0.02 + 0.01,
            pulseOffset: Math.random() * Math.PI * 2
        };
    }

    /**
     * Update particle positions
     */
    updateParticles(deltaTime) {
        const time = performance.now() * 0.001;
        const dt = Math.min(deltaTime, 50); // Cap delta time to prevent jumps

        this.particles.forEach((particle, index) => {
            // Apply base movement
            particle.y += particle.speedY * dt * 0.1;
            particle.x += particle.speedX * dt * 0.1;

            // Apply wobble
            particle.x += Math.sin(time * particle.wobbleSpeed + particle.wobbleOffset) * 0.2;

            // Apply size pulsing
            const pulseFactor = Math.sin(time * particle.pulseSpeed + particle.pulseOffset);
            particle.size = particle.originalSize * (1 + pulseFactor * 0.2);

            // Apply opacity pulsing
            particle.opacity = particle.originalOpacity * (0.8 + pulseFactor * 0.2);

            // Mouse influence - particles move away from cursor
            const dx = particle.x - this.mousePosition.x;
            const dy = particle.y - this.mousePosition.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            const maxDistance = 150;

            if (distance < maxDistance) {
                const force = (1 - distance / maxDistance) * this.mouseInfluence;
                particle.x += dx * force;
                particle.y += dy * force;
            }

            // Reset particle when it goes off screen (top)
            if (particle.y < -particle.size * 2) {
                const newParticle = this.createParticle(true);
                this.particles[index] = newParticle;
            }

            // Wrap horizontally
            if (particle.x < -particle.size) {
                particle.x = this.canvas.width + particle.size;
            } else if (particle.x > this.canvas.width + particle.size) {
                particle.x = -particle.size;
            }
        });
    }

    /**
     * Render particles
     */
    renderParticles() {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw particles
        this.particles.forEach(particle => {
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);

            // Create gradient for each particle (bubble effect)
            const gradient = this.ctx.createRadialGradient(
                particle.x - particle.size * 0.3,
                particle.y - particle.size * 0.3,
                0,
                particle.x,
                particle.y,
                particle.size
            );

            gradient.addColorStop(0, `rgba(255, 255, 255, ${particle.opacity * 1.5})`);
            gradient.addColorStop(0.5, `rgba(255, 255, 255, ${particle.opacity})`);
            gradient.addColorStop(1, `rgba(255, 255, 255, ${particle.opacity * 0.3})`);

            this.ctx.fillStyle = gradient;
            this.ctx.fill();

            // Add subtle border for bubble effect
            this.ctx.strokeStyle = `rgba(255, 255, 255, ${particle.opacity * 0.5})`;
            this.ctx.lineWidth = 0.5;
            this.ctx.stroke();
        });
    }

    /**
     * Main animation loop
     */
    animate(currentTime) {
        if (!this.isRunning) return;

        // Calculate delta time
        const deltaTime = currentTime - this.lastTime;

        // Only update at target frame rate
        if (deltaTime >= this.frameInterval) {
            this.lastTime = currentTime - (deltaTime % this.frameInterval);

            // Update and render
            this.updateParticles(deltaTime);
            this.renderParticles();
        }

        this.animationId = requestAnimationFrame(this.animate);
    }

    /**
     * Start the particle animation
     */
    start() {
        if (this.isRunning) return;

        this.isRunning = true;
        this.lastTime = performance.now();
        this.animationId = requestAnimationFrame(this.animate);
    }

    /**
     * Stop the particle animation
     */
    stop() {
        this.isRunning = false;
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
    }

    /**
     * Handle window resize
     */
    onResize() {
        const dpr = Math.min(window.devicePixelRatio, 2);

        this.canvas.width = window.innerWidth * dpr;
        this.canvas.height = window.innerHeight * dpr;

        this.canvas.style.width = `${window.innerWidth}px`;
        this.canvas.style.height = `${window.innerHeight}px`;

        this.ctx.scale(dpr, dpr);

        // Recalculate particle count
        this.adjustParticleCount();

        // Reposition particles if needed
        if (this.particles.length !== this.particleCount) {
            const diff = this.particleCount - this.particles.length;
            if (diff > 0) {
                for (let i = 0; i < diff; i++) {
                    this.particles.push(this.createParticle());
                }
            } else {
                this.particles.splice(this.particleCount);
            }
        }
    }

    /**
     * Handle mouse movement
     */
    onMouseMove(event) {
        this.mousePosition.x = event.clientX;
        this.mousePosition.y = event.clientY;
    }

    /**
     * Set particle count
     */
    setParticleCount(count) {
        this.particleCount = count;
        this.createParticles();
    }

    /**
     * Set particle speed
     */
    setSpeed(multiplier) {
        this.particles.forEach(particle => {
            particle.speedY *= multiplier;
            particle.speedX *= multiplier;
        });
    }

    /**
     * Add burst of particles at position
     */
    burst(x, y, count = 10) {
        for (let i = 0; i < count; i++) {
            const angle = (Math.PI * 2 / count) * i;
            const speed = Math.random() * 2 + 1;

            const particle = this.createParticle();
            particle.x = x;
            particle.y = y;
            particle.speedX = Math.cos(angle) * speed;
            particle.speedY = Math.sin(angle) * speed - 1;
            particle.opacity = 0.5;
            particle.size = Math.random() * 3 + 2;

            this.particles.push(particle);
        }

        // Remove excess particles after a delay
        setTimeout(() => {
            this.particles.splice(this.particleCount, count);
        }, 2000);
    }

    /**
     * Cleanup
     */
    dispose() {
        this.stop();
        window.removeEventListener('resize', this.onResize);
        window.removeEventListener('mousemove', this.onMouseMove);
        this.particles = [];

        if (this.ctx) {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        }
    }
}

/**
 * Three.js Particle System (optional enhancement)
 * For when more advanced 3D particle effects are needed
 */
export class ThreeParticleSystem {
    constructor(scene) {
        this.scene = scene;
        this.particles = null;
        this.particleCount = 200;
        this.positions = null;
        this.velocities = [];
    }

    init() {
        if (!this.scene || typeof THREE === 'undefined') {
            return false;
        }

        const geometry = new THREE.BufferGeometry();
        this.positions = new Float32Array(this.particleCount * 3);
        const sizes = new Float32Array(this.particleCount);

        for (let i = 0; i < this.particleCount; i++) {
            const i3 = i * 3;
            this.positions[i3] = (Math.random() - 0.5) * 50;
            this.positions[i3 + 1] = Math.random() * 30 - 15;
            this.positions[i3 + 2] = (Math.random() - 0.5) * 50;

            sizes[i] = Math.random() * 0.5 + 0.1;

            this.velocities.push({
                x: (Math.random() - 0.5) * 0.01,
                y: Math.random() * 0.02 + 0.01,
                z: (Math.random() - 0.5) * 0.01
            });
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(this.positions, 3));
        geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

        const material = new THREE.PointsMaterial({
            color: 0xffffff,
            size: 0.2,
            transparent: true,
            opacity: 0.6,
            blending: THREE.AdditiveBlending,
            sizeAttenuation: true
        });

        this.particles = new THREE.Points(geometry, material);
        this.scene.add(this.particles);

        return true;
    }

    update(deltaTime) {
        if (!this.particles) return;

        for (let i = 0; i < this.particleCount; i++) {
            const i3 = i * 3;
            const vel = this.velocities[i];

            this.positions[i3] += vel.x;
            this.positions[i3 + 1] += vel.y;
            this.positions[i3 + 2] += vel.z;

            // Reset particles that go too high
            if (this.positions[i3 + 1] > 15) {
                this.positions[i3 + 1] = -15;
            }
        }

        this.particles.geometry.attributes.position.needsUpdate = true;
    }

    dispose() {
        if (this.particles) {
            this.particles.geometry.dispose();
            this.particles.material.dispose();
            this.scene.remove(this.particles);
        }
    }
}
