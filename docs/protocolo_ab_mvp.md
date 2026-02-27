# Protocolo A/B MVP - Sensibilidade de Limpeza Visual

## Objetivo
Validar rapidamente (em casa/escritorio) se o sistema detecta piora visual de limpeza entre uma cena "limpa" (A) e a mesma cena apos inserir sujeira/objetos (B).

## Escopo do teste
- Tipo: comparativo A/B por foto.
- Ambiente: sala, escritorio, bancada, piso ou superficie de maquina simulada.
- Resultado esperado: score e classificacao piores no estado B em relacao ao estado A.

## Hipotese
Para a mesma cena e mesma condicao de captura, quando adicionamos itens de sujeira visual, o sistema reduz o score de limpeza e muda a classe para `sujo`.

## Preparacao
1. Defina 3 cenas fixas:
- Cena 1: piso/sala.
- Cena 2: bancada/superficie de trabalho.
- Cena 3: equipamento/objeto simulando maquina.
2. Marque o ponto da camera no chao (fita) para repetir enquadramento.
3. Padronize iluminacao (sem ligar/desligar luz entre A e B).
4. Distancia recomendada: 1,0m a 1,5m.
5. Angulo recomendado: 30 a 45 graus da horizontal.

## Cenarios A/B
Para cada cena:
1. Tire foto A (limpo).
2. Adicione 1 a 3 itens de teste no mesmo local:
- papel pequeno,
- plastico/embalagem,
- po simulado (farinha leve em pequena quantidade),
- mancha visual (papel/pano escuro).
3. Tire foto B (sujo) sem mover camera.
4. Tire foto C (relimpo), removendo os itens para validar retorno de score.

## Volume minimo para demo com credibilidade
- 3 cenas x 5 repeticoes por cena = 15 pares A/B.
- Opcional: incluir C (relimpo) para robustez: 45 fotos totais (A, B, C).

## Regras de captura
- Mesmo celular para todo o teste.
- Evitar zoom digital.
- Evitar pessoas no frame.
- Nao alterar iluminacao entre A e B.
- Nomear arquivos no padrao:
`scene_{1|2|3}_rep_{01..05}_{A|B|C}.jpg`

## Metricas do MVP
1. Diferenca de score:
- `delta = score_B - score_A` (esperado: negativo na maior parte dos casos).
2. Taxa de sensibilidade:
- `% de pares em que B piora vs A`.
3. Retorno apos limpeza:
- `% de pares em que score_C melhora vs B`.

## Criterios de aceite para demo
- Sensibilidade A/B >= 80% (B pior que A em pelo menos 12 de 15 pares).
- Melhora B/C >= 80% (C melhor que B em pelo menos 12 de 15 pares, se C existir).
- Sem erro tecnico em upload/inferencia nas 45 fotos.

## Rubrica de classificacao sugerida
- `limpo`: nenhum objeto inesperado relevante detectado.
- `sujo`: ao menos um objeto inesperado relevante detectado.

## Estrutura de score (simples e explicavel)
Score inicial: 100.
Penalidades:
- `-8` por objeto pequeno inesperado detectado em area alvo.
- `-15` por mancha/residuo de alto contraste em area alvo.
- `-20` por acumulacao (>= 3 achados).
Clampe em `[0, 100]`.

Observacao: no MVP, a logica pode ser por heuristica sobre deteccoes + area ocupada no frame.

## Template de coleta (copiar para planilha)
Colunas:
- `timestamp`
- `scene_id`
- `repeticao`
- `estado` (A/B/C)
- `arquivo`
- `score`
- `classe`
- `achados_qtd`
- `falha_upload` (0/1)
- `falha_inferencia` (0/1)
- `observacoes`

## Execucao rapida (backend atual)
1. Subir API:
```bash
cd api
uvicorn main:app --reload
```
2. Testar upload:
```bash
curl -X POST "http://127.0.0.1:8000/detect" \
  -F "file=@/caminho/scene_1_rep_01_A.jpg"
```

## Entregavel final da demo
- Tabela com todos os pares A/B/C.
- Grafico simples por cena (`A`, `B`, `C`).
- 3 exemplos visuais (antes/depois) com score e classe.
- Relatorio final de 1 pagina com:
- objetivo,
- metodo,
- metricas,
- resultado,
- limitacoes e proximos passos.

## Limitacoes (deixar explicito na apresentacao)
- Mede limpeza visual, nao sanitizacao microbiologica/quimica.
- Resultado depende de protocolo de captura.
- Necessita calibracao com dados reais da fabrica para uso operacional.
