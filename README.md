# MOCS - Document Processing and RAG System

## 🏗️ Arquitetura

### Backend (FastAPI + Python)

- **Framework**: FastAPI com Python 3.13
- **Banco de Dados**: PostgreSQL com extensão pgvector para embeddings
- **OCR**: Tesseract OCR para extração de texto de PDFs
- **IA/ML**: OpenAI GPT-4o-mini para geração de respostas e text-embedding-3-small para embeddings
- **Processamento**: LangChain para pipeline de RAG
- **Autenticação**: Sistema de dependências com FastAPI

### Frontend (Next.js + React)

- **Framework**: Next.js 15 com React 19
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Upload**: React Dropzone para upload de arquivos
- **TypeScript**: Tipagem estática completa

### Infraestrutura

- **Containerização**: Docker + Docker Compose
- **Banco de Dados**: PostgreSQL com pgvector
- **Gerenciamento de Dependências**: UV (Python) e npm (Node.js)

## 🛠️ Tecnologias Utilizadas

### Backend

- **FastAPI**: Framework web moderno e rápido para APIs
- **SQLAlchemy**: ORM para interação com banco de dados
- **AsyncPG**: Driver assíncrono para PostgreSQL
- **Pydantic**: Validação de dados e configurações
- **LangChain**: Framework para aplicações de IA
- **OpenAI**: API para modelos de linguagem e embeddings
- **Tesseract OCR**: Extração de texto de imagens
- **Pillow**: Processamento de imagens
- **PDF2Image**: Conversão de PDF para imagens
- **pgvector**: Extensão PostgreSQL para busca vetorial

### Frontend

- **Next.js**: Framework React para produção
- **React 19**: Biblioteca para interfaces de usuário
- **TypeScript**: Superset do JavaScript com tipagem estática
- **Tailwind CSS**: Framework CSS utilitário
- **Axios**: Cliente HTTP
- **React Dropzone**: Componente para upload de arquivos

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Chave da API OpenAI

## 🚀 Como Executar

### 1. Clone o repositório

```bash
git clone <repository-url>
cd mocs-project
```

### 2. Configure as variáveis de ambiente

```bash
# Copie o arquivo de exemplo
cp backend/env.example backend/.env

# Edite o arquivo .env e adicione sua chave da OpenAI
# OPENAI__API_KEY=sua_chave_aqui
```

### 3. Execute com Docker Compose

```bash
# Execute todos os serviços
docker-compose up --build

# Ou execute em background
docker-compose up -d --build
```

### 4. Acesse a aplicação

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs

## 🔧 Desenvolvimento Local

### Backend

```bash
cd backend

# Instale as dependências
uv sync

# Execute o servidor de desenvolvimento
uv run uvicorn app.core.app:get_application --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend

# Instale as dependências
npm install

# Execute o servidor de desenvolvimento
npm run dev
```

## 🔒 Segurança

- Validação de tipos de arquivo
- Limite de tamanho de upload (10MB)
- Sanitização de entrada
- CORS configurado adequadamente
- Variáveis de ambiente para configurações sensíveis

## 📊 Decisões Técnicas

### Por que FastAPI?

Foi o framework para Python que mais utilizei e ele oferece facilidades que considero essenciais, como documentação automática com OpenAPI/Swagger e validação de dados integrada com Pydantic. Isso faz com que eu opte por ele na maioria dos projetos em Python, pela praticidade e agilidade no desenvolvimento.

### Por que PostgreSQL + pgvector?

É o banco de dados que mais utilizo e, por já contar com a extensão pgvector, facilita muito a configuração e o desenvolvimento para implementar buscas vetoriais eficientes e suporte direto a embeddings.

### Por que LangChain?

Já utilizei em outros projetos profissionais e gosto bastante do LangChain para desenvolver agents. Por estar familiarizado e por já ter integração pronta com a OpenAI (na qual eu tinha créditos 😅), além de oferecer um pipeline de RAG pré-construído, optei por ele.

### Por que Next.js?

É um dos padrões mais adotados na indústria moderna e pode ser configurado facilmente pelo CLI, que é bem completo.

---
