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

    # ইউটিউব ব্লক এড়াতে এই সেটআপগুলো অত্যন্ত জরুরি
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'extract_flat': False,
        'youtube_include_dash_manifest': False,
        # এই হেডারগুলো ইউটিউবকে মনে করাবে এটি একটি আসল ব্রাউজার
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # শুধু তথ্যের জন্য
            info = ydl.extract_info(url, download=False)
            
            # সরাসরি ভিডিও এবং অডিও লিঙ্ক বাছাই
            video_url = info.get('url')
            audio_url = None
            
            # বেস্ট অডিও লিঙ্ক খোঁজা
            if 'formats' in info:
                for f in info['formats']:
                    if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                        audio_url = f.get('url')
                        break
            
            if not audio_url:
                audio_url = video_url

            return jsonify({
                "api_dev": "@MasumVai",
                "api_channel": "@MasumVaiBD",
                "time_s": round(time.time() - start_time, 4),
                "title": info.get('title'),
                "data": {
                    "video": video_url,
                    "audio": audio_url
                }
            }), 200

    except Exception as e:
        # এরর মেসেজ ক্লিন করে পাঠানো
        error_msg = str(e)
        if "Sign in to confirm" in error_msg:
            error_msg = "YouTube blocked this request. Please try again after 5 minutes or use cookies."
            
        return jsonify({
            "api_dev": "@MasumVai",
            "status": "error",
            "message": error_msg
        }), 500

# Vercel handler
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)
