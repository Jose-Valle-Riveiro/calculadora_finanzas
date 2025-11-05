#!/usr/bin/env python3
"""
Programa interactivo estilo Excel para cálculos financieros.
Soporta:
 - Valor Actual (VA)
 - Valor Futuro (VF)
 - Pagos / Anualidad (PMT)
 - Interés / Tasa
 - Valor Actual Neto (VAN)
 - Número de periodos (n)
 - Tasa Interna de Retorno (TIR)

Resultados mostrados en formato de quetzales, por ejemplo: Q1,000.00

Uso: python3 finanzas_excel_style.py
"""

import math


def q_format(x):
    try:
        return f"Q{float(x):,.2f}"
    except Exception:
        return f"Q{x}"


def input_float(prompt):
    while True:
        val = input(prompt).strip()
        try:
            return float(val)
        except ValueError:
            print("Entrada inválida. Ingresa un número, por ejemplo 5.5")


def pedir_tasa_periodica():
    print("Introduce la tasa de interés:")
    print("  1) Tasa por periodo (ej. 1.5 para 1.5%)")
    print("  2) Tasa anual y períodos por año (ej. 12 y 12 para mensual)")
    opt = input("Opción (1/2): ").strip()
    if opt == "2":
        tasa_anual = input_float("Tasa anual en % (ej. 12): ")
        periodos_año = input_float("Periodos por año (ej. 12): ")
        if periodos_año == 0:
            print("Periodos por año no puede ser 0, usando 1.")
            periodos_año = 1
        return (tasa_anual / 100.0) / periodos_año
    else:
        tasa = input_float("Tasa por periodo en % (ej. 1.5): ")
        return tasa / 100.0


# ----- Fórmulas -----

def vf_single_sum(pv, r, n):
    return pv * (1 + r) ** n

def pv_single_sum(fv, r, n):
    return fv / ((1 + r) ** n)

def fv_annuity(pmt, r, n, due=False):
    if abs(r) < 1e-12:
        res = pmt * n
    else:
        res = pmt * (((1 + r) ** n - 1) / r)
    if due:
        res *= (1 + r)
    return res

def pv_annuity(pmt, r, n, due=False):
    if abs(r) < 1e-12:
        res = pmt * n
    else:
        res = pmt * ((1 - (1 + r) ** (-n)) / r)
    if due:
        res *= (1 + r)
    return res

def pmt_from_pv(pv, r, n, due=False):
    if abs(r) < 1e-12:
        return pv / n
    denom = 1 - (1 + r) ** (-n)
    pmt = (r * pv) / denom
    if due:
        pmt /= (1 + r)
    return pmt

def pmt_from_fv(fv, r, n, due=False):
    if abs(r) < 1e-12:
        return fv / n
    numer = r * fv
    denom = (1 + r) ** n - 1
    pmt = numer / denom
    if due:
        pmt /= (1 + r)
    return pmt

def interes_general(pv, fv, n):
    if pv <= 0 or fv <= 0 or n <= 0:
        raise ValueError("PV, FV y n deben ser positivos.")
    return (fv / pv) ** (1 / n) - 1

def valor_actual_neto(flujos, r):
    return sum(cf / ((1 + r) ** i) for i, cf in enumerate(flujos))

def numero_periodos(pv, fv, r):
    if pv <= 0 or fv <= 0 or r <= -1:
        raise ValueError("Valores inválidos para PV, FV o r.")
    return math.log(fv / pv) / math.log(1 + r)

def tir(flujos, guess=0.1, tol=1e-6, max_iter=1000):
    r = guess
    for _ in range(max_iter):
        f = sum(cf / ((1 + r) ** i) for i, cf in enumerate(flujos))
        f_prime = sum(-i * cf / ((1 + r) ** (i + 1)) for i, cf in enumerate(flujos))
        if abs(f_prime) < 1e-12:
            break
        r_new = r - f / f_prime
        if abs(r_new - r) < tol:
            return r_new
        r = r_new
    return r

# ----- Menús -----

def menu_va():
    while True:
        print('\n--- Valor Actual (VA) ---')
        print('1) VA de un monto futuro (suma única)')
        print('2) VA de una anualidad (pagos periódicos) - ordinaria')
        print('3) VA de una anualidad (pagos al inicio - due)')
        print('4) VA combinada (anualidad + monto futuro)')
        print('0) Volver')
        opt = input('Elige una opción: ').strip()
        if opt == '0':
            return
        elif opt == '1':
            fv = input_float('FV (monto futuro): ')
            r = pedir_tasa_periodica()
            n = input_float('Número de periodos: ')
            va = pv_single_sum(fv, r, n)
            print('VA =', q_format(va))
        elif opt == '2' or opt == '3':
            pmt = input_float('Pago periódico (PMT): ')
            r = pedir_tasa_periodica()
            n = input_float('Número de periodos: ')
            due = (opt == '3')
            va = pv_annuity(pmt, r, n, due=due)
            print('VA =', q_format(va))
        elif opt == '4':
            pmt = input_float('Pago periódico (PMT): ')
            fv = input_float('Monto futuro adicional (FV) [0 si no aplica]: ')
            r = pedir_tasa_periodica()
            n = input_float('Número de periodos: ')
            va_pmt = pv_annuity(pmt, r, n, due=False)
            va_fv = pv_single_sum(fv, r, n)
            va = va_pmt + va_fv
            print('VA (total) =', q_format(va))
        else:
            print('Opción no válida.')

