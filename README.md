# Iron Burguer — Análise e Projeto de Sistemas

Trabalho da disciplina **Análise e Projeto de Sistemas (APS)** — FATECS, Ciência de Dados e
Machine Learning, UniCEUB. Professor: Eduardo Castro, MSc.

**Equipe:** Gabriel Francisco Pires de Assis · Guilherme Mendes Carlos ·
Pedro Rebello Borges de Barros · Pedro Vargas dos Santos e Silva

O projeto modela o **aplicativo de autoatendimento do food truck Iron Burguer**: é o próprio
cliente quem consulta o cardápio, monta o pedido, paga e acompanha a produção pelo celular.

---

## Entrega atual — versão 8.0

| Arquivo ou pasta | Conteúdo |
| --- | --- |
| `DAN_Iron_Burguer_v8.pdf` | Documento de Análise de Negócio |
| `DDR_Iron_Burguer_v8.pdf` | Documento de Definição de Requisitos |
| [`docs/`](docs) | Versões `.docx` do DAN e do DDR, diagramas em PNG e a apresentação de Design Patterns em HTML |

Conteúdo de `docs/`:

| Arquivo ou pasta | Conteúdo |
| --- | --- |
| `DAN_Iron_Burguer_v8.docx` e `DDR_Iron_Burguer_v8.docx` | Documentos editáveis |
| [`diagramas/`](docs/diagramas) | Diagramas em PNG: EAS, casos de uso, classes, organograma e os 26 de sequência |
| `Design_Patterns_Iron_Burguer.html` | Apresentação do trabalho de Design Patterns (ver abaixo) |

### Documentos

Os dois documentos são o **modelo oficial da disciplina preenchido**: capa, estilos,
cabeçalho, tabelas e sumário automático são os dos arquivos fornecidos pelo professor.

- **DAN v8.0** — 22 páginas. Seções 1.1 a 3.7 na estrutura do modelo, mais **3.8 Regras de
  Negócio**.
- **DDR v8.0** — 72 páginas. Capítulos 1 a 7 na estrutura do modelo, com **1.3 Escopo do
  Sistema**, **1.4 Documentos de Referência**, **2.2 Rastreabilidade Funcionalidade x Caso
  de Uso**, **2.3 Atores do Sistema** e **2.5 Matriz de Rastreabilidade da Solução**; o
  capítulo 8 traz os **26 diagramas de sequência**.

As **26 especificações de caso de uso** seguem o formato do caderno de exercícios da
disciplina: *Nome do UC*, *Funcionalidade (DAN)*, *Problema atendido*, *Descrição*,
*Ator principal*, *Pré-condições*, *Pós-condições*, *Fluxo Principal*, *Fluxos
Alternativos*, *Fluxos de Exceção*, *Regras de Negócio*, *Mensagens* e *Relacionamentos* —
cada ficha fecha a rastreabilidade UC → F → S → P dentro dela mesma.

Números do modelo: 15 problemas, 15 soluções, 26 funcionalidades, 26 casos de uso, 5 atores,
20 classes, 5 enumerações, 36 regras de negócio e 30 mensagens. A numeração é 1:1 entre funcionalidade e caso de uso — **F*n*** corresponde
sempre a **UC*n***.

---

## Trabalho de Design Patterns

Atividade separada da entrega do DAN e do DDR: pesquisa em grupo sobre categorias e padrões
de projeto do catálogo GoF, apresentada em **25/11/2026** (cerca de 15 minutos). Os
exemplos usam o modelo do aplicativo Iron Burguer.

O grupo apresenta **uma categoria, a dos padrões comportamentais, e dois padrões: Command e
State**. Os dois atacam problemas do enunciado: o estoque de um pedido pago que é cancelado e
o pedido entregue duas vezes. Atendendo ao pedido do professor, cada padrão traz dois
**diagramas de classe**: o da **estrutura padrão** (participantes do GoF, com base no quadro
"Estrutura" do Refactoring.Guru) e o da **implementação** no Iron Burguer, com as mesmas
classes do código mostrado no slide seguinte. São **14 slides**.

| Arquivo | Conteúdo |
| --- | --- |
| `Design_Patterns_Iron_Burguer.pdf` | Apresentação em PDF, 14 slides: para cada padrão, conceito, estrutura padrão, implementação e código |
| `Design_Patterns_Guia_de_Estudo.pdf` | Divisão da apresentação entre os integrantes, fala sugerida para cada slide, como ler os diagramas UML e perguntas prováveis com respostas |
| [`docs/diagramas/design_patterns/`](docs/diagramas/design_patterns) | Os 4 diagramas de classe em PNG (`*_estrutura.png` e `*_implementacao.png`) |
| `docs/Design_Patterns_Iron_Burguer.html` | Versão anterior da apresentação (15 slides, com quatro padrões de duas categorias e sem os diagramas de classe) |

