import streamlit as st
import sqlite3
import openai
import base64
from dotenv import load_dotenv
from openai import OpenAI
import os
import time

st.set_page_config(page_title="FURIA", layout="centered")

#customizacao do app streamlit
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

# carrega a chave da OpenAI
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# conecta ao banco de dados
conn = sqlite3.connect('know_your_fan.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS usuarios") #exclui a tabela usuarios toda vez que inicia (opcional,por ser apenas uma amostragem)
#criação das tabelas
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    idade INTEGER,
    cpf TEXT,
    sexo TEXT,
    adress TEXT,
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

#interface do streamlit
st.title("Formulário Fã FURIA 🇧🇷")
st.write("Preencha suas informações abaixo e ganhe **30% de desconto** nos produtos FURIA!")

with st.form(key="formulario_furia"): #pegando os inputs do usuário e botando nas respectivas variáveis
    nome = st.text_input("Digite seu nome completo")
    idade = st.number_input("Digite sua idade", min_value=0, max_value=120)
    cpf = st.text_input("Digite seu CPF")
    sexo = st.selectbox("Selecione seu sexo", ["Masculino", "Feminino", "Outro"])
    adress = st.text_input("Digite o estado e cidade onde você mora")
    interesses = st.text_area("Quais seus maiores interesses em e-sports? Ex: jogos, times, jogadores")
    eventos = st.text_area("Quais eventos relacionados à FURIA você participou? Ex: campeonatos de CSGO, Kings League, etc.")
    compras = st.text_area("Compras relacionadas a e-sports no último ano")
    redes_sociais = st.text_area("Links de redes sociais (Instagram, Twitter, etc.)")
    documento = st.file_uploader("Envie uma foto do seu documento (RG ou CPF)", type=["jpg", "jpeg", "png"])
    
    enviar = st.form_submit_button("Enviar informações")

if enviar: # se ele clicar em enviar
    documento_valido = False #inicializa a variável como False

    if documento is not None: #se o usuário enviar o documento
            
        bytes_data = documento.read()  # le o arquivo enviado 
        base64_image = base64.b64encode(bytes_data).decode('utf-8') # converte a imagem para base64
         

        client = OpenAI(api_key=openai.api_key)
        # verifica se o documetno é válido com chatgpt vision
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um verificador de documentos de identidade"},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"""
Analise esta imagem e extraia o Nome completo e o CPF. Compare esses valores extraídos com os seguintes informados pelo usuário:
Nome informado: {nome}
CPF informado: {cpf}

Responda apenas com:
- '1' se o documento é válido e os dados extraídos batem com os informados.
- '0' se o documento não é válido ou os dados extraídos não batem.

Não inclua mais nada na resposta além de '1' ou '0'.
"""},
                        {"type": "image_url",
                         "image_url": {
                             "url": f"data:{documento.type};base64,{base64_image}",
                         },
                        },
                    ],
                }
            ],
        )

        resposta_validacao = completion.choices[0].message.content #botei a resposta do chatgpt na variável resposta_validacao (ou é 1 ou 0)


        if "1" in resposta_validacao.lower(): # se a resposta for 1, o documento é válido
            documento_valido = True
        else:
            documento_valido = False

    # criei o prompt para a IA gerar o perfil do fã
    prompt_fan = f"""
    Baseado nas seguintes informações do usuário:
    Nome: {nome}
    Idade: {idade}
    Endereço: {adress}
    CPF: {cpf}
    Sexo: {sexo}
    Interesses: {interesses}
    Eventos: {eventos}
    Compras: {compras}
    Redes sociais: {redes_sociais}
    Crie um perfil detalhado sobre ele como fã de e-sports. Não inclua informações pessoais, como o CPF, apenas descreva o perfil do fã. O perfil deve incluir os seguintes tópicos:
    - Nome
    - Idade
    - Endereço
    - Sexo
    - Interesses
    - Eventos
    - Compras
    - Redes sociais
    """
    # gpt irá fazer um resumo com base nas informações do usuário
    # e gerar um perfil detalhado sobre ele como fã de e-sports
    # e também uma sessão específica de conteúdos e produtos que o usuário gostaria de consumir com base nos seus interesses e gostos.
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um analista profissional da área de marketing da FURIA (time de eSports) que utiliza da estratégia Know Your Fan para entender o público do time. Analise as informações do usuário e crie um perfil detalhado sobre ele como fã de e-sports. Crie uma sessão específica de conteúdos e produtos  que o usuário gostaria de consumir com base nos seus interesses e gostos. (com links de cada sugestão para o usuário consumir/comprar)"},
            {"role": "user", "content": prompt_fan}
        ]
    )

    resposta_gerada = response.choices[0].message.content

    if documento_valido: # se e somente se o documento foi valido, ou seja, ter retornado 1, todas as informações serão salvas no banco de dados e o perfil gerado

        print(nome, idade, cpf, sexo, adress, interesses, eventos, compras, redes_sociais, documento_valido)
            # Inserir usuário no banco de dados
        cursor.execute('''
        INSERT INTO usuarios (nome, idade, cpf, sexo, adress, interesses, eventos, compras, redes_sociais, documento_validado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome, idade, cpf, sexo, adress, interesses, eventos, compras, redes_sociais, documento_valido))
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
        st.warning("⚠️ Documento inválido ou informações incompletas. Verifique os dados e tente novamente.")