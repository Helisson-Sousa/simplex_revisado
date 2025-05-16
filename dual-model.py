import LPdata as data

# Dados
c = data.c
A = data.A_original
b = data.b
restricoes_tipo = data.restricoes_tipo
sinais_variaveis = data.sinais_variaveis
tipo_objetivo = data.tipo_objetivo  # 'max' ou 'min'

# === MODELO PRIMAL ===
print(f"Primal: {'Maximizar' if tipo_objetivo == 'max' else 'Minimizar'} Z =", " + ".join(f"{c[i]}x{i+1}" for i in range(len(c))))

for i in range(A.shape[0]):
    expr = " + ".join(f"{A[i][j]}x{j+1}" for j in range(A.shape[1]))
    print(f"{expr} {restricoes_tipo[i]} {b[i]}")

print("\nCondicoes de Nao Negatividade:")
for j, sinal in enumerate(sinais_variaveis):
    if sinal == '>=':
        print(f"x{j+1} >= 0")
    elif sinal == '<=':
        print(f"x{j+1} <= 0")
    elif sinal == '=':
        print(f"x{j+1} livre")
    else:
        print(f"x{j+1} com sinal desconhecido: {sinal}")

# === MODELO DUAL ===
print("\nModelo Dual:")
print(f"{'Maximizar' if tipo_objetivo == 'min' else 'Minimizar'} W =", " + ".join(f"{b[i]}y{i+1}" for i in range(len(b))))
print("Sujeito a:")

# Geração das restrições do dual
for j in range(A.shape[1]):
    expr = " + ".join(f"{A[i][j]}y{i+1}" for i in range(A.shape[0]))

    # O sinal da desigualdade depende do tipo de variável primal
    sinal_dual = sinais_variaveis[j]
    if sinal_dual == '>=':
        simbolo = '>=' if tipo_objetivo == 'max' else '<='
    elif sinal_dual == '<=':
        simbolo = '<=' if tipo_objetivo == 'max' else '>='
    elif sinal_dual == '=':
        simbolo = '='
    else:
        raise ValueError(f"Sinal não reconhecido para x{j+1}: {sinal_dual}")

    print(f"{expr} {simbolo} {c[j]}")

# Domínio das variáveis dual: depende das restrições do primal
print("\nDominios das variaveis dual:")
for i, tipo in enumerate(restricoes_tipo):
    if tipo == "<=":
        if tipo_objetivo == "max":
            print(f"y{i+1} >= 0")
        else:  # minimização
            print(f"y{i+1} <= 0")
    elif tipo == ">=":
        if tipo_objetivo == "max":
            print(f"y{i+1} <= 0")
        else:
            print(f"y{i+1} >= 0")
    elif tipo == "=":
        print(f"y{i+1} livre")
    else:
        print(f"y{i+1} com restrição desconhecida: {tipo}")
