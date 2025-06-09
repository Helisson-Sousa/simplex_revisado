# 🧮 Simplex Revisado em Python

Este projeto tem como objetivo a implementação do **método Simplex Revisado** utilizando Python, com recursos adicionais para análise econômica e sensibilidade das soluções de Programação Linear. A atividade faz parte da primeira unidade da disciplina Otimização Linear, ministrada pelo professor Anand Subramanian.

## 📚 Funcionalidades

- Implementação do **Simplex Revisado**
- Geração e exibição do **modelo dual**
- Impressão da:
  - **Solução primal**
  - **Solução dual**
  - **Variação dos recursos** (ranges de sensibilidade)
- Identificação de:
  - Recursos **abundantes**
  - Recursos **escassos**
- Opção de **imprimir o log de execução** do algoritmo

## 🧠 Conceitos Envolvidos

- Programação Linear
- Simplex Revisado
- Análise de Sensibilidade (custos reduzidos e ranges de recursos)
- Interpretação econômica das soluções (identificação de escassez/abundância)
- Relação primal-dual

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- NumPy
- SciPy

## 💻 Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/seuusuario/simplex-revisado.git
cd simplex-revisado
```

2. Instale os pacotes necessários:

```bash
pip install -r requirements.txt
```

3. Execute um exemplo:

```bash
python LPsolve.py
```

## 📦 Requisitos

Conteúdo do arquivo `requirements.txt`:

```txt
numpy
scipy
```

## 📄 Licença

Este projeto está licenciado sob a licença MIT.