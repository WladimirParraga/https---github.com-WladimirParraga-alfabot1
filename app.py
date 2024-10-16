from flask import Flask, request, render_template, send_file, session
import requests
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar sesiones

# Configurar la API key de OpenAI y Eleven Labs desde variables de entorno
openai_api_key = os.getenv("OPENAI_API_KEY")
eleven_labs_api_key = os.getenv("ELEVEN_LABS_API_KEY")

@app.route('/')
def index():
    # Limpiar la memoria al empezar una nueva sesión
    session.clear()
    return render_template('index.html')

@app.route('/record', methods=['POST'])
def record_audio():
    # Guardar el archivo de audio subido
    audio_file = request.files['audio']
    audio_path = os.path.join('static/audio', 'audio_recibido.mp3')
    audio_file.save(audio_path)

    # Usar la API HTTP de OpenAI Whisper para convertir audio a texto
    with open(audio_path, "rb") as audio_file_for_api:
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={
                "Authorization": f"Bearer {openai_api_key}"
            },
            files={
                "file": audio_file_for_api
            },
            data={
                "model": "whisper-1"
            }
        )

    # Verificar si la transcripción fue exitosa
    transcript = response.json()
    
    if "text" in transcript:
        user_text = transcript['text']
        print(f"Texto transcrito: {user_text}")
    else:
        return f"Error en la transcripción: {transcript}", 500

    # Recuperar el historial de conversación de la sesión
    if 'conversation_history' not in session:
        session['conversation_history'] = [
            {"role": "system", "content": "Eres un robot que se llama Alfabot, que responde solo en español, sin mezclar idiomas, cuando tengas que enumerar cosas o decir numeros dilos en español. Tu objetivo es apoyar en la enseñanza del abecedario. Mantén el flujo de la conversación y recuerda las interacciones previas."}
        ]

    # Añadir la nueva entrada del usuario al historial
    session['conversation_history'].append({"role": "user", "content": user_text})

    # Enviar el historial completo de mensajes a ChatGPT
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": session['conversation_history']  # Pasar el historial completo
        }
    )

    chatgpt_response = response.json()
    
    if "choices" in chatgpt_response and len(chatgpt_response['choices']) > 0:
        assistant_text = chatgpt_response['choices'][0]['message']['content']
        print(f"Respuesta de ChatGPT: {assistant_text}")

        # Añadir la respuesta del asistente al historial
        session['conversation_history'].append({"role": "assistant", "content": assistant_text})
    else:
        return "Error en la respuesta de ChatGPT", 500

    # Usar Eleven Labs para convertir la respuesta a voz
    audio_response = text_to_speech(assistant_text)

    # Guardar el audio generado
    with open("static/audio/respuesta.mp3", "wb") as f:
        f.write(audio_response)

    return send_file("static/audio/respuesta.mp3", mimetype="audio/mp3")

# Función para convertir texto a voz usando Eleven Labs
def text_to_speech(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/1BxAZWANeDIxeyHKSJF2"
    headers = {
        "Content-Type": "application/json",
        "xi-api-key": eleven_labs_api_key
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.7
        }
    }
    response = requests.post(url, json=data, headers=headers)
    return response.content

if __name__ == "__main__":
    app.run(debug=True)
