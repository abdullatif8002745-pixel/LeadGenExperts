// HTML to Video Converter - Main Application Logic

class HTMLToVideoConverter {
    constructor() {
        this.initElements();
        this.initEventListeners();
        this.recordedBlob = null;
        this.isRecording = false;
    }

    initElements() {
        // Editor elements
        this.htmlInput = document.getElementById('htmlInput');
        this.renderBtn = document.getElementById('renderBtn');
        this.loadSampleBtn = document.getElementById('loadSampleBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.previewFrame = document.getElementById('previewFrame');
        this.dimensionsInfo = document.getElementById('dimensionsInfo');

        // Video settings
        this.videoDuration = document.getElementById('videoDuration');
        this.frameRate = document.getElementById('frameRate');
        this.videoWidth = document.getElementById('videoWidth');
        this.videoHeight = document.getElementById('videoHeight');
        this.animationType = document.getElementById('animationType');
        this.quality = document.getElementById('quality');

        // Recording elements
        this.recordBtn = document.getElementById('recordBtn');
        this.recordingStatus = document.getElementById('recordingStatus');
        this.recordingProgress = document.getElementById('recordingProgress');

        // Download elements
        this.downloadSection = document.getElementById('downloadSection');
        this.downloadMp4 = document.getElementById('downloadMp4');
        this.downloadMov = document.getElementById('downloadMov');
        this.videoPreview = document.getElementById('videoPreview');

        // Canvas
        this.renderCanvas = document.getElementById('renderCanvas');
    }

    initEventListeners() {
        this.renderBtn.addEventListener('click', () => this.renderPreview());
        this.loadSampleBtn.addEventListener('click', () => this.loadSample());
        this.clearBtn.addEventListener('click', () => this.clearEditor());
        this.recordBtn.addEventListener('click', () => this.startRecording());
        this.downloadMp4.addEventListener('click', () => this.downloadVideo('mp4'));
        this.downloadMov.addEventListener('click', () => this.downloadVideo('mov'));

        // Update dimensions display when width/height change
        this.videoWidth.addEventListener('change', () => this.updateDimensionsInfo());
        this.videoHeight.addEventListener('change', () => this.updateDimensionsInfo());
    }

    loadSample() {
        const sampleHTML = `<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 200vh;
            padding: 40px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        .card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            font-size: 3rem;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }
        h2 {
            color: #333;
            margin-bottom: 15px;
        }
        p {
            color: #666;
            line-height: 1.8;
            margin-bottom: 15px;
        }
        .feature-list {
            list-style: none;
            padding: 20px 0;
        }
        .feature-list li {
            padding: 15px 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
            margin-bottom: 10px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .feature-list li::before {
            content: "✨";
            font-size: 1.5rem;
        }
        .cta-button {
            display: inline-block;
            padding: 18px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            font-size: 1.2rem;
            margin-top: 20px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 30px;
        }
        .stat-box {
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            color: white;
        }
        .stat-number {
            font-size: 2.5rem;
            font-weight: bold;
        }
        .stat-label {
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>Welcome to Our Platform</h1>
            <p>Transform your ideas into reality with our powerful tools and services. We help businesses grow and succeed in the digital age.</p>
            <a href="#" class="cta-button">Get Started Today</a>
        </div>

        <div class="card">
            <h2>Why Choose Us?</h2>
            <ul class="feature-list">
                <li>Lightning-fast performance</li>
                <li>24/7 Customer Support</li>
                <li>Easy to Use Interface</li>
                <li>Secure & Reliable</li>
                <li>Affordable Pricing</li>
            </ul>
        </div>

        <div class="card">
            <h2>Our Impact</h2>
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">10K+</div>
                    <div class="stat-label">Happy Clients</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">500+</div>
                    <div class="stat-label">Projects</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">99%</div>
                    <div class="stat-label">Satisfaction</div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>Contact Us</h2>
            <p>Ready to start your journey? Get in touch with us today and let's create something amazing together!</p>
            <p>Email: hello@example.com</p>
            <p>Phone: +1 (555) 123-4567</p>
        </div>
    </div>
</body>
</html>`;
        this.htmlInput.value = sampleHTML;
    }

    clearEditor() {
        this.htmlInput.value = '';
        this.previewFrame.innerHTML = `
            <div class="placeholder-text">
                <span>📝</span>
                <p>Enter HTML code and click "Render Preview"</p>
            </div>
        `;
        this.recordBtn.disabled = true;
        this.downloadSection.classList.add('hidden');
        this.dimensionsInfo.textContent = '--';
    }

    renderPreview() {
        const htmlContent = this.htmlInput.value.trim();
        if (!htmlContent) {
            alert('Please enter some HTML code first!');
            return;
        }

        // Create an iframe for isolated rendering
        this.previewFrame.innerHTML = '';
        const iframe = document.createElement('iframe');
        iframe.style.width = '100%';
        iframe.style.height = '100%';
        iframe.style.minHeight = '400px';
        iframe.style.border = 'none';
        iframe.style.background = 'white';

        this.previewFrame.appendChild(iframe);

        // Write content to iframe
        const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        iframeDoc.open();
        iframeDoc.write(htmlContent);
        iframeDoc.close();

        // Enable recording after preview is rendered
        this.recordBtn.disabled = false;
        this.updateDimensionsInfo();
    }

    updateDimensionsInfo() {
        const width = this.videoWidth.value;
        const height = this.videoHeight.value;
        this.dimensionsInfo.textContent = `Output: ${width} x ${height}px`;
    }

    async startRecording() {
        if (this.isRecording) return;

        const htmlContent = this.htmlInput.value.trim();
        if (!htmlContent) {
            alert('Please render a preview first!');
            return;
        }

        this.isRecording = true;
        this.recordBtn.disabled = true;
        this.recordBtn.classList.add('recording');
        this.recordingStatus.classList.remove('hidden');
        this.downloadSection.classList.add('hidden');

        try {
            await this.recordVideo(htmlContent);
        } catch (error) {
            console.error('Recording error:', error);
            alert('An error occurred during recording: ' + error.message);
        } finally {
            this.isRecording = false;
            this.recordBtn.disabled = false;
            this.recordBtn.classList.remove('recording');
            this.recordingStatus.classList.add('hidden');
        }
    }

    async recordVideo(htmlContent) {
        const width = parseInt(this.videoWidth.value);
        const height = parseInt(this.videoHeight.value);
        const fps = parseInt(this.frameRate.value);
        const duration = parseInt(this.videoDuration.value);
        const animationType = this.animationType.value;
        const qualityValue = parseFloat(this.quality.value);

        const totalFrames = fps * duration;
        const canvas = this.renderCanvas;
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');

        // Create an offscreen container for rendering
        const container = document.createElement('div');
        container.style.cssText = `
            position: fixed;
            left: -9999px;
            top: 0;
            width: ${width}px;
            background: white;
            overflow: hidden;
        `;
        document.body.appendChild(container);

        // Create iframe for HTML content
        const iframe = document.createElement('iframe');
        iframe.style.cssText = `
            width: ${width}px;
            height: ${height}px;
            border: none;
            background: white;
        `;
        container.appendChild(iframe);

        // Write HTML content
        const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        iframeDoc.open();
        iframeDoc.write(htmlContent);
        iframeDoc.close();

        // Wait for content to load
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Get the scrollable height
        const scrollHeight = iframeDoc.documentElement.scrollHeight;
        const maxScroll = Math.max(0, scrollHeight - height);

        // Set up MediaRecorder with canvas stream
        const stream = canvas.captureStream(fps);

        // Try different codecs
        let mimeType = 'video/webm;codecs=vp9';
        if (!MediaRecorder.isTypeSupported(mimeType)) {
            mimeType = 'video/webm;codecs=vp8';
        }
        if (!MediaRecorder.isTypeSupported(mimeType)) {
            mimeType = 'video/webm';
        }

        const mediaRecorder = new MediaRecorder(stream, {
            mimeType: mimeType,
            videoBitsPerSecond: 8000000 * qualityValue
        });

        const chunks = [];
        mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) {
                chunks.push(e.data);
            }
        };

