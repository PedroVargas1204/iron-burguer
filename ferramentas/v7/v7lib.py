"""Acrescenta seções ao DAN/DDR da v6 clonando as tabelas do próprio documento.

Nada é formatado do zero: toda seção nova é um clone de uma seção que já existe
na v6, com o texto trocado. Assim o estilo dos títulos (Heading 1/2/3), o
sombreado, as bordas e as larguras continuam idênticos — e o sumário automático
continua enxergando os títulos novos.
"""
import copy
import sys

sys.path.insert(0, "/home/claude/work/mod")

from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph
from docxlib import (Montador, ajustar_colunas, celula_conteudo, clonar_par,
                     limpar, preencher_tab, tabelas_do_corpo)

W = qn


# ------------------------------------------------------------------ clonagem
def _trocar_titulo(tab, titulo):
    cab = tab.rows[0].cells[0]
    ref_p, _ = limpar(cab)
    cab._tc.append(clonar_par(ref_p, titulo))
    return tab


def nova_secao(modelo, depois, titulo):
    """Clona uma seção 2x1 (título + conteúdo) e insere depois de `depois`."""
    el = copy.deepcopy(modelo._tbl)
    depois._tbl.addnext(el)
    nova = Table(el, modelo._parent)
    _trocar_titulo(nova, titulo)
    return nova          # a célula de conteúdo é esvaziada pelo Montador


def novo_capitulo(modelo, depois, titulo):
    """Clona uma faixa de capítulo 1x1 e insere depois de `depois`."""
    el = copy.deepcopy(modelo._tbl)
    depois._tbl.addnext(el)
    nova = Table(el, modelo._parent)
    return _trocar_titulo(nova, titulo)


def par_depois(depois, modelo_par, texto):
    """Insere um parágrafo solto (fora de tabela) logo após um elemento."""
    novo = clonar_par(modelo_par, texto)
    depois._tbl.addnext(novo)
    return novo


# ------------------------------------------------------------------ montagem
def _marcar(r, tag, ligado):
    rpr = r.find(W('w:rPr'))
    if rpr is None:
        rpr = r.makeelement(W('w:rPr'), {})
        r.insert(0, rpr)
    e = rpr.find(W(tag))
    if ligado:
        if e is None:
            rpr.insert(0, rpr.makeelement(W(tag), {}))
    elif e is not None:
        rpr.remove(e)


def normalizar_tab(tbl_el, negrito_col0=True):
    """Negrito só no cabeçalho (e na 1ª coluna, quando pedido); nada em itálico.

    A tabela usada como forma vem do modelo com o corpo inteiro em negrito;
    sem isto a tabela nova sairia com formatação diferente das demais.
    """
    for ri, tr in enumerate(tbl_el.findall(W('w:tr'))):
        for ci, tc in enumerate(tr.findall(W('w:tc'))):
            for r in tc.findall('.//' + W('w:r')):
                _marcar(r, 'w:b', ri == 0 or (ci == 0 and negrito_col0))
                _marcar(r, 'w:i', False)
    return tbl_el


class M(Montador):
    """Montador com tabela de dados derivada de um modelo do próprio documento."""

    MODELO_TAB = None          # Table usada como forma para as tabelas de dados

    def par(self, texto, bold=False, italic=False):
        return Montador.par(self, texto, bold, italic)

    def tab(self, linhas, larguras, negrito_col0=True):
        el = copy.deepcopy(M.MODELO_TAB._tbl)
        ajustar_colunas(el, larguras)
        preencher_tab(el, linhas, self.doc, negrito_col0)
        normalizar_tab(el, negrito_col0)
        self.cel._tc.append(el)
        self.par("")
        return self


def mont(tab, doc):
    return M(celula_conteudo(tab), doc)


# ------------------------------------------------------------- fichas de UC
def _largura(tc, valor):
    pr = tc.find(W('w:tcPr'))
    if pr is None:
        pr = tc.makeelement(W('w:tcPr'), {})
        tc.insert(0, pr)
    for sp in pr.findall(W('w:gridSpan')):
        pr.remove(sp)
    w = pr.find(W('w:tcW'))
    if w is None:
        w = pr.makeelement(W('w:tcW'), {})
        pr.append(w)
    w.set(W('w:w'), str(valor))
    w.set(W('w:type'), 'dxa')


def _sombrear(tc, cor):
    pr = tc.find(W('w:tcPr'))
    sh = pr.find(W('w:shd'))
    if sh is None:
        sh = pr.makeelement(W('w:shd'), {})
        pr.append(sh)
    sh.set(W('w:val'), 'clear')
    sh.set(W('w:color'), 'auto')
    sh.set(W('w:fill'), cor)


def rotulo_de(linha):
    return linha.cells[0].text.strip()


def linha_modelo(tab):
    """Uma linha comum rótulo|valor, para servir de forma às linhas novas."""
    return tab.rows[1]._tr


def inserir_linha(tab, pos, rotulo, valor, doc):
    """Insere uma linha rótulo|valor na posição `pos`, clonando uma linha comum."""
    tr = copy.deepcopy(linha_modelo(tab))
    preencher_tab_linha(tr, rotulo, valor, doc)
    if pos >= len(tab.rows):
        tab._tbl.append(tr)
    else:
        tab.rows[pos]._tr.addprevious(tr)
    return tr


