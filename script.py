import speedtest
import schedule
import time
import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)
historico_testes = []

def realizar_teste():
    servidor = speedtest.Speedtest()
    velocidade_download = servidor.download() / 10**6  # converter para megabits por segundo
    velocidade_upload = servidor.upload() / 10**6  # converter para megabits por segundo
    resultado = {
        "data": time.strftime("%Y-%m-%d %H:%M:%S"),
        "velocidade_download": round(velocidade_download, 2),
        "velocidade_upload": round(velocidade_upload, 2)
    }
    historico_testes.append(resultado)
    print("Teste realizado em", resultado["data"])
    salvar_historico()

def salvar_historico():
    with open("historico_testes.json", "w") as arquivo:
        json.dump(historico_testes, arquivo)

def carregar_historico():
    try:
        with open("historico_testes.json", "r") as arquivo:
            historico_testes.extend(json.load(arquivo))
    except FileNotFoundError:
        pass

@app.route("/")
def index():
    return render_template("index.html", historico_testes=historico_testes, is_running=schedule.next_run is not None)

@app.route("/run-test")
def run_test():
    realizar_teste()
    return jsonify({"status": "success"})

def agendar_teste():
    realizar_teste()
    schedule.every(30).minutes.do(realizar_teste)

if __name__ == "__main__":
    carregar_historico()
    agendar_teste()
    app.run(port=5000)
