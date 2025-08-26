from flask import jsonify
from collections import deque

# ----------------------
# DADOS MOCK (linhas e estações)
# ----------------------
LINES = {
    "Azul": ["Jabaquara", "Conceição", "São Judas", "Saúde", "Praça da Árvore", 
             "Santa Cruz", "Vila Mariana", "Ana Rosa", "Paraíso", "São Joaquim", 
             "Liberdade", "Sé", "Luz", "Tiradentes", "Carandiru", "Santana", "Tucuruvi"],

    "Vermelha": ["Barra Funda", "República", "Sé", "Brás", "Tatuapé", "Itaquera"],

    "Verde": ["Vila Prudente", "Tamanduateí", "Sacoma", "Alto do Ipiranga", 
              "Santos-Imigrantes", "Chácara Klabin", "Ana Rosa", "Paraíso", 
              "Brigadeiro", "Trianon-Masp", "Consolação", "Clínicas", 
              "Santuário Nossa Senhora de Fátima-Sumaré", "Vila Madalena"],

    "Amarela": ["Luz", "República", "Paulista", "Pinheiros", "Butantã"]
}

GRAPH = {}
for line, stations in LINES.items():
    for i, station in enumerate(stations):
        if station not in GRAPH:
            GRAPH[station] = []
        if i > 0:
            GRAPH[station].append(stations[i-1])
        if i < len(stations)-1:
            GRAPH[station].append(stations[i+1])

# ----------------------
# FUNÇÕES DE APOIO
# ----------------------
def get_station_line(station):
    return [line for line, stations in LINES.items() if station in stations]

def bfs_route(origin, destination):
    if origin not in GRAPH or destination not in GRAPH:
        return None
    queue = deque([[origin]])
    visited = set()
    while queue:
        path = queue.popleft()
        station = path[-1]
        if station == destination:
            return path
        if station not in visited:
            visited.add(station)
            for neighbor in GRAPH[station]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    return None

def format_route_short(path):
    if not path:
        return "Não foi possível encontrar uma rota."

    instructions = []
    total_time = 0
    current_line = get_station_line(path[0])[0]

    for i in range(1, len(path)):
        station = path[i]
        lines_here = get_station_line(station)
        shared_lines = set(get_station_line(path[i-1])) & set(lines_here)

        if shared_lines:
            total_time += 2
        else:
            instructions.append(f"Pegue a Linha {current_line} até **{path[i-1]}**")
            total_time += 4
            current_line = lines_here[0]

    instructions.append(f"Pegue a Linha {current_line} até **{path[-1]}**")
    return "\n".join(instructions) + f"\n⏱️ Tempo estimado: **{total_time} minutos**"

# ----------------------
# CONTEXTO DE USUÁRIO
# ----------------------
user_context = {}

# ----------------------
# FUNÇÃO PRINCIPAL
# ----------------------
def handle_text_command(data):
    user_id = data.get("user_id", "default")
    text = data.get("text")
    language = data.get("language")

    if not text or not language:
        return jsonify({ "error": True, "message": "Texto e idioma são obrigatórios." }), 400

    if user_id not in user_context:
        user_context[user_id] = {"state": None, "origin": None, "destination": None}

    context = user_context[user_id]
    lower_text = text.lower()

    if language == "pt":
        # ----------------------
        # CONTEXTO DE ROTA
        # ----------------------
        if context["state"] == "awaiting_origin":
            if text.title() in GRAPH:
                context["origin"] = text.title()
                context["state"] = "awaiting_destination"
                ai_response = f"Beleza, você está na estação {context['origin']}. Para qual estação deseja ir?"
            else:
                ai_response = "Não encontrei essa estação. Pode repetir o nome?"

        elif context["state"] == "awaiting_destination":
            if text.title() in GRAPH:
                context["destination"] = text.title()
                path = bfs_route(context["origin"], context["destination"])
                ai_response = format_route_short(path)
                user_context[user_id] = {"state": None, "origin": None, "destination": None}
            else:
                ai_response = "Não encontrei essa estação de destino. Pode repetir?"

        # ----------------------
        # COMANDOS FIXOS
        # ----------------------
        elif "rota" in lower_text or "ir para" in lower_text or "estação" in lower_text:
            context["state"] = "awaiting_origin"
            ai_response = "Claro! Em qual estação você está agora?"

        elif "olá" in lower_text or "oi" in lower_text:
            ai_response = "Olá! Seja bem-vindo ao Metrô de São Paulo. Como posso ajudar?"

        elif "banheiro" in lower_text:
            ai_response = "Os banheiros ficam próximos às áreas de integração ou no piso de acesso."

        elif "lanchonete" in lower_text or "comer" in lower_text:
            ai_response = "Você encontra lanchonetes próximas à bilheteria principal."

        elif "loja" in lower_text or "shopping" in lower_text:
            ai_response = "Existem lojas no corredor principal próximo às catracas."

        elif "saída" in lower_text:
            ai_response = "As saídas estão sinalizadas com placas verdes. Qual rua você deseja acessar?"

        elif "obrigado" in lower_text or "obrigada" in lower_text:
            ai_response = "De nada! Tenha uma boa viagem."

        else:
            ai_response = f'Desculpe, não entendi "{text}". Pode repetir de outra forma?'

    else:
        ai_response = "I cannot process this language. Please switch to Portuguese."

    return jsonify({
        "response_text": ai_response,
        "transcript": text,
        "context": context
    })
