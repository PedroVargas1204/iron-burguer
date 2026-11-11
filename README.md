# Iron Burguer — Análise e Projeto de Sistemas

Trabalho da disciplina **Análise e Projeto de Sistemas (APS)** — FATECS, Ciência de Dados e
Machine Learning, UniCEUB. Professor: Eduardo Castro, MSc.

**Equipe:** Gabriel Francisco Pires de Assis · Guilherme Mendes Carlos ·
Pedro Rebello Borges de Barros · Pedro Vargas dos Santos e Silva

O projeto modela o **aplicativo de autoatendimento do food truck Iron Burguer**: é o próprio
cliente quem consulta o cardápio, monta o pedido, paga e acompanha a produção pelo celular.

---

## Entrega atual — versão 5.0

| Pasta | Conteúdo |
| --- | --- |
| [`documentos/`](documentos) | DAN e DDR versão 5.0, em `.docx` e `.pdf` |
| [`diagramas/`](diagramas) | Os 36 diagramas em PNG, em resolução ampliada |
| [`apresentacao/`](apresentacao) | Apresentação sobre Padrões de Projeto (GoF) |
| [`prototipo/`](prototipo) | Protótipo navegável do aplicativo |

### Documentos

- **DAN v5.0** — 30 páginas. Problemas, solução, matriz de rastreabilidade, EAS,
  regras de negócio, escopo, requisitos não funcionais e premissas.
- **DDR v5.0** — 92 páginas. Diagrama de casos de uso, diagrama de classes, requisitos de
  dados, as **26 especificações de caso de uso** e os **26 diagramas de sequência**, além
  dos diagramas de atividade e de máquina de estados.

Números do modelo: 15 problemas, 15 soluções, 26 funcionalidades, 26 casos de uso, 5 atores,
20 classes, 5 enumerações, 36 regras de negócio e 30 mensagens. A numeração é 1:1 entre
funcionalidade e caso de uso — **F*n*** corresponde sempre a **UC*n***.

### Apresentação

`apresentacao/Design_Patterns_Iron_Burguer.html` abre em qualquer navegador. Use as **setas**
para navegar, **N** para as notas do orador e **Ctrl+P** para gerar um PDF. São 15 slides
sobre quatro padrões do catálogo GoF, aplicados ao projeto:

| Padrão | Categoria | Onde entra |
| --- | --- | --- |
| Prototype | Criacional | Lanches sugeridos clonados no app (UC08) |
| Singleton | Criacional | Fila de produção e numeração da senha (UC13) |
| Command | Comportamental | Operações do pedido dentro da fila (UC11, UC13) |
| State | Comportamental | Situações do pedido e transições (UC11, UC15) |

### Protótipo

`prototipo/Prototipo_Iron_Burguer.html` abre em qualquer navegador e simula o aplicativo nos
três perfis — Cliente, Produção e Gerente. Um painel lateral mostra, a cada ação, **qual regra
de negócio e qual mensagem do DDR** foram aplicadas. É uma demonstração de interface: a lógica
das regras roda de verdade, mas não há banco de dados nem operadora de pagamento real.

---

## O que mudou na versão 5.0

A versão 5.0 atende aos apontamentos da correção da 1ª etapa, incorpora as regras definidas em
sala e entrega os produtos pedidos na atualização do projeto.

| Correção do professor | Tratamento |
| --- | --- |
| A solução deve ser um aplicativo que permita ao cliente realizar o pedido | Solução reescrita em torno do autoatendimento; o caixa passou a ser o processo *As Is* |
| Problemas não cobriam toda a situação do enunciado | Reescritos a partir do enunciado: de 9 para 15 |
| Registro de pedido e registro de entrega organizados incorretamente na EAS | EAS reorganizada: Entrada = cadastros, Processamento = registros e atualizações, Saída = informações |
| Falta o ator Cliente; não tem atendente | Cliente virou ator principal com 7 casos de uso; o Atendente deixou de existir |
| Faltam casos de uso | De 12 para 26 casos de uso |
| O *extend* e o *include* estão incorretos | Refeitos: 7 inclusões e 2 extensões, cada uma justificada |
| Faltam classes no diagrama de classes | De 11 para 20 classes e 5 enumerações |

Regras definidas em sala e aplicadas em todo o modelo:

- O cancelamento **não gera reembolso**: o valor pago permanece com a empresa (RNG21).
- Pedidos cancelados aparecem **em linha própria** no relatório de fluxo de caixa (RNG35).
- O aplicativo **não oferece alteração** de pedido: para mudar, cancela-se e registra-se
  um novo (RNG16).

---

## Cronograma

| Etapa | Objeto | Data |
| --- | --- | --- |
| 1ª etapa | Apresentação sobre Padrões de Projeto | 24/11/2026 |
| 2ª etapa | Entrega do DAN e do DDR atualizados | 01/12/2026 |
| Apresentação | Apresentação do trabalho atualizado | 02/12/2026 |

---

## Versões anteriores

Os arquivos na raiz do repositório (`DAN_Iron_Burguer_Atualizado.docx`,
`DDR_Iron_Burguer_Atualizado.docx`, `Iron_Burguer_Apresentacao_DAN_DDR.pdf` e os resumos)
são da **1ª etapa** e foram mantidos como histórico. A branch `review1` guarda uma segunda
frente de trabalho do grupo, cuja organização da EAS, numeração 1:1 e estrutura das
especificações de caso de uso foram incorporadas à versão 5.0.

**Para a entrega, use sempre os arquivos de `documentos/`.**
