# Plano de Desenvolvimento do MVP QuotasBNB

## Configuração Inicial
- [x] Instalar dependências necessárias (Django, django-allauth, Pillow, mysqlclient)
- [ ] Configurar banco de dados MySQL no settings.py
- [ ] Criar estrutura básica do projeto

## Autenticação e Usuários
- [ ] Implementar modelo de usuário com campos para anunciante/cliente
- [ ] Configurar sistema de autenticação padrão (email/senha)
- [ ] Implementar login social (Google, Facebook, Instagram)
- [ ] Criar templates para login, cadastro e recuperação de senha

## Modelos e Banco de Dados
- [ ] Criar modelo de imóveis (properties)
- [ ] Criar modelo de fotos de imóveis (property_photos)
- [ ] Criar modelo de períodos disponíveis (property_periods)
- [ ] Criar modelo de reservas (reservations)
- [ ] Implementar migrations e seeds

## Funcionalidades de Imóveis
- [ ] Implementar cadastro de imóveis
- [ ] Implementar upload seguro de imagens
- [ ] Implementar definição de períodos disponíveis
- [ ] Implementar listagem e pesquisa de imóveis
- [ ] Implementar visualização detalhada de imóveis

## Sistema de Reservas
- [ ] Implementar reserva de períodos
- [ ] Implementar bloqueio de períodos após reserva
- [ ] Implementar confirmação de reserva

## Painéis de Usuário
- [ ] Criar painel para anunciantes (gerenciar imóveis e reservas)
- [ ] Criar painel para clientes (visualizar reservas)
- [ ] Implementar notificações por email

## Administração
- [ ] Configurar painel de administração
- [ ] Implementar gerenciamento de usuários
- [ ] Implementar gerenciamento de imóveis
- [ ] Implementar gerenciamento de reservas

## Finalização
- [ ] Validar todas as funcionalidades
- [ ] Preparar para deploy
- [ ] Criar README com instruções de instalação e uso
