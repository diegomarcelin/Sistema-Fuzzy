import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt


# Variáveis de entrada
precipitacao = np.arange(0, 500, 1)
vazao = np.arange(0, 3000, 1)
salinidade_inicial = np.arange(0, 50, 1)

# Variável de saída
salinidade = np.arange(0, 50, 1)

# Definir as funções de pertinência


def trapmf(x, a, b, c, d):
    if a == b:
        # Quando a == b, retorno 1 se x >= a, caso contrário 0
        return np.maximum(0, np.minimum((d - x) / (d - c), 1))
    if c == d:
        return np.maximum(0, np.minimum((x - a) / (b - a), 1))
    return np.maximum(0, np.minimum((x-a)/(b-a), np.minimum(1, (d-x)/(d-c))))


def trimf(x, a, b, c):
    if a == b or b == c:
        # Quando a == b, retorno 1 se x >= a, caso contrário 0
        return (x >= a).astype(float)
    return np.maximum(0, np.minimum((x-a)/(b-a), (c-x)/(c-b)))


# Funções de pertinência para Precipitação Pluvial
precipitacao_B = trapmf(precipitacao, 0, 0, 80, 120)
precipitacao_M = trimf(precipitacao, 100, 145, 190)
precipitacao_MA = trimf(precipitacao, 176, 213.5, 252)
precipitacao_A = trimf(precipitacao, 225, 270, 315)
precipitacao_AL = trapmf(precipitacao, 290, 325, 500, 500)

# Funções de pertinência para Vazão
vazao_B = trapmf(vazao, 0, 0, 700, 900)
vazao_M = trimf(vazao, 700, 1050, 1400)
vazao_MA = trimf(vazao, 1250, 1525, 1800)
vazao_A = trimf(vazao, 1700, 1975, 2250)
vazao_AL = trapmf(vazao, 2200, 2500, 3000, 3000)

# Funções de pertinência para Salinidade Inicial
salinidade_inicial_BS = trapmf(salinidade_inicial, 0, 0, 4, 7.7)
salinidade_inicial_B = trimf(salinidade_inicial, 7, 12, 17)
salinidade_inicial_MB = trimf(salinidade_inicial, 13, 19.25, 25.5)
salinidade_inicial_M = trimf(salinidade_inicial, 23, 27.5, 32)
salinidade_inicial_A = trapmf(salinidade_inicial, 28, 33, 50, 50)

# Funções de pertinência para Salinidade
salinidade_BS = trapmf(salinidade, 0, 0, 4, 7.7)
salinidade_B = trimf(salinidade, 7, 12, 17)
salinidade_MB = trimf(salinidade, 13, 19.25, 25.5)
salinidade_M = trimf(salinidade, 23, 27.5, 32)
salinidade_A = trapmf(salinidade, 28, 33, 50, 50)

# Função para t-norma do mínimo


def tnorm(a, b):
    return np.minimum(a, b)


