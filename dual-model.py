import LPdata as data

# Dados
c = data.c
A = data.A_original
b = data.b
restricoes_tipo = data.restricoes_tipo
sinais_variaveis = data.sinais_variaveis

# Modelo Primal
print("Primal: Maximizar Z =", " + ".join(f"{c[i]}x{i+1}" for i in range(len(c))))

print("\nRestricoes:")
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

# Modelo Dual
print("\nModelo Dual:")
print("Minimizar W =", " + ".join(f"{b[i]}y{i+1}" for i in range(len(b))))
print("Sujeito a:")

for j in range(A.shape[1]):
    expr = " + ".join(f"{A[i][j]}y{i+1}" for i in range(A.shape[0]))

    sinal_dual = sinais_variaveis[j]
    if sinal_dual == '>=':
        simbolo = '>='
    elif sinal_dual == '<=':
        simbolo = '<='
    elif sinal_dual == '=':
        simbolo = '='
    else:
        raise ValueError(f"Sinal não reconhecido para x{j+1}: {sinal_dual}")

    print(f"{expr} {simbolo} {c[j]}")

print("\nDominios das variaveis dual:")
for i, tipo in enumerate(restricoes_tipo):
    if tipo == "<=":
        print(f"y{i+1} >= 0")
    elif tipo == ">=":
        print(f"y{i+1} <= 0")
    elif tipo == "=":
        print(f"y{i+1} livre")
    else:
        print(f"y{i+1} com restrição desconhecida: {tipo}")
