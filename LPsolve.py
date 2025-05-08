import numpy as np
import scipy.linalg as la
import LPdata as data

np.seterr(divide='ignore', invalid='ignore')

# Dados
c = -1 * data.c_ext  # Maximização vira minimização
A = data.A
b = data.b

# Número de variáveis
n_var = len(c)
m = len(b)

# Índices iniciais da base (últimas m colunas — as variáveis de folga)
base = list(range(n_var - m, n_var))
nao_base = list(set(range(n_var)) - set(base))

# LOOP PRINCIPAL DO SIMPLEX REVISADO
while True:
    # Matrizes básicas e não básicas
    B = A[:, base]
    N = A[:, nao_base]
    c_B = c[base]
    c_N = c[nao_base]

    # Inversa da base e solução básica
    B_inv = la.inv(B)
    x_B = B_inv @ b

    # Vetor solução total (x), começa zerado
    x = np.zeros(n_var)
    for i, bi in enumerate(base):
        x[bi] = x_B[i]

    # Multiplicadores simplex (pi) - Solução Dual
    pi = c_B @ B_inv

    # Custos reduzidos
    custos_reduzidos = c_N - pi @ N

    print("\n-----------------------------")
    print("Base atual:", [f"x{i+1}" for i in base])
    print("x_B:", x_B)

    n_dec = n_var - m
    # Vetor completo de custos reduzidos (0 para variáveis básicas)
    custos_reduzidos_completos = np.zeros(n_var)
    for i, j in enumerate(nao_base):
        custos_reduzidos_completos[j] = custos_reduzidos[i]

    # Mostrar apenas os custos reduzidos das variáveis de decisão (x1 até xn_dec)
    custos_decisao = np.round(custos_reduzidos_completos[:n_dec], 1)
    print("Custos reduzidos (variáveis de decisão):", custos_decisao)

    # Teste de otimalidade
    if all(custos_reduzidos >= 0):
        print("\n✅ Solução ótima encontrada!")

        # Solução primal (x)
        print("Solução Primal (x):", x)
        print("Valor ótimo de Z (Primal):", -1 * c @ x)  # Multiplica por -1 para voltar à maximização

        # Solução dual (pi ou y)
        print("\nSolução Dual (y):", abs(pi))
        print("Valor ótimo de W (Dual):", abs(b @ pi))  # Garantir que seja positivo (valor absoluto)

        # variáveis de folga
        x_folga = x[n_var - m:]
        nomes_folga = [f"x{i+1}" for i in range(n_var - m, n_var)]

        print("Variáveis de folga:")
        for nome, valor in zip(nomes_folga, x_folga):
            print(f"  {nome} = {round(valor, 2)}")

        break

    # Escolhe variável que entra (menor custo reduzido)
    indice_entrada_local = np.argmin(custos_reduzidos)
    indice_entrada = nao_base[indice_entrada_local]
    a_q = A[:, indice_entrada]

    # Direção simplex
    direcao = B_inv @ a_q

    # Verifica se o problema é ilimitado
    if all(direcao <= 0):
        print("Problema ilimitado!")
        break

    # Razões θ
    theta = np.divide(x_B, direcao, out=np.full_like(x_B, np.inf), where=direcao > 0)
    indice_saida_local = np.argmin(theta)
    indice_saida = base[indice_saida_local]

    print(f"\n➡️ Entra: x{indice_entrada + 1} | Sai: x{indice_saida + 1} | θ = {theta[indice_saida_local]}")

    # Atualiza base
    base[indice_saida_local] = indice_entrada
    nao_base = list(set(range(n_var)) - set(base))
