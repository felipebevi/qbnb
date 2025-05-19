# QuotasBNB - Plataforma de Aluguel de Imóveis

QuotasBNB é uma plataforma de aluguel de imóveis entre pessoas, no estilo Airbnb, desenvolvida com Django e Bootstrap. Este MVP (Minimum Viable Product) permite que usuários se cadastrem como anunciantes e/ou clientes, cadastrem imóveis, definam períodos disponíveis, realizem buscas e façam reservas.

## Funcionalidades

- **Autenticação de Usuários**
  - Cadastro e login via e-mail/senha
  - Login social (Google, Facebook)
  - Perfil de usuário (anunciante e/ou cliente)

- **Cadastro de Imóveis**
  - Título, descrição, endereço, preço
  - Upload de até 10 fotos
  - Definição de até 3 períodos disponíveis

- **Listagem e Pesquisa**
  - Busca por localidade, datas, preço
  - Visualização de fotos, descrição, localização
  - Filtros de disponibilidade

- **Reservas**
  - Reserva de períodos disponíveis
  - Bloqueio automático de períodos reservados
  - Notificações por e-mail

- **Painel do Usuário**
  - Visualização de imóveis cadastrados (anunciante)
  - Status das reservas por período (anunciante)
  - Visualização de reservas realizadas (cliente)

- **Administração**
  - Gerenciamento de usuários, imóveis e reservas
  - Painel administrativo personalizado

## Requisitos

- Python 3.8+
- Django 4.2+
- MySQL 5.7+ (configurado para SQLite em desenvolvimento)
- Outras dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/felipebevi/qbnb.git
   cd qbnb
   ```

2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure o banco de dados em `quotasbnb/settings.py`:
   ```python
   # Para desenvolvimento (SQLite)
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }
   
   # Para produção (MySQL)
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'username',
           'USER': 'username',
           'PASSWORD': 'password!',
           'HOST': 'username',
           'PORT': '3306',
       }
   }
   ```

5. Execute as migrações:
   ```
   python manage.py migrate
   ```

6. Crie um superusuário:
   ```
   python manage.py createsuperuser
   ```

7. Inicie o servidor de desenvolvimento:
   ```
   python manage.py runserver
   ```

8. Acesse o sistema em `http://localhost:8000`

## Configuração do Login Social

Para configurar o login social, siga os passos abaixo:

### Google

1. Acesse o [Google Developer Console](https://console.developers.google.com/)
2. Crie um novo projeto
3. Configure as credenciais OAuth 2.0
4. Adicione as URLs de redirecionamento: `http://seu-dominio.com/accounts/google/login/callback/`
5. Obtenha o Client ID e Client Secret
6. Adicione as credenciais no painel admin do Django em `Sites` e `Social Applications`

### Facebook

1. Acesse o [Facebook Developer Portal](https://developers.facebook.com/)
2. Crie um novo aplicativo
3. Configure o produto "Login do Facebook"
4. Adicione as URLs de redirecionamento: `http://seu-dominio.com/accounts/facebook/login/callback/`
5. Obtenha o App ID e App Secret
6. Adicione as credenciais no painel admin do Django em `Sites` e `Social Applications`

## Deploy em Servidor Compartilhado

1. Faça upload dos arquivos para o servidor via FTP ou SSH
2. Configure o arquivo `settings.py` para produção:
   - Defina `DEBUG = False`
   - Atualize `ALLOWED_HOSTS`
   - Configure o banco de dados MySQL
   - Configure o envio de e-mails

3. Crie um arquivo `.htaccess` na raiz do projeto:
   ```
   <IfModule mod_wsgi.c>
       WSGIScriptAlias / /path/to/quotasbnb/quotasbnb/wsgi.py
       WSGIPythonPath /path/to/quotasbnb
       
       <Directory /path/to/quotasbnb/quotasbnb>
           <Files wsgi.py>
               Require all granted
           </Files>
       </Directory>
   </IfModule>
   
   <IfModule mod_rewrite.c>
       RewriteEngine On
       RewriteCond %{REQUEST_FILENAME} !-f
       RewriteRule ^(.*)$ /path/to/quotasbnb/quotasbnb/wsgi.py [QSA,L]
   </IfModule>
   ```

4. Execute as migrações no servidor:
   ```
   python manage.py migrate
   ```

5. Colete os arquivos estáticos:
   ```
   python manage.py collectstatic
   ```

6. Crie um superusuário:
   ```
   python manage.py createsuperuser
   ```

## Estrutura do Banco de Dados

O sistema utiliza os seguintes modelos:

- **User** (Django built-in)
  - Campos padrão do Django para autenticação

- **UserProfile**
  - Extensão do modelo User
  - Campos para perfil de anunciante/cliente

- **Property**
  - Informações do imóvel (título, descrição, endereço, preço)
  - Relacionamento com o proprietário (User)

- **PropertyPhoto**
  - Fotos do imóvel
  - Relacionamento com Property

- **PropertyPeriod**
  - Períodos disponíveis para aluguel
  - Campos de data início/fim e status de reserva

- **Reservation**
  - Reservas realizadas
  - Relacionamento com User (cliente) e PropertyPeriod

## Segurança

- Upload seguro de imagens com validação de tipo e tamanho
- Proteção contra CSRF em todos os formulários
- Autenticação e autorização em todas as views sensíveis
- Sanitização de dados de entrada

## Customização

- Para alterar o tema visual, edite os arquivos em `templates/`
- Para adicionar novas funcionalidades, crie novas apps ou estenda as existentes
- Para personalizar o painel admin, edite `quotasbnb/admin.py`

## Suporte

Para dúvidas ou problemas, entre em contato através de:
- E-mail: suporte@quotasbnb.com
- GitHub Issues: https://github.com/seu-usuario/quotasbnb/issues

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.
