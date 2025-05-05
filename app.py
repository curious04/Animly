from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import subprocess
import tempfile
import requests
import logging
import traceback
import shutil
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

def check_ffmpeg():
    """Check if FFmpeg is installed and accessible."""
    try:
        ffmpeg_path = shutil.which('ffmpeg')
        if not ffmpeg_path:
            raise RuntimeError(
                "FFmpeg not found. Please install FFmpeg and add it to your PATH. "
                "Visit https://ffmpeg.org/download.html for installation instructions."
            )
        logger.info(f"FFmpeg found at: {ffmpeg_path}")
        return True
    except Exception as e:
        logger.error(f"FFmpeg check failed: {str(e)}")
        return False

def generate_manim_code(prompt):
    """Generate Manim code based on the user's prompt using Ollama."""
    try:
        # Prepare the prompt for Ollama
        system_prompt = """You are a Python expert specializing in Manim animations. 
        Generate only the Python code for a Manim animation based on the user's description. 
        The code should be complete and runnable. Always include necessary imports and a Scene class.
        Make sure to use proper Manim syntax and include all required transformations.
        The code should be simple and focused on the requested animation.
        Only return the Python code, no explanations or markdown formatting."""

        # Make request to Ollama API
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "codellama",
                "prompt": f"{system_prompt}\n\nUser: Create a Manim animation for: {prompt}\n\nAssistant:",
                "stream": False
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.text}")

        # Extract the generated code
        code = response.json()['response']
        
        # Clean up the response (remove any markdown formatting)
        code = code.replace('```python', '').replace('```', '').strip()
        
        # Ensure the code has necessary imports
        if "from manim import *" not in code:
            code = "from manim import *\n\n" + code
            
        # Ensure there's a Scene class
        if "class" not in code:
            code += "\n\nclass AnimationScene(Scene):\n    def construct(self):\n        # Your animation code here\n        pass"
            
        return code
                
    except Exception as e:
        logger.error(f"Error generating code: {str(e)}")
        logger.error(traceback.format_exc())
        raise Exception(f"Error generating animation: {str(e)}")

def create_animation(code):
    """Create animation using Manim."""
    if not check_ffmpeg():
        raise RuntimeError("FFmpeg is required but not found. Please install FFmpeg first.")

    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, 'animation.py')
    
    try:
        # Write the code to a temporary file
        with open(temp_file, 'w') as f:
            f.write(code)
        
        logger.debug(f"Generated code:\n{code}")
        
        # Run Manim command
        result = subprocess.run(
            ['manim', '-pql', temp_file],
            capture_output=True,
            text=True
        )
        
        logger.debug(f"Manim output:\n{result.stdout}")
        if result.stderr:
            logger.error(f"Manim error:\n{result.stderr}")
        
        # Get the output video path
        output_dir = os.path.join(temp_dir, 'media', 'videos')
        if not os.path.exists(output_dir):
            logger.error(f"Output directory not found: {output_dir}")
            return None
            
        video_files = [f for f in os.listdir(output_dir) if f.endswith('.mp4')]
        
        if video_files:
            video_path = os.path.join(output_dir, video_files[0])
            logger.info(f"Video generated at: {video_path}")
            return video_path
        else:
            logger.error("No video files found in output directory")
            return None
            
    except Exception as e:
        logger.error(f"Error creating animation: {str(e)}")
        logger.error(traceback.format_exc())
        return None

@app.route('/generate', methods=['POST'])
def generate_animation():
    try:
        data = request.json
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        # Generate Manim code
        code = generate_manim_code(prompt)
        
        # Create animation
        video_path = create_animation(code)
        
        if video_path and os.path.exists(video_path):
            # Convert the video path to a URL-friendly format
            video_url = f"/video/{os.path.basename(video_path)}"
            return jsonify({
                'success': True,
                'code': code,
                'video_path': video_url
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to generate animation. Check server logs for details.'
            }), 500
            
    except Exception as e:
        logger.error(f"Error in generate_animation: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Serve video files
@app.route('/video/<filename>')
def serve_video(filename):
    try:
        return send_from_directory('media/videos', filename)
    except Exception as e:
        logger.error(f"Error serving video: {str(e)}")
        return jsonify({'error': 'Video not found'}), 404

if __name__ == '__main__':
    app.run(debug=True) 