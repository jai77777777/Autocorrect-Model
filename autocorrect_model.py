import os  # Used to create environment variables
from flask import Flask, request, jsonify, render_template_string  # Framework used for the web applications
from textblob import TextBlob

os.environ['FLASK_ENV'] = 'development'
app = Flask(__name__)

def autocorrect_text(text):
    blob = TextBlob(text)
    return str(blob.correct())

@app.route('/autocorrect', methods=['POST'])
def autocorrect():
    data = request.json
    corrected_text = autocorrect_text(data.get('text', ''))
    return jsonify({'corrected_text': corrected_text})

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        text = file.read().decode('utf-8')
        corrected_text = autocorrect_text(text)
        return jsonify({'corrected_text': corrected_text})

@app.route('/')
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Grammar Guardian | Autocorrect</title>
            <style>
                body {
                    font-family: 'Inter', sans-serif;
                    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
                    min-height: 100vh;
                    margin: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: #2d3748;
                }
                .container {
                    background: rgba(255, 255, 255, 0.9);
                    backdrop-filter: blur(15px);
                    border-radius: 25px;
                    padding: 2.5rem;
                    width: 100%;
                    max-width: 700px;
                    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
                    border: 1px solid rgba(255, 255, 255, 0.4);
                    text-align: center;
                }
                h1 {
                    color: #4a5568;
                    font-size: 2.2rem;
                    font-weight: 700;
                    background: linear-gradient(45deg, #6a11cb, #2575fc);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
                textarea {
                    width: 100%;
                    height: 120px;
                    padding: 1.2rem;
                    border: 2px solid #e2e8f0;
                    border-radius: 15px;
                    resize: vertical;
                    font-size: 1rem;
                    transition: all 0.3s ease;
                    margin-bottom: 15px;
                }
                textarea:focus {
                    outline: none;
                    border-color: #6a11cb;
                    box-shadow: 0 0 0 3px rgba(106, 17, 203, 0.2);
                }
                input[type="file"] {
                    margin: 1.5rem 0;
                }
                button {
                    background: linear-gradient(45deg, #6a11cb, #2575fc);
                    color: white;
                    border: none;
                    padding: 1rem 2.5rem;
                    border-radius: 10px;
                    font-size: 1.1rem;
                    font-weight: 700;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    width: 100%;
                    margin-top: 12px;
                }
                button:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
                }
                #output {
                    background: rgba(237, 242, 247, 0.85);
                    padding: 1.8rem;
                    border-radius: 15px;
                    min-height: 120px;
                    font-size: 1rem;
                    white-space: pre-wrap;
                    margin-top: 1.5rem;
                    text-align: left;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Autocorrect System ✨</h1>

                <textarea id="input-text" placeholder="Enter your text here..." spellcheck="false"></textarea>
                <button id="correct-btn">Correct Text</button>

                <br><br>
                <strong>OR</strong>
                <br><br>

                <input type="file" id="file-input" accept=".txt">
                <button id="upload-btn">Upload & Correct File</button>

                <div id="output">
                    <strong>Corrected Text:</strong> <br>
                    <div id="output-text"></div>
                </div>
            </div>

            <script>
                document.getElementById('correct-btn').addEventListener('click', async () => {
                    const inputText = document.getElementById('input-text').value;
                    const outputText = document.getElementById('output-text');

                    if (!inputText.trim()) {
                        outputText.textContent = 'Please enter some text.';
                        return;
                    }

                    outputText.textContent = 'Processing...';

                    try {
                        const response = await fetch('/autocorrect', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ text: inputText }),
                        });

                        const data = await response.json();
                        outputText.textContent = data.corrected_text;
                    } catch (error) {
                        outputText.textContent = 'Error: Could not connect to the server';
                    }
                });

                document.getElementById('upload-btn').addEventListener('click', async () => {
                    const fileInput = document.getElementById('file-input').files[0];
                    const outputText = document.getElementById('output-text');

                    if (!fileInput) {
                        outputText.textContent = 'Please select a file.';
                        return;
                    }

                    const formData = new FormData();
                    formData.append('file', fileInput);

                    outputText.textContent = 'Processing...';

                    try {
                        const response = await fetch('/upload', {
                            method: 'POST',
                            body: formData
                        });

                        const data = await response.json();
                        if (data.error) {
                            outputText.textContent = data.error;
                        } else {
                            outputText.textContent = data.corrected_text;
                        }
                    } catch (error) {
                        outputText.textContent = 'Error: Could not connect to the server';
                    }
                });
            </script>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)