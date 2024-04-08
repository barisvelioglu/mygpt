from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Initialize the text generation pipeline with the Mistral-7B-v0.1 model
text_generator = pipeline("text-generation", model="mistralai/Mistral-7B-v0.1")

@app.route('/generate', methods=['POST'])
def generate():
    # Retrieve the prompt from the incoming request
    data = request.get_json(force=True)
    prompt = data.get('prompt', '')  # Default to an empty string if no prompt provided
    
    # Generate text based on the provided prompt
    generated_texts = text_generator(prompt, max_length=50, num_return_sequences=1)
    generated_text = generated_texts[0]['generated_text']
    
    # Return the generated text as a JSON response
    return jsonify({"generated_text": generated_text})

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
