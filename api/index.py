from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import time
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/yt', methods=['GET'])
def get_video_data():
    start_time = time.time()
    url = request.args.get('url')

    if not url:
        return jsonify({
            "api_dev": "@MasumVai",
            "error": "URL missing! Please provide a YouTube link."
        }), 400

    try:
        # Advanced options to bypass bot detection
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
            }
        }

        # কুকি ফাইল যদি আপলোড করে থাকেন তবে সেটি ব্যবহার হবে
        if os.path.exists('cookies.txt'):
            ydl_opts['cookiefile'] = 'cookies.txt'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # অডিও লিঙ্ক বের করা
            audio_link = None
            if 'formats' in info:
                for f in info['formats']:
                    if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                        audio_link = f.get('url')
                        break
            
            if not audio_link:
                audio_link = info.get('url')

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

# Root route for welcome message
@app.route('/')
def home():
    return jsonify({"message": "YouTube API is live!", "usage": "/api/yt?url=URL"})

# Vercel handler
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)
