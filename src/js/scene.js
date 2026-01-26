/**
 * scene.js - Three.js Scene Manager
 * Handles 3D scene setup, lighting, and section groups
 */

export class SceneManager {
    constructor() {
        this.scene = null;
        this.renderer = null;
        this.sectionGroups = [];
        this.lights = {};
        this.isWebGLAvailable = this.checkWebGL();
        this.currentSection = 0;
        this.targetSection = 0;
        this.animationProgress = 0;
    }

    /**
     * Check WebGL availability
     */
    checkWebGL() {
        try {
            const canvas = document.createElement('canvas');
            return !!(window.WebGLRenderingContext &&
                (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
        } catch (e) {
            return false;
        }
    }

    /**
     * Initialize the Three.js scene
     */
    init(canvas) {
        if (!this.isWebGLAvailable) {
            console.warn('WebGL not available, using fallback');
            document.body.classList.add('no-webgl');
            return false;
        }

        // Create scene
        this.scene = new THREE.Scene();
        this.scene.fog = new THREE.Fog(0x000000, 10, 100);

        // Create renderer
        this.renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            antialias: true,
            alpha: true,
            powerPreference: 'high-performance'
        });

        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1;

        // Setup lights
        this.setupLights();

        // Create section groups
        this.createSectionGroups();

        // Handle resize
        window.addEventListener('resize', () => this.onResize());

        return true;
    }

    /**
     * Setup scene lighting
     */
    setupLights() {
        // Ambient light for base illumination
        this.lights.ambient = new THREE.AmbientLight(0xffffff, 0.3);
        this.scene.add(this.lights.ambient);

        // Main directional light (sun-like)
        this.lights.directional = new THREE.DirectionalLight(0xffffff, 1);
        this.lights.directional.position.set(10, 20, 10);
        this.lights.directional.castShadow = true;
        this.lights.directional.shadow.mapSize.width = 2048;
        this.lights.directional.shadow.mapSize.height = 2048;
        this.lights.directional.shadow.camera.near = 0.5;
        this.lights.directional.shadow.camera.far = 50;
        this.lights.directional.shadow.camera.left = -20;
        this.lights.directional.shadow.camera.right = 20;
        this.lights.directional.shadow.camera.top = 20;
        this.lights.directional.shadow.camera.bottom = -20;
        this.scene.add(this.lights.directional);

        // Yellow accent light
        this.lights.accent = new THREE.PointLight(0xFFD400, 0.8, 30);
        this.lights.accent.position.set(-5, 5, 5);
        this.scene.add(this.lights.accent);

        // Fill light
        this.lights.fill = new THREE.PointLight(0xffffff, 0.3, 50);
        this.lights.fill.position.set(5, -5, -5);
        this.scene.add(this.lights.fill);
    }

    /**
     * Create 3D groups for each section
     */
    createSectionGroups() {
        const sectionCount = 6;
        const sectionDepth = 50; // Distance between sections in Z-axis

        for (let i = 0; i < sectionCount; i++) {
            const group = new THREE.Group();
            group.position.z = -i * sectionDepth;
            group.userData = {
                sectionIndex: i,
                initialZ: -i * sectionDepth
            };

            // Add section-specific 3D elements
            this.addSectionContent(group, i);

            this.scene.add(group);
            this.sectionGroups.push(group);
        }
    }

    /**
     * Add 3D content to each section group
     */
    addSectionContent(group, sectionIndex) {
        switch (sectionIndex) {
            case 0: // Hero - 3D House/Roof
                this.createHeroContent(group);
                break;
            case 1: // Services - Floating icons
                this.createServicesContent(group);
                break;
            case 2: // About - Abstract shapes
                this.createAboutContent(group);
                break;
            case 3: // Projects - Photo frames
                this.createProjectsContent(group);
                break;
            case 4: // Testimonials - Quote marks
                this.createTestimonialsContent(group);
                break;
            case 5: // Contact - Location pin
                this.createContactContent(group);
                break;
        }
    }

