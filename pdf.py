import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from concurrent.futures import ThreadPoolExecutor

CLEAN_CHARS = re.compile(r'[^\w\s.-]', re.UNICODE)
MULTISPACE = re.compile(r'\s+')

def limpar_nome(nome_arquivo):
    nome, extensao = os.path.splitext(nome_arquivo)
    nome_limpo = CLEAN_CHARS.sub('', nome)
    nome_limpo = MULTISPACE.sub('_', nome_limpo.strip())
    return nome_limpo + extensao.lower()

def processar_arquivo(caminho_completo):
    diretorio, nome_arquivo = os.path.split(caminho_completo)
    novo_nome = limpar_nome(nome_arquivo)

    if novo_nome != nome_arquivo:
        novo_caminho = os.path.join(diretorio, novo_nome)
        try:
            os.rename(caminho_completo, novo_caminho)
        except FileExistsError:
            print(f"Aviso: {novo_nome} já existe. Pulando {nome_arquivo}")
        except OSError as e:
            print(f"Erro ao renomear {nome_arquivo}: {e}")

def iniciar_processamento():
    diretorio = filedialog.askdirectory(title="Selecione a pasta com os PDFs")
    if not diretorio:
        return

    diretorio = os.path.normpath(diretorio)

    if not os.path.isdir(diretorio):
        messagebox.showerror("Erro", f"{diretorio} não é um diretório válido!")
        return

    arquivos_pdf = []
    with os.scandir(diretorio) as entries:
        for entry in entries:
            #oque defini o tipo de arquivo a ser mudado e esse ".pdf"
            if entry.is_file() and entry.name.lower().endswith('.pdf'):
                arquivos_pdf.append(entry.path)

    if not arquivos_pdf:
        messagebox.showinfo("Nenhum Arquivo", "Nenhum arquivo PDF encontrado na pasta selecionada.")
        return

    progress["maximum"] = len(arquivos_pdf)
    progress["value"] = 0
    janela.update_idletasks()

    with ThreadPoolExecutor() as executor:
        for i, _ in enumerate(executor.map(processar_arquivo, arquivos_pdf), 1):
            progress["value"] = i
            janela.update_idletasks()

    messagebox.showinfo("Concluído", "Processamento finalizado com sucesso!")

janela = tk.Tk()
janela.title("Renomeador de PDFs")
janela.geometry("350x150")
janela.resizable(False, False)

frame = ttk.Frame(janela, padding=10)
frame.pack(expand=True, fill="both")

label = ttk.Label(frame, text="Selecione uma pasta com arquivos PDF")
label.pack(pady=5)

btn_selecionar = ttk.Button(frame, text="Selecionar Pasta", command=iniciar_processamento)
btn_selecionar.pack(pady=5)

progress = ttk.Progressbar(frame, orient="horizontal", length=250, mode="determinate")
progress.pack(pady=10)

janela.mainloop()