def inferencia_fuzzy(precip, sal_ini, vaz):
    lista_salinidade_BS = []
    lista_salinidade_B = []
    lista_salinidade_MB = []
    lista_salinidade_M = []
    maior_BS = 0
    maior_B = 0
    maior_MB = 0
    maior_M = 0
    media_dos_maximos = 0

    # ----------Calculo das pertinências----------
    # ---Precipitação(chuva)
    precip_B_val = fuzz.interp_membership(precipitacao, precipitacao_B, precip)
    precip_M_val = fuzz.interp_membership(
        precipitacao, precipitacao_M, precip)
    precip_MA_val = fuzz.interp_membership(
        precipitacao, precipitacao_MA, precip)
    precip_A_val = fuzz.interp_membership(
        precipitacao, precipitacao_A, precip)
    precip_AL_val = fuzz.interp_membership(
        precipitacao, precipitacao_AL, precip)

    # ---Salinidade inicial
    sal_ini_BS_val = fuzz.interp_membership(
        salinidade_inicial, salinidade_inicial_BS, sal_ini)
    sal_ini_B_val = fuzz.interp_membership(
        salinidade_inicial, salinidade_inicial_B, sal_ini)
    sal_ini_MB_val = fuzz.interp_membership(
        salinidade_inicial, salinidade_inicial_MB, sal_ini)
    sal_ini_M_val = fuzz.interp_membership(
        salinidade_inicial, salinidade_inicial_M, sal_ini)
    sal_ini_A_val = fuzz.interp_membership(
        salinidade_inicial, salinidade_inicial_A, sal_ini)

    # ---Vazão
    vaz_B_val = fuzz.interp_membership(vazao, vazao_B, vaz)
    vaz_M_val = fuzz.interp_membership(vazao, vazao_M, vaz)
    vaz_MA_val = fuzz.interp_membership(vazao, vazao_MA, vaz)
    vaz_A_val = fuzz.interp_membership(vazao, vazao_A, vaz)
    vaz_AL_val = fuzz.interp_membership(vazao, vazao_AL, vaz)

    # ------------------------BASE DE REGRAS--------------------
    # --- E aplicação da t-norma para as regras ativadas.
    if precip_B_val > 0 and sal_ini_MB_val > 0 and vaz_M_val > 0:
        regra1 = tnorm(tnorm(precip_B_val, sal_ini_MB_val), vaz_M_val)
        lista_salinidade_MB.append(regra1)
        print("Regra1 ativada - tnorma resultante:", regra1)
    if precip_B_val > 0 and sal_ini_M_val > 0 and vaz_MA_val > 0:
        regra2 = tnorm(tnorm(precip_B_val, sal_ini_M_val), vaz_MA_val)
        lista_salinidade_MB.append(regra2)
        print("Regra2 ativada - tnorma resultante:", regra2)
    if precip_B_val > 0 and sal_ini_MB_val > 0 and vaz_MA_val > 0:
        regra3 = tnorm(tnorm(precip_B_val, sal_ini_MB_val), vaz_MA_val)
        lista_salinidade_B.append(regra3)
        print("Regra3 ativada - tnorma resultante:", regra3)
    if precip_B_val > 0 and sal_ini_MB_val > 0 and vaz_A_val > 0:
        regra4 = tnorm(tnorm(precip_B_val, sal_ini_MB_val), vaz_A_val)
        lista_salinidade_B.append(regra4)
        print("Regra4 ativada - tnorma resultante:", regra4)
    if precip_B_val > 0 and sal_ini_B_val > 0 and vaz_A_val > 0:
        regra5 = tnorm(tnorm(precip_B_val, sal_ini_B_val), vaz_A_val)
        lista_salinidade_MB.append(regra5)
        print("Regra5 ativada - tnorma resultante:", regra5)
    if precip_B_val > 0 and sal_ini_M_val > 0 and vaz_AL_val > 0:
        regra6 = tnorm(tnorm(precip_B_val, sal_ini_M_val), vaz_AL_val)
        lista_salinidade_B.append(regra6)
        print("Regra6 ativada - tnorma resultante:", regra6)
    if precip_B_val > 0 and sal_ini_MB_val > 0 and vaz_A_val > 0:
        regra7 = tnorm(tnorm(precip_B_val, sal_ini_MB_val), vaz_A_val)
        lista_salinidade_MB.append(regra7)
        print("Regra7 ativada - tnorma resultante:", regra7)
    if precip_B_val > 0 and sal_ini_B_val > 0 and vaz_A_val > 0:
        regra8 = tnorm(tnorm(precip_B_val, sal_ini_B_val), vaz_A_val)
        lista_salinidade_MB.append(regra8)
        print("Regra8 ativada - tnorma resultante:", regra8)
    if precip_B_val > 0 and sal_ini_M_val > 0 and vaz_B_val > 0:
        regra9 = tnorm(tnorm(precip_B_val, sal_ini_M_val), vaz_B_val)
        lista_salinidade_M.append(regra9)
        print("Regra9 ativada - tnorma resultante:", regra9)
    if precip_B_val > 0 and sal_ini_M_val > 0 and vaz_M_val > 0:
        regra10 = tnorm(tnorm(precip_B_val, sal_ini_M_val), vaz_M_val)
        lista_salinidade_MB.append(regra10)
        print("Regra10 ativada - tnorma resultante:", regra10)
    if precip_B_val > 0 and sal_ini_B_val > 0 and vaz_B_val > 0:
        regra11 = tnorm(tnorm(precip_B_val, sal_ini_B_val), vaz_B_val)
        lista_salinidade_B.append(regra11)
        print("Regra11 ativada - tnorma resultante:", regra11)
    if precip_M_val > 0 and sal_ini_M_val > 0 and vaz_B_val > 0:
        regra12 = tnorm(tnorm(precip_M_val, sal_ini_M_val), vaz_B_val)
        lista_salinidade_MB.append(regra12)
        print("Regra12 ativada - tnorma resultante:", regra12)
    if precip_M_val > 0 and sal_ini_MB_val > 0 and vaz_B_val > 0:
        regra13 = tnorm(tnorm(precip_M_val, sal_ini_MB_val), vaz_B_val)
        lista_salinidade_MB.append(regra13)
        print("Regra13 ativada - tnorma resultante:", regra13)
    if precip_M_val > 0 and sal_ini_M_val > 0 and vaz_M_val > 0:
        regra14 = tnorm(tnorm(precip_M_val, sal_ini_M_val), vaz_M_val)
        lista_salinidade_MB.append(regra14)
        print("Regra14 ativada - tnorma resultante:", regra14)
    if precip_M_val > 0 and sal_ini_M_val > 0 and vaz_MA_val > 0:
        regra15 = tnorm(tnorm(precip_M_val, sal_ini_M_val), vaz_MA_val)
        lista_salinidade_MB.append(regra15)
        print("Regra15 ativada - tnorma resultante:", regra15)
    if precip_M_val > 0 and sal_ini_MB_val > 0 and vaz_M_val > 0:
        regra16 = tnorm(tnorm(precip_M_val, sal_ini_MB_val), vaz_M_val)
        lista_salinidade_B.append(regra16)
        print("Regra16 ativada - tnorma resultante:", regra16)
    if precip_M_val > 0 and sal_ini_A_val > 0 and vaz_B_val > 0:
        regra17 = tnorm(tnorm(precip_M_val, sal_ini_A_val), vaz_B_val)
        lista_salinidade_M.append(regra17)
        print("Regra17 ativada - tnorma resultante:", regra17)
    if precip_B_val > 0 and sal_ini_A_val > 0 and vaz_M_val > 0:
        regra18 = tnorm(tnorm(precip_B_val, sal_ini_A_val), vaz_M_val)
        lista_salinidade_MB.append(regra18)
        print("Regra18 ativada - tnorma resultante:", regra18)
    if precip_M_val > 0 and sal_ini_A_val > 0 and vaz_MA_val > 0:
        regra19 = tnorm(tnorm(precip_M_val, sal_ini_A_val), vaz_MA_val)
        lista_salinidade_B.append(regra19)
        print("Regra19 ativada - tnorma resultante:", regra19)
    if precip_M_val > 0 and sal_ini_B_val > 0 and vaz_M_val > 0:
        regra20 = tnorm(tnorm(precip_M_val, sal_ini_B_val), vaz_M_val)
        lista_salinidade_B.append(regra20)
        print("Regra20 ativada - tnorma resultante:", regra20)
    if precip_M_val > 0 and sal_ini_B_val > 0 and vaz_B_val > 0:
        regra21 = tnorm(tnorm(precip_M_val, sal_ini_B_val), vaz_B_val)
        lista_salinidade_B.append(regra21)
        print("Regra21 ativada - tnorma resultante:", regra21)
    if precip_MA_val > 0 and sal_ini_M_val > 0 and vaz_B_val > 0:
        regra22 = tnorm(tnorm(precip_MA_val, sal_ini_M_val), vaz_B_val)
        lista_salinidade_MB.append(regra22)
        print("Regra22 ativada - tnorma resultante:", regra22)
    if precip_MA_val > 0 and sal_ini_MB_val > 0 and vaz_B_val > 0:
        regra23 = tnorm(tnorm(precip_MA_val, sal_ini_MB_val), vaz_B_val)
        lista_salinidade_MB.append(regra23)
        print("Regra23 ativada - tnorma resultante:", regra23)
    if precip_A_val > 0 and sal_ini_M_val > 0 and vaz_B_val > 0:
        regra24 = tnorm(tnorm(precip_A_val, sal_ini_M_val), vaz_B_val)
        lista_salinidade_MB.append(regra24)
        print("Regra24 ativada - tnorma resultante:", regra24)
    if precip_A_val > 0 and sal_ini_MB_val > 0 and vaz_B_val > 0:
        regra25 = tnorm(tnorm(precip_A_val, sal_ini_M_val), vaz_B_val)
        lista_salinidade_B.append(regra25)
        print("Regra25 ativada - tnorma resultante:", regra25)
    if precip_AL_val > 0 and sal_ini_M_val > 0 and vaz_B_val > 0:
        regra26 = tnorm(tnorm(precip_AL_val, sal_ini_M_val), vaz_B_val)
        lista_salinidade_BS.append(regra26)
        print("Regra26 ativada - tnorma resultante:", regra26)
    if precip_AL_val > 0 and sal_ini_MB_val > 0 and vaz_B_val > 0:
        regra27 = tnorm(tnorm(precip_AL_val, sal_ini_MB_val), vaz_B_val)
        lista_salinidade_BS.append(regra27)
        print("Regra27 ativada - tnorma resultante:", regra27)
    if precip_AL_val > 0 and sal_ini_B_val > 0 and vaz_B_val > 0:
        regra28 = tnorm(tnorm(precip_AL_val, sal_ini_B_val), vaz_B_val)
        lista_salinidade_BS.append(regra28)
        print("Regra28 ativada - tnorma resultante:", regra28)
    elif lista_salinidade_BS == [] and lista_salinidade_B == [] and lista_salinidade_MB == [] and lista_salinidade_M == []:
        print("Nenhuma das regras foram ativadas.")
        intervalo_maximos = []
        alfa_corte = 0
        pertinencias = []
        return media_dos_maximos, intervalo_maximos, alfa_corte, pertinencias

    # Aplicação da t-conorma nas listas das regras ativadas
    if len(lista_salinidade_BS) > 0:
        maior_BS = max(lista_salinidade_BS)
    if len(lista_salinidade_B) > 0:
        maior_B = max(lista_salinidade_B)
    if len(lista_salinidade_MB) > 0:
        maior_MB = max(lista_salinidade_MB)
    if len(lista_salinidade_M) > 0:
        maior_M = max(lista_salinidade_M)

    # Verificando quem tem maior grau de pertinência entre as regras ativadas
    maior_pertinencia = max(maior_BS, maior_B, maior_MB, maior_M)

    if maior_pertinencia == maior_BS:
        conjunto = salinidade_BS
        alfa_corte = maior_BS
    elif maior_pertinencia == maior_B:
        conjunto = salinidade_B
        alfa_corte = maior_B
    elif maior_pertinencia == maior_MB:
        conjunto = salinidade_MB
        alfa_corte = maior_MB
    else:
        conjunto = salinidade_M
        alfa_corte = maior_M

    # Ajustar a função de pertinência pelo alfa-corte
    # Inicio do processo de defuzzificação.
    pertinencias = [fuzz.interp_membership(
        salinidade, conjunto, x) for x in salinidade]
    alfa_corte_indices = [i for i, p in enumerate(
        pertinencias) if p >= alfa_corte]
    intervalo_maximos = [salinidade[i] for i in alfa_corte_indices]

    # Calcular o centro dos máximos (COM)
    if intervalo_maximos:
        centro_dos_maximos = (min(intervalo_maximos) +
                              max(intervalo_maximos)) / 2
    else:
        centro_dos_maximos = None  # Caso não haja pontos máximos

    return centro_dos_maximos, intervalo_maximos, alfa_corte, pertinencias

