
import os
from flask import Flask, request, jsonify
import json
from youtube_transcript_api import YouTubeTranscriptApi
app = Flask(__name__)

@app.route('/api', methods=['POST'])
def echo():
    if request.is_json:
        data = request.get_json()
        id=data['videoid']
        result=send_json_as_post(id)
        return jsonify(result), 200
    else:
        return jsonify({"error": "Invalid JSON"}), 400

if __name__ == '__main__':
    app.run(debug=True,port=os.getenv("PORT", default=8000))


def send_json_as_post(id):
    # retrieve the video URL from the child process backend
    video_url = id

    # retrieve the transcript in English
    transcript = YouTubeTranscriptApi.get_transcript(
        video_url, languages=['en'])

    # concatenate the transcript text without time stamps
    lines = [line['text'] for line in transcript]
    transcript_text = ' '.join(lines)

    # format the output as a JSON object
    output = {
        "video_url": video_url,
        "transcript": transcript_text
    }

    json_output = json.dumps(output)

    # return the response from the server
    return(json_output)
