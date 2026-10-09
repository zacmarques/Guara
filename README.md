# 🐺 GUARA
## Gestão Unificada de Autoria e Registro Acadêmico

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103.0-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![License: CC BY-NC](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

</div>

Uma ferramenta em Python para automatizar a gestão de publicações acadêmicas, integrando **ORCID** e **Currículo Lattes** de forma rápida e simples.

---

### 🚀 Link Principal
<div style="background-color: #f0f0f0; border: 1px solid #ccc; padding: 15px; border-radius: 8px; text-align: center; display: inline-block; width: fit-content; margin: 10px;">
    <a href="https://github.com/zacmarques/Guara" target="_blank" style="text-decoration: none; color: #000; font-weight: bold; font-size: 16px;">
        📦 Acessar Repositório no GitHub
    </a>
</div>

---

## 🎯 Objetivo
O **GUARA** visa eliminar o processo manual, burocrático e cansativo de registrar publicações acadêmicas. A ferramenta permite que pesquisadores sincronizem suas publicações entre **ORCID** e **Lattes** automaticamente, economizando tempo para o que realmente importa: pesquisar e descansar.

---

## ✨ Funcionalidades

- 📝 **Registro de Entradas Acadêmicas**: Gerenciamento completo de publicações acadêmicas.
- 🔄 **Integração ORCID**: Exportação automática de publicações para a plataforma ORCID.
- 📚 **Importação Lattes**: Sincronização de dados para o Currículo Lattes.
- 🚀 **Automação de Tarefas Repetitivas**: Python automatiza o trabalho manual para manter o processo prático e rápido.
- 🔐 **Autenticação e Sessão**: Sistema de usuário, login e senha. Cada pesquisador inicia uma sessão que persiste os dados durante o preenchimento. Se o navegador fechar ou ocorrer uma interrupção, os dados da sessão são mantidos — sem necessidade de reiniciar tudo.

---

## 🛠️ Tecnologias

- **Python** 🐍
- **FastAPI** (Framework Web) ⚡
- **ORCID API** 🔗
- **Currículo Lattes** 📄

---

## 🚀 Como Começar

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/zacmarques/Guara.git
   ```

2. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure seu .env** com as credenciais do ORCID e Lattes.

4. **Execute a aplicação:**

   ```bash
   uvicorn src.main:app --reload
   ```

---

## 📁 Estrutura do Projeto

```text
Guara/
├── src/             # Código-fonte
├── tests/           # Testes
├── .specify/        # Configurações de especificação
├── pyproject.toml   # Configuração do projeto
├── requirements.txt # Dependências
└── central_producoes_historicas.xlsx # Dados históricos
```

---

## 🤝 Contribuindo

Este projeto é open source e feito para a comunidade acadêmica. Contribuições são bem-vindas! Se você tem uma ideia ou correção, não hesite em abrir uma issue ou pull request.

---

## 📄 Licença

Este projeto está licenciado sob a **CC BY-NC 4.0 (Attribution-NonCommercial 4.0 International)**.

> **Regras de Uso:**
> - Qualquer um pode utilizar em uso pessoal, para fins de pesquisa e/ou estudos.
> - Fica vedada qualquer tentativa de privatização ou comercialização do código do Guara.
> - O Guara é uma feature do público acadêmico e deve se manter público.

---

<div align="center">
  <p>Desenvolvido por <strong>Isaac Marques de Souza Garcia </strong> </p>
</div>