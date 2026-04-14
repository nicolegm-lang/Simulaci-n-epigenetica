import streamlit as st

st.set_page_config(page_title="Simulador Epigenético", layout="wide")

st.title("🧬 Simulador de Dinámica Epigenética")
st.markdown("Explora la relación entre el metabolismo, la maquinaria enzimática y los estados biológicos reales de la cromatina.")

# --- BARRA LATERAL: COFACTORES ---
st.sidebar.header(" Cofactores Metabólicos")
folato = st.sidebar.slider("Nivel de SAM / Folato (para DNMT)", 0, 100, 80)
acetil_coa = st.sidebar.slider("Nivel de Acetil-CoA (para HAT)", 0, 100, 80)
alfa_kg = st.sidebar.slider("Nivel de α-KG (para TET)", 0, 100, 80)

st.sidebar.info("Si el cofactor baja del 20%, la enzima correspondiente se inactiva.")

# --- INTERFAZ PRINCIPAL ---
col1, col2 = st.columns([1, 1])

with col1:
    st.header(" Maquinaria Molecular")
    
    st.subheader("ADN")
    dnmt_check = st.checkbox("Activar DNMT (Metilación)")
    tet_check = st.checkbox("Activar TET (Desmetilación)")
    
    st.subheader("Acetilación de Histonas")
    hat_check = st.checkbox("Activar HAT (Acetilación)")
    hdac_check = st.checkbox("Activar HDAC (Desacetilación)")
    
    st.subheader("Metilación de Histonas")
    h3k4_check = st.checkbox("Escribir H3K4me3 (Marca Activa)")
    h3k27_check = st.checkbox("Escribir H3K27me3 (Marca Represiva)")

# --- LÓGICA BIOLÓGICA (EL MOTOR) ---

# 1. Validar enzimas con sus cofactores
dnmt_activa = dnmt_check and (folato >= 20)
tet_activa = tet_check and (alfa_kg >= 20)
hat_activa = hat_check and (acetil_coa >= 20)
hdac_activa = hdac_check  # No depende de cofactores en este modelo

# 2. Variables iniciales
estado_gen = "ESTADO BASAL"
expresion_final = 50
diagnostico = "Esperando actividad enzimática..."
color_alerta = "info"

# 3. Reglas de Diagnóstico (Prioridad de Estados)
# PRIORIDAD 1: Estado Bivalente (Marcas opuestas de histonas)
if h3k4_check and h3k27_check:
    estado_gen = "ESTADO BIVALENTE (Poised)"
    expresion_final = 15
    color_alerta = "warning"
    diagnostico = "🧠 Marcas antagónicas (H3K4me3 y H3K27me3) coexisten. Típico de promotores en células madre: el gen está en pausa, listo para activarse o silenciarse de forma definitiva."

# PRIORIDAD 2: Turnover Dinámico / Equilibrio (Conflicto de maquinaria)
elif (dnmt_activa and tet_activa) or (hat_activa and hdac_activa):
    estado_gen = "EQUILIBRIO DINÁMICO (Estado Intermedio)"
    expresion_final = 50
    color_alerta = "warning"
    
    if hat_activa and hdac_activa:
        diagnostico = "⚖️ Equilibrio dinámico: La acción simultánea de HAT (abre) y HDAC (cierra) mantiene un recambio constante de grupos acetilo, resultando en un estado intermedio de la cromatina."
    else:
        diagnostico = "⚖️ Turnover de metilación: Ciclo constante de metilación/desmetilación (DNMT/TET) que mantiene al promotor en un estado plástico."
        
# PRIORIDAD 3: Silenciado Puro
elif (dnmt_activa or hdac_activa or h3k27_check) and not (tet_activa or hat_activa or h3k4_check):
    estado_gen = "SILENCIADO PURO (Heterocromatina)"
    expresion_final = 5
    color_alerta = "error"
    diagnostico = "🔒 Las señales represivas dominan por completo sin oposición. La cromatina está fuertemente compactada (Gen OFF)."

# PRIORIDAD 4: Activado Puro
elif (tet_activa or hat_activa or h3k4_check) and not (dnmt_activa or hdac_activa or h3k27_check):
    estado_gen = "ACTIVADO PURO (Eucromatina)"
    expresion_final = 95
    color_alerta = "success"
    diagnostico = "🟢 Las señales activadoras dominan. El promotor está completamente libre y el ADN relajado (Gen ON)."

# --- RENDERIZADO DE RESULTADOS ---
with col2:
    st.header("📊 Diagnóstico del Sistema")
    
    # Alertas si faltan cofactores
    if dnmt_check and not dnmt_activa:
        st.warning("⚠️ DNMT seleccionada, pero falta SAM/Folato para funcionar.")
    if tet_check and not tet_activa:
        st.warning("⚠️ TET seleccionada, pero falta α-KG para funcionar.")
    if hat_check and not hat_activa:
        st.warning("⚠️ HAT seleccionada, pero falta Acetil-CoA para funcionar.")

    # Barra de progreso
    st.progress(expresion_final / 100)
    
    # Mensaje de estado principal
    if color_alerta == "success":
        st.success(f"**{estado_gen}** - Expresión: {expresion_final}%")
    elif color_alerta == "error":
        st.error(f"**{estado_gen}** - Expresión: {expresion_final}%")
    elif color_alerta == "warning":
        st.warning(f"**{estado_gen}** - Expresión: {expresion_final}%")
    else:
        st.info(f"**{estado_gen}** - Expresión: {expresion_final}%")

    st.write("### Interpretación Biológica:")
    st.write(diagnostico)
