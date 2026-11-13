"""Atualiza o sumário automático e exporta o PDF, via LibreOffice/UNO.

O `soffice --convert-to pdf` não recalcula o campo TOC: ele apenas reposiciona o
resultado já gravado. Aqui o documento é aberto de verdade, os índices são
atualizados e só então o .docx e o .pdf são gravados.
"""
import os
import subprocess
import sys
import time

import uno
from com.sun.star.beans import PropertyValue


def p(nome, valor):
    pv = PropertyValue()
    pv.Name, pv.Value = nome, valor
    return pv


def contexto(porta=2002, espera=90):
    local = uno.getComponentContext()
    resolver = local.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local)
    alvo = ("uno:socket,host=127.0.0.1,port=%d;urp;"
            "StarOffice.ComponentContext" % porta)
    fim = time.time() + espera
    while True:
        try:
            return resolver.resolve(alvo)
        except Exception:
            if time.time() > fim:
                raise
            time.sleep(0.5)


def main():
    entrada = os.path.abspath(sys.argv[1])
    saida_docx = os.path.abspath(sys.argv[2])
    saida_pdf = os.path.splitext(saida_docx)[0] + ".pdf"

    perfil = "/tmp/lo-v7"
    soffice = subprocess.Popen([
        "soffice", "--headless", "--invisible", "--nologo", "--norestore",
        "-env:UserInstallation=file://" + perfil,
        "--accept=socket,host=127.0.0.1,port=2002;urp;",
    ])
    try:
        ctx = contexto()
        desktop = ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", ctx)
        doc = desktop.loadComponentFromURL(
            uno.systemPathToFileUrl(entrada), "_blank", 0, (p("Hidden", True),))

        # várias passadas: cada atualização muda a paginação, e os números do
        # sumário só se estabilizam quando o tamanho dele para de mudar
        for _ in range(4):
            indices = doc.getDocumentIndexes()
            for i in range(indices.getCount()):
                indices.getByIndex(i).update()
            doc.refresh()
            try:
                doc.getTextFields().refresh()
            except Exception:
                pass

        doc.storeToURL(uno.systemPathToFileUrl(saida_docx),
                       (p("FilterName", "MS Word 2007 XML"),))
        doc.storeToURL(uno.systemPathToFileUrl(saida_pdf),
                       (p("FilterName", "writer_pdf_Export"),))
        doc.close(False)
        print("gravado:", saida_docx, "e", saida_pdf)
    finally:
        try:
            desktop.terminate()
        except Exception:
            pass
        soffice.wait(timeout=60)


main()
