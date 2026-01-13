from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import time

app = Flask(__name__)
CORS(app)

@app.route('/api/yt', methods=['GET'])
def youtube_api():
    start_time = time.time()
    video_url = request.args.get('url')

    if not video_url:
        return jsonify({"error": "URL missing! Please provide a YouTube link."}), 400

    try:
        # yt-dlp configuration
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'cachedir': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video info
            info = ydl.extract_info(video_url, download=False)
            
            # Filter for a direct audio link if possible
            audio_url = None
            if 'formats' in info:
                for f in info['formats']:
                    if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                        audio_url = f.get('url')
                        break
            
            # If no separate audio, use the main URL
            if not audio_url:
                audio_url = info.get('url')

            # Your Custom Response Format
            response = {
                "api_dev": "@MasumVai",
                "api_channel": "@MasumVaiBD",
                "time_s": round(time.time() - start_time, 4),
                "title": info.get('title'),
                "data": {
                    "video": info.get('url'),
                    "audio": audio_url
                }
            }

            return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "api_dev": "@MasumVai",
            "status": "error",
            "message": str(e)
        }), 500

# Vercel entry point
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({"message": "YouTube API is active. Use /api/yt?url=URL"})
