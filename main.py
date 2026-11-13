import re

import streamlit as st

from rsa import desencriptar, encriptar


def leer_entero(texto, nombre):
    texto = texto.strip()
    if not re.fullmatch(r"[+-]?\d+", texto):
        raise ValueError(f"{nombre} debe ser un número entero")
    return int(texto)


def pedir_parametros(operacion):
    columna_p, columna_q, columna_e = st.columns(3)
    p = columna_p.text_input("Primo p", key=f"p_{operacion}")
    q = columna_q.text_input("Primo q", key=f"q_{operacion}")
    e = columna_e.text_input("Exponente e", key=f"e_{operacion}")
    return p, q, e


def mostrar_resumen(resultado):
    relleno = "Sí, un espacio" if resultado["relleno"] else "No"
    columna_n, columna_phi = st.columns(2)
    columna_n.write(f"**Módulo n** · {resultado['n']}")
    columna_phi.write(f"**φ** · {resultado['phi']}")
    st.write(f"**Longitud original (L)** · {resultado['longitud']}")
    st.write(f"**Relleno** · {relleno}")


def mostrar_bloques(bloques):
    filas = []
    for numero, bloque in enumerate(bloques, start=1):
        filas.append({
            "N.º": numero,
            "Caracteres": bloque["caracteres"].replace(" ", "␠"),
            "ASCII 1": bloque["ascii_1"],
            "ASCII 2": bloque["ascii_2"],
            "Bloque original (m)": bloque["bloque_original"],
            "Bloque cifrado (c)": bloque["bloque_cifrado"],
        })

    st.subheader("Detalle por bloque")
    st.caption("␠ representa un espacio.")
    st.dataframe(filas, hide_index=True)


def mostrar_encriptacion():
    with st.form("formulario_encriptar"):
        mensaje = st.text_area("Mensaje original (M)", key="entrada_mensaje")
        p, q, e = pedir_parametros("encriptar")
        enviado = st.form_submit_button("Encriptar")

    if enviado:
        try:
            st.session_state["resultado_encriptar"] = encriptar(
                mensaje, leer_entero(p, "p"), leer_entero(q, "q"), leer_entero(e, "e")
            )
        except ValueError as error:
            st.session_state.pop("resultado_encriptar", None)
            st.error(str(error))

    resultado = st.session_state.get("resultado_encriptar")
    if resultado is not None:
        st.subheader("Cifrado (C)")
        st.code(resultado["cifrado"], language="text", wrap_lines=True)
        mostrar_resumen(resultado)
        e_publico, n_publico = resultado["llave_publica"]
        st.write(f"**Llave pública (e, n)** · ({e_publico}, {n_publico})")
        mostrar_bloques(resultado["bloques"])


def mostrar_desencriptacion():
    with st.form("formulario_desencriptar"):
        cifrado = st.text_area(
            "Cifrado (C)",
            key="entrada_cifrado",
            help="Separa los bloques de seis dígitos con un solo espacio.",
        )
        longitud = st.text_input("Longitud original (L)", key="entrada_longitud")
        p, q, e = pedir_parametros("desencriptar")
        enviado = st.form_submit_button("Desencriptar")

    if enviado:
        try:
            st.session_state["resultado_desencriptar"] = desencriptar(
                cifrado,
                leer_entero(longitud, "L"),
                leer_entero(p, "p"),
                leer_entero(q, "q"),
                leer_entero(e, "e"),
            )
        except ValueError as error:
            st.session_state.pop("resultado_desencriptar", None)
            st.error(str(error))

    resultado = st.session_state.get("resultado_desencriptar")
    if resultado is not None:
        st.text_area(
            "Mensaje recuperado (M)",
            value=resultado["mensaje"],
            key="mensaje_recuperado",
            disabled=True,
        )
        mostrar_resumen(resultado)
        st.write(f"**Exponente privado d** · {resultado['d']}")
        mostrar_bloques(resultado["bloques"])


st.set_page_config(page_title="Criptografía RSA")
st.title("Criptografía RSA", anchor=False)

pestaña_encriptar, pestaña_desencriptar = st.tabs(["Encriptar", "Desencriptar"])
with pestaña_encriptar:
    mostrar_encriptacion()
with pestaña_desencriptar:
    mostrar_desencriptacion()
