import numpy as np
import re

def parse_expression(expr):
    expr = expr.replace('-', '+-')
    terms = expr.split('+')
    coeffs = [0] * 100
    for term in terms:
        if not term.strip():
            continue
        match = re.match(r'([-\d\.]*)x(\d+)', term.strip())
        if match:
            coef_str, var_idx = match.groups()
            coef = float(coef_str) if coef_str not in ('', '+', '-') else float(coef_str + '1')
            coeffs[int(var_idx)-1] = coef
    while coeffs and coeffs[-1] == 0:
        coeffs.pop()
    return coeffs

def parse_modelo_txt(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    obj_line = next(line for line in lines if line.lower().startswith('maximizar'))
    c = parse_expression(obj_line.split('=')[1])

    restr_start = lines.index('Restricoes:') + 1
    restr_end = lines.index('Condicoes de Nao Negatividade:')
    restr_lines = lines[restr_start:restr_end]

    A_base = []
    b = []
    sinais = []

    for restr in restr_lines:
        if '<=' in restr:
            lhs, rhs = restr.split('<=')
            sinais.append('<=')
        elif '>=' in restr:
            lhs, rhs = restr.split('>=')
            sinais.append('>=')
        elif '=' in restr:
            lhs, rhs = restr.split('=')
            sinais.append('=')
        else:
            raise ValueError(f"Restrição mal formatada: {restr}")
        A_base.append(parse_expression(lhs))
        b.append(float(rhs.strip()))

    cond_lines = lines[restr_end + 1:]
    sinais_variaveis = []
    for cond in cond_lines:
        if '>=' in cond:
            sinais_variaveis.append('>=')
        elif '<=' in cond:
            sinais_variaveis.append('<=')
        elif 'livre' in cond.lower():
            sinais_variaveis.append('=')
        else:
            raise ValueError(f"Condição de variável mal formatada: {cond}")

    max_len = max(len(row) for row in A_base)
    A_base = [row + [0]*(max_len - len(row)) for row in A_base]
    c = c + [0]*(max_len - len(c))

    A_ext = []
    c_ext = list(c)
    artificial_vars = []

    for i, sinal in enumerate(sinais):
        row = list(A_base[i])

        slack = []
        artificial = []

        if sinal == '<=':
            slack = [0] * len(A_ext) + [1]  # nova folga
            c_ext.append(0)
        elif sinal == '>=':
            slack = [0] * len(A_ext) + [-1]  # novo excesso
            artificial = [0] * len(A_ext) + [1]
            c_ext.extend([0, 1e5])
            artificial_vars.append(len(c_ext) - 1)
        elif sinal == '=':
            artificial = [0] * len(A_ext) + [1]
            c_ext.append(1e5)
            artificial_vars.append(len(c_ext) - 1)

        row += slack + artificial
        A_ext = [r + [0]*(len(row)-len(r)) for r in A_ext]  # padding para manter colunas alinhadas
        A_ext.append(row)

    A = np.array(A_ext, dtype=float)
    b = np.array(b, dtype=float)
    c_ext = np.array(c_ext, dtype=float)
    c = np.array(c, dtype=float)
    A_original = np.array(A_base, dtype=float)
    restricoes_tipo = sinais

    return A, A_original, restricoes_tipo, b, c, c_ext, artificial_vars, sinais_variaveis

# === Tornando as variáveis globais, como LPsolve espera ===
A, A_original, restricoes_tipo, b, c, c_ext, artificiais, sinais_variaveis = parse_modelo_txt("modelo.txt")