# UFSC: Introdução à Compiladores - INE5622

# code-compiler
### Lexic and Syntax compiler using Python PLY.

---

# Make commands to help you
## To execute all make commands, you should be in the root of the repository!
## See all available options with `make help`

---

## Docker options:
### Requires Docker and Docker Compose to be installed on your system. You can get in the official Docker documentation: [docs.docker.com/get-docker](https://docs.docker.com/get-docker)

#### Install lexical environment with Docker for using the program:

1. Run: `make run-lexical-docker FILE=<path_to_file>`

   Replace `<path_to_file>` with the path of the file to be analyzed.

### Install syntax environment with Docker for using the program:

1. Run: `make run-syntax-docker FILE=<path_to_file>`

   Replace `<path_to_file>` with the path of the file to be analyzed.

---

## Local options:
### Use for development, debugging, or running locally.

### Install development environment:

1. Run: `make create-venv`

### Run lexical

1. Run: `make run-lexical FILE=<path_to_file>`

   Replace `<path_to_file>` with the path of the file to be analyzed.

### Run syntax 

1. Run: `make run-syntax FILE=<path_to_file>`

   Replace `<path_to_file>` with the path of the file to be analyzed.

### Compile requirements:

1. Run: `make compile-requirements`

### Sync requirements:

1. Run: `make sync-requirements`

### Check tests and linters:

1. Run: `make tox`

### Auto-format with linters:

1. Run: `make lint`
