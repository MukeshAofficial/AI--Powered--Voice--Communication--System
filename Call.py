import openai  

from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse,Gather

app = Flask(__name__)


OPENAI_API_KEY = 'API_KEY'
openai.api_key = OPENAI_API_KEY

def generate_response(input_text):
    # Use OpenAI's API to generate a response
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=input_text,
        max_tokens=50  
    )
    return response.choices[0].text.strip()

@app.route('/incoming-call', methods=['GET', 'POST'])
def gather_input():
    response = VoiceResponse()
    response.say('Hello')

    gather = Gather(input_='speech', action='/results', language='en-GB', speech_model='phone_call',
                    hints='maneater, you make my dreams, out of touch')
    gather.say('Please ask your question')

    response.append(gather)
    return str(response)

@app.route('/results', methods=['POST'])
def process_results():
    speech_result = request.values.get('SpeechResult')
    if speech_result:
        # Generate response using OpenAI
        with open('transcription.txt', 'w') as f:
            f.write(speech_result)
        print("Transcription:", speech_result)
        generated_response = generate_response(speech_result)

        print("Generated response:", generated_response)

        # Return TwiML response with the generated response
        response = VoiceResponse()
        response.say(generated_response)
        return str(response)
    else:
        # If no speech result is received, handle accordingly
        return "No speech result received."

if __name__ == "__main__":
    app.run(debug=True)
