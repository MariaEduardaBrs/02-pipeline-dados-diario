# Pipeline diário de dados

![CI](https://github.com/MariaEduardaBrs/02-pipeline-dados-diario/actions/workflows/ci.yml/badge.svg)

Pipeline automatizado que coleta o clima de três cidades todos os dias, guarda o histórico, gera um gráfico e publica uma página pública, tudo com GitHub Actions, sem servidor próprio.

**Página publicada:** https://mariaeduardabrs.github.io/02-pipeline-dados-diario/

Projeto de estudo, feito para praticar CI/CD, automação e boas práticas de engenharia.

## Como funciona

```mermaid
flowchart LR
    A[Agendamento diário] --> B[Coleta na API Open-Meteo]
    B --> C[Histórico em CSV na branch dados]
    C --> D[Gráfico SVG e página HTML]
    D --> E[GitHub Pages]
```

1. Um workflow agendado (`publicar.yml`) roda todo dia por volta das 06:17 (horário de Brasília).
2. O script busca temperatura, umidade e vento de São Paulo, Salvador e Brasília.
3. Os registros novos são acrescentados a um CSV guardado na branch `dados`. Rodar duas vezes no mesmo horário não duplica linhas.
4. O pipeline gera um gráfico de linhas em SVG e uma página HTML.
5. A página é publicada no GitHub Pages.

## Estrutura

| Arquivo | Função |
|---|---|
| `coleta.py` | Busca os dados na API pública (apenas biblioteca padrão do Python) |
| `historico.py` | Lê e grava o CSV, sem duplicar registros |
| `grafico.py` | Gera o gráfico em SVG, com datas e grade |
| `pagina.py` | Gera a página HTML com gráfico, tabela e créditos |
| `pipeline.py` | Encadeia coleta, histórico, gráfico e página |
| `estatisticas.py` | Funções auxiliares de estatística (ainda não usadas no pipeline) |
| `.github/workflows/ci.yml` | Lint e testes a cada push e pull request |
| `.github/workflows/publicar.yml` | Coleta agendada e publicação no Pages |
| `.github/dependabot.yml` | Atualização semanal das dependências |

## Decisões de engenharia

- **Testes sem internet.** A API é substituída por respostas falsas, então a esteira não depende de serviço externo.
- **Histórico idempotente.** A chave de cada registro é a dupla (cidade, momento), então reexecutar não duplica dados.
- **Gráfico feito à mão em SVG.** Evita bibliotecas pesadas e dependências extras. Os pontos são posicionados pela data real da coleta.
- **Entrada tratada como não confiável.** Todo texto que vai para HTML ou SVG passa por `escape`.
- **Histórico em branch separada.** A `main` é protegida, então o robô grava os dados na branch `dados`.
- **Permissões mínimas.** O workflow lê por padrão. Só o job de coleta escreve (para gravar o histórico) e só o job de publicação tem permissão do Pages.
- **Proteção da `main`.** Só recebe código por pull request com Lint e Testes verdes (Python 3.12 e 3.13).
- **Dependências travadas.** Versões fixas no `requirements.txt`, instaladas só em formato compilado (`--only-binary`), e Dependabot semanal para atualizá-las.
- **Execuções concorrentes.** O `concurrency` impede duas publicações ao mesmo tempo.

## Como rodar os testes

```
pip install -r requirements.txt
python -m pytest
```

## Limitações conhecidas

- Os dados vêm de uma única fonte e de apenas três cidades.
- O agendamento do GitHub pode atrasar alguns minutos e, em repositórios públicos sem atividade, pode ser pausado depois de um tempo.
- As actions estão referenciadas por tag (por exemplo `@v4`), e não por SHA de commit.
- Próximos passos: varredura de segredos, análise de qualidade com cobertura e fixação das actions por SHA.

## Créditos

Dados meteorológicos: [Open-Meteo.com](https://open-meteo.com/), licença CC BY 4.0.


