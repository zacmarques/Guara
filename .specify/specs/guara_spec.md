# GUARA - Gerenciador Unificado de Atualização de Registros Acadêmicos
## Especificação do Sistema (System Specification)

---

## 1. Visão Geral

### 1.1 Nome e Identidade
- **Nome do Sistema**: GUARA (Gerenciador Unificado de Atualização de Registros Acadêmicos)
- **Tipo**: Aplicação Web SaaS em nuvem
- **Linguagem**: Python 3.12+
- **Framework**: FastAPI

### 1.2 Propósito
O sistema GUARA é uma aplicação web que permite o registro, sincronização e gerenciamento automatizado de dados acadêmicos na API do ORCID (OAuth 2.0). O usuário pode puxar seus artigos via DOI ou criar entradas manualmente sem ter o DOI.

### 1.3 Características
- Acesso anônimo e autenticado
- Integração com API ORCID
- Interface CRUD para produção histórica
- Armazenamento em MySQL

---

## 2. Arquitetura do Sistema

### 2.1 Paradigma de Arquitetura
- Clean Architecture (Onion/Hexagonal)
- Domain-Driven Design (DDD)
- Microserviço cloud-ready com validação de limite zero-trust

### 2.2 Stack Técnico
- **Backend**: Python 3.12+, FastAPI, SQLAlchemy 2.0 (Async ORM), Pydantic v2
- **Database**: MySQL via asyncmy/aiomysql driver
- **Deploy**: Nuvem com segurança de acesso rigorosa

---

## 3. Domínio Central

### 3.1 Requisitos do Domínio
- **Ingestão de Metadados**: Dual-path intake:
  1. Busca automática via DOI Resolver API (Crossref / DataCite)
  2. Interface CRUD manual para entradas não-DOI ou sobrescritas de campos
- **Estruturação de Schema**: O schema do banco de dados e entidades deve refletir exatamente a estrutura definida em `central_producoes_historicas.xlsx`
- **Gerenciamento de Produções Históricas**: Armazenamento de dados históricos com histórico de mudanças

### 3.2 Entidades do Domínio
- Produção Acadêmica (Production)
- Metadata (Metadata)
- Usuário (User)
- Histórico de Alterações (Change History)

---

## 4. Funcionalidades Principais

### 4.1 Integração ORCID
- Autenticação OAuth2 com ORCID API
- Recuperação automática de metadados via DOI
- Sincronização bidirecional de dados

### 4.2 Interface CRUD Manual
- Criação de novas entradas
- Edição de campos existentes
- Exclusão de registros
- Busca e filtragem de produção

### 4.3 Armazenamento de Dados
- Persistência em MySQL
- Validade de dados com Pydantic
- Tratamento de transações assíncronas

---

## 5. Segurança e Conformidade

### 5.1 Segurança de Acesso
- Controle de acesso baseado em tokens JWT
- Validação de credenciais no nível de API
- Proteção contra vazamento de credenciais

### 5.2 Conformidade Regulatória
- Atendimento às regulamentações de proteção de dados (GDPR, LGPD)
- Controles adequados para proteção de informações sensíveis

---

## 6. Requisitos Técnicos

### 6.1 Configuração do Ambiente
- Variáveis de ambiente para configuração de banco e API
- Suporte a múltiplos provedores de serviços (AWS, GCP, Azure)

### 6.2 Monitoramento e Observabilidade
- Métricas de desempenho
- Logs estruturados
- Alertas críticos

---

## 7. Estrutura de Diretórios

```
guara/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── v1/
│   │   └── auth/
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── domain/
│   │   ├── models/
│   │   ├── repositories/
│   │   └── services/
│   └── utils/
├── migrations/
├── tests/
└── requirements.txt
```

---

## 8. Próximos Passos

- Desenvolvimento do esqueleto da aplicação
- Implementação das entidades do domínio
- Configuração de banco de dados e conexões
- Criação de testes unitários e de integração
- Implementação da interface CRUD e API ORCID
- Configuração de segurança e monitoramento