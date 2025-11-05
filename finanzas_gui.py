import tkinter as tk
from tkinter import ttk, messagebox
from calculadora import (
    q_format, pv_single_sum, vf_single_sum, pv_annuity,
    fv_annuity, pmt_from_pv, pmt_from_fv,
    interes_general, valor_actual_neto,
    numero_periodos, tir
)

class CalculadoraFinanciera:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Financiera - Estilo Excel")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # Estilo moderno
        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 11))
        style.configure("TCombobox", font=("Segoe UI", 11))

        ttk.Label(root, text="Seleccione la operación:", font=("Segoe UI", 12, "bold")).pack(pady=10)

        self.operaciones = [
            "Valor Actual (VA)",
            "Valor Futuro (VF)",
            "Pagos / Anualidad (PMT)",
            "Interés / Tasa",
            "Valor Actual Neto (VAN)",
            "Número de periodos (n)",
            "Tasa Interna de Retorno (TIR)"
        ]

        self.combo_oper = ttk.Combobox(root, values=self.operaciones, state="readonly")
        self.combo_oper.current(0)
        self.combo_oper.pack(pady=5)

        ttk.Button(root, text="Continuar", command=self.mostrar_campos).pack(pady=10)

        self.frame_campos = ttk.Frame(root)
        self.frame_campos.pack(pady=10)

        self.resultado_label = ttk.Label(root, text="", font=("Segoe UI", 12, "bold"))
        self.resultado_label.pack(pady=10)

    def limpiar_campos(self):
        for widget in self.frame_campos.winfo_children():
            widget.destroy()

    def mostrar_campos(self):
        self.limpiar_campos()
        oper = self.combo_oper.get()

        if oper == "Valor Actual (VA)":
            self.crear_campos(["FV", "Tasa (%)", "Nº periodos"])
            ttk.Button(self.frame_campos, text="Calcular", command=self.calc_va).pack(pady=5)

        elif oper == "Valor Futuro (VF)":
            self.crear_campos(["PV", "Tasa (%)", "Nº periodos"])
            ttk.Button(self.frame_campos, text="Calcular", command=self.calc_vf).pack(pady=5)

        elif oper == "Pagos / Anualidad (PMT)":
            self.crear_campos(["PV", "Tasa (%)", "Nº periodos"])
            ttk.Button(self.frame_campos, text="Calcular", command=self.calc_pmt).pack(pady=5)

        elif oper == "Interés / Tasa":
            self.crear_campos(["PV", "FV", "Nº periodos"])
            ttk.Button(self.frame_campos, text="Calcular", command=self.calc_tasa).pack(pady=5)

        elif oper == "Valor Actual Neto (VAN)":
            ttk.Label(self.frame_campos, text="Flujos separados por coma (ej: -1000,300,400,500):").pack()
            self.entry_flujos = ttk.Entry(self.frame_campos, width=40)
            self.entry_flujos.pack(pady=5)
            ttk.Label(self.frame_campos, text="Tasa (%)").pack()
            self.entry_tasa = ttk.Entry(self.frame_campos)
            self.entry_tasa.pack(pady=5)
            ttk.Button(self.frame_campos, text="Calcular", command=self.calc_van).pack(pady=5)

        elif oper == "Número de periodos (n)":
            self.crear_campos(["PV", "FV", "Tasa (%)"])
            ttk.Button(self.frame_campos, text="Calcular", command=self.calc_n).pack(pady=5)

        elif oper == "Tasa Interna de Retorno (TIR)":
            ttk.Label(self.frame_campos, text="Flujos separados por coma (ej: -1000,300,400,500):").pack()
            self.entry_flujos = ttk.Entry(self.frame_campos, width=40)
            self.entry_flujos.pack(pady=5)
            ttk.Button(self.frame_campos, text="Calcular", command=self.calc_tir).pack(pady=5)

    def crear_campos(self, nombres):
        self.entries = {}
        for nombre in nombres:
            ttk.Label(self.frame_campos, text=nombre + ":").pack()
            entry = ttk.Entry(self.frame_campos)
            entry.pack(pady=3)
            self.entries[nombre] = entry

    def calc_va(self):
        try:
            fv = float(self.entries["FV"].get())
            r = float(self.entries["Tasa (%)"].get()) / 100
            n = float(self.entries["Nº periodos"].get())
            res = pv_single_sum(fv, r, n)
            self.resultado_label.config(text=f"VA = {q_format(res)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calc_vf(self):
        try:
            pv = float(self.entries["PV"].get())
            r = float(self.entries["Tasa (%)"].get()) / 100
            n = float(self.entries["Nº periodos"].get())
            res = vf_single_sum(pv, r, n)
            self.resultado_label.config(text=f"VF = {q_format(res)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calc_pmt(self):
        try:
            pv = float(self.entries["PV"].get())
            r = float(self.entries["Tasa (%)"].get()) / 100
            n = float(self.entries["Nº periodos"].get())
            res = pmt_from_pv(pv, r, n)
            self.resultado_label.config(text=f"PMT = {q_format(res)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calc_tasa(self):
        try:
            pv = float(self.entries["PV"].get())
            fv = float(self.entries["FV"].get())
            n = float(self.entries["Nº periodos"].get())
            r = interes_general(pv, fv, n)
            self.resultado_label.config(text=f"Tasa por periodo = {r * 100:.2f}%")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calc_van(self):
        try:
            flujos = [float(x) for x in self.entry_flujos.get().split(",")]
            r = float(self.entry_tasa.get()) / 100
            res = valor_actual_neto(flujos, r)
            self.resultado_label.config(text=f"VAN = {q_format(res)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calc_n(self):
        try:
            pv = float(self.entries["PV"].get())
            fv = float(self.entries["FV"].get())
            r = float(self.entries["Tasa (%)"].get()) / 100
            n = numero_periodos(pv, fv, r)
            self.resultado_label.config(text=f"n = {n:.4f} periodos")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calc_tir(self):
        try:
            flujos = [float(x) for x in self.entry_flujos.get().split(",")]
            r = tir(flujos)
            self.resultado_label.config(text=f"TIR = {r * 100:.4f}%")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraFinanciera(root)
    root.mainloop()