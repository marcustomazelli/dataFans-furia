import streamlit as st
import sqlite3
import openai
import base64
from dotenv import load_dotenv
from openai import OpenAI
import os
import time

st.set_page_config(page_title="FURIA", layout="centered")

# Estilo customizado
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        background-color: #FFD700;
        color: black;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stTextInput>div>input, .stTextArea>div>textarea {
        background-color: #262730;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image("assets/furia.png", width=1000)

# Carregar a chave da OpenAI
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Conectar ao banco de dados
conn = sqlite3.connect('know_your_fan.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS usuarios")
# Criação das tabelas já atualizada
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    idade INTEGER,
    cpf TEXT,
    sexo TEXT
    endereco TEXT,
    interesses TEXT,
    eventos TEXT,
    compras TEXT,
    redes_sociais TEXT,
    documento_validado BOOLEAN
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS respostas_ia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    resposta_gerada TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
)
''')
conn.commit()

# Interface do Streamlit
st.title("Formulário Fã FURIA 🇧🇷")
st.write("Preencha suas informações abaixo e ganhe **30% de desconto** nos produtos FURIA!")

with st.form(key="formulario_furia"):
    nome = st.text_input("Digite seu nome")
    idade = st.number_input("Digite sua idade", min_value=0, max_value=120)
    cpf = st.text_input("Digite seu CPF")
    sexo = st.selectbox("Selecione seu sexo", ["Masculino", "Feminino", "Outro"])
    endereco = st.text_input("Digite seu endereço")
    interesses = st.text_area("Quais seus maiores interesses em e-sports? Ex: jogos, times, jogadores")
    eventos = st.text_area("Quais eventos relacionados à FURIA você participou? Ex: campeonatos de CSGO, Kings League, etc.")
    compras = st.text_area("Compras relacionadas a e-sports no último ano")
    redes_sociais = st.text_area("Links de redes sociais (Instagram, Twitter, etc.)")
    documento = st.file_uploader("Envie uma foto do seu documento (RG ou CPF)", type=["jpg", "jpeg", "png"])
    
    enviar = st.form_submit_button("Enviar informações")

if enviar:
    documento_valido = False

    if documento is not None:
            
        bytes_data = documento.read()
        base64_image = base64.b64encode(bytes_data).decode('utf-8')
         

        client = OpenAI(api_key=openai.api_key)

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um verificador de documentos de identidade"},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analise esta imagem e extraia Nome, CPF e Data de Nascimento. Responda apenas com '1' se o documento parece válido, caso não seja responda com '0'. Não quero que responda nada além de 1 ou 0."},
                        {"type": "image_url",
                         "image_url": {
                             "url": f"data:{documento.type};base64,{base64_image}",
                         },
                        },
                    ],
                }
            ],
        )

        resposta_validacao = completion.choices[0].message.content


        if "1" in resposta_validacao.lower():
            documento_valido = True
        else:
            documento_valido = False

    # Criar o prompt para a IA gerar o perfil do fã
    prompt_fan = f"""
    Baseado nas seguintes informações do usuário:
    Nome: {nome}
    Idade: {idade}
    Endereço: {endereco}
    CPF: {cpf}
    Sexo: {sexo}
    Interesses: {interesses}
    Eventos: {eventos}
    Compras: {compras}
    Redes sociais: {redes_sociais}
    Crie um perfil detalhado sobre ele como fã de e-sports. Não inclua informações pessoais, como o CPF, apenas descreva o perfil do fã, não inclua nenhuma informação a mais do que o usuário botou. O perfil deve incluir os seguintes tópicos:
    - Nome
    - Idade
    - Endereço
    - Sexo
    - Interesses
    - Eventos
    - Compras
    - Redes sociais
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um analista profissional da área de marketing da FURIA (time de eSports) que utiliza da estratégia Know Your Fan para entender o público do time."},
            {"role": "user", "content": prompt_fan}
        ]
    )

    resposta_gerada = response.choices[0].message.content

    if documento_valido:

        print(nome, idade, cpf, sexo, endereco, interesses, eventos, compras, redes_sociais, documento_valido)
            # Inserir usuário no banco de dados
        cursor.execute('''
        INSERT INTO usuarios (nome, idade, cpf, sexo, endereco, interesses, eventos, compras, redes_sociais, documento_validado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome, idade, cpf, sexo, endereco, interesses, eventos, compras, redes_sociais, documento_valido))
        conn.commit()

        usuario_id = cursor.lastrowid

            # Salvar resposta da IA
        cursor.execute('''
        INSERT INTO respostas_ia (usuario_id, resposta_gerada)
        VALUES (?, ?)
        ''', (usuario_id, resposta_gerada))
        conn.commit()

        st.success("🔄 Validando documento...")
        time.sleep(1)
        st.success("✅ Documento validado com sucesso!")
        st.balloons()
        st.success("Perfil gerado com sucesso! 🎉")
        st.markdown(f"### Perfil do Fã\n{resposta_gerada}")
        st.info("Parabéns! Você ganhou **30% de desconto** em produtos FURIA! 🛍️")
    else:
        st.warning("⚠️ Documento inválido ou incompleto.")
        st.success("Mande o documento correto para validar seu cadastro.")