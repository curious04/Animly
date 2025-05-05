# AnimX - AI Animation Generator

AnimX is a web application that generates 2D animations using Manim based on natural language prompts. It uses OpenAI's GPT model to convert your descriptions into Manim code and then renders the animations.

## Prerequisites

- Python 3.7+
- Node.js 14+
- OpenAI API key

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd animx
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Node.js dependencies:
```bash
npm install
```

4. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Running the Application

1. Start the Flask backend:
```bash
python app.py
```

2. In a new terminal, start the React frontend:
```bash
npm start
```

3. Open your browser and navigate to `http://localhost:3000`

## Usage

1. Enter a description of the animation you want to create in the text field
2. Click "Generate Animation"
3. Wait for the code to be generated and the animation to be rendered
4. View the generated code and the resulting animation

## Example Prompts

- "Create a bouncing ball animation with a shadow"
- "Animate a square transforming into a circle"
- "Show a wave function moving across the screen"
- "Create an animation of a growing tree"

## Notes

- The application uses Manim's low quality preset (`-pql`) for faster rendering
- Generated animations are temporarily stored and will be cleaned up automatically
- Make sure you have enough disk space for temporary files and rendered videos

## License

MIT 