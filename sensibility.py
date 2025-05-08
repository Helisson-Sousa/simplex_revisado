import numpy as np

def analise_sensibilidade(c, A, b, base, nao_base, B_inv, pi):
    n_var = len(c)
    m = len(b)
    nomes_vars = [f"X{i+1}" for i in range(n_var)]

    print("\n\n🔎 ANÁLISE DE SENSIBILIDADE")
    print("\nRANGES IN WHICH THE BASIS IS UNCHANGED:\n")

    # --- COEFICIENTES DA FUNÇÃO OBJETIVO ---
    print("OBJ COEFFICIENT RANGES")
    print(f"{'VARIABLE':<8} {'CURRENT':>10} {'ALLOWABLE':>15} {'ALLOWABLE':>15}")
    print(f"{'':<8} {'COEF':>10} {'INCREASE':>15} {'DECREASE':>15}")

    for i in range(n_var):
        nome = nomes_vars[i]
        coef_original = -c[i]

        if i in base:
            print(f"{nome:<8} {coef_original:>10.6f} {'N/A':>15} {'N/A':>15}")
        else:
            j = nao_base.index(i)
            red_cost = -(c[i] - pi @ A[:, i])
            if red_cost > 0:
                dec = red_cost
                inc = float('inf')
            elif red_cost < 0:
                inc = -red_cost
                dec = float('inf')
            else:
                inc = dec = float('inf')
            print(f"{nome:<8} {coef_original:>10.6f} {inc:>15.6f} {dec:>15.6f}")

    # --- INTERVALOS DO LADO DIREITO (RHS) ---
    print("\nRIGHTHAND SIDE RANGES")
    print(f"{'ROW':<5} {'CURRENT':>10} {'ALLOWABLE':>15} {'ALLOWABLE':>15}")
    print(f"{'':<5} {'RHS':>10} {'INCREASE':>15} {'DECREASE':>15}")

    x_B = B_inv @ b
    for i in range(m):
        row = i + 1
        rhs_i = b[i]
        limites = []
        for j in range(m):
            if B_inv[i, j] > 0:
                limites.append((x_B[j] / B_inv[i, j], 'decrease'))  # corrigido: ERA 'up'
            elif B_inv[i, j] < 0:
                limites.append((-x_B[j] / B_inv[i, j], 'increase'))  # corrigido: ERA 'down'

        inc = min([lim[0] for lim in limites if lim[1] == 'increase'], default=float('inf'))
        dec = min([lim[0] for lim in limites if lim[1] == 'decrease'], default=float('inf'))
        print(f"{row:<5} {rhs_i:>10.6f} {inc:>15.6f} {dec:>15.6f}")
