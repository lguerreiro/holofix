"""
verificar.py - Confere quais missões já estão funcionando.

Como usar (com o servidor PARADO ou rodando, tanto faz):
    python verificar.py          -> testa todas as missões
    python verificar.py 2        -> testa só a missão 2

Não altere este arquivo. Ele não precisa de internet.
"""

import sys

import dados
from app import app

cliente = app.test_client()
resultados = []


def checar(missao, descricao, condicao, dica=""):
    resultados.append((missao, descricao, bool(condicao), dica))


def seguro(func):
    """Roda um bloco de testes sem deixar um erro derrubar os outros."""
    def envolvido(missao):
        try:
            func(missao)
        except Exception as e:  # noqa: BLE001
            checar(missao, "o código rodou sem erro", False, f"{type(e).__name__}: {e}")
    return envolvido


def nova_ordem(codigo="CMP-01", tecnico="Ana"):
    return cliente.post("/api/ordens", json={"maquina_codigo": codigo, "tecnico": tecnico})


# ----------------------------------------------------------------
@seguro
def missao1(m):
    r = cliente.get("/api/maquinas")
    checar(m, "GET /api/maquinas responde 200", r.status_code == 200, f"veio {r.status_code}")
    lista = r.get_json(silent=True)
    checar(m, "devolve uma lista com as 3 máquinas", isinstance(lista, list) and len(lista) == 3,
           "use list(dados.maquinas.values())")

    r = cliente.get("/api/maquinas/CMP-01")
    j = r.get_json(silent=True) or {}
    checar(m, "GET /api/maquinas/CMP-01 responde 200 com o nome", r.status_code == 200 and j.get("nome") == "Compressor Atlas")
    checar(m, "inclui 'procedimento' e 'total_passos'", j.get("procedimento") and j.get("total_passos") == 6,
           "busque o procedimento pelo procedimento_id da máquina")

    r = cliente.get("/api/maquinas/cmp-01")
    checar(m, "aceita código em minúsculas (cmp-01)", r.status_code == 200, "use codigo.upper()")

    r = cliente.get("/api/maquinas/XYZ-99")
    checar(m, "código inexistente devolve 404", r.status_code == 404, f"veio {r.status_code}")


@seguro
def missao2(m):
    r = nova_ordem()
    j = r.get_json(silent=True) or {}
    checar(m, "POST /api/ordens responde 201", r.status_code == 201, f"veio {r.status_code}")
    checar(m, "a ordem começa no passo 0 com status em_andamento",
           j.get("passo_atual") == 0 and j.get("status") == "em_andamento")
    checar(m, "a resposta traz o texto do passo (use montar_ordem)", "texto_passo" in j)

    r = cliente.post("/api/ordens", json={"maquina_codigo": "CMP-01"})
    checar(m, "sem técnico devolve 400", r.status_code == 400, f"veio {r.status_code}")
    r = nova_ordem(codigo="NAO-EXISTE")
    checar(m, "máquina inexistente devolve 404", r.status_code == 404, f"veio {r.status_code}")

    ordem_id = j.get("id", 1)
    r = cliente.get(f"/api/ordens/{ordem_id}")
    checar(m, "GET /api/ordens/<id> encontra a ordem criada", r.status_code == 200)
    r = cliente.get("/api/ordens/999")
    checar(m, "GET de ordem inexistente devolve 404", r.status_code == 404)


@seguro
def missao3(m):
    oid = (nova_ordem("IMP-03").get_json(silent=True) or {}).get("id", 1)  # IMP-03 tem 4 passos

    r = cliente.post(f"/api/ordens/{oid}/voltar")
    checar(m, "voltar no primeiro passo devolve 400", r.status_code == 400, f"veio {r.status_code}")

    r = cliente.post(f"/api/ordens/{oid}/avancar")
    checar(m, "avançar leva ao passo 1", (r.get_json(silent=True) or {}).get("passo_atual") == 1)

    r = cliente.post(f"/api/ordens/{oid}/concluir")
    checar(m, "concluir antes do último passo devolve 400", r.status_code == 400, f"veio {r.status_code}")

    r = cliente.post(f"/api/ordens/{oid}/voltar")
    checar(m, "voltar leva de volta ao passo 0", (r.get_json(silent=True) or {}).get("passo_atual") == 0)

    for _ in range(3):
        cliente.post(f"/api/ordens/{oid}/avancar")
    r = cliente.post(f"/api/ordens/{oid}/avancar")
    checar(m, "avançar depois do último passo devolve 400", r.status_code == 400, f"veio {r.status_code}")

    r = cliente.post(f"/api/ordens/{oid}/concluir")
    j = r.get_json(silent=True) or {}
    checar(m, "concluir no último passo muda status para concluida",
           r.status_code == 200 and j.get("status") == "concluida")
    checar(m, "a ordem concluída ganha data de fim", bool(j.get("fim")), "use dados.agora()")


