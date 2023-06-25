# UFSC: Introdução à Compiladores - INE5622

# code-compiler
### Lexic and Parser compiler using Python PLY.

---

# Make commands to help you
## To execute all make commands, you should be in the root of the repository!
## See all available options with `make help`

---

## Docker options:
### Requires Docker and Docker Compose to be installed on your system. You can get in the official Docker documentation: [docs.docker.com/get-docker](https://docs.docker.com/get-docker)

#### Install lexer environment with Docker for using the program:

1. Run: `make run-lexer-docker`

### Install parser environment with Docker for using the program:

1. Run: `make run-parser-docker`

---

## Local options:
### Use for development, debugging or running locally.

### Install development environment:

1. Run: `make create-venv`

### Run lexer

1. Run: `make run-lexer`

### Run parser 

1. Run: `make run-parser`

### Compile requirements:

1. Run: `make compile-requirements`

### Sync requirements:

1. Run: `make sync-requirements`

### Check tests and linters:

1. Run: `make tox`

### Auto-format with linters:

1. Run: `make lint`
