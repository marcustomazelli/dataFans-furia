# 📄 Projeto: Know Your Fan - Fã FURIA

Este projeto é uma aplicação interativa em Python desenvolvida com **Streamlit**, que tem como objetivo **coletar, analisar e gerar perfis personalizados de fãs da FURIA** (time brasileiro de eSports) com o apoio de **Inteligência Artificial (OpenAI)** e **validação de documentos via imagem**.

---

## 🌐 Aplicação Online

Acesse a versão pública hospedada no Railway:

🔗 [https://web-production-ec804.up.railway.app/](https://web-production-ec804.up.railway.app/)

---

## 🚀 Funcionalidades

### 1. **Formulário interativo para fãs da FURIA**
- Nome
- Idade
- CPF
- Sexo
- Estado e cidade onde mora
- Interesses em e-sports
- Participação em eventos
- Compras de produtos de e-sports
- Links de redes sociais
- Upload de documento (RG/CPF)

### 2. **Validação do documento com IA (GPT-4o Vision)**
- A imagem é convertida para base64
- Enviada para a OpenAI via API
- A IA analisa e retorna "1" se o documento parecer válido, "0" caso contrário

### 3. **Análise do perfil do fã com IA (GPT-4o)**
- A IA gera um perfil detalhado do fã com base nas respostas do formulário
- Informa:
  - Nome, idade, sexo, localização
  - Interesses em jogos, jogadores e times
  - Eventos e compras
  - Sugestão de produtos e conteúdos que o fã gostaria de consumir

### 4. **Banco de dados com SQLite**
- Tabela `usuarios`: armazena todos os dados do formulário
- Tabela `respostas_ia`: armazena os perfis gerados pela IA

### 5. **Interface moderna com Streamlit**
- Visual temático com cores da FURIA
- Layout responsivo e animado (confetes, mensagens de sucesso)
- Estilo CSS customizado via Markdown

---

## 🧠 Tecnologias Utilizadas

| Tecnologia | Função |
|------------|--------|
| `Python` | Lógica e backend |
| `Streamlit` | Interface web interativa |
| `OpenAI API (GPT-4o Vision)` | Validação de documento (imagem) |
| `OpenAI API (GPT-4o-mini)` | Geração do perfil do fã |
| `SQLite3` | Armazenamento local de dados |
| `dotenv` | Gerenciamento de variáveis de ambiente |
| `base64` | Conversão de imagens para texto (para a API) |

---

## 📁 Estrutura do Projeto (recomendada)

```
project/
├── assets/
│   └── furia.png
├── .streamlit/
│   └── config.toml
├── .env
├── .gitignore
├── main.py
├── requirements.txt
├── Procfile
```

---

## 📦 Instalação local (modo dev)

1. Clone o repositório:
```bash
git clone https://github.com/marcustomazelli/dataFans-furia.git
cd dataFans-furia
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # no Windows use venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Adicione sua chave OpenAI no arquivo `.env`:
```
OPENAI_API_KEY=sk-...
```

5. Rode o projeto:
```bash
streamlit run main.py
```

---

## 📌 Observações importantes

- Este é um protótipo: os dados do banco SQLite não são persistidos no Railway (voláteis).
- Toda vez que o app reinicia, o banco é recriado do zero.
- O uso da API da OpenAI pode consumir créditos pagos.
- O projeto está focado em simular uma experiência de "Conheça seu Fã" para uso de IA em marketing e engajamento de torcedores.

---

## ✍️ Autor

**Marcus Tomazelli**  
Estudante de Engenharia da Computação, desenvolvedor iniciante e fã da FURIA.  
Conecte-se: [marcustomazelli](https://www.linkedin.com/in/marcus-tomazelli/)

---

## 🏴 Inspirado por

- A estratégia "Know Your Fan" usada em clubes e organizações esportivas
- O potencial de IA para personalizar experiências de torcedores

