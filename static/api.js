// api.js - função única para conversar com o servidor (já pronto)
//
// Uso:
//   const r = await chamarApi("GET", "/api/maquinas");
//   if (r.ok) { ...r.dados... } else { alert(r.erro); }

async function chamarApi(metodo, url, corpo) {
  const opcoes = { method: metodo, headers: {} };
  if (corpo !== undefined) {
    opcoes.headers["Content-Type"] = "application/json";
    opcoes.body = JSON.stringify(corpo);
  }

  let resposta;
  try {
    resposta = await fetch(url, opcoes);
  } catch (e) {
    return { ok: false, status: 0, dados: null, erro: "Sem conexão com o servidor. Ele está rodando?" };
  }

  let dados = null;
  try {
    dados = await resposta.json();
  } catch (e) {
    // O Flask devolve HTML (não JSON) quando a rota não existe
    return {
      ok: false, status: resposta.status, dados: null,
      erro: "Rota " + metodo + " " + url + " ainda não existe no servidor (veja o app.py).",
    };
  }

  if (!resposta.ok) {
    return { ok: false, status: resposta.status, dados: dados, erro: (dados && dados.erro) || "Erro " + resposta.status };
  }
  return { ok: true, status: resposta.status, dados: dados, erro: null };
}
