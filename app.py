import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from streamlit_calendar import calendar

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="f(x) = Corujinha", page_icon="📐", layout="wide")

# --- CSS PARA O TEMA "PAPEL MILIMETRADO" ---
st.markdown("""
<style>
    /* 1. FUNDO PAPEL MILIMETRADO */
    .stApp {
        background-color: #ffffff;
        background-image: linear-gradient(#e5e7eb 1px, transparent 1px),
                          linear-gradient(90deg, #e5e7eb 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* 2. TIPOGRAFIA ESTILO LIVRO DE MATEMÁTICA */
    h1, h2, h3 {
        font-family: 'Times New Roman', Times, serif;
        color: #1e3a8a; /* Azul Escuro Acadêmico */
    }
    
    /* 3. CARTÕES COM BORDA TÉCNICA */
    .math-card {
        background-color: rgba(255, 255, 255, 0.95);
        border: 2px solid #1e3a8a;
        border-radius: 4px; /* Cantos menos arredondados, mais técnicos */
        padding: 20px;
        box-shadow: 5px 5px 0px rgba(30, 58, 138, 0.2); /* Sombra dura estilo desenho técnico */
        margin-bottom: 20px;
    }

    /* 4. BOTÕES GEOMÉTRICOS */
    div.stButton > button {
        background-color: #1e3a8a;
        color: white;
        border-radius: 2px;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        border: 1px solid #1e3a8a;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background-color: #ffffff;
        color: #1e3a8a;
        border: 1px solid #1e3a8a;
        transform: translate(2px, 2px); /* Efeito de clique mecânico */
    }

    /* 5. INPUTS */
    .stTextInput input, .stNumberInput input, .stDateInput input {
        border-bottom: 2px solid #1e3a8a !important;
        border-top: none; border-left: none; border-right: none;
        border-radius: 0px;
        background-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNÇÕES HTML AUXILIARES ---
def math_card_start(): st.markdown('<div class="math-card">', unsafe_allow_html=True)
def math_card_end(): st.markdown('</div>', unsafe_allow_html=True)

# --- BANCO DE DADOS ---
def get_connection(): return sqlite3.connect("sistema_math.db")
def init_db():
    conn = get_connection(); c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS alunos (id INTEGER PRIMARY KEY, nome TEXT, email TEXT, valor REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS aulas (id INTEGER PRIMARY KEY, aluno_nome TEXT, start_time TEXT, end_time TEXT, descricao TEXT)")
    conn.commit(); conn.close()
init_db()

# --- HEADER COM LATEX ---
c_logo, c_text = st.columns([1, 10])
with c_logo:
    st.image("logo.png", width=200) 
with c_text:
    st.markdown("# $f(x) = $ Gestão Prof. Corujinha")
    st.caption("$\sum$ (Organização + Aulas) = $\infty$ Sucesso")

st.markdown("---")

# --- VARIÁVEIS DO DASHBOARD (A "EQUAÇÃO" DO DIA) ---
conn = get_connection()
df_alunos = pd.read_sql("SELECT * FROM alunos", conn)
df_aulas = pd.read_sql("SELECT * FROM aulas", conn)
conn.close()

total_alunos = len(df_alunos)
total_aulas = len(df_aulas)
receita_est = df_alunos['valor'].sum() if not df_alunos.empty else 0

# --- DASHBOARD MATEMÁTICO ---
col1, col2, col3 = st.columns(3)
with col1:
    math_card_start()
    st.markdown("### $\mathcal{A}$ = Conjunto Alunos")
    st.markdown(f"# $n(\mathcal{{A}}) = {total_alunos}$")
    math_card_end()
with col2:
    math_card_start()
    st.markdown("### $\int$ Aulas Agendadas")
    st.markdown(f"# $x = {total_aulas}$")
    math_card_end()
with col3:
    math_card_start()
    st.markdown("### $\$$ Receita Prevista")
    st.markdown(f"# $\approx R\$ {receita_est:.2f}$")
    math_card_end()

# --- MENU PRINCIPAL (TABS) ---
tab_agenda, tab_calc, tab_db = st.tabs(["📅 Agenda ($t$)", "➕ Agendar ($x,y$)", "📋 Dados ($\Delta$)"])

# --- ABA 1: AGENDA (Calendário Técnico) ---
with tab_agenda:
    math_card_start()
    st.markdown("### Linha do Tempo $t$")
    
    events = []
    # Converte dados do banco para o calendário
    for i, row in df_aulas.iterrows():
        events.append({
            "title": f"{row['aluno_nome']}",
            "start": row['start_time'],
            "end": row['end_time'],
            "backgroundColor": "#1e3a8a",
            "borderColor": "#000000"
        })
        
    calendar_opts = {
        "headerToolbar": {"left": "prev,next today", "center": "title", "right": "timeGridWeek,dayGridMonth"},
        "initialView": "timeGridWeek",
        "slotMinTime": "07:00:00", "slotMaxTime": "22:00:00",
        "height": 600
    }
    
    calendar(events=events, options=calendar_opts)
    math_card_end()

# --- ABA 2: AGENDAR (Formulário) ---
with tab_calc:
    c_form, c_decor = st.columns([2, 1])
    
    with c_form:
        math_card_start()
        st.markdown("### Novo Ponto no Gráfico (Aula)")
        
        with st.form("form_math"):
            lista_nomes = df_alunos['nome'].tolist()
            
            if not lista_nomes:
                st.warning("O conjunto de alunos está vazio $\emptyset$. Cadastre alunos na aba Dados.")
                aluno = None
            else:
                aluno = st.selectbox("Selecione a Variável $a$ (Aluno)", lista_nomes)
            
            c1, c2 = st.columns(2)
            data = c1.date_input("Coordenada $x$ (Data)")
            hora = c2.time_input("Coordenada $y$ (Hora)")
            desc = st.text_input("Definição do Problema (Conteúdo da aula)")
            
            # Botão de cálculo
            if st.form_submit_button("Calcular Agendamento $\Rightarrow$"):
                if aluno:
                    start = f"{data}T{hora}"
                    end = (datetime.combine(data, hora) + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
                    
                    conn = get_connection()
                    conn.execute("INSERT INTO aulas (aluno_nome, start_time, end_time, descricao) VALUES (?, ?, ?, ?)",
                                 (aluno, start, end, desc))
                    conn.commit()
                    conn.close()
                    st.success("Q.E.D. (Aula agendada com sucesso!)")
                    st.rerun()
        math_card_end()
        
    with c_decor:
        st.latex(r'''
            \text{Seja } f(t) \text{ o aprendizado.} \\
            \lim_{t \to \infty} f(t) = \text{Sucesso}
        ''')
        st.info("O sistema enviará a notificação para o email cadastrado na base de dados.")

# --- ABA 3: DADOS DOS ALUNOS ---
with tab_db:
    col_input, col_table = st.columns([1, 2])
    
    with col_input:
        math_card_start()
        st.markdown("### Inserir Variável")
        nome_novo = st.text_input("Nome ($n$)")
        email_novo = st.text_input("Email ($e$)")
        valor_novo = st.number_input("Valor ($v$)", value=100.0)
        
        if st.button("Adicionar Elemento $\in$ Turma"):
            if nome_novo and email_novo:
                conn = get_connection()
                conn.execute("INSERT INTO alunos (nome, email, valor) VALUES (?, ?, ?)", (nome_novo, email_novo, valor_novo))
                conn.commit()
                conn.close()
                st.rerun()
        math_card_end()
        
    with col_table:
        math_card_start()
        st.markdown("### Matriz de Alunos")
        if not df_alunos.empty:
            st.dataframe(df_alunos, hide_index=True, use_container_width=True)
        else:
            st.write("Matriz Nula.")
        math_card_end()