"""DDR v7 = DDR v6 + 1.3, 1.4, 2.2, 2.3, 2.5, capítulos 9 a 11 e fichas no formato do caderno."""
import json
import re
import sys

sys.path.insert(0, "/home/claude/work/v7")
sys.path.insert(0, "/home/claude/work/mod")

from docx import Document
from docx.oxml.ns import qn
from docxlib import clonar_par, tabelas_do_corpo
import v7lib as L

W = qn
V5 = "/home/claude/work/v5/"

MOD = json.load(open(V5 + "modelo.json"))
UC = MOD["UC"]
PS = {p["id"]: p for p in MOD["PS"]}
ATORES = MOD["ATORES"]
FASEC = {"E": "Entrada", "P": "Processamento", "S": "Saída"}
NOME = {u["n"]: u["nome"] for u in UC}

RNF = [
    ["RNF01", "Desempenho", "O cardápio deve ser apresentado em até 3 segundos e a confirmação do pedido processada em até 5 segundos, considerando conexão móvel no local de atendimento."],
    ["RNF02", "Desempenho", "O aplicativo deve suportar pelo menos 50 clientes registrando pedidos simultaneamente, compatível com o pico de demanda relatado pelo proprietário."],
    ["RNF03", "Usabilidade", "O cliente deve conseguir montar e confirmar um pedido em no máximo 5 toques a partir da tela inicial, sem treinamento prévio."],
    ["RNF04", "Usabilidade", "A situação do pedido deve estar visível na tela inicial do cliente, sem necessidade de navegação adicional."],
    ["RNF05", "Segurança", "As senhas de acesso devem ser armazenadas cifradas e o tráfego entre o aplicativo e o servidor deve usar canal seguro."],
    ["RNF06", "Segurança", "Os dados do cartão não trafegam nem são armazenados pelo aplicativo: a captura e a autorização são feitas pela Operadora de Pagamento."],
    ["RNF07", "Segurança", "O acesso a cada funcionalidade é controlado pelo perfil do usuário, e todo cliente só enxerga os seus próprios pedidos (RNG09 e RNG31)."],
    ["RNF08", "Disponibilidade", "O aplicativo deve estar disponível durante todo o horário de atendimento cadastrado."],
    ["RNF09", "Portabilidade", "O aplicativo deve funcionar nos navegadores e sistemas operacionais móveis de maior uso, sem exigir instalação de programa adicional."],
    ["RNF10", "Rastreabilidade", "Toda mudança de situação de pedido deve registrar data, hora e usuário responsável, permitindo auditoria das entregas."],
]

ESTADOS = [
    ["Recebido", "Pedido montado e confirmado pelo cliente, ainda sem pagamento",
     "Pagar (UC12) ou cancelar (UC11). O aplicativo não oferece alteração de itens (RNG16)."],
    ["Pago", "Pagamento autorizado; o pedido entra no fim da fila de produção",
     "Entrar em produção (UC13) ou ser cancelado sem reembolso, com devolução dos ingredientes ao estoque (RNG21 e RNG22)."],
    ["Em produção", "A produção iniciou o preparo, respeitada a ordem da fila",
     "Ser concluído e passar a Pronto (UC14). A partir daqui o pedido não pode mais ser cancelado (RNG17)."],
    ["Pronto", "Produto finalizado; o cliente é notificado e a senha é chamada",
     "Ser entregue (UC15)."],
    ["Entregue", "Produto retirado pelo cliente. Estado final.",
     "Nada: o pedido não pode ser entregue duas vezes (RNG26)."],
    ["Cancelado", "Pedido cancelado pelo cliente antes da produção. Estado final.",
     "Nada. O valor pago, se houver, permanece com a empresa e aparece em linha própria no fluxo de caixa (RNG21 e RNG35)."],
]

ESCOPO = [
    ["Dentro do escopo", "Fora do escopo"],
    ["Cadastros de produto, ingrediente, ficha técnica, fornecedor, cliente, funcionário e local e horário de atendimento",
     "Emissão de documento fiscal"],
    ["Registro, pagamento, cancelamento e acompanhamento do pedido pelo próprio cliente",
     "Alteração de itens de um pedido já registrado: o aplicativo não oferece essa opção (RNG16)"],
    ["Controle da fila de produção, da situação do pedido e da entrega",
     "Reembolso ou estorno de pagamento: o cancelamento não devolve o valor pago (RNG21)"],
    ["Controle de estoque de ingredientes, com baixa na venda e reposição na compra",
     "Entrega em domicílio e integração com aplicativos de entrega"],
    ["Relatórios de pedidos e entregas, de fluxo de caixa e de estoque",
     "Processamento da transação financeira, feito pela Operadora de Pagamento"],
]

