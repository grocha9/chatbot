# AjudaBot

Chatbot de atendimento para a loja fictícia **Loja Girassol**. Backend em Python (Flask), frontend em HTML, CSS e JavaScript puro, comunicação por API REST em JSON.

O código já está pronto e testado. Este guia lista **o que você precisa fazer** para rodar, publicar e entender o projeto.

---

## 1. Rodar no seu computador

Abra o terminal dentro da pasta `chatbot-atendimento`.

```
python -m venv venv
```

Ative o ambiente virtual:

- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

Instale e rode:

```
pip install -r requirements.txt
python app.py
```

Abra **http://127.0.0.1:5000** no navegador.

**Se der erro:**

| Erro | Causa e solução |
|---|---|
| `ModuleNotFoundError: flask` | O ambiente virtual não está ativo. Ative de novo (deve aparecer `(venv)` no terminal) e rode `pip install -r requirements.txt`. |
| `python` não é reconhecido | Tente `python3` ou `py`. |
| `Address already in use` | Outra coisa está usando a porta 5000. Use `app.run(port=5001)` em `app.py`. |
| Fonte diferente da esperada | A fonte vem do Google Fonts. Sem internet, o navegador usa uma fonte do sistema. Funciona igual. |

## 2. Testar cada funcionalidade

Clique ou digite estas mensagens e confira:

| Mensagem | Resposta esperada |
|---|---|
| `Oi` | Saudação |
| `Qual o prazo de entrega?` | "O prazo de entrega é de 3 a 7 dias úteis..." |
| `Quero trocar um produto` | Regras de troca e devolução |
| `Aceita pix?` | Formas de pagamento |
| `Que horas vocês abrem?` | Horários |
| `Quero falar com um humano` | Atendimento humano |
| `Obrigado, tchau` | Despedida |
| `asdfgh` | Resposta padrão (não entendi) |
| `Oi, qual o prazo?` | Entrega (a regra mais importante vence a saudação) |

Para testar o **erro de comunicação**: com o site aberto, pare o servidor (Ctrl+C no terminal) e envie uma mensagem. Deve aparecer a mensagem vermelha "Não consegui falar com o servidor...".

Para testar a **API direto** (com o servidor rodando, em outro terminal):

```
curl -X POST http://127.0.0.1:5000/api/chat -H "Content-Type: application/json" -d "{\"message\": \"Qual o prazo de entrega?\"}"
```

Para testar **Gunicorn** (Linux/Mac/WSL; o Gunicorn não roda direto no Windows):

```
gunicorn app:app
```

## 3. Colocar no GitHub

1. Crie uma conta em github.com, se ainda não tiver.
2. Clique em **New repository**, dê o nome `chatbot-atendimento`, deixe **sem** README, `.gitignore` ou licença, e crie.
3. No terminal, dentro da pasta do projeto:

```
git init
git add .
git commit -m "AjudaBot: primeira versão"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/chatbot-atendimento.git
git push -u origin main
```

Troque `SEU-USUARIO` pelo seu usuário do GitHub. Se o GitHub pedir senha, use um **Personal Access Token** (Settings > Developer settings > Personal access tokens), não a senha da conta.

Confira se a pasta `venv` **não** subiu (o `.gitignore` já cuida disso).

## 4. Publicar no Render (plano gratuito)

1. Crie uma conta em render.com e entre com o GitHub.
2. Clique em **New > Web Service** e escolha o repositório `chatbot-atendimento`.
3. Preencha:
   - **Language:** Python 3
   - **Branch:** main
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
4. Clique em **Deploy Web Service** e aguarde o build terminar (alguns minutos).
5. Abra o endereço `https://seu-servico.onrender.com` que o Render mostrar e repita os testes da seção 2.

**Para saber:**

- No plano gratuito, o serviço "dorme" após alguns minutos sem uso. O primeiro acesso depois disso pode levar cerca de um minuto. Isso é normal.
- O arquivo `.python-version` pede o Python 3.13.4. Se o Render reclamar da versão no build, leia a mensagem de erro e ajuste o número nesse arquivo.
- Cada `git push` na branch `main` publica uma nova versão automaticamente.

## 5. Personalizar

Tudo que o bot responde fica em **`chatbot.py`**, na lista `RULES`. Cada regra tem um nome, uma expressão regular e a resposta.

- Para mudar uma resposta, edite o texto.
- Para adicionar uma categoria, copie uma regra e coloque na posição certa: **a ordem é a prioridade** (a primeira que combinar vence).
- O `\b` nas expressões garante palavra inteira, então "oi" não combina com "moita".
- A mensagem do usuário é normalizada antes (minúsculas e sem acentos), então escreva as expressões sem acento: `credito`, não `crédito`.

## Como os arquivos se comunicam

```
Navegador                         Servidor (Flask)
─────────                         ────────────────
templates/index.html  ◄── GET / ── app.py
static/script.js ── POST /api/chat {"message": "..."} ──► app.py
                                                            │ chama get_reply()
                                                            ▼
static/script.js ◄── {"reply": "..."} ──────────────── chatbot.py
```

- `app.py`: rotas, validação e erros.
- `chatbot.py`: normalização do texto e regras de resposta (separado do Flask).
- `templates/index.html`: estrutura da página.
- `static/style.css`: visual e responsividade.
- `static/script.js`: envia a mensagem, mostra "digitando", exibe a resposta e trata erros.
- `requirements.txt`: dependências. `.python-version`: versão do Python no Render. `.gitignore`: o que o Git ignora.

## Segurança

- O JavaScript usa `textContent`, nunca `innerHTML`, então nada digitado vira HTML.
- A API valida o JSON, o tipo e o tamanho da mensagem (máximo 500 caracteres) e responde erros em JSON.
- Não há `debug=True` e nenhuma chave ou senha no código.
