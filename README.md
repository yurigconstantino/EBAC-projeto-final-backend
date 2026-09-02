# Interknot API

Projeto final do curso de Desenvolvedor Full Stack com Python da Ebac, um sistema Backend de uma rede social, desenvolvido com Django e cdREST Framework. A API permite criar contas, autenticar usuários, publicar textos e imagens, seguir outros usuários, curtir posts e comentar.

## Tecnologias

- Python 3.13+
- Django 6
- Django REST Framework
- JWT com `djangorestframework-simplejwt`
- SQLite no ambiente local

## Requisitos

- Python 3.13 ou superior
- `pip` ou Poetry

## Instalação

Clone o projeto e entre na pasta do backend:

```bash
git clone <url-do-repositorio>
cd interknot
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Git Bash:

```bash
source .venv/Script/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Ou, usando Poetry:

```bash
poetry install
poetry shell
```

## Configuração e execução

Execute as migrações para criar as tabelas para o bando de dados:

```bash
python manage.py migrate
```

O comando abaixo limpa os dados existentes e cria 20 usuários, posts, curtidas e comentários fictícios:

```bash
python manage.py seed
```

Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

A API ficará disponível em `http://127.0.0.1:8000/`.

Para criar um usuário administrador:

```bash
python manage.py createsuperuser
```

O painel administrativo está em `http://127.0.0.1:8000/admin/`.

## Dados de teste

Os usuários criados pelo seed usam a senha `123456`.

## Endpoints

Todas as rotas abaixo usam o prefixo `http://127.0.0.1:8000`.

### Contas

| Método | Rota                              | Descrição                                |
| ------ | --------------------------------- | ---------------------------------------- |
| `POST` | `/api/accounts/register/`         | Cria uma conta                           |
| `POST` | `/api/accounts/login/`            | Autentica e retorna tokens JWT           |
| `GET`  | `/api/accounts/me/`               | Retorna o usuário autenticado            |
| `PUT`  | `/api/accounts/me/update/`        | Atualiza perfil, e-mail, senha ou avatar |
| `POST` | `/api/accounts/follow/<user_id>/` | Segue ou deixa de seguir um usuário      |
| `GET`  | `/api/accounts/follow/<user_id>/` | Consulta o status de seguimento          |
| `GET`  | `/api/accounts/following/`        | Lista os usuários seguidos               |

Exemplo de cadastro:

```http
POST /api/accounts/register/
Content-Type: application/json

{
    "username": "Usuario",
    "email": "usuario@email.com",
    "password": "UmaSenhaForte123"
}
```

### Posts

| Método          | Rota                        | Descrição                                                   |
| --------------- | --------------------------- | ----------------------------------------------------------- |
| `GET`           | `/api/posts/`               | Lista o feed do usuário, com posts próprios e de quem segue |
| `POST`          | `/api/posts/`               | Cria um post                                                |
| `GET`           | `/api/posts/<id>/`          | Consulta um post                                            |
| `PUT` / `PATCH` | `/api/posts/<id>/`          | Atualiza um post                                            |
| `DELETE`        | `/api/posts/<id>/`          | Exclui um post                                              |
| `POST`          | `/api/posts/<id>/like/`     | Alterna a curtida do usuário                                |
| `POST`          | `/api/posts/<id>/comment/`  | Adiciona um comentário                                      |
| `GET`           | `/api/posts/<id>/comments/` | Lista os comentários do post                                |
| `GET`           | `/api/posts/explore/`       | Lista posts de outros usuários                              |
| `GET`           | `/api/posts/my_posts/`      | Lista os posts do usuário autenticado                       |

Posts podem ser enviados como JSON ou `multipart/form-data` quando houver imagem:

São aceitos arquivos JPG, JPEG, PNG, GIF e WEBP, com limite de 15 MB. As imagens ficam disponíveis sob `/media/` durante o desenvolvimento.

