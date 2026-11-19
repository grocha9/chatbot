const log = document.getElementById("log");
const form = document.getElementById("chat-form");
const input = document.getElementById("message");
const sendBtn = document.getElementById("send");
const suggestions = document.getElementById("suggestions");

let busy = false;

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function scrollToBottom() {
  log.scrollTop = log.scrollHeight;
}

// textContent (e não innerHTML) impede que o texto vire HTML: evita XSS.
function addMessage(text, classes) {
  const el = document.createElement("div");
  el.className = "msg " + classes;
  el.textContent = text;
  log.appendChild(el);
  scrollToBottom();
  return el;
}

function showTyping() {
  const el = document.createElement("div");
  el.className = "msg bot typing";
  el.setAttribute("aria-label", "AjudaBot está digitando");
  for (let i = 0; i < 3; i++) el.appendChild(document.createElement("span"));
  log.appendChild(el);
  scrollToBottom();
  return el;
}

function setBusy(value) {
  busy = value;
  input.disabled = value;
  sendBtn.disabled = value;
}

async function sendMessage(text) {
  text = text.trim();
  if (!text || busy) return;

  setBusy(true);
  addMessage(text, "user");
  input.value = "";
  const typing = showTyping();
  const startedAt = Date.now();
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10000);

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
      signal: controller.signal,
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw Object.assign(new Error(data.error || "Erro inesperado."), { fromServer: true });
    }
    // Pausa mínima para o indicador de digitação ser percebido.
    await wait(Math.max(0, 700 - (Date.now() - startedAt)));
    typing.remove();
    addMessage(data.reply, "bot");
  } catch (err) {
    typing.remove();
    let msg = "Não consegui falar com o servidor. Verifique sua conexão e tente de novo.";
    if (err.name === "AbortError") msg = "O servidor demorou para responder. Tente de novo em instantes.";
    if (err.fromServer) msg = err.message;
    addMessage(msg, "bot error");
  } finally {
    clearTimeout(timeout);
    setBusy(false);
    input.focus();
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(input.value);
});

suggestions.addEventListener("click", (event) => {
  const chip = event.target.closest(".chip");
  if (chip) sendMessage(chip.textContent);
});

addMessage(
  "Olá! Eu sou o AjudaBot, da Loja Girassol. Escolha uma sugestão ou escreva sua dúvida.",
  "bot"
);
