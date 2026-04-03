from flask import Flask, request, jsonify, render_template
from starter_preprocess import TextPreprocessor

app = Flask(__name__)
preprocessor = TextPreprocessor()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/clean", methods=["POST"])
def clean_text():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Request body must be valid JSON."
            }), 400

        url = data.get("url", "").strip()
        if not url:
            return jsonify({
                "success": False,
                "error": "Please provide a Project Gutenberg .txt URL."
            }), 400

        raw_text = preprocessor.fetch_from_url(url)
        cleaned_text = preprocessor.clean_text(raw_text)
        statistics = preprocessor.get_text_statistics(cleaned_text)
        summary = preprocessor.create_summary(cleaned_text, 3)

        return jsonify({
            "success": True,
            "cleaned_text": cleaned_text,
            "statistics": statistics,
            "summary": summary
        }), 200

    except ValueError as exc:
        return jsonify({
            "success": False,
            "error": str(exc)
        }), 400

    except Exception as exc:
        return jsonify({
            "success": False,
            "error": str(exc)
        }), 500


@app.route("/api/analyze", methods=["POST"])
def analyze_text():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Request body must be valid JSON."
            }), 400

        text = data.get("text", "").strip()
        if not text:
            return jsonify({
                "success": False,
                "error": "Please provide text to analyze."
            }), 400

        cleaned_text = preprocessor.clean_text(text)
        statistics = preprocessor.get_text_statistics(cleaned_text)

        return jsonify({
            "success": True,
            "statistics": statistics
        }), 200

    except Exception as exc:
        return jsonify({
            "success": False,
            "error": str(exc)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)