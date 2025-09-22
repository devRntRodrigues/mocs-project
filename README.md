# MOCS - Document Processing and RAG System

Sistema de processamento de documentos com capacidades de OCR, extração de texto e RAG (Retrieval-Augmented Generation) para análise inteligente de documentos.

## 🚀 Visão Geral

O MOCS é uma aplicação full-stack que permite o upload, processamento e análise inteligente de documentos PDF. O sistema utiliza OCR (Optical Character Recognition) para extrair texto de documentos, armazena os dados em um banco PostgreSQL com extensão pgvector para busca semântica, e oferece uma interface web moderna para interação com os documentos através de perguntas e respostas.

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

### DevOps

- **Docker**: Containerização da aplicação
- **Docker Compose**: Orquestração de múltiplos containers
- **UV**: Gerenciador de dependências Python moderno
- **Alembic**: Migrações de banco de dados

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

## 📁 Estrutura do Projeto

```
mocs-project/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── core/           # Configurações e utilitários
│   │   ├── documents/      # Módulo de documentos
│   │   ├── rag/           # Módulo RAG
│   │   └── routers.py     # Roteamento principal
│   ├── uploads/           # Diretório de uploads
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/               # Interface Next.js
│   ├── src/
│   │   ├── app/           # Páginas Next.js
│   │   ├── components/    # Componentes React
│   │   ├── lib/          # Utilitários
│   │   └── types/        # Tipos TypeScript
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml     # Orquestração de containers
└── README.md
```

## 🎯 Funcionalidades

### Upload e Processamento de Documentos

- Upload de arquivos PDF
- Extração de texto usando OCR (Tesseract)
- Armazenamento seguro de documentos
- Geração de embeddings para busca semântica

### Sistema RAG (Retrieval-Augmented Generation)

- Busca semântica em documentos
- Geração de respostas contextuais usando GPT-4o-mini
- Interface de perguntas e respostas
- Histórico de conversas

### Interface Web

- Upload drag-and-drop de documentos
- Visualização de documentos processados
- Chat interface para perguntas
- Listagem de documentos com paginação

## 🔒 Segurança

- Validação de tipos de arquivo
- Limite de tamanho de upload (10MB)
- Sanitização de entrada
- CORS configurado adequadamente
- Variáveis de ambiente para configurações sensíveis

## 📊 Decisões Técnicas

### Por que FastAPI?

- Performance superior comparado a outros frameworks Python
- Documentação automática com OpenAPI/Swagger
- Validação automática de dados com Pydantic
- Suporte nativo a async/await
- Type hints integrados

### Por que PostgreSQL + pgvector?

- Banco relacional robusto e confiável
- Extensão pgvector para busca vetorial eficiente
- Suporte a embeddings de alta dimensão
- ACID compliance para integridade dos dados

### Por que LangChain?

- Framework maduro para aplicações de IA
- Integração nativa com OpenAI
- Pipeline de RAG pré-construído
- Facilita manutenção e extensibilidade

### Por que Next.js?

- Framework React otimizado para produção
- Server-side rendering (SSR)
- Roteamento automático
- Otimizações de performance integradas
- Excelente experiência de desenvolvimento

### Por que Docker?

- Ambiente de desenvolvimento consistente
- Facilita deploy em diferentes ambientes
- Isolamento de dependências
- Orquestração simplificada com Docker Compose

## 🚀 Deploy

O projeto está configurado para deploy em qualquer ambiente que suporte Docker:

1. Configure as variáveis de ambiente de produção
2. Execute `docker-compose up -d` no servidor
3. Configure proxy reverso (nginx) se necessário
4. Configure SSL/TLS para produção

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para dúvidas ou suporte, entre em contato através dos issues do repositório.

---

**Desenvolvido com ❤️ usando FastAPI, Next.js e OpenAI**
