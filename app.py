from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException

from chatbot import get_reply

MAX_MESSAGE_LENGTH = 500

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024  # recusa corpos de requisição grandes


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Envie um JSON no formato {\"message\": \"...\"}."), 400

    message = data.get("message")
    if not isinstance(message, str) or not message.strip():
        return jsonify(error="O campo 'message' deve ser um texto não vazio."), 400
    if len(message) > MAX_MESSAGE_LENGTH:
        return jsonify(error=f"A mensagem pode ter no máximo {MAX_MESSAGE_LENGTH} caracteres."), 400

    return jsonify(reply=get_reply(message))


ERROR_MESSAGES = {
    404: "Rota não encontrada.",
    405: "Método não permitido para esta rota.",
    413: "Requisição grande demais.",
}


@app.errorhandler(HTTPException)
def handle_http_error(error):
    """Erros em /api/ voltam em JSON; as demais páginas seguem o padrão."""
    if request.path.startswith("/api/"):
        return jsonify(error=ERROR_MESSAGES.get(error.code, "Erro na requisição.")), error.code
    return error


if __name__ == "__main__":
    # Só para uso local. Em produção o Render usa: gunicorn app:app
    app.run()
