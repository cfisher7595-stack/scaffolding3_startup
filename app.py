"""
app.py
Flask web service for the warm-up assignment
"""

from flask import Flask, request, jsonify, render_template
from starter_preprocess import TextPreprocessor

app = Flask(__name__)
preprocessor = TextPreprocessor()


@app.route('/')
def home():
    """Render a simple HTML form for URL input"""
    return render_template('index.html')


@app.route('/api/clean', methods=['POST'])
def clean_text():
    """
    API endpoint that accepts a URL and returns cleaned text

    Expected JSON input:
    {"url": "https://www.gutenberg.org/files/1342/1342-0.txt"}

    Returns JSON:
    {
        "success": true/false,
        "cleaned_text": "...",
        "statistics": {...},
        "summary": "...",
        "error": "..." (if applicable)
    }
    """
    try:
        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'url' in request body."
            }), 400

        url = data["url"]

        raw_text = preprocessor.fetch_from_url(url)
        cleaned_text = preprocessor.clean_gutenberg_text(raw_text)
        normalized_text = preprocessor.normalize_text(cleaned_text, preserve_sentences=True)

        statistics = preprocessor.get_text_statistics(normalized_text)
        summary = preprocessor.create_summary(normalized_text, num_sentences=3)

        return jsonify({
            "success": True,
            "cleaned_text": normalized_text[:500],
            "statistics": statistics,
            "summary": summary
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """
    API endpoint that accepts raw text and returns statistics only

    Expected JSON input:
    {"text": "Your raw text here..."}

    Returns JSON:
    {
        "success": true/false,
        "statistics": {...},
        "error": "..." (if applicable)
    }
    """
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'text' in request body."
            }), 400

        text = data["text"]
        normalized_text = preprocessor.normalize_text(text, preserve_sentences=True)
        statistics = preprocessor.get_text_statistics(normalized_text)

        return jsonify({
            "success": True,
            "statistics": statistics
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    app.run(debug=True, port=5000, host='0.0.0.0')