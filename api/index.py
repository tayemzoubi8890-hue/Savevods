from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def download():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "No URL"}), 400
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "url": info.get('url'),
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration_string')
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