    /**
     * Hero section 3D content - Stylized house with roof
     */
    createHeroContent(group) {
        // House base
        const houseGeometry = new THREE.BoxGeometry(4, 3, 4);
        const houseMaterial = new THREE.MeshStandardMaterial({
            color: 0x1a1a1a,
            metalness: 0.3,
            roughness: 0.7
        });
        const house = new THREE.Mesh(houseGeometry, houseMaterial);
        house.position.set(6, -1, -5);
        house.castShadow = true;
        house.receiveShadow = true;
        group.add(house);

        // Roof
        const roofGeometry = new THREE.ConeGeometry(3.5, 2, 4);
        const roofMaterial = new THREE.MeshStandardMaterial({
            color: 0xFFD400,
            metalness: 0.5,
            roughness: 0.3,
            emissive: 0xFFD400,
            emissiveIntensity: 0.1
        });
        const roof = new THREE.Mesh(roofGeometry, roofMaterial);
        roof.position.set(6, 1.5, -5);
        roof.rotation.y = Math.PI / 4;
        roof.castShadow = true;
        group.add(roof);

        // Floating geometric accents
        const accentGeometry = new THREE.OctahedronGeometry(0.5);
        const accentMaterial = new THREE.MeshStandardMaterial({
            color: 0xFFD400,
            metalness: 0.8,
            roughness: 0.2,
            emissive: 0xFFD400,
            emissiveIntensity: 0.2
        });

        for (let i = 0; i < 5; i++) {
            const accent = new THREE.Mesh(accentGeometry, accentMaterial);
            accent.position.set(
                5 + Math.random() * 4 - 2,
                Math.random() * 4 - 1,
                -3 + Math.random() * -4
            );
            accent.scale.setScalar(0.3 + Math.random() * 0.4);
            accent.userData.floatOffset = Math.random() * Math.PI * 2;
            accent.userData.floatSpeed = 0.5 + Math.random() * 0.5;
            group.add(accent);
        }

        // Ground plane
        const groundGeometry = new THREE.PlaneGeometry(20, 20);
        const groundMaterial = new THREE.MeshStandardMaterial({
            color: 0x0a0a0a,
            metalness: 0.9,
            roughness: 0.5
        });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.position.set(6, -2.5, -5);
        ground.receiveShadow = true;
        group.add(ground);
    }

    /**
     * Services section 3D content
     */
    createServicesContent(group) {
        // Create floating service icons
        const iconPositions = [
            { x: -6, y: 1, z: -3 },
            { x: -2, y: 2, z: -5 },
            { x: 2, y: 0, z: -4 },
            { x: 6, y: 1.5, z: -6 }
        ];

        const iconMaterial = new THREE.MeshStandardMaterial({
            color: 0xFFD400,
            metalness: 0.7,
            roughness: 0.3,
            emissive: 0xFFD400,
            emissiveIntensity: 0.15
        });

        iconPositions.forEach((pos, i) => {
            let geometry;
            switch (i % 4) {
                case 0:
                    geometry = new THREE.BoxGeometry(1.5, 1.5, 1.5);
                    break;
                case 1:
                    geometry = new THREE.ConeGeometry(0.8, 1.5, 4);
                    break;
                case 2:
                    geometry = new THREE.TorusGeometry(0.6, 0.2, 16, 32);
                    break;
                case 3:
                    geometry = new THREE.IcosahedronGeometry(0.8);
                    break;
            }

            const mesh = new THREE.Mesh(geometry, iconMaterial);
            mesh.position.set(pos.x, pos.y, pos.z);
            mesh.userData.floatOffset = i * (Math.PI / 2);
            mesh.userData.rotationSpeed = 0.3 + Math.random() * 0.3;
            mesh.castShadow = true;
            group.add(mesh);
        });
    }

    /**
     * About section 3D content
     */
    createAboutContent(group) {
        // Abstract geometric composition
        const shapes = [];
        const shapeMaterial = new THREE.MeshStandardMaterial({
            color: 0x2a2a2a,
            metalness: 0.5,
            roughness: 0.5
        });

        const yellowMaterial = new THREE.MeshStandardMaterial({
            color: 0xFFD400,
            metalness: 0.8,
            roughness: 0.2,
            emissive: 0xFFD400,
            emissiveIntensity: 0.1
        });

        // Large abstract shapes
        const torusKnot = new THREE.Mesh(
            new THREE.TorusKnotGeometry(1.5, 0.4, 100, 16),
            yellowMaterial
        );
        torusKnot.position.set(7, 0, -5);
        torusKnot.userData.rotationSpeed = 0.2;
        group.add(torusKnot);

        // Supporting shapes
        for (let i = 0; i < 8; i++) {
            const size = 0.3 + Math.random() * 0.5;
            const geometry = new THREE.BoxGeometry(size, size, size);
            const mesh = new THREE.Mesh(geometry, i % 3 === 0 ? yellowMaterial : shapeMaterial);
            mesh.position.set(
                5 + Math.random() * 6 - 3,
                Math.random() * 4 - 2,
                -3 + Math.random() * -6
            );
            mesh.rotation.set(
                Math.random() * Math.PI,
                Math.random() * Math.PI,
                Math.random() * Math.PI
            );
            mesh.userData.floatOffset = Math.random() * Math.PI * 2;
            group.add(mesh);
        }
    }

