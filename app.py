import streamlit as st
from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


def moeda_br(valor, tam):
    if isinstance(valor, str):
        valor = valor.replace(".", "").replace(",", ".")
    try:
        valor = float(valor)
    except Exception:
        valor = 0.0
    s = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s.rjust(tam)


def data_br(data):
    if isinstance(data, str) and "/" in data:
        return data
    if isinstance(data, datetime):
        return data.strftime("%d/%m/%Y")
    return ""


def texto_esq(txt, tam):
    # Texto alinhado à esquerda, espaços à direita
    return str(txt)[:tam].ljust(tam)


def texto_dir(txt, tam):
    # Texto alinhado à direita, espaços à esquerda
    return str(txt)[:tam].rjust(tam)


def num_dir(num, tam):
    # Numérico alinhado à direita, zeros à esquerda
    return str(num)[:tam].zfill(tam)


header_fields = [
    ("Tipo", "0", 1),
    ("Tipo de Movimentação", "01", 2),
    ("Data do arquivo", datetime.now().strftime("%d/%m/%Y"), 10),
    ("Data de inicio do arquivo", datetime.now().strftime("%d/%m/%Y"), 10),
    ("Data de fim do arquivo", datetime.now().strftime("%d/%m/%Y"), 10),
    ("Filler", "", 176),
    ("Código sequencial do arquivo", "1", 10),
    ("Marcador de final de linha", "*", 1),
]

detail_fields = [
    ("Tipo", "1", 1),
    ("Auto de Infração", "", 25),
    ("Codigo do Municipio atual da Placa", "", 8),
    ("Placa", "", 7),
    ("Proprietário do veículo na data da infração", "", 60),
    ("Endereço do proprietário do Veículo", "", 60),
    ("Número da residência do proprietário do veículo", "", 10),
    ("Complemento sobre a residência do proprietário do veículo", "", 30),
    ("Bairro da residência do proprietário do veículo", "", 30),
    ("Codigo do Municipio da residência do proprietário do veículo", "", 8),
    ("CEP da residência do proprietário do veículo", "", 9),
    ("UF da residência do proprietário do veículo", "", 2),
    ("Proprietário Atual", "", 60),
    ("Endereço do proprietário atual", "", 60),
    ("Número da residência do proprietário atual", "", 10),
    ("Complemento sobre a residência do proprietário atual", "", 30),
    ("Bairro da residência do proprietário atual", "", 30),
    ("Codigo do Municipio da residência do proprietário atual", "", 8),
    ("CEP da residência do proprietário atual", "", 9),
    ("UF da residência do proprietário atual", "", 2),
    ("CPF ou CNPJ do proprietário atual", "", 15),
    ("Data da infração", "", 10),
    ("Vencimento da infração", "", 10),
    ("Hora da Infração", "", 5),
    ("Local da Infração", "", 100),
    ("Enquadramento da Infração", "", 10),
    ("Valor da Infração - R$", "", 15),
    ("Data da situação da infração", "", 10),
    ("Situação da infração", "", 2),
    ("Observação da Situação", "", 200),
    ("Nosso Número", "", 20),
    ("Agente Autuador", "", 17),
    ("Tipificação legal da Multa", "", 100),
    ("Data de Postagem", "", 10),
    ("Data do Pagamento", "", 10),
    ("Data de Crédito", "", 10),
    ("Valor Pago R$", "", 20),
    ("Banco arrecadador", "", 10),
    ("Agencia Arrecadadora", "", 10),
    ("Número de Processo de JARI", "", 20),
    ("Data de Cadastro do Processo de JARI", "", 10),
    ("Data de Julgamento do Processo de JARI", "", 10),
    ("Motivo Resultado", "", 200),
    ("Número do equipamento eletronico(infrações de radar,etc)", "", 50),
    ("Data de Inicio Cálculo dos Acréscimos", "", 10),
    ("Marcador de final de linha", "*", 1),
]

trailer_fields = [
    ("Tipo", "9", 1),
    ("Quantidade Total de Infrações", "1", 15),
    ("Valor Total das Infrações", "", 15),
    ("Espaços para uso futuro", "", 188),
    ("Marcador de final de linha", "*", 1),
]

st.title("Gerador de Arquivo de Multas de Trânsito (Layout Simulado)")

st.header("Header (Arquivo)")
header_vals = []
for nome, valor, tam in header_fields:
    if nome == "Filler" or nome == "Marcador de final de linha":
        header_vals.append(texto_esq(valor, tam))
    else:
        v = st.text_input(nome, value=valor, max_chars=tam, key=f"header_{nome}")
        if "Data" in nome:
            header_vals.append(texto_esq(data_br(v), tam))
        elif "Código" in nome or "Numero" in nome or "Quantidade" in nome:
            header_vals.append(num_dir(v, tam))
        else:  # Tipo e outros
            header_vals.append(texto_esq(v, tam))

st.header("Detalhe (Multa)")
detail_vals = []
for nome, valor, tam in detail_fields:
    v = st.text_input(nome, value=valor, max_chars=tam, key=f"detail_{nome}")
    if nome == "Marcador de final de linha":
        detail_vals.append(texto_esq(valor, tam))
    elif "Valor" in nome:
        detail_vals.append(moeda_br(v, tam))
    elif nome in [
        "Codigo do Municipio atual da Placa",
        "Codigo do Municipio da residência do proprietário do veículo",
        "CEP da residência do proprietário do veículo",
        "Codigo do Municipio da residência do proprietário atual",
        "CEP da residência do proprietário atual",
        "CPF ou CNPJ do proprietário atual",
        "Enquadramento da Infração",
        "Situação da infração",
        "Nosso Número",
        "Agente Autuador",
        "Número de Processo de JARI",
        "Número do equipamento eletronico(infrações de radar,etc)",
    ]:
        detail_vals.append(num_dir(v, tam))
    else:  # Textos, datas e outros
        detail_vals.append(texto_esq(v, tam))

st.header("Trailer (Resumo)")
trailer_vals = []
for nome, valor, tam in trailer_fields:
    if nome == "Marcador de final de linha" or nome == "Espaços para uso futuro":
        trailer_vals.append(texto_esq(valor, tam))
    else:
        v = st.text_input(nome, value=valor, max_chars=tam, key=f"trailer_{nome}")
        if "Valor" in nome:
            trailer_vals.append(moeda_br(v, tam))
        elif "Quantidade" in nome or "Código" in nome or "Numero" in nome:
            trailer_vals.append(num_dir(v, tam))
        else:  # Tipo
            trailer_vals.append(texto_esq(v, tam))

if st.button("Gerar arquivo TXT"):
    txt = (
        "".join(header_vals)
        + "\n"
        + "".join(detail_vals)
        + "\n"
        + "".join(trailer_vals)
        + "\n"
    )
    with open("multas_simulado.txt", "w", encoding="utf-8") as f:
        f.write(txt)
    st.success("Arquivo multas_simulado.txt gerado com sucesso!")
    st.code(txt)