# Função principal.


def main():
    lista_precipitacao = [13.6, 115, 148, 31, 3, 320, 110, 180, 102, 123, 23]
    lista_salinidade_inicial = [14, 30, 24, 18, 18, 26, 20, 18, 25, 30, 23]
    lista_vazao = [2016, 1163, 763, 1515, 2273, 687, 938, 800, 584, 469, 1454]

    for i in range(len(lista_precipitacao)):
        print(f"Coleta {i+1}")
        centro_dos_maximos, intervalo_maximos, alfa_corte, pertinencias = inferencia_fuzzy(
            lista_precipitacao[i], lista_salinidade_inicial[i], lista_vazao[i])
        print(
            f"Salinidade estimada: {centro_dos_maximos:.2f}" if centro_dos_maximos is not None else "Não há pontos máximos para calcular.")
        print("\n")

        # Plotagem
        plt.figure()
        plt.plot(salinidade, salinidade_BS, 'b',
                 linewidth=1.5, label='Baixissima')
        plt.plot(salinidade, salinidade_B, 'g', linewidth=1.5, label='Baixa')
        plt.plot(salinidade, salinidade_MB, 'c',
                 linewidth=1.5, label='Média Baixa')
        plt.plot(salinidade, salinidade_M, 'y', linewidth=1.5, label='Média')
        plt.plot(salinidade, salinidade_A, 'r', linewidth=1.5, label='Alta')

        if centro_dos_maximos is not None:
            if pertinencias != []:
                plt.axvline(x=centro_dos_maximos, color='m', linestyle='--',
                            label=f'Centro dos Máximos = {centro_dos_maximos:.2f}', linewidth=2)
                plt.scatter(intervalo_maximos, [
                    alfa_corte] * len(intervalo_maximos), color='orange', zorder=5)
                plt.fill_between(salinidade, 0, [min(alfa_corte, pertinencia) for pertinencia in pertinencias], where=[
                    pert >= alfa_corte for pert in pertinencias], color='gray', alpha=0.5)
                # Preencher apenas a área abaixo do alfa-corte
                plt.title(
                    f'Defuzzificação da Coleta {i+1} - Método Centro dos Máximos', fontsize=15)
                plt.xlabel('Salinidade(‰)', fontsize=12)
                plt.ylabel('Grau de Pertinência', fontsize=12)
                plt.legend()
                plt.grid(True)  # Adicionar grade ao gráfico
                plt.show()
            else:
                plt.title(
                    f'Nenhuma Regra Ativada na Coleta {i+1}', fontsize=15)
                plt.xlabel('Salinidade(‰)', fontsize=12)
                plt.ylabel('Grau de Pertinência', fontsize=12)
                plt.legend()
                plt.grid(True)  # Adicionar grade ao gráfico
                plt.show()


main()