        // Start recording
        mediaRecorder.start(100);

        // Render frames
        for (let frame = 0; frame < totalFrames; frame++) {
            const progress = frame / totalFrames;
            this.recordingProgress.textContent = Math.round(progress * 100) + '%';

            // Apply animation
            await this.applyAnimation(iframe, iframeDoc, animationType, progress, maxScroll, height);

            // Capture frame using html2canvas
            try {
                const captureCanvas = await html2canvas(iframeDoc.body, {
                    width: width,
                    height: height,
                    windowWidth: width,
                    windowHeight: height,
                    scale: 1,
                    useCORS: true,
                    logging: false,
                    backgroundColor: '#ffffff'
                });

                // Draw to main canvas
                ctx.clearRect(0, 0, width, height);
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, width, height);
                ctx.drawImage(captureCanvas, 0, 0, width, height);

            } catch (e) {
                console.warn('Frame capture warning:', e);
                // Draw a fallback frame
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, width, height);
            }

            // Wait for next frame
            await new Promise(resolve => setTimeout(resolve, 1000 / fps));
        }

        // Stop recording
        mediaRecorder.stop();

        // Wait for recording to complete
        await new Promise(resolve => {
            mediaRecorder.onstop = resolve;
        });

        // Clean up
        document.body.removeChild(container);

        // Create blob
        this.recordedBlob = new Blob(chunks, { type: mimeType });

        // Show download section and video preview
        this.downloadSection.classList.remove('hidden');
        this.videoPreview.src = URL.createObjectURL(this.recordedBlob);

        this.recordingProgress.textContent = '100%';
    }

    async applyAnimation(iframe, iframeDoc, type, progress, maxScroll, viewportHeight) {
        const body = iframeDoc.body;

        switch (type) {
            case 'scroll':
                // Scroll from top to bottom
                iframeDoc.documentElement.scrollTop = maxScroll * progress;
                break;

            case 'scrollUp':
                // Scroll from bottom to top
                iframeDoc.documentElement.scrollTop = maxScroll * (1 - progress);
                break;

            case 'zoomIn':
                // Zoom in effect
                const scaleIn = 0.8 + (0.2 * progress);
                body.style.transform = `scale(${scaleIn})`;
                body.style.transformOrigin = 'center top';
                break;

            case 'zoomOut':
                // Zoom out effect
                const scaleOut = 1 + (0.2 * (1 - progress));
                body.style.transform = `scale(${scaleOut})`;
                body.style.transformOrigin = 'center top';
                break;

            case 'fadeIn':
                // Fade in effect
                body.style.opacity = progress;
                break;

            case 'static':
            default:
                // No animation
                break;
        }
    }

    downloadVideo(format) {
        if (!this.recordedBlob) {
            alert('No video recorded yet!');
            return;
        }

        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        let filename, mimeType;

        if (format === 'mp4') {
            // Note: WebM is the native format, but we'll name it MP4
            // For true MP4 conversion, server-side processing would be needed
            filename = `html-video-${timestamp}.webm`;
            mimeType = 'video/webm';

            // Show info about format
            this.showFormatInfo('mp4');
        } else if (format === 'mov') {
            filename = `html-video-${timestamp}.webm`;
            mimeType = 'video/webm';

            // Show info about format
            this.showFormatInfo('mov');
        }

        // Create download link
        const url = URL.createObjectURL(this.recordedBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    showFormatInfo(requestedFormat) {
        // Show a one-time info message about browser video format limitations
        const key = 'formatInfoShown';
        if (sessionStorage.getItem(key)) return;

        sessionStorage.setItem(key, 'true');

        const message = `Note: Browser-based recording produces WebM format.
For ${requestedFormat.toUpperCase()} conversion, you can use:
- VLC Media Player (free)
- HandBrake (free)
- CloudConvert (online)
- FFmpeg (command line)

The downloaded file will play in most modern video players.`;

        setTimeout(() => alert(message), 500);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.converter = new HTMLToVideoConverter();
});
