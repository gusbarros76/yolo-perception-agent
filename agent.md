# agent.md

## Contexto
Este repositório implementa a camada de percepção visual do projeto: recebe imagem, executa detecção (YOLOv8) e retorna eventos estruturados em JSON.

## Objetivo do trabalho
Evoluir este codebase de MVP para uma base estável, testável e pronta para integração com agentes consumidores.

## Escopo atual (o que existe)
- API FastAPI em `api/main.py`
- Endpoint `GET /health`
- Endpoint `POST /detect` com upload de imagem
- Abstração de inferência (`Detector`) em `api/inference/base.py`
- Implementação real YOLO em `api/inference/yolo.py`
- Schema de saída em `api/schemas/detection.py`
- Web ainda não implementado (somente `web/README.md`)

## Não-escopo atual
- Lógica de decisão/autonomia do agente
- Persistência de eventos
- Autenticação/autorização
- Streaming em tempo real

## Diretrizes para mudanças
- Manter separação clara entre `API`, `inferência` e `schema`.
- Evitar acoplamento direto da API ao provedor de modelo; preferir injeção/seleção configurável de detector.
- Tratar erros de entrada explicitamente (arquivo inválido, imagem corrompida, formato não suportado).
- Qualquer novo endpoint deve ter contrato de request/response tipado com Pydantic.
- Preservar respostas determinísticas no formato:
  - `label: str`
  - `confidence: float`
  - `bbox: {x,y,w,h}` inteiros

## Padrão de qualidade mínimo (Definition of Done)
- Testes automatizados para comportamento principal e falhas esperadas.
- Tipagem e lint sem erros.
- `README` atualizado com execução local e exemplos de uso.
- Sem dependências locais acidentais versionadas (ex.: `.venv`).
- Mudanças observáveis por endpoint devem vir com exemplo de payload/resposta.

## Prioridades recomendadas
1. Criar suíte de testes (`pytest`) para `/health`, `/detect`, e validação de payload.
2. Tornar detector configurável por ambiente (mock vs yolo real).
3. Adicionar tratamento de exceção no pipeline de imagem/inferência.
4. Versionar contrato de API (ex.: prefixo `/v1`).
5. Implementar frontend mínimo para upload + visualização do JSON retornado.

## Riscos atuais
- Sem testes: alto risco de regressão.
- Sem validação robusta de arquivo: risco de erro 500 em entradas inválidas.
- Dependências sem pinagem em `api/requirements.txt`: baixa reprodutibilidade.
- Presença de ambiente virtual local dentro do projeto pode poluir fluxo de build/CI.

## Convenções operacionais para próximas tarefas
- Antes de codar: confirmar impacto no contrato da API.
- Durante implementação: priorizar mudanças pequenas e verificáveis.
- Após implementação: executar testes e registrar resultado no retorno da tarefa.
- Sempre documentar trade-offs quando optar por solução temporária.
