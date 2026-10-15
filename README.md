# Holofix

Assistência remota de manutenção com óculos inteligentes.
Faculdade Pecege, Hackathon ADS, 1º semestre, 17/10/2026.

O técnico vê no óculos o passo a passo da manutenção de uma máquina. Se tiver dúvida, pede ajuda a um especialista, que responde por um painel web. A resposta aparece na lente.

Nesta hackathon o óculos é simulado: a tela dele roda no navegador, do mesmo tamanho e com o mesmo visual da lente.

## Como rodar   

    pip install flask
    python app.py

Com o servidor rodando, abra no navegador:

- http://localhost:5000/oculos  (simulação do óculos: setas do teclado e Enter)
- http://localhost:5000/painel  (painel do especialista)
- http://localhost:5000/api/maquinas  (a API direto, para ver o JSON)

## Como conferir

Em outro terminal:

    python verificar.py      (todas as missões)
    python verificar.py 2    (só a missão 2)

## Arquivos

- app.py: a API. Todos os TODOs estão aqui.
- dados.py: máquinas e procedimentos de exemplo. Podem criar os de vocês.
- verificar.py: testa as missões. Não alterar.
- static/: telas do óculos e do painel, já prontas.

## Missões

1. Máquinas 
2. Abrir e consultar ordem de serviço
3. Avançar, voltar e concluir passos

Meta mínima: missões 1 a 3.

4. Pedir ajuda (bônus)
5. Painel do especialista (bônus)
