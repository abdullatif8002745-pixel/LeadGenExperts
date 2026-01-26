# REXX Roofing LLC - 3D Interactive Website

A premium, production-ready 3D interactive website for REXX Roofing LLC featuring immersive scroll-based animations, particle effects, and a cinematic user experience.

## Features

- **3D Scroll Experience**: True depth-based section transitions using Three.js and WebGL
- **Particle System**: Floating white bubble particles in the background
- **GSAP Animations**: Smooth, performant scroll-triggered animations
- **Responsive Design**: Fully optimized for mobile, tablet, and desktop
- **Performance Optimized**: Automatic performance detection with fallbacks
- **Accessibility**: WCAG compliant with reduced motion support
- **SEO Ready**: Semantic HTML, meta tags, and structured data

## Tech Stack

- **Three.js**: 3D graphics and WebGL rendering
- **GSAP + ScrollTrigger**: Scroll-based animations
- **Vanilla JavaScript (ES6+)**: Modular architecture
- **CSS3**: Custom properties, animations, responsive design
- **HTML5**: Semantic markup

## Project Structure

```
src/
├── assets/
│   └── favicon.svg
├── models/          # 3D models (if needed)
├── textures/        # Texture files (if needed)
├── js/
│   ├── main.js           # Application entry point
│   ├── scene.js          # Three.js scene management
│   ├── camera.js         # Camera controls
│   ├── particles.js      # Particle system
│   ├── scrollAnimations.js # GSAP ScrollTrigger
│   └── ui.js             # UI components & forms
├── index.html       # Main HTML file
└── style.css        # All styles
```

## Quick Start

### Option 1: Using a Local Server (Recommended)

Due to ES6 modules, the project requires a local server:

**Using Python:**
```bash
cd src
python -m http.server 8000
# Visit http://localhost:8000
```

**Using Node.js (http-server):**
```bash
npm install -g http-server
cd src
http-server -p 8000
# Visit http://localhost:8000
```

**Using VS Code Live Server:**
1. Install the "Live Server" extension
2. Right-click on `src/index.html`
3. Select "Open with Live Server"

**Using PHP:**
```bash
cd src
php -S localhost:8000
# Visit http://localhost:8000
```

### Option 2: Using Node.js Development Server

```bash
# Install dependencies (if package.json exists)
npm install

# Start development server
npm run dev
```

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Performance Modes

The website automatically detects device capabilities and adjusts:

- **High Performance**: Full 3D effects, 60fps animations, max particles
- **Medium Performance**: Reduced particle count, optimized 3D
- **Low Performance**: 2D fallback mode, minimal animations

## Customization

### Colors
Edit CSS variables in `style.css`:
```css
:root {
    --color-black: #000000;
    --color-yellow: #FFD400;
    --color-white: #FFFFFF;
}
```

### Content
Update section content directly in `index.html`. All text is editable without touching the JavaScript.

### 3D Elements
Modify `scene.js` to customize:
- Section-specific 3D models
- Lighting setup
- Material properties

## Sections

1. **Hero**: Company intro with 3D house model
2. **Services**: Residential, Commercial, Repair, Inspection
3. **About**: Company story and features
4. **Projects**: Filterable project gallery
5. **Testimonials**: Customer reviews slider
6. **Contact**: Form with validation + Google Maps

## Form Handling

The contact form includes:
- Real-time validation
- Phone number formatting
- Loading states
- Success/error messages

To connect to a real backend, modify `FormHandler.simulateSubmission()` in `ui.js`.

## SEO

The website includes:
- Semantic HTML5 structure
- Meta tags (description, keywords, Open Graph, Twitter)
- Schema.org Local Business markup
- Optimized for roofing business search terms

## Accessibility

- Skip to main content link
- ARIA labels and roles
- Keyboard navigation
- Reduced motion support
- High contrast color scheme
- Focus indicators

## License

Proprietary - REXX Roofing LLC

## Support

For technical support or customization requests, contact the development team.

---

Built with precision and expertise, just like a REXX roof.
