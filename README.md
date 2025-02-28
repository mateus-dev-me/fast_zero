# 🚀 TaskManager FastAPI
[![Python Version](https://img.shields.io/badge/Python-3.13%2B-blue)](https://www.python.org/downloads/release)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.8%2B-green)](https://docs.djangoproject.com/en/stable/releases/)

TaskManager é uma API RESTful desenvolvida com **FastAPI** para gerenciar usuários e tarefas. A API fornece autenticação baseada em token e operações CRUD para usuários e tarefas. Você pode executá-la localmente ou dentro de contêineres Docker.

## 📖 Documentação da API

A documentação interativa da API está disponível no Swagger UI:

- **[TaskManager API Docs (Swagger UI)](https://task-manager-fastapi.fly.dev/docs)**

## 📌 Tecnologias Utilizadas

- **Python 3.13+**
- **FastAPI** (Framework principal)
- **Uvicorn** (Servidor ASGI)
- **SQLAlchemy 2.0** (ORM)
- **PostgreSQL**
- **Pydantic** (Validação e tipagem)
- **JWT (JSON Web Token)** (Autenticação)
- **Pytest** (TDD)
- **Alembic** (Migrações de banco de dados)
- **Docker & Docker Compose** (Containerização)
- **Github Actions** (Integração Contínua)
- **Fly.io** (Hospedagem)

---

## Endpoints da API

### 🔐 Autenticação

| Método | Rota                          | Descrição                  |
|-------:|:------------------------------|:---------------------------|
| `POST` | `/api/v1/auth/token`          | Obter token de acesso      |
| `POST` | `/api/v1/auth/refresh_token`  | Renovar token de acesso    |

### 👤 Usuários

| Método   | Rota                      | Descrição            |
|---------:|:--------------------------|:---------------------|
| `POST`   | `/api/v1/users/`          | Criar usuário        |
| `GET`    | `/api/v1/users/`          | Listar usuários      |
| `GET`    | `/api/v1/users/{user_id}` | Obter detalhes       |
| `PUT`    | `/api/v1/users/{user_id}` | Atualizar usuário    |
| `DELETE` | `/api/v1/users/{user_id}` | Excluir usuário      |

### ✅ Tarefas

| Método   | Rota                       | Descrição            |
|---------:|:---------------------------|:---------------------|
| `POST`   | `/api/v1/tasks/`           | Criar tarefa         |
| `GET`    | `/api/v1/tasks/`           | Listar tarefas       |
| `PATCH`  | `/api/v1/tasks/{task_id}`  | Atualizar tarefa     |
| `DELETE` | `/api/v1/tasks/{task_id}`  | Excluir tarefa       |

---

# 📁 Descrição dos Diretórios

A estrutura do projeto está organizada para promover uma separação clara de responsabilidades, facilitando a manutenção, escalabilidade e testes. A seguir, uma breve descrição de cada diretório e seus arquivos:

## app/
- **main.py**  
  Ponto de entrada da aplicação. Inicializa a instância do FastAPI, registra os routers e configurações iniciais do servidor.

## app/core/
- **config.py**  
  Responsável por carregar as configurações globais da aplicação (ex.: variáveis de ambiente, URL do banco, chave secreta).
- **security.py**  
  Contém funções e classes relacionadas à segurança, como a implementação e verificação de tokens JWT.

## app/database/
- **models.py**  
  Define os modelos de dados utilizando um ORM (por exemplo, SQLAlchemy) para representar as tabelas do banco de dados.
- **session.py**  
  Gerencia a sessão de conexão com o banco de dados, facilitando a execução de queries e a gestão de transações.

## app/repositories/
- **task_repository.py**  
  Implementa a camada de acesso a dados para as tarefas, encapsulando operações CRUD.
- **user_repository.py**  
  Implementa a camada de acesso a dados para os usuários, abstraindo as operações de persistência.

## app/routers/
- **v1/**  
  Diretório destinado à versão 1 da API, permitindo o versionamento das rotas.
  - **endpoints/**  
    Contém os controladores que definem os endpoints da API.
    - **auth_controller.py**  
      Gerencia os endpoints de autenticação (login, renovação de token, etc.).
    - **task_controller.py**  
      Define os endpoints para o gerenciamento das tarefas (criação, listagem, atualização e exclusão).
    - **user_controller.py**  
      Define os endpoints para o gerenciamento dos usuários (criação, listagem, atualização e exclusão).

## app/schemas/
- **base.py**  
  Define esquemas básicos e modelos compartilhados entre diferentes partes da aplicação.
- **tasks.py**  
  Esquemas para a validação e serialização dos dados relacionados às tarefas.
- **token.py**  
  Esquemas para manipulação dos dados dos tokens JWT, facilitando a geração e validação.
- **users.py**  
  Esquemas para a validação e serialização dos dados dos usuários.

## app/services/
- **task_service.py**  
  Contém a lógica de negócio para operações relacionadas às tarefas, coordenando a interação entre repositórios e controladores.
- **user_service.py**  
  Contém a lógica de negócio para operações relacionadas aos usuários, encapsulando regras de validação e manipulação de dados.


---

## 📜 Licença
Este projeto está sob a licença **MIT**. Sinta-se à vontade para usá-lo, modificá-lo e contribuir!
