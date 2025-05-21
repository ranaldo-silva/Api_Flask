from flask import jsonify

def handle_text_command(data):
    text = data.get("text")
    language = data.get("language")

    if not text or not language:
        return jsonify({ "error": True, "message": "Texto e idioma são obrigatórios." }), 400

    print(f"Comando de texto recebido [{language}]: \"{text}\"")

    if language == "pt":
        if "olá" in text.lower():
            ai_response = "Olá! Como posso ajudar você hoje?"
        elif "horários dos trens" in text.lower():
            ai_response = "Para verificar os horários dos trens, preciso saber a linha e a estação."
        elif "locais próximos" in text.lower():
            ai_response = "Claro! Que tipo de local você gostaria de encontrar perto de você?"
        elif "mapa" in text.lower() or "rota" in text.lower():
            ai_response = "Posso te ajudar com mapas e rotas. Qual o seu ponto de partida e destino?"
        elif "obrigado" in text.lower() or "obrigada" in text.lower():
            ai_response = "De nada! Se precisar de mais alguma coisa, é só chamar."
        else:
            ai_response = f'Desculpe, não entendi "{text}". Poderia repetir de outra forma?'
    elif language == "en":
        if "hello" in text.lower():
            ai_response = "Hello there! How may I assist you today?"
        elif "train schedules" in text.lower():
            ai_response = "To check train schedules, I need to know the line and station."
        else:
            ai_response = f'Sorry, I didn’t understand "{text}". Can you rephrase that?'
    else:
        ai_response = "I cannot process this language. Please switch to Portuguese or English."

    return jsonify({
        "response_text": ai_response,
        "transcript": text
    })