    /**
     * Projects section 3D content
     */
    createProjectsContent(group) {
        // Create floating photo frame representations
        const frameMaterial = new THREE.MeshStandardMaterial({
            color: 0x1a1a1a,
            metalness: 0.3,
            roughness: 0.7
        });

        const imageMaterial = new THREE.MeshStandardMaterial({
            color: 0x2a2a2a,
            metalness: 0.1,
            roughness: 0.9
        });

        const positions = [
            { x: 6, y: 1, z: -4, ry: -0.2 },
            { x: 8, y: -0.5, z: -6, ry: 0.3 },
            { x: 4, y: 0.5, z: -8, ry: -0.1 }
        ];

        positions.forEach((pos, i) => {
            // Frame
            const frameGroup = new THREE.Group();

            const frame = new THREE.Mesh(
                new THREE.BoxGeometry(3, 2.2, 0.15),
                frameMaterial
            );
            frameGroup.add(frame);

            // Inner image area
            const image = new THREE.Mesh(
                new THREE.BoxGeometry(2.6, 1.8, 0.1),
                imageMaterial
            );
            image.position.z = 0.03;
            frameGroup.add(image);

            // Yellow accent line
            const accentLine = new THREE.Mesh(
                new THREE.BoxGeometry(2.6, 0.05, 0.16),
                new THREE.MeshStandardMaterial({
                    color: 0xFFD400,
                    emissive: 0xFFD400,
                    emissiveIntensity: 0.3
                })
            );
            accentLine.position.y = -0.95;
            frameGroup.add(accentLine);

            frameGroup.position.set(pos.x, pos.y, pos.z);
            frameGroup.rotation.y = pos.ry;
            frameGroup.userData.floatOffset = i * Math.PI / 3;
            group.add(frameGroup);
        });
    }

    /**
     * Testimonials section 3D content
     */
    createTestimonialsContent(group) {
        // Create quote mark shapes
        const quoteMaterial = new THREE.MeshStandardMaterial({
            color: 0xFFD400,
            metalness: 0.6,
            roughness: 0.3,
            emissive: 0xFFD400,
            emissiveIntensity: 0.2
        });

        // Create stylized quote marks using spheres
        const createQuoteMark = (x, y, z, scale) => {
            const quoteGroup = new THREE.Group();

            const sphere1 = new THREE.Mesh(
                new THREE.SphereGeometry(0.5, 32, 32),
                quoteMaterial
            );
            sphere1.position.set(0, 0, 0);
            quoteGroup.add(sphere1);

            const sphere2 = new THREE.Mesh(
                new THREE.SphereGeometry(0.3, 32, 32),
                quoteMaterial
            );
            sphere2.position.set(-0.3, -0.7, 0);
            quoteGroup.add(sphere2);

            quoteGroup.position.set(x, y, z);
            quoteGroup.scale.setScalar(scale);
            quoteGroup.userData.floatOffset = Math.random() * Math.PI * 2;
            return quoteGroup;
        };

        group.add(createQuoteMark(-5, 2, -4, 1.5));
        group.add(createQuoteMark(-4, 2, -4, 1.5));
        group.add(createQuoteMark(7, -1, -6, 1));
        group.add(createQuoteMark(8, -1, -6, 1));

        // Add floating stars
        const starMaterial = new THREE.MeshStandardMaterial({
            color: 0xFFD400,
            metalness: 0.9,
            roughness: 0.1,
            emissive: 0xFFD400,
            emissiveIntensity: 0.3
        });

        for (let i = 0; i < 5; i++) {
            const star = new THREE.Mesh(
                new THREE.OctahedronGeometry(0.2),
                starMaterial
            );
            star.position.set(
                -3 + i * 0.5,
                3,
                -5
            );
            star.userData.floatOffset = i * 0.5;
            group.add(star);
        }
    }

