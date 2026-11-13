"""DAN v7 = DAN v6 + 3.8 Regras de Negócio, 3.9 RNF e 3.10 Premissas e Restrições."""
import json
import sys

sys.path.insert(0, "/home/claude/work/v7")
sys.path.insert(0, "/home/claude/work/mod")

from docx import Document
from docxlib import tabelas_do_corpo
import v7lib as L

MOD = json.load(open("/home/claude/work/v5/modelo.json"))
RNG = MOD["RNG"]

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

PREM = [
    ["Premissa", "O cliente possui celular com acesso à internet no local de atendimento."],
    ["Premissa", "O food truck dispõe de conexão de dados durante todo o horário de atendimento."],
    ["Premissa", "A Operadora de Pagamento responde à solicitação de autorização em tempo real."],
    ["Premissa", "Os dois funcionários passam a se dedicar à produção e à entrega, já que o pedido deixa de ser feito no caixa."],
    ["Restrição", "O pagamento é feito exclusivamente pelo aplicativo, por cartão ou PIX; não há pagamento em dinheiro."],
    ["Restrição", "O aplicativo não permite alterar um pedido já confirmado: a mudança é feita por cancelamento e novo pedido (RNG16)."],
    ["Restrição", "O cancelamento não gera reembolso ao cliente (RNG21)."],
    ["Restrição", "A emissão de documento fiscal está fora do escopo desta versão."],
    ["Restrição", "Não há entrega em domicílio: a retirada é feita no próprio food truck."],
]

ENT = sys.argv[1]
SAI = sys.argv[2]

d = Document(ENT)
TS = tabelas_do_corpo(d)
MODELO_SECAO = TS[3]            # 2x1 "1.1 Empresa"
L.M.MODELO_TAB = TS[15]         # 16x4 "Fase (E/P/S)"

ref = L.achar(d, "3.7 Usuários x Funcionalidade")

t = L.nova_secao(MODELO_SECAO, ref, "3.8 Regras de Negócio")
m = L.mont(t, d)
m.par("As regras de negócio descrevem as condições gerais que precisam ser respeitadas "
      "para que os objetivos específicos da seção 3.4 sejam atingidos. Estão "
      "consolidadas abaixo e são referenciadas, uma a uma, nas especificações de caso "
      "de uso do DDR.")
m.tab([["Código", "Regra de Negócio", "Casos de Uso"]] + [list(r) for r in RNG],
      [1100, 6400, 2139])
m.fim()

t2 = L.nova_secao(MODELO_SECAO, t, "3.9 Requisitos Não Funcionais")
m = L.mont(t2, d)
m.par("Os requisitos não funcionais definem as qualidades que o aplicativo deve "
      "apresentar, independentemente das funcionalidades. São detalhados no capítulo 11 "
      "do DDR.")
m.tab([["Código", "Categoria", "Requisito Não Funcional"]] + RNF, [1100, 1700, 6839])
m.fim()

t3 = L.nova_secao(MODELO_SECAO, t2, "3.10 Premissas e Restrições")
m = L.mont(t3, d)
m.par("As premissas são condições assumidas como verdadeiras para a construção da "
      "solução. As restrições limitam as alternativas de projeto e delimitam o que o "
      "aplicativo não fará nesta versão.")
m.tab([["Tipo", "Descrição"]] + PREM, [1500, 8139])
m.fim()

L.trocar_versao(d, "Versão 6.0", "Versão 7.0", 30)
L.trocar_versao(d, "VERSÃO 6.0", "VERSÃO 7.0", 30)

L.atualizar_campos(d)
d.save(SAI)
print("DAN v7 gravado:", SAI)