DOCREF = [
    ["Documento", "Conteúdo utilizado"],
    ["Enunciado Iron Burguer - Prof. Eduardo Castro, UniCEUB",
     "Descrição do negócio, do processo atual e dos problemas relatados pelo proprietário"],
    ["DAN - Documento de Análise de Negócio do Aplicativo Iron Burguer, versão 7.0",
     "Problemas, solução, regras de negócio, requisitos não funcionais, matriz de rastreabilidade e EAS"],
    ["Correção da 1ª etapa - Prof. Eduardo Castro",
     "Apontamentos sobre a solução, o diagrama de casos de uso e o diagrama de classes"],
    ["Regras definidas em sala de aula",
     "Cancelamento sem reembolso, cancelados no fluxo de caixa e ausência de alteração de pedido no aplicativo"],
    ["Caderno de Exercícios - Diagrama de Sequência, Prof. Eduardo Castro",
     "Notação adotada nos diagramas de sequência: boundary, control, entity, create, fragmentos alt e loop e mensagens numeradas"],
    ["Modelo de DDR com UML - UniCEUB, versão 2",
     "Estrutura e seções deste documento"],
]


def tag(n):
    return "UC%02d" % n


# ------------------------------------------------------------------ entrada
ENT_DDR, ENT_DAN, SAI = sys.argv[1], sys.argv[2], sys.argv[3]

d = Document(ENT_DDR)
TS = tabelas_do_corpo(d)
SECAO = TS[7]                 # 2x1 "1.1 Objetivo do Documento"
CAPITULO = TS[6]              # 1x1 "1. INTRODUÇÃO"
L.M.MODELO_TAB = TS[20]       # 26x3 "Classe"

# a matriz vem do próprio DAN, para que os dois documentos digam o mesmo
dan = Document(ENT_DAN)
MATRIZ = [[c.text.strip() for c in r.cells]      # as quebras de linha são mantidas
          for r in tabelas_do_corpo(dan)[15].rows]


def mont(t):
    return L.mont(t, d)


# ------------------------------------------------------- capítulo 1: 1.3 e 1.4
t13 = L.nova_secao(SECAO, TS[8], "1.3 Escopo do Sistema")
m = mont(t13)
m.par("O Iron Burguer é um aplicativo de autoatendimento: é o próprio cliente quem "
      "consulta o cardápio, monta o pedido, paga e acompanha a produção pelo celular. A "
      "operação interna do food truck passa a ser feita pelos perfis Gerente e Produção "
      "dentro do mesmo aplicativo.")
m.tab(ESCOPO, [4819, 4820], False)
m.fim()

t14 = L.nova_secao(SECAO, t13, "1.4 Documentos de Referência")
m = mont(t14)
m.tab(DOCREF, [3400, 6239], False)
m.fim()

# --------------------------------------------------- capítulo 2: 2.2, 2.3 e 2.5
L._trocar_titulo(TS[11], "2.4 Relacionamentos do Diagrama de Caso de Uso")

# o diagrama de caso de uso tinha 22,1 cm de altura e não cabia na mesma
# página que a faixa 2.1, o que deixava uma página em branco antes dele
L.reduzir_imagem(TS[10].rows[1].cells[0], 20.3)

t22 = L.nova_secao(SECAO, TS[10], "2.2 Rastreabilidade: Funcionalidade x Caso de Uso")
m = mont(t22)
m.par("Cada funcionalidade da EAS deu origem a exatamente um caso de uso, e a numeração "
      "foi mantida: a funcionalidade Fn corresponde sempre ao caso de uso UCn.")
m.tab([["Fase", "Funcionalidade (DAN)", "Caso de Uso (DDR)", "Ator"]] +
      [[FASEC[u["fase"]], "F%d - %s" % (u["n"], u["nome"]),
        "%s - %s" % (tag(u["n"]), u["nome"]),
        u["ator"] or "(inclusão/extensão)"] for u in UC],
      [1200, 3100, 3100, 2239], False)
m.fim()

t23 = L.nova_secao(SECAO, t22, "2.3 Atores do Sistema")
m = mont(t23)
m.par("O aplicativo tem três atores primários - Cliente, Gerente e Produção - e um ator "
      "secundário, a Operadora de Pagamento, que é um sistema externo. O ator Usuário é "
      "uma generalização: reúne o que é comum a quem acessa o aplicativo.")
m.tab([["Ator", "Tipo", "Descrição"]] +
      [[a["nome"], a["tipo"], a["desc"]] for a in ATORES], [1700, 1900, 6039])
m.tab([["Decisão de modelagem", "Justificativa"],
       ["Funcionário é classe, mas não é ator",
        "No diagrama de classe, Funcionario generaliza Gerente e Producao para fatorar "
        "matrícula e data de admissão. No diagrama de caso de uso a generalização "
        "significa herdar casos de uso, e Funcionário não tem nenhum caso de uso "
        "próprio: por isso ele não aparece como ator."]], [2400, 7239])
m.fim()

t25 = L.nova_secao(SECAO, TS[11], "2.5 Matriz de Rastreabilidade da Solução")
m = mont(t25)
m.par("A matriz é a mesma do DAN, estendida até o caso de uso: ela mostra, em uma única "
      "leitura, de qual problema cada caso de uso nasceu. Como Fn corresponde a UCn, a "
      "última coluna é a tradução direta da anterior.")
