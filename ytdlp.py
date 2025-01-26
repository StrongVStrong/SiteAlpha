from flask import Flask, request, jsonify, Response
import yt_dlp
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DownloadDIR = "downloads"
os.makedirs(DownloadDIR, exist_ok = True)

def download_vid(url, format_id):
    options = {
        'outtmpl': os.path.join(DownloadDIR, '%(title)s.%(ext)s'),
        'format': format_id
    }
    
    with yt_dlp.YoutubeDL(options) as ydl:
        return ydl.extract_info(url, download = True)
        
@app.route('/formats', methods=['POST'])
def get_formats():
    try:
        data = request.json
        url = data.get('url')

        if not url:
            return jsonify({"error": "URL is required."}), 400

        options = {'simulate': True}
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            # Initialize the dictionary to hold filtered formats
            filtered_formats = {
                "video": [],
                "audio": []
            }
            
            # Loop through formats and filter out based on extensions
            for fmt in formats:
                # Video: Check if it's a valid video format (mp4 or webm) and extract resolution
                if fmt.get("ext") in ["mp4", "webm"] and fmt.get("height"):
                    resolution = f"{fmt['height']}p"
                    filtered_formats["video"].append({
                        "format_id": fmt["format_id"],
                        "resolution": resolution,
                        "ext": fmt["ext"]
                    })
                
                # Audio: Check for audio-only formats (m4a or mp3)
                if fmt.get("ext") == "m4a" or (fmt.get("ext") == "webm" and fmt.get("abr")):
                    # For m4a audio files
                    if fmt.get("ext") == "m4a":
                        bitrate = f"{int(fmt['abr'])} kbps" if "abr" in fmt else "N/A"
                        filtered_formats["audio"].append({
                            "format_id": fmt["format_id"],
                            "abr": bitrate,
                            "ext": "m4a"
                        })
                    # For webm audio files
                    elif fmt.get("ext") == "webm" and fmt.get("abr"):
                        bitrate = f"{int(fmt['abr'])} kbps"
                        filtered_formats["audio"].append({
                            "format_id": fmt["format_id"],
                            "abr": bitrate,
                            "ext": "mp3"
                        })
            
        # Return filtered formats with the title
        return jsonify({
            "title": info.get("title"),
            "formats": filtered_formats,
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/download', methods=['POST'])
def download():
  try:
    data = request.json
    url = data.get('url')
    format_id = data.get('format')

    if not url or not format_id:
      return jsonify({'error': 'URL/format not provided'}), 400

    ydl_opts = {
      'format': format_id,
      'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(url, download=False)
      if 'url' not in info:
        raise ValueError("Video URL could not be extracted.")

      video_url = info['url']
      print(f"Video URL extracted: {video_url}")

      return jsonify({'url': video_url})

  except Exception as e:
    return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug = True, port = 5000)