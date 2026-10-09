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
- 🔐 **Autenticação e Sessão**: Sistema de usuário, login e senha. Cada pesquisador inicia uma sessão que persiste os dados durante o preenchimento no banco de dados local (`guara.db`). Se o navegador fechar ou ocorrer uma interrupção, os dados da sessão são mantidos — sem necessidade de reiniciar tudo.

---

## 🛠️ Tecnologias

- **Python** 🐍
- **FastAPI** (Framework Web) ⚡
- **SQLite** (Banco de dados local) 🗄️
- **ORCID API** 🔗
- **Currículo Lattes** 📄

---
## 📁 Estrutura do Projeto

```Guara/
├── src/                               # Código-fonte
├── tests/                             # Testes automatizados
├── .specify/                          # Configurações de especificação
├── .gitignore                         # Regras de arquivos não versionados (como guara.db e .env)
├── pyproject.toml                     # Configuração do projeto
├── requirements.txt                   # Dependências Python
└── central_producoes_historicas.xlsx  # Dados salvos legado
```

## 🚀 Como Começar

1. **Clone o repositório:**

   ```text
   bash
   git clone [https://github.com/zacmarques/Guara.git](https://github.com/zacmarques/Guara.git)
	```

2. **Acesse a pasta e instale dependências**
	```text
 	bash
	cd Guara
	pip install -r requirements.txt
	```

3. **Configure as Variáveis de Ambiente:**
Crie um arquivo .env na raiz do projeto com as credenciais do ORCID e Lattes (não versione este arquivo).

4. **Banco de Dados Local (guara.db):**
Nota: Ao executar a aplicação, o arquivo guara.db será criado/atualizado automaticamente. Ele já consta no .gitignore para não ser enviado ao GitHub, mantendo seus dados de sessão e autenticação seguros.

5. **Executando a aplicação**
	```text
 	bash
	uvicorn src.main:app --reload
	```

## 🤝 Contribuindo

Este projeto é open source e feito para a comunidade acadêmica.
Contribuições são bem-vindas! Se você tem uma ideia ou correção, não hesite em abrir uma issue ou pull request.
Usei "https://dribbble.com/shots/27214788-Keyvo-Websit" como referência de design minimalista para o frontend e deixo aqui a devida citação do autor.

> [!IMPORTANT]
> Sou um profissional da área de História, não um programador formado. Use o aplicativo sabendo que podem ocorrer erros e problemas, e a utilização é por sua conta e risco.

## 📄 Licença
Este projeto está licenciado sob a CC BY-NC 4.0 (Attribution-NonCommercial 4.0 International).

> [!IMPORTANT]
> Regras de Uso:
> Qualquer um pode utilizar em uso pessoal, para fins de pesquisa e/ou estudos.
> Fica vedada qualquer tentativa de privatização ou comercialização do código do Guara.
> O Guara é uma feature do público acadêmico e deve se manter público.
