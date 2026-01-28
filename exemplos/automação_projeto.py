import requests
from bs4 import BeautifulSoup
import csv
import re
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ================== CONFIG ==================
APP_NOME = "Automação Web Premium+"
APP_VERSAO = "v1.3"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# ================== CORE ==================

def extrair_preco(texto):
    padrao = r'(R\$|\$|£)?\s?\d{1,3}(\.\d{3})*(\,\d{2}|\.\d{2})'
    achado = re.search(padrao, texto)
    return achado.group().strip() if achado else ""

def coletar_dados(url, termo, log):
    log("Conectando ao site...")
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    resultados = []

    log("Analisando conteúdo...")
    for el in soup.find_all(string=True):
        if el.parent.name in ["script", "style", "noscript"]:
            continue

        texto = el.strip()
        if not texto:
            continue

        if termo.lower() in texto.lower():
            resultados.append({
                "conteudo": texto,
                "preco": extrair_preco(texto),
                "termo": termo,
                "url": url,
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    return resultados

def salvar_csv(dados):
    nome = f"resultado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(nome, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["conteudo", "preco", "termo", "url", "data"])
        for d in dados:
            w.writerow([d["conteudo"], d["preco"], d["termo"], d["url"], d["data"]])
    return nome

# ================== INTERFACE ==================

def logar(msg):
    area_log.insert("end", msg + "\n")
    area_log.see("end")
    janela.update()

def executar():
    area_log.delete("1.0", "end")
    status.set("Executando...")
    janela.update()

    url = entrada_url.get().strip()
    termo = entrada_termo.get().strip()

    if not url or not termo:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")
        return

    try:
        dados = coletar_dados(url, termo, logar)

        if not dados:
            logar("Nenhum resultado encontrado.")
            status.set("Finalizado sem resultados")
            return

        arquivo = salvar_csv(dados)
        logar(f"{len(dados)} resultados encontrados.")
        logar(f"Arquivo gerado: {arquivo}")

        status.set("Concluído com sucesso")
        messagebox.showinfo("Sucesso", f"{len(dados)} registros salvos.")

    except Exception as e:
        status.set("Erro")
        messagebox.showerror("Erro", str(e))

def iniciar():
    global entrada_url, entrada_termo, area_log, status, janela

    janela = tk.Tk()
    janela.title(f"{APP_NOME} {APP_VERSAO}")
    janela.geometry("620x460")
    janela.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")

    frame = ttk.Frame(janela, padding=15)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text=APP_NOME, font=("Segoe UI", 18, "bold")).pack(pady=5)
    ttk.Label(frame, text="Coleta inteligente de dados web", foreground="gray").pack()

    ttk.Label(frame, text="URL do site").pack(anchor="w", pady=(15, 0))
    entrada_url = ttk.Entry(frame)
    entrada_url.pack(fill="x")

    ttk.Label(frame, text="Termo de busca").pack(anchor="w", pady=(10, 0))
    entrada_termo = ttk.Entry(frame)
    entrada_termo.pack(fill="x")

    ttk.Button(frame, text="Iniciar Coleta", command=executar).pack(pady=15)

    ttk.Label(frame, text="Log de execução").pack(anchor="w")
    area_log = tk.Text(frame, height=8)
    area_log.pack(fill="x")

    status = tk.StringVar(value="Aguardando ação")
    ttk.Label(frame, textvariable=status, foreground="blue").pack(pady=10)

    ttk.Label(frame, text="© Premium+ Automation", font=("Segoe UI", 8)).pack(side="bottom")

    janela.mainloop()

# ================== START ==================

if __name__ == "__main__":
    print(f">>> {APP_NOME} INICIADA <<<")
    iniciar()