m.tab([MATRIZ[0] + ["Caso de Uso"]] +
      [linha + [", ".join(tag(int(n)) for n in re.findall(r"\bF(\d+)\b", linha[3]))]
       for linha in MATRIZ[1:]],
      [900, 2600, 2600, 1800, 1739], True)
m.fim()

# ------------------------------------------------- fichas: rótulos do caderno
FICHAS = [TS[i] for i in list(range(35, 42)) + list(range(43, 54)) + list(range(55, 63))]
assert len(FICHAS) == 26, len(FICHAS)


def rotulos(tab):
    return [r.cells[0].text.strip() for r in tab.rows]


def renomear_rotulo(tab, de, para):
    for r in tab.rows:
        if r.cells[0].text.strip() == de:
            cel = r.cells[0]
            ps = cel._tc.findall(W('w:p'))
            from docx.text.paragraph import Paragraph
            ref = Paragraph(ps[0], d)
            for p in ps[1:]:
                cel._tc.remove(p)
            cel._tc.replace(ps[0], clonar_par(ref, para, bold=True))
            return True
    return False


for i, tab in enumerate(FICHAS, start=1):
    nome = tab.rows[0].cells[0].text.strip()
    assert nome.startswith(tag(i)), (i, nome)

    L.faixa_para_linha(tab, "Nome do UC", d)
    renomear_rotulo(tab, "Funcionalidade", "Funcionalidade (DAN)")
    renomear_rotulo(tab, "Fluxo Básico", "Fluxo Principal")

    pid = UC[i - 1]["ps"].split("/")[0]
    pos = rotulos(tab).index("Funcionalidade (DAN)") + 1
    L.inserir_linha(tab, pos, "Problema atendido",
                    "%s - %s" % (pid, PS[pid]["prob"]), d)

    if "Relacionamentos" not in rotulos(tab):
        L.inserir_linha(tab, len(tab.rows), "Relacionamentos", "Não se aplica", d)

# --------------------------------------------------------- capítulos 9, 10 e 11
ULTIMO = TS[-1]               # 2x1 "UC26 - ..." do capítulo 8

c9 = L.quebrar_antes(L.novo_capitulo(CAPITULO, ULTIMO, "9. DIAGRAMA DE ATIVIDADE"))
t = L.nova_secao(SECAO, c9, "9.1 Fluxo do Pedido no Aplicativo")
m = mont(t)
m.par("O diagrama de atividade apresenta o fluxo do pedido de ponta a ponta, em raias "
      "que identificam de quem é cada atividade. As raias tornam visível o ponto central "
      "da solução: consultar o cardápio, montar, confirmar e pagar o pedido são "
      "atividades do Cliente, e não de um atendente no caixa.")
m.imagem(V5 + "atividade.png", 14.5)
m.fim()

c10 = L.quebrar_antes(L.novo_capitulo(CAPITULO, t, "10. DIAGRAMA DE MÁQUINA DE ESTADOS"))
t = L.nova_secao(SECAO, c10, "10.1 Ciclo de Vida do Pedido")
m = mont(t)
m.par("O diagrama detalha o ciclo de vida de um objeto da classe Pedido. Os seis estados "
      "são exatamente os literais da enumeração SituacaoPedido, e as transições "
      "representadas são as únicas que a operação alterarSituacao() deve aceitar.")
m.imagem(V5 + "estados.png", 10.5)
m.tab([["Estado", "Significado", "O que pode acontecer a seguir"]] + ESTADOS,
      [1400, 3400, 4839])
m.fim()

c11 = L.novo_capitulo(CAPITULO, t, "11. REQUISITOS NÃO FUNCIONAIS")
t = L.nova_secao(SECAO, c11, "11.1 Requisitos Não Funcionais")
m = mont(t)
m.par("Os requisitos não funcionais definem as qualidades que o aplicativo deve "
      "apresentar, independentemente das funcionalidades. São os mesmos relacionados na "
      "seção 3.9 do DAN.")
m.tab([["Código", "Categoria", "Requisito Não Funcional"]] + RNF, [1100, 1700, 6839])
m.fim()

# ------------------------------------------------------------------- versão
L.trocar_versao(d, "Versão 6.0", "Versão 7.0", 30)
L.nova_linha_historico(
    TS[1], "12/11/2026",
    "Versão 7.0 - Acrescentados o escopo, os documentos de referência, a "
    "rastreabilidade Funcionalidade x Caso de Uso, os atores, a matriz de "
    "rastreabilidade, o diagrama de atividade, a máquina de estados e os "
    "requisitos não funcionais; especificações de caso de uso no formato do "
    "caderno de exercícios", "Equipe técnica", d)

# o rótulo mudou para "Fluxo Principal": as citações no corpo acompanham
print("citações de 'Fluxo Básico' trocadas:", L.trocar_texto(d, "Fluxo Básico", "Fluxo Principal"))

L.soltar_sumario(TS[5])
L.atualizar_campos(d)
d.save(SAI)
print("DDR v7 gravado:", SAI)
