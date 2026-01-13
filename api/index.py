from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import time

app = Flask(__name__)
CORS(app)

@app.route('/api/yt', methods=['GET'])
def get_video_data():
    start_time = time.time()
    url = request.args.get('url')

    if not url:
        return jsonify({"api_dev": "@MasumVai", "error": "URL missing!"}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # অডিও লিঙ্ক বাছাই
            audio_link = next((f['url'] for f in info.get('formats', []) 
                              if f.get('acodec') != 'none' and f.get('vcodec') == 'none'), info.get('url'))

            return jsonify({
                "api_dev": "@MasumVai",
                "api_channel": "@MasumVaiBD",
                "time_s": round(time.time() - start_time, 4),
                "title": info.get('title'),
                "data": {
                    "video": info.get('url'),
                    "audio": audio_link
                }
            }), 200

    except Exception as e:
        return jsonify({
            "api_dev": "@MasumVai",
            "status": "error",
            "message": str(e)
        }), 500

# Vercel এর জন্য এটি জরুরি
def handler(event, context):
    return app(event, context)
