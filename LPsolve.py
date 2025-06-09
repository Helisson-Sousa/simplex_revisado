import numpy as np
import scipy.linalg as la
import LPdata as data
import sensibility as sens
import subprocess

np.seterr(divide='ignore', invalid='ignore')

# Tipo de problema: "min" ou "max"
tipo_problema = data.tipo_objetivo.lower()

# Dados do problema
c = data.c_ext
A = data.A
b = data.b

# Mostra os modelos (PRIMAL e DUAL) no início
print("MODELO PRIMAL E DUAL")
subprocess.run(["python", "dual-model.py"])

# Número de variáveis e restrições
n_var = len(c)
m = len(b)

# Índices iniciais da base (últimas m colunas — variáveis de folga)
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

    # Vetor solução total
    x = np.zeros(n_var)
    for i, bi in enumerate(base):
        x[bi] = x_B[i]

    # Multiplicadores simplex (pi)
    pi = c_B @ B_inv

    # Custos reduzidos
    custos_reduzidos = c_N - pi @ N

    # Vetor completo dos custos reduzidos
    custos_reduzidos_completos = np.zeros(n_var)
    for i, j in enumerate(nao_base):
        custos_reduzidos_completos[j] = custos_reduzidos[i]

    # Teste de otimalidade e escolha da variável que entra
    if tipo_problema == "min":
        cond_otimalidade = all(custos_reduzidos >= -1e-8)
        indice_entrada_local = np.argmin(custos_reduzidos)
    elif tipo_problema == "max":
        cond_otimalidade = all(custos_reduzidos <= 1e-8)
        indice_entrada_local = np.argmax(custos_reduzidos)
    else:
        raise ValueError("Tipo de problema deve ser 'min' ou 'max'.")

    if cond_otimalidade:
        break  # Sai do loop e imprime tudo organizado abaixo

    # Escolhe variável que entra
    indice_entrada = nao_base[indice_entrada_local]
    a_q = A[:, indice_entrada]

    # Direção simplex
    direcao = B_inv @ a_q

    # Verifica ilimitado
    if all(direcao <= 0):
        print("Problema ilimitado!")
        break

    # Calcula θ
    theta = np.divide(x_B, direcao, out=np.full_like(x_B, np.inf), where=direcao > 0)
    indice_saida_local = np.argmin(theta)
    indice_saida = base[indice_saida_local]

    # Atualiza base
    base[indice_saida_local] = indice_entrada
    nao_base = list(set(range(n_var)) - set(base))

# =============================
# Exibição Final
# =============================

print("\nSOLUÇÃO PRIMAL")
print("Solução Primal (x):", x)
print("Valor ótimo de Z (Primal):", c @ x)

print("\nSOLUÇÃO DUAL")
print("Solução Dual (y):", pi)
print("Valor ótimo de W (Dual):", b @ pi)

# Variáveis de folga
x_folga = x[n_var - m:]
nomes_folga = [f"x{i+1}" for i in range(n_var - m, n_var)]

print("\nVARIÁVEIS DE FOLGA")
for nome, valor in zip(nomes_folga, x_folga):
    print(f"{nome} = {round(valor, 2)}")

# Análise de sensibilidade
print("\nANÁLISE DE SENSIBILIDADE")
sens.analise_sensibilidade(c, A, b, base, nao_base, B_inv, pi)
