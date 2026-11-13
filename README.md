# Iron Burguer — Análise e Projeto de Sistemas

Trabalho da disciplina **Análise e Projeto de Sistemas (APS)** — FATECS, Ciência de Dados e
Machine Learning, UniCEUB. Professor: Eduardo Castro, MSc.

**Equipe:** Gabriel Francisco Pires de Assis · Guilherme Mendes Carlos ·
Pedro Rebello Borges de Barros · Pedro Vargas dos Santos e Silva

O projeto modela o **aplicativo de autoatendimento do food truck Iron Burguer**: é o próprio
cliente quem consulta o cardápio, monta o pedido, paga e acompanha a produção pelo celular.

---

## Entrega atual — versão 7.0

| Pasta | Conteúdo |
| --- | --- |
| [`documentos/`](documentos) | DAN e DDR versão 7.0, em `.docx` e `.pdf` |
| [`diagramas/`](diagramas) | Os 36 diagramas em PNG, em resolução ampliada |
| [`apresentacao/`](apresentacao) | Apresentação sobre Padrões de Projeto (GoF) |
| [`ferramentas/v7`](ferramentas/v7) | Scripts que geram a v7 a partir da v6 |

### Documentos

Os dois documentos são o **modelo oficial da disciplina preenchido**: capa, estilos,
cabeçalho, tabelas e sumário automático são os dos arquivos fornecidos pelo professor.

- **DAN v7.0** — 23 páginas. Seções 1.1 a 3.7 na estrutura do modelo, mais **3.8 Regras de
  Negócio**, **3.9 Requisitos Não Funcionais** e **3.10 Premissas e Restrições**.
- **DDR v7.0** — 75 páginas. Capítulos 1 a 7 na estrutura do modelo, com **1.3 Escopo do
  Sistema**, **1.4 Documentos de Referência**, **2.2 Rastreabilidade Funcionalidade x Caso
  de Uso**, **2.3 Atores do Sistema** e **2.5 Matriz de Rastreabilidade da Solução**; o
  capítulo 8 traz os **26 diagramas de sequência** e os capítulos **9 a 11**, o diagrama de
  atividade, a máquina de estados e os requisitos não funcionais.

As **26 especificações de caso de uso** seguem o formato do caderno de exercícios da
disciplina: *Nome do UC*, *Funcionalidade (DAN)*, *Problema atendido*, *Descrição*,
*Ator principal*, *Pré-condições*, *Pós-condições*, *Fluxo Principal*, *Fluxos
Alternativos*, *Fluxos de Exceção*, *Regras de Negócio*, *Mensagens* e *Relacionamentos* —
cada ficha fecha a rastreabilidade UC → F → S → P dentro dela mesma.

Números do modelo: 15 problemas, 15 soluções, 26 funcionalidades, 26 casos de uso, 5 atores,
20 classes, 5 enumerações, 36 regras de negócio, 30 mensagens e 10 requisitos não
funcionais. A numeração é 1:1 entre funcionalidade e caso de uso — **F*n*** corresponde
sempre a **UC*n***.

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

- `DAN_Iron_Burguer_Entrega01.docx` e `DDR_Iron_Burguer_Entrega01.docx`, na raiz: documentos da 1ª etapa.
- `documentos/`: versões 5.0, 6.0 e 7.0 do DAN e do DDR.
- Branch `review1`: segunda frente de trabalho do grupo.
