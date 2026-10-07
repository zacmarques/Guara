# Especificação de Integração ORCID

## Visão Geral
A integração com a API ORCID requer configuração de um endpoint OAuth 2.0 com redirect URI em localhost, que será convertido para HTTPS para uso em produção.

## Configuração de Redirect URI

### Desenvolvimento Local
- **Redirect URI**: `http://localhost:8000/auth/orcid/callback`
- **Porta padrão**: 8000 (pode ser alterada conforme configuração do servidor)
- **Protocolo**: HTTP (apenas em desenvolvimento)

### Ambiente de Produção
- **Redirect URI**: `https://guara.example.com/auth/orcid/callback`
- **Protocolo**: HTTPS (obrigatório para produção)
- **Domínio**: Domínio configurado para o sistema GUARA

## Configuração de Segurança

### OAuth 2.0 Flow
1. Iniciar autenticação com ORCID
2. Redirecionamento para URI configurado
3. Obter código de autorização
4. Trocar código por token de acesso
5. Usar token para acessar dados ORCID

### Validação de URI
- URI deve ser registrada no perfil da aplicação ORCID
- Deve ser uma URL válida e acessível
- Em produção, o protocolo HTTPS é obrigatório

## Implementação Técnica

### Endpoints Necessários
- `/auth/orcid/login` - Iniciar fluxo OAuth
- `/auth/orcid/callback` - Receber resposta OAuth
- `/auth/orcid/logout` - Encerrar sessão

### Configuração de Ambiente
```bash
ORCID_CLIENT_ID=seu_client_id_aqui
ORCID_CLIENT_SECRET=sua_client_secret_aqui
ORCID_REDIRECT_URI=http://localhost:8000/auth/orcid/callback
```

### Exemplo de Configuração em Produção
```bash
ORCID_CLIENT_ID=seu_client_id_aqui
ORCID_CLIENT_SECRET=sua_client_secret_aqui
ORCID_REDIRECT_URI=https://guara.example.com/auth/orcid/callback
```

## Considerações de Segurança

### Proteção contra CSRF
- Implementar tokens de estado (state)
- Validar tokens no callback

### Gerenciamento de Tokens
- Armazenar tokens de acesso e refresh
- Implementar mecanismo de refresh automático
- Proteger tokens em sessão segura

## Próximos Passos
1. Registrar aplicação no ORCID Developer Portal
2. Configurar redirect URI em produção
3. Implementar endpoints OAuth 2.0
4. Testar fluxo completo de autenticação
5. Validar acesso a dados ORCID
```