| Integrante | Slides |
| --- | --- |
| Gabriel | 1 a 4 (abertura, escolha da categoria e conceitos) e 14 (síntese) |
| Guilherme | 5 a 7 (padrões comportamentais, conceito e estrutura do Command) |
| Pedro Rebello | 8 e 9 (classes e código do Command no Iron Burguer) |
| Pedro Vargas | 10 a 13 (State) |

| Padrão | Categoria | Exemplo no Iron Burguer |
| --- | --- | --- |
| Command | Comportamental | Baixa de estoque desfeita no cancelamento de pedido pago (UC17, UC18) |
| State | Comportamental | Situações do pedido e as operações permitidas em cada uma (UC11, UC14, UC15) |

--- | --- |
| `Design_Patterns_Iron_Burguer.pdf` | Apresentação em PDF, 23 slides: para cada padrão, conceito, estrutura padrão, implementação e código |
| `Design_Patterns_Guia_de_Estudo.pdf` | Divisão da apresentação entre os integrantes, fala sugerida para cada slide, como ler os diagramas UML e perguntas prováveis com respostas |
| [`docs/diagramas/design_patterns/`](docs/diagramas/design_patterns) | Os 8 diagramas de classe em PNG (`*_estrutura.png` e `*_implementacao.png`) |
| `docs/Design_Patterns_Iron_Burguer.html` | Versão anterior da apresentação (15 slides, sem os diagramas de classe), com notas do orador: **setas** para navegar, **N** para as notas |

| Integrante | Slides |
| --- | --- |
| Gabriel | 1 a 5 (abertura, conceitos e criacionais) e 23 (síntese) |
| Guilherme | 6 a 13 (Prototype e Singleton) |
| Pedro Rebello | 14 a 18 (comportamentais e Command) |
| Pedro Vargas | 19 a 22 (State) |

| Padrão | Categoria | Exemplo no Iron Burguer |
| --- | --- | --- |
| Prototype | Criacional | Incluir um produto a partir de outro, com a ficha técnica (UC01, RNG02) |
| Singleton | Criacional | Fila de produção única para o Cliente e a Produção (UC12, UC13) |
| Command | Comportamental | Baixa de estoque desfeita no cancelamento de pedido pago (UC17, UC18) |
| State | Comportamental | Situações do pedido e as operações permitidas em cada uma (UC11, UC14, UC15) |

---

## Correções da 1ª entrega

O DAN e o DDR atendem aos apontamentos da correção da 1ª entrega, incorporam as regras definidas
em sala e trazem os produtos pedidos na atualização do projeto.

| Correção do professor | Tratamento |
| --- | --- |
| A solução deve ser um aplicativo que permita ao cliente realizar o pedido | Solução reescrita em torno do autoatendimento; o caixa passou a ser o processo *As Is* |
| Problemas não cobriam toda a situação do enunciado | Reescritos a partir do enunciado: de 9 para 15 |
| Registro de pedido e registro de entrega organizados incorretamente na EAS | EAS reorganizada: Entrada = cadastros, Processamento = registros e atualizações, Saída = informações |
| Falta o ator Cliente; não tem atendente | Cliente é o ator principal; o Atendente deixou de existir |
| Faltam casos de uso | De 12 para 26 casos de uso |
| O *extend* e o *include* estão incorretos | Refeitos: 6 inclusões e 2 extensões, cada uma justificada |
| Faltam classes no diagrama de classes | De 11 para 20 classes e 5 enumerações |

Regras definidas em sala e aplicadas em todo o modelo:

- O cancelamento **não gera reembolso**: o valor pago permanece com a empresa (RNG21).
- Pedidos cancelados aparecem **em linha própria** no relatório de fluxo de caixa (RNG35).
- O aplicativo **não oferece alteração** de pedido: para mudar, cancela-se e registra-se
  um novo (RNG16).

---

## Cronograma

| Data | Objeto |
| --- | --- |
| 25/11/2026 | Apresentação do trabalho de Design Patterns |
| 01/12/2026 | Entrega do DAN e do DDR atualizados |
| 02/12/2026 | Apresentação do trabalho atualizado |

---

## Versões anteriores

- `DAN_Iron_Burguer_Entrega01.docx` e `DDR_Iron_Burguer_Entrega01.docx`: documentos da 1ª entrega.
- As versões 5.0, 6.0 e 7.0 do DAN e do DDR ficam no histórico do repositório.
- Branch `review1`: segunda frente de trabalho do grupo.
