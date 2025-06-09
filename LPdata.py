import numpy as np
import re

M = 1e5  # Valor grande para método Big-M

def parse_expression(expr):
    expr = expr.replace('-', '+-')  # Garante separação correta
    terms = expr.split('+')
    coeffs = [0] * 100  # Máximo de 100 variáveis

    for term in terms:
        term = term.strip()
        if not term:
            continue
        match = re.match(r'([-\d\.]*)\s*x\s*(\d+)', term.replace(' ', ''))
        if match:
            coef_str, var_idx = match.groups()
            coef = float(coef_str) if coef_str not in ('', '+', '-') else float(coef_str + '1')
            coeffs[int(var_idx)-1] = coef

    # Remove zeros à direita
    while coeffs and coeffs[-1] == 0:
        coeffs.pop()
    return coeffs

def parse_modelo_txt(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Identifica tipo de objetivo
    obj_line = next(line for line in lines if line.lower().startswith(('maximizar', 'minimizar')))
    tipo_objetivo = 'max' if 'maximizar' in obj_line.lower() else 'min'
    c = parse_expression(obj_line.split('=')[1])

    # Restrições
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

    # Condições de não negatividade
    cond_lines = lines[restr_end + 1:]
    sinais_variaveis = []
    for cond in cond_lines:
        cond = cond.lower()
        if '>=' in cond:
            sinais_variaveis.append('>=')  # padrão
        elif '<=' in cond:
            sinais_variaveis.append('<=')
        elif 'livre' in cond:
            sinais_variaveis.append('=')
        else:
            raise ValueError(f"Condição de variável mal formatada: {cond}")

    max_len = max(len(row) for row in A_base)
    A_base = [row + [0]*(max_len - len(row)) for row in A_base]
    c = c + [0]*(max_len - len(c))

    n_vars = max_len
    slack_artificial_count = 0
    A_ext = []
    c_ext = list(c)
    artificial_vars = []

    for i, sinal in enumerate(sinais):
        row = list(A_base[i])
        slack = []
        artificial = []

        if tipo_objetivo == 'max':
            if sinal == '<=':
                slack = [0]*slack_artificial_count + [1]
                c_ext.append(0)
                slack_artificial_count += 1
            elif sinal == '>=':
                slack = [0]*slack_artificial_count + [-1]
                artificial = [0]*(slack_artificial_count + 1) + [1]
                c_ext.extend([0, M])
                artificial_vars.append(len(c_ext) - 1)
                slack_artificial_count += 2
            elif sinal == '=':
                artificial = [0]*slack_artificial_count + [1]
                c_ext.append(M)
                artificial_vars.append(len(c_ext) - 1)
                slack_artificial_count += 1

        elif tipo_objetivo == 'min':
            if sinal == '>=':
                slack = [0]*slack_artificial_count + [1]
                c_ext.append(0)
                slack_artificial_count += 1
            elif sinal == '<=':
                slack = [0]*slack_artificial_count + [-1]
                artificial = [0]*(slack_artificial_count + 1) + [1]
                c_ext.extend([0, M])
                artificial_vars.append(len(c_ext) - 1)
                slack_artificial_count += 2
            elif sinal == '=':
                artificial = [0]*slack_artificial_count + [1]
                c_ext.append(M)
                artificial_vars.append(len(c_ext) - 1)
                slack_artificial_count += 1

        row += slack + artificial
        A_ext = [r + [0]*(len(row) - len(r)) for r in A_ext]
        A_ext.append(row)

    # Conversão final
    A = np.array(A_ext, dtype=float)
    b = np.array(b, dtype=float)
    c_ext = np.array(c_ext, dtype=float)
    c = np.array(c, dtype=float)
    A_original = np.array(A_base, dtype=float)
    restricoes_tipo = sinais

    return A, A_original, restricoes_tipo, b, c, c_ext, artificial_vars, sinais_variaveis, tipo_objetivo

# === Tornando as variáveis globais, como LPsolve espera ===
A, A_original, restricoes_tipo, b, c, c_ext, artificiais, sinais_variaveis, tipo_objetivo = parse_modelo_txt("modelo.txt")
