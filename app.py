import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from googletrans import Translator

# ---------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------
st.set_page_config(
    page_title="🎤 Analizador Urbano by Anuel",
    page_icon="🎧",
    layout="wide"
)

# Fondo negro con detalles rojos (estilo Anuel)
st.markdown(
    """
    <style>
    body {
        background-color: #000000;
        color: #FFFFFF;
    }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #000000 70%, #1a0000);
        color: white;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a0000, #000000);
        color: white;
    }
    [data-testid="stMarkdownContainer"] h1, h2, h3, h4 {
        color: #ff0000;
    }
    .stButton>button {
        background-color: #ff0000;
        color: white;
        border-radius: 12px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #b30000;
        color: #fff;
    }
    .stProgress > div > div > div > div {
        background-color: #ff0000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# TÍTULO Y DESCRIPCIÓN
# ---------------------------
st.title("🎶 Analizador de Letras by Anuel")
st.markdown("""
Este proyecto analiza letras o frases inspiradas en la **música urbana y el trap latino**.  
Convierte tus versos en datos con **vibras de Real hasta la Muerte 💀**:

- 🎧 *Análisis de sentimiento y subjetividad de tus barras*
- 🔥 *Palabras más potentes y repetidas*
- 🌍 *Traducción al inglés automática*
""")

# ---------------------------
# BARRA LATERAL
# ---------------------------
st.sidebar.title("🎤 Opciones del Estudio")
modo = st.sidebar.selectbox(
    "Selecciona cómo vas a soltar tus barras:",
    ["Escribir letra", "Subir archivo"]
)

# ---------------------------
# FUNCIONES DE PROCESO
# ---------------------------
def contar_palabras(texto):
    stop_words = set([
        "a", "al", "como", "con", "de", "del", "el", "ella", "en", "es", "la", "las",
        "los", "lo", "mi", "no", "por", "que", "se", "sin", "su", "te", "tu", "un", "una",
        "y", "yo", "the", "to", "of", "and", "a", "in", "for", "on", "with", "my", "me"
    ])
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]
    contador = {}
    for palabra in palabras_filtradas:
        contador[palabra] = contador.get(palabra, 0) + 1
    contador_ordenado = dict(sorted(contador.items(), key=lambda x: x[1], reverse=True))
    return contador_ordenado, palabras_filtradas

translator = Translator()

def traducir_texto(texto):
    try:
        return translator.translate(texto, src='es', dest='en').text
    except:
        return texto

def procesar_texto(texto):
    texto_ingles = traducir_texto(texto)
    blob = TextBlob(texto_ingles)
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    frases = [frase.strip() for frase in re.split(r'[.!?]+', texto) if frase.strip()]
    contador_palabras, palabras = contar_palabras(texto_ingles)
    return {
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "frases": frases,
        "contador_palabras": contador_palabras,
        "texto_original": texto,
        "texto_traducido": texto_ingles
    }

# ---------------------------
# VISUALIZACIONES
# ---------------------------
def crear_visualizaciones(resultados):
    st.subheader("📊 Vibras del Análisis")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Energía del sentimiento:**")
        sentimiento_norm = (resultados["sentimiento"] + 1) / 2
        st.progress(sentimiento_norm)
        if resultados["sentimiento"] > 0.05:
            st.success(f"🔥 Positividad alta ({resultados['sentimiento']:.2f}) – Vibra de éxito 💰")
        elif resultados["sentimiento"] < -0.05:
            st.error(f"💀 Tono oscuro ({resultados['sentimiento']:.2f}) – Trap puro y sin miedo")
        else:
            st.info(f"😐 Neutro ({resultados['sentimiento']:.2f}) – Verso tranquilo pero firme")

        st.write("**Nivel de subjetividad:**")
        st.progress(resultados["subjetividad"])
        if resultados["subjetividad"] > 0.5:
            st.warning("🎭 Alta subjetividad – Letras personales y con sentimiento")
        else:
            st.info("🧊 Baja subjetividad – Letras más objetivas y narrativas")

    with col2:
        st.write("**Palabras más repetidas (Top 10):**")
        if resultados["contador_palabras"]:
            st.bar_chart(dict(list(resultados["contador_palabras"].items())[:10]))

    st.subheader("🌍 Traducción al Inglés")
    with st.expander("Ver letra original y traducción"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Letra original (Español):**")
            st.text(resultados["texto_original"])
        with col2:
            st.markdown("**Traducción (Inglés):**")
            st.text(resultados["texto_traducido"])

    st.subheader("💬 Frases analizadas")
    for i, frase in enumerate(resultados["frases"][:10], 1):
        blob = TextBlob(traducir_texto(frase))
        sent = blob.sentiment.polarity
        emoji = "🔥" if sent > 0.05 else ("💀" if sent < -0.05 else "😐")
        st.write(f"{i}. {emoji} *{frase}* (Sentimiento: {sent:.2f})")

# ---------------------------
# MODO DE USO
# ---------------------------
if modo == "Escribir letra":
    st.subheader("✍️ Escribe una letra o frase de Anuel o tuya")
    texto = st.text_area("", height=200, placeholder="Ejemplo: 'Sola, pero con mil cadenas de oro brillando en el cuello...'")

    if st.button("Analizar letra 🎶"):
        if texto.strip():
            with st.spinner("Analizando tus barras, espera un momento..."):
                resultados = procesar_texto(texto)
                crear_visualizaciones(resultados)
        else:
            st.warning("Por favor escribe algo para analizar.")

elif modo == "Subir archivo":
    st.subheader("📂 Sube un archivo con tu letra o texto")
    archivo = st.file_uploader("", type=["txt", "csv", "md"])
    if archivo is not None:
        contenido = archivo.getvalue().decode("utf-8")
        with st.expander("Ver contenido del archivo"):
            st.text(contenido[:1000] + ("..." if len(contenido) > 1000 else ""))
        if st.button("Analizar archivo 🎧"):
            with st.spinner("Analizando el contenido..."):
                resultados = procesar_texto(contenido)
                crear_visualizaciones(resultados)

# ---------------------------
# PIE DE PÁGINA
# ---------------------------
st.markdown("---")
st.markdown("<p style='text-align: center; color: #ff0000;'>💀 Real Hasta la Muerte - App by Anuel Style 💀</p>", unsafe_allow_html=True)