def preencher_tab_linha(tr, rotulo, valor, doc, estilo_valor=None):
    tcs = tr.findall(W('w:tc'))
    for tc, texto, negrito in ((tcs[0], rotulo, True), (tcs[-1], valor, None)):
        ps = tc.findall(W('w:p'))
        ref = Paragraph(ps[0], doc)
        for p in ps[1:]:
            tc.remove(p)
        novo = clonar_par(ref, texto, bold=negrito)
        tc.replace(ps[0], novo)
        if texto is valor and estilo_valor is not None:
            Paragraph(novo, doc).style = estilo_valor
    return tr


def faixa_para_linha(tab, rotulo, doc, larguras=(1900, 7739), cor='E7E6E6'):
    """Converte a faixa de título da ficha numa linha rótulo | valor.

    O nome do caso de uso continua num parágrafo Heading 3, para que o
    sumário automático siga listando os casos de uso como antes.
    """
    tr0 = tab.rows[0]._tr
    nome = tab.rows[0].cells[0].text.strip()
    estilo = tab.rows[0].cells[0].paragraphs[0].style

    novo = copy.deepcopy(linha_modelo(tab))
    preencher_tab_linha(novo, rotulo, nome, doc, estilo_valor=estilo)
    tcs = novo.findall(W('w:tc'))
    _largura(tcs[0], larguras[0])
    _largura(tcs[1], larguras[1])
    _sombrear(tcs[0], cor)
    _sombrear(tcs[1], cor)
    tr0.addprevious(novo)
    tab._tbl.remove(tr0)
    return novo


# -------------------------------------------------------------- utilitários
def achar(doc, prefixo):
    for t in tabelas_do_corpo(doc):
        if t.rows and t.rows[0].cells[0].text.strip().startswith(prefixo):
            return t
    raise KeyError(prefixo)


def reduzir_imagem(cel, altura_cm):
    """Limita a altura de uma figura já existente, mantendo a proporção.

    Uma figura que ocupa quase toda a altura útil não cabe na mesma página que
    a faixa do título: a linha inteira é empurrada e sobra uma página em
    branco antes dela.
    """
    alvo = int(altura_cm * 360000)
    for ext in list(cel._tc.iter(W('wp:extent'))) + list(cel._tc.iter(W('a:ext'))):
        cx, cy = int(ext.get('cx')), int(ext.get('cy'))
        if cy <= alvo:
            continue
        ext.set('cx', str(int(cx * alvo / cy)))
        ext.set('cy', str(alvo))
    return cel


def quebrar_antes(tab):
    """Faz o capítulo começar em página nova, sem parágrafo vazio solto."""
    p = tab.rows[0].cells[0]._tc.find(W('w:p'))
    ppr = p.find(W('w:pPr'))
    if ppr is None:
        ppr = p.makeelement(W('w:pPr'), {})
        p.insert(0, ppr)
    if ppr.find(W('w:pageBreakBefore')) is None:
        ppr.insert(0, ppr.makeelement(W('w:pageBreakBefore'), {}))
    return tab


def trocar_versao(doc, de, para, limite):
    """Troca o rótulo de versão só na capa, preservando o histórico."""
    n = 0
    for i, t in enumerate(doc.element.body.iter(W('w:t'))):
        if i > limite:
            break
        if t.text and de in t.text:
            t.text = t.text.replace(de, para)
            n += 1
    return n


def nova_linha_historico(tab, data, descricao, autor, doc):
    """Acrescenta uma linha ao HISTÓRICO DE REVISÕES, clonando a última."""
    tr = copy.deepcopy(tab.rows[-1]._tr)
    valores = {0: data, 2: descricao, 4: autor}
    for ci, tc in enumerate(tr.findall(W('w:tc'))):
        if ci not in valores:
            continue
        ps = tc.findall(W('w:p'))
        ref = Paragraph(ps[0], doc)
        for p in ps[1:]:
            tc.remove(p)
        tc.replace(ps[0], clonar_par(ref, valores[ci]))
    tab._tbl.append(tr)
    return tr


def trocar_texto(doc, de, para):
    """Troca um termo em todo o corpo, preservando a formatação de cada run."""
    n = 0
    for t in doc.element.body.iter(W('w:t')):
        if t.text and de in t.text:
            t.text = t.text.replace(de, para)
            n += 1
    return n


def soltar_sumario(tab):
    """Tira o sumário de dentro da célula e o deixa solto no corpo.

    Uma linha de tabela que precisa de mais de duas páginas não é quebrada
    corretamente: a parte que não cabe é descartada na conversão em PDF. Solto
    no corpo, o sumário pagina normalmente. A faixa "SUMÁRIO" continua sendo a
    mesma tabela do modelo, agora com uma linha só.
    """
    cel = tab.rows[1].cells[0]
    ref = tab._tbl
    for ch in list(cel._tc.iterchildren()):
        if ch.tag.endswith('}p') or ch.tag.endswith('}sdt') or ch.tag.endswith('}tbl'):
            cel._tc.remove(ch)
            ref.addnext(ch)
            ref = ch
    tab._tbl.remove(tab.rows[1]._tr)
    return tab


def atualizar_campos(doc):
    """Marca o documento para recalcular o sumário ao abrir."""
    st = doc.settings.element
    for e in st.findall(W('w:updateFields')):
        st.remove(e)
    e = st.makeelement(W('w:updateFields'), {})
    e.set(W('w:val'), 'true')
    st.append(e)
