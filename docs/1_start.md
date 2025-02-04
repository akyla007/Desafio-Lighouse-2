# Instalação de Dependências

Este documento descreve como instalar as dependências do projeto a partir do arquivo `pyproject.toml`.

## Pré-requisitos

- Python 3.12 ou superior
- Pip (gerenciador de pacotes do Python)

## Passos para Instalação

### Windows e Linux

1. **Crie um ambiente virtual**:
   
   Navegue até o diretório onde o arquivo `pyproject.toml` está localizado e crie um ambiente virtual:
   ```sh
   - No Windows:
     ```sh
     python -m venv venv
     ```
   - No Linux:
     ```sh
     python -m venv venv
     ```
   ```

2. **Ative o ambiente virtual**:
   
   - No Windows:
     ```sh
     .\venv\Scripts\activate
     ```
   - No Linux:
     ```sh
     source venv/bin/activate
     ```

3. **Instale o Poetry**:
   
   Com o ambiente virtual ativado, instale o Poetry usando o pip:
   ```sh
   pip install poetry
   ```

4. **Instale as dependências**:
   
   Use o Poetry para instalar as dependências listadas no `pyproject.toml`:
   ```sh
   poetry install
   ```

## Verificação

Para verificar se as dependências foram instaladas corretamente, você pode listar os pacotes instalados:
```sh
poetry show
```

Se todos os pacotes listados no `pyproject.toml` aparecerem, a instalação foi bem-sucedida.

## Problemas Comuns

- **Poetry não encontrado**: Certifique-se de que o Poetry está no seu ambiente virtual. Você pode precisar reativar o ambiente virtual ou reinstalar o Poetry.
- **Versão do Python incompatível**: Verifique se você está usando uma versão do Python compatível com o projeto.

Para mais informações, consulte a [documentação oficial do Poetry](https://python-poetry.org/docs/).

## Execução dos Scripts e Teste do Projeto

Siga para o [2_project.md](2_project.md) para mais detalhes.