@seguro
def missao4(m):
    oid = (nova_ordem().get_json(silent=True) or {}).get("id", 1)
    r = cliente.post(f"/api/ordens/{oid}/ajuda", json={"mensagem": "Não encontro a peça"})
    j = r.get_json(silent=True) or {}
    checar(m, "POST /api/ordens/<id>/ajuda responde 201", r.status_code == 201, f"veio {r.status_code}")
    checar(m, "o pedido nasce com status aberto e guarda o passo", j.get("status") == "aberto" and j.get("passo") == 0)

    o = cliente.get(f"/api/ordens/{oid}").get_json(silent=True) or {}
    checar(m, "a ordem passa para aguardando_ajuda", o.get("status") == "aguardando_ajuda")

    r = cliente.post(f"/api/ordens/{oid}/ajuda", json={"mensagem": ""})
    checar(m, "mensagem vazia devolve 400", r.status_code == 400, f"veio {r.status_code}")
    r = cliente.post("/api/ordens/999/ajuda", json={"mensagem": "oi"})
    checar(m, "ordem inexistente devolve 404", r.status_code == 404, f"veio {r.status_code}")


@seguro
def missao5(m):
    oid = (nova_ordem().get_json(silent=True) or {}).get("id", 1)
    pid = (cliente.post(f"/api/ordens/{oid}/ajuda", json={"mensagem": "Socorro"}).get_json(silent=True) or {}).get("id", 1)

    r = cliente.get("/api/ajudas")
    lista = r.get_json(silent=True)
    checar(m, "GET /api/ajudas devolve a lista de pedidos", r.status_code == 200 and isinstance(lista, list) and len(lista) >= 1)
    checar(m, "cada pedido traz os dados da ordem (técnico, máquina)",
           isinstance(lista, list) and lista and isinstance(lista[0].get("ordem"), dict))

    r = cliente.post(f"/api/ajudas/{pid}/responder", json={"resposta": "Olhe atrás do painel"})
    j = r.get_json(silent=True) or {}
    checar(m, "responder muda o pedido para respondido", r.status_code == 200 and j.get("status") == "respondido")

    o = cliente.get(f"/api/ordens/{oid}").get_json(silent=True) or {}
    checar(m, "a ordem volta para em_andamento", o.get("status") == "em_andamento")
    checar(m, "o óculos enxerga a resposta em ordem['ajuda']",
           (o.get("ajuda") or {}).get("resposta") == "Olhe atrás do painel")

    r = cliente.get("/api/ajudas?status=aberto")
    checar(m, "filtro ?status=aberto não traz respondidos", r.status_code == 200 and r.get_json(silent=True) == [])

    r = cliente.get("/api/ordens")
    checar(m, "GET /api/ordens lista as ordens para o painel",
           r.status_code == 200 and isinstance(r.get_json(silent=True), list))


MISSOES = {
    1: ("Máquinas", missao1),
    2: ("Abrir e consultar ordem de serviço", missao2),
    3: ("Navegar pelos passos", missao3),
    4: ("Pedir ajuda (bônus)", missao4),
    5: ("Painel do especialista (bônus)", missao5),
}

if __name__ == "__main__":
    app.logger.disabled = True
    escolhidas = [int(a) for a in sys.argv[1:]] or list(MISSOES)
    total_ok = 0
    total = 0
    for n in escolhidas:
        nome, func = MISSOES[n]
        dados.reiniciar()
        inicio = len(resultados)
        func(n)
        itens = resultados[inicio:]
        ok = sum(1 for i in itens if i[2])
        total_ok += ok
        total += len(itens)
        selo = "[COMPLETA]" if ok == len(itens) else ("[PARCIAL] " if ok else "[PENDENTE]")
        print(f"\n{selo}  Missão {n} - {nome}: {ok}/{len(itens)}")
        for _, desc, passou, dica in itens:
            linha = f"   {'ok' if passou else ' X'}  {desc}"
            if not passou and dica:
                linha += f"   (dica: {dica})"
            print(linha)
    print(f"\nTotal: {total_ok}/{total} verificações")
    if not sys.argv[1:]:
        minimo = sum(1 for m, _, ok_, _ in resultados if m <= 3 and ok_)
        print(f"Meta mínima (missões 1 a 3): {minimo}/20\n")
    dados.reiniciar()
