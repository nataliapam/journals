
import streamlit as st
import pandas as pd

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_excel("REVISTAS_LISTADO_DEPURADO_ORDENADO_LIMPIO.xlsx")
    df["Revista_normalizada"] = df["Revista"].str.lower().str.strip()
    return df

df = load_data()

st.title("Buscador de Revistas Académicas")
st.markdown("Consulta rápida de puntuaciones en AJG, CNRS, CNU, VHB y ABDC")

# Entrada del usuario
busqueda = st.text_area("Introduce uno o varios nombres de revista (una por línea):").strip()

if busqueda:
    # Convertir a lista y limpiar
    nombres = [nombre.lower().strip() for nombre in busqueda.split("\n") if nombre.strip()]
    
    # Buscar coincidencias parciales (contain)
    resultados = df[df["Revista_normalizada"].apply(lambda x: any(nombre in x for nombre in nombres))]
    
    if not resultados.empty:
        # Pivotar para ver por filas una revista y columnas los rankings por origen
        tabla = resultados.pivot_table(index="Revista", columns="Origen", values="Rating", aggfunc="first").reset_index()
        st.dataframe(tabla, use_container_width=True)

        # Descargar
        csv = tabla.to_csv(index=False).encode('utf-8')
        st.download_button("Descargar resultados como CSV", csv, "resultados_revistas.csv", "text/csv")
    else:
        st.warning("No se encontraron coincidencias.")
