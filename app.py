from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from scraper import scrape_url
from sheets_integration import save_to_sheets
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store scraping status
scraping_status = {}


def scrape_and_save(url, job_id):
    """Background task to scrape and save to Google Sheets"""
    try:
        scraping_status[job_id] = {'status': 'processing', 'message': 'Scraping website...'}

        # Scrape the website
        scraped_data = scrape_url(url)

        scraping_status[job_id] = {'status': 'processing', 'message': 'Saving to Google Sheets...'}

        # Save to Google Sheets
        success = save_to_sheets(scraped_data)

        if success:
            scraping_status[job_id] = {
                'status': 'completed',
                'message': 'Data successfully saved to Google Sheets!',
                'data': {
                    'company_name': scraped_data.get('company_name', 'Not Found')
                }
            }
        else:
            scraping_status[job_id] = {
                'status': 'error',
                'message': 'Failed to save data to Google Sheets'
            }

    except Exception as e:
        scraping_status[job_id] = {
            'status': 'error',
            'message': f'Error: {str(e)}'
        }


@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')


@app.route('/api/scrape', methods=['POST'])
def scrape():
    """API endpoint to scrape a website"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Generate a job ID
        import uuid
        job_id = str(uuid.uuid4())

        # Start background scraping task
        thread = threading.Thread(target=scrape_and_save, args=(url, job_id))
        thread.daemon = True
        thread.start()

        return jsonify({
            'message': 'Scraping started',
            'job_id': job_id
        }), 202

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status/<job_id>', methods=['GET'])
def get_status(job_id):
    """Get the status of a scraping job"""
    if job_id in scraping_status:
        return jsonify(scraping_status[job_id])
    else:
        return jsonify({'status': 'not_found', 'message': 'Job not found'}), 404


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)

    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