def menu_vf():
    while True:
        print('\n--- Valor Futuro (VF) ---')
        print('1) VF de un monto actual (suma única)')
        print('2) VF de una anualidad (pagos periódicos) - ordinaria')
        print('3) VF de anualidad (pagos al inicio - due)')
        print('4) VF combinada (suma actual + anualidad)')
        print('0) Volver')
        opt = input('Elige una opción: ').strip()
        if opt == '0':
            return
        elif opt == '1':
            pv = input_float('VA (monto actual): ')
            r = pedir_tasa_periodica()
            n = input_float('Número de periodos: ')
            vf = vf_single_sum(pv, r, n)
            print('VF =', q_format(vf))
        elif opt == '2' or opt == '3':
            pmt = input_float('Pago periódico (PMT): ')
            r = pedir_tasa_periodica()
            n = input_float('Número de periodos: ')
            due = (opt == '3')
            vf = fv_annuity(pmt, r, n, due=due)
            print('VF =', q_format(vf))
        elif opt == '4':
            pv = input_float('VA (monto actual): ')
            pmt = input_float('Pago periódico (PMT): ')
            r = pedir_tasa_periodica()
            n = input_float('Número de periodos: ')
            vf_total = vf_single_sum(pv, r, n) + fv_annuity(pmt, r, n, due=False)
            print('VF (total) =', q_format(vf_total))
        else:
            print('Opción no válida.')

def menu_pagos():
    while True:
        print('\n--- Pagos / Anualidad (PMT) ---')
        print('1) Calcular PMT para amortizar un VA (préstamo) - pago al final')
        print('2) Calcular PMT para amortizar un VA (préstamo) - pago al inicio (due)')
        print('3) Calcular PMT requerido para alcanzar un VF (ahorro) - pago al final')
        print('4) Calcular PMT requerido para alcanzar un VF (ahorro) - pago al inicio (due)')
        print('0) Volver')
        opt = input('Elige una opción: ').strip()
        if opt == '0':
            return
        elif opt == '1' or opt == '2':
            pv = input_float('VA (monto del préstamo): ')
            r = pedir_tasa_periodica()
            n = input_float('Número de periodos: ')
            due = (opt == '2')
            pmt = pmt_from_pv(pv, r, n, due=due)
            print('PMT =', q_format(pmt))
        elif opt == '3' or opt == '4':
            fv = input_float('VF objetivo (monto a alcanzar): ')
            r = pedir_tasa_periodica()
            n = input_float('Número de periodos: ')
            due = (opt == '4')
            pmt = pmt_from_fv(fv, r, n, due=due)
            print('PMT =', q_format(pmt))
        else:
            print('Opción no válida.')

def menu_interes():
    print('\n--- Interés / Tasa ---')
    pv = input_float('Valor actual (PV): ')
    fv = input_float('Valor futuro (FV): ')
    n = input_float('Número de periodos: ')
    r = interes_general(pv, fv, n)
    print(f'Tasa por periodo = {r * 100:.4f}%')

def menu_van():
    print('\n--- Valor Actual Neto (VAN) ---')
    n = int(input_float('Número de flujos (incluyendo el inicial): '))
    flujos = []
    for i in range(n):
        flujos.append(input_float(f'Flujo {i} (usa negativo para inversión inicial): '))
    r = pedir_tasa_periodica()
    van = valor_actual_neto(flujos, r)
    print('VAN =', q_format(van))

def menu_n():
    print('\n--- Número de periodos (n) ---')
    pv = input_float('Valor actual (PV): ')
    fv = input_float('Valor futuro (FV): ')
    r = pedir_tasa_periodica()
    n = numero_periodos(pv, fv, r)
    print(f'n = {n:.4f} periodos')

def menu_tir():
    print('\n--- Tasa Interna de Retorno (TIR) ---')
    n = int(input_float('Número de flujos (incluyendo el inicial): '))
    flujos = []
    for i in range(n):
        flujos.append(input_float(f'Flujo {i} (usa negativo para inversión inicial): '))
    guess = input_float('Suposición inicial (ej. 10% = 10): ') / 100
    r = tir(flujos, guess)
    print(f'TIR = {r * 100:.4f}%')

def main_menu():
    print('=== Calculadora financiera (estilo Excel) ===')
    while True:
        print('\nMenú principal:')
        print('1) Valor Actual (VA)')
        print('2) Valor Futuro (VF)')
        print('3) Pagos / Anualidad (PMT)')
        print('4) Interés / Tasa')
        print('5) Valor Actual Neto (VAN)')
        print('6) Número de periodos (n)')
        print('7) Tasa Interna de Retorno (TIR)')
        print('0) Salir')
        opt = input('Elige una opción: ').strip()
        if opt == '1':
            menu_va()
        elif opt == '2':
            menu_vf()
        elif opt == '3':
            menu_pagos()
        elif opt == '4':
            menu_interes()
        elif opt == '5':
            menu_van()
        elif opt == '6':
            menu_n()
        elif opt == '7':
            menu_tir()
        elif opt == '0':
            print('Saliendo. ¡Hasta luego!')
            break
        else:
            print('Opción no válida.')

if __name__ == '__main__':
    main_menu()