    /**
     * Contact section 3D content
     */
    createContactContent(group) {
        // Location pin
        const pinMaterial = new THREE.MeshStandardMaterial({
            color: 0xFFD400,
            metalness: 0.7,
            roughness: 0.3,
            emissive: 0xFFD400,
            emissiveIntensity: 0.15
        });

        // Pin body (teardrop shape using sphere + cone)
        const pinGroup = new THREE.Group();

        const pinSphere = new THREE.Mesh(
            new THREE.SphereGeometry(1, 32, 32),
            pinMaterial
        );
        pinSphere.position.y = 1;
        pinGroup.add(pinSphere);

        const pinCone = new THREE.Mesh(
            new THREE.ConeGeometry(1, 2, 32),
            pinMaterial
        );
        pinCone.rotation.x = Math.PI;
        pinCone.position.y = -0.5;
        pinGroup.add(pinCone);

        // Inner circle
        const innerCircle = new THREE.Mesh(
            new THREE.SphereGeometry(0.4, 32, 32),
            new THREE.MeshStandardMaterial({
                color: 0x000000,
                metalness: 0.9,
                roughness: 0.1
            })
        );
        innerCircle.position.y = 1;
        innerCircle.position.z = 0.7;
        pinGroup.add(innerCircle);

        pinGroup.position.set(7, 0, -5);
        pinGroup.scale.setScalar(0.8);
        pinGroup.userData.floatOffset = 0;
        group.add(pinGroup);

        // Decorative rings
        const ringMaterial = new THREE.MeshStandardMaterial({
            color: 0x2a2a2a,
            metalness: 0.5,
            roughness: 0.5,
            transparent: true,
            opacity: 0.5
        });

        for (let i = 0; i < 3; i++) {
            const ring = new THREE.Mesh(
                new THREE.TorusGeometry(1.5 + i * 0.5, 0.05, 16, 64),
                ringMaterial
            );
            ring.rotation.x = Math.PI / 2;
            ring.position.set(7, -1.5, -5);
            ring.userData.ringIndex = i;
            group.add(ring);
        }
    }

    /**
     * Update section positions based on scroll
     */
    updateSections(scrollProgress, deltaTime) {
        const sectionDepth = 50;

        this.sectionGroups.forEach((group, index) => {
            const targetZ = group.userData.initialZ + scrollProgress * sectionDepth * 6;
            const targetOpacity = 1 - Math.abs(targetZ) / (sectionDepth * 2);

            // Smooth transition
            group.position.z += (targetZ - group.position.z) * 0.1;

            // Animate children
            group.children.forEach(child => {
                // Floating animation
                if (child.userData.floatOffset !== undefined) {
                    const time = performance.now() * 0.001;
                    const floatSpeed = child.userData.floatSpeed || 1;
                    child.position.y += Math.sin(time * floatSpeed + child.userData.floatOffset) * 0.002;
                }

                // Rotation animation
                if (child.userData.rotationSpeed !== undefined) {
                    child.rotation.y += child.userData.rotationSpeed * deltaTime;
                    child.rotation.x += child.userData.rotationSpeed * 0.5 * deltaTime;
                }

                // Ring pulsing
                if (child.userData.ringIndex !== undefined) {
                    const time = performance.now() * 0.001;
                    const scale = 1 + Math.sin(time * 2 + child.userData.ringIndex) * 0.1;
                    child.scale.set(scale, scale, 1);
                }
            });
        });
    }

    /**
     * Render the scene
     */
    render(camera) {
        if (this.renderer && this.scene && camera) {
            this.renderer.render(this.scene, camera);
        }
    }

    /**
     * Handle window resize
     */
    onResize() {
        if (this.renderer) {
            this.renderer.setSize(window.innerWidth, window.innerHeight);
            this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        }
    }

    /**
     * Cleanup resources
     */
    dispose() {
        if (this.renderer) {
            this.renderer.dispose();
        }

        this.sectionGroups.forEach(group => {
            group.traverse(child => {
                if (child.geometry) child.geometry.dispose();
                if (child.material) {
                    if (Array.isArray(child.material)) {
                        child.material.forEach(m => m.dispose());
                    } else {
                        child.material.dispose();
                    }
                }
            });
        });
    }
}
