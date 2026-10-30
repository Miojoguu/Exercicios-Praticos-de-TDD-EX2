# Exercício 2 — validação de `Person` com TDD

Implementação em **Python 3.11+**, usando **pytest** e **pytest-cov**, do método
`PersonDAO.isValidToInclude(person)`. O método retorna uma lista com todos os
erros encontrados, na ordem das regras de validação.

## Repositório Git

Este diretório já é um repositório Git independente, com os ciclos vermelho e
verde registrados em commits separados. A URL remota será adicionada aqui assim
que a publicação externa for autorizada.

## Regras implementadas

- o nome deve ter pelo menos duas partes, todas compostas somente por letras;
- letras Unicode, como em `João Ávila`, são aceitas;
- a idade deve pertencer ao intervalo fechado `[1, 200]`;
- a pessoa deve possuir pelo menos um e-mail associado;
- cada e-mail deve ter partes não vazias no formato `local@dominio.sufixo`;
- sufixos com mais de uma parte, como `.com.br`, são aceitos, mas partes vazias
  como em `dominio..com` são rejeitadas.

## Estrutura

```text
EX2/
├── exercise2/
│   ├── __init__.py
│   ├── models.py
│   └── person_dao.py
├── tests/
│   └── test_person_dao.py
├── docs/
│   └── coverage.md
├── pyproject.toml
└── README.md
```

## Preparação do ambiente

Na raiz do projeto, crie um ambiente virtual e instale as dependências de
desenvolvimento.

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### Linux ou macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Build

```bash
python -m build
```

O comando cria os pacotes `wheel` e `sdist` em `dist/`.

## Execução dos testes

```bash
python -m pytest -q
```

Resultado verificado localmente:

```text
...................................                                      [100%]
35 passed in 0.25s
```

## Cobertura de código

Execute a suíte com cobertura de linhas e ramificações:

```bash
python -m pytest --cov=exercise2 --cov-branch \
  --cov-report=term-missing \
  --cov-report=markdown:docs/coverage.md \
  --cov-report=html:htmlcov \
  --cov-report=xml:coverage.xml -q
```

No PowerShell, o mesmo comando pode ser escrito em uma única linha. A
configuração em `pyproject.toml` exige **100%** de cobertura; portanto, qualquer
queda abaixo desse valor faz o comando terminar com erro.

Evidência obtida na execução final:

| Arquivo | Instruções | Não cobertas | Ramificações | Ramificações parciais | Cobertura |
|---|---:|---:|---:|---:|---:|
| `exercise2/__init__.py` | 3 | 0 | 0 | 0 | 100% |
| `exercise2/models.py` | 6 | 0 | 0 | 0 | 100% |
| `exercise2/person_dao.py` | 35 | 0 | 12 | 0 | 100% |
| **Total** | **44** | **0** | **12** | **0** | **100%** |

O relatório Markdown gerado está em
[`docs/coverage.md`](docs/coverage.md). O relatório HTML navegável é criado em
`htmlcov/index.html` e o relatório para integração contínua em `coverage.xml`.

## Evidência do processo TDD

O histórico Git separa explicitamente as etapas do ciclo:

1. **Vermelho** — commit `a2f84fc`: os testes foram escritos primeiro; a
   execução resultou em `34 failed`, pois os métodos lançavam
   `NotImplementedError`.
2. **Verde** — commit `65c6d0d`: implementação mínima das regras. Um teste
   revelou a necessidade de aceitar `.com.br`; após o ajuste, o resultado foi
   `35 passed` com 100% de cobertura de linhas e ramificações.
3. **Refatoração** — validações foram mantidas pequenas, mensagens foram
   centralizadas em constantes e o padrão de e-mail foi compilado uma única
   vez na classe.

## Exemplo de uso

```python
from exercise2 import Email, Person, PersonDAO

person = Person(
    id=1,
    name="Maria da Silva",
    age=35,
    emails=[Email(id=1, name="maria@example.com")],
)

errors = PersonDAO().isValidToInclude(person)
assert errors == []
```

