"""Lógica de respostas do AjudaBot.

Fica separada do Flask: para mudar ou adicionar respostas, edite apenas
a lista RULES abaixo. Nada aqui depende de rotas ou de requisições.
"""
import re
import unicodedata


def normalize(text: str) -> str:
    """Minúsculas, sem acentos e com espaços compactados."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", text.lower()).strip()


# Ordem = prioridade. A primeira regra que combinar vence.
# \b garante palavra inteira: "oi" não combina com "moita" ou "pois".
RULES = [
    (
        "humano",
        r"\b(humano|atendente|operador|falar com (um |uma )?(pessoa|alguem)|suporte humano)\b",
        "Certo! Vou te encaminhar para um atendente humano. Você também pode "
        "escrever para ajuda@lojagirassol.example. Respondemos de segunda a sexta, "
        "das 9h às 18h.",
    ),
    (
        "trocas",
        r"\b(troca\w*|trocar|devol\w*|reembols\w*|estorn\w*|arrepend\w*|cancel\w*)\b",
        "Você tem até 7 dias após o recebimento para desistir da compra, e até 30 dias "
        "para trocar por defeito. O produto deve estar sem uso e na embalagem original. "
        "O reembolso é feito na mesma forma de pagamento em até 10 dias úteis.",
    ),
    (
        "entrega",
        r"\b(entrega\w*|prazo\w*|rastre\w*|frete|pedido\w*|encomenda\w*|chega|chegar|chegou)\b",
        "O prazo de entrega é de 3 a 7 dias úteis. Assim que o pedido for enviado, "
        "você recebe por e-mail o código de rastreamento para acompanhar no site dos Correios.",
    ),
    (
        "pagamento",
        r"\b(pagamento\w*|pagar|pix|boleto|cartao|cartoes|credito|debito|parcel\w*)\b",
        "Aceitamos Pix (com 5% de desconto), boleto e cartões de crédito e débito. "
        "No crédito você pode parcelar em até 6x sem juros.",
    ),
    (
        "horarios",
        r"\b(horario\w*|funcionamento|funciona\w*|abre|abrem|fecha|fecham|aberto|expediente)\b",
        "Nosso atendimento funciona de segunda a sexta, das 9h às 18h, e aos sábados, "
        "das 9h às 13h. A loja online fica aberta 24 horas.",
    ),
    (
        "despedida",
        r"\b(obrigad[oa]|valeu|agradec\w*|tchau|adeus|ate logo|ate mais|falou)\b",
        "Por nada! Fico feliz em ajudar. Até a próxima!",
    ),
    (
        "saudacao",
        r"\b(oi|ola|opa|hey|hello|e ai|bom dia|boa tarde|boa noite)\b",
        "Olá! Eu sou o AjudaBot, assistente virtual da Loja Girassol. "
        "Posso ajudar com entrega, trocas, pagamento e horários.",
    ),
]

COMPILED = [(name, re.compile(pattern), reply) for name, pattern, reply in RULES]

DEFAULT_REPLY = (
    "Não entendi muito bem. Posso ajudar com entrega e rastreamento, trocas e "
    "devoluções, formas de pagamento ou horários. Se preferir, peça para falar "
    "com um atendente."
)


def get_reply(message: str) -> str:
    text = normalize(message)
    for _name, pattern, reply in COMPILED:
        if pattern.search(text):
            return reply
    return DEFAULT_REPLY
