"""
dados.py - "Banco de dados" do Holofix (em memória).

Os dados ficam em listas e dicionários Python. Quando o servidor
reinicia, tudo volta ao estado inicial abaixo. Para a hackathon isso
basta; salvar em arquivo ou SQLite é um desafio extra.

ENTIDADES
---------
Maquina       -> equipamento que recebe manutenção (identificada por um código / QR code)
Procedimento  -> lista de passos para fazer uma manutenção
OrdemServico  -> uma manutenção em andamento ou concluída (técnico + máquina)
PedidoAjuda   -> técnico pede ajuda ao especialista remoto durante uma ordem
"""

from datetime import datetime

# ---------------------------------------------------------------
# PROCEDIMENTOS: cada procedimento tem um id, um título e uma lista de passos
# ---------------------------------------------------------------
procedimentos = {
    1: {
        "id": 1,
        "titulo": "Troca do filtro de ar do compressor",
        "passos": [
            "Desligue o compressor no painel e aguarde 5 minutos.",
            "Coloque luvas e óculos de proteção.",
            "Abra a tampa lateral soltando os 4 parafusos.",
            "Retire o filtro antigo e verifique se há sujeira no alojamento.",
            "Encaixe o filtro novo com a seta apontando para dentro.",
            "Feche a tampa e religue o compressor.",
        ],
    },
    2: {
        "id": 2,
        "titulo": "Lubrificação da esteira",
        "passos": [
            "Pare a esteira e acione a trava de segurança.",
            "Limpe os rolamentos com pano seco.",
            "Aplique graxa nos 6 pontos marcados em amarelo.",
            "Gire a esteira manualmente por 1 volta completa.",
            "Retire a trava e ligue a esteira em velocidade baixa.",
        ],
    },
    3: {
        "id": 3,
        "titulo": "Inspeção da impressora 3D",
        "passos": [
            "Verifique se a mesa está nivelada.",
            "Limpe o bico com a agulha de limpeza.",
            "Confira se o filamento não está embolado.",
            "Imprima o cubo de teste de 20 mm.",
        ],
    },
}

# ---------------------------------------------------------------
# MÁQUINAS: a chave é o código que vai no QR code
# ---------------------------------------------------------------
maquinas = {
    "CMP-01": {"codigo": "CMP-01", "nome": "Compressor Atlas", "local": "Galpão A", "procedimento_id": 1},
    "EST-02": {"codigo": "EST-02", "nome": "Esteira de embalagem", "local": "Linha 2", "procedimento_id": 2},
    "IMP-03": {"codigo": "IMP-03", "nome": "Impressora 3D do laboratório", "local": "Lab 5", "procedimento_id": 3},
}

# ---------------------------------------------------------------
# ORDENS DE SERVIÇO e PEDIDOS DE AJUDA: começam vazios
# ---------------------------------------------------------------
ordens = {}        # id -> ordem
pedidos_ajuda = {} # id -> pedido

# Contadores para gerar ids novos (1, 2, 3, ...)
contador = {"ordem": 0, "ajuda": 0}


def proximo_id(tipo):
    """Gera o próximo id para 'ordem' ou 'ajuda'."""
    contador[tipo] += 1
    return contador[tipo]


def agora():
    """Data e hora atual em texto, ex.: '2026-10-05 14:32:10'."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def reiniciar():
    """Apaga ordens e pedidos (usado pelo verificador)."""
    ordens.clear()
    pedidos_ajuda.clear()
    contador["ordem"] = 0
    contador["ajuda"] = 0
