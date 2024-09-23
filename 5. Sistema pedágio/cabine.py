import socket
import random
import string
import time
import json
import threading
import logging

# Configuração Cliente
# SERVER_ADDRESS = ("localhost", 12345)
SERVER_ADDRESS = ("10.20.221.235", 12345)
MIN_WAIT_TIME = 2
MAX_WAIT_TIME = 5

# Configuração Logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("cliente_pedagio.log"),  # Log no arquivo
        logging.StreamHandler(),  # Log no terminal
    ],
)


def gerar_placa():
    letras = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    numeros = "".join(random.choices("0123456789", k=4))
    return letras + numeros


def gerar_veiculo():
    placa = gerar_placa()

    valor_pago = random.randint(1, 10)

    servico = random.choice(
        ["Sem Parar", "ConectCar", "Veloe", "Move Mais", "C6 Taggy"]
    )

    return {"placa": placa, "valor": valor_pago, "servico": servico}


def enviar_veiculo(veiculo):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(SERVER_ADDRESS)

        mensagem = json.dumps(veiculo)
        sock.sendall(mensagem.encode("utf-8"))

        # Resposta inicial: Recebido
        resposta_inicial = sock.recv(1024).decode("utf-8")
        logging.info(f"Cabine: {resposta_inicial} para o veículo {veiculo['placa']}")

        # Resposta final: Processado
        resposta_final = sock.recv(1024).decode("utf-8")
        logging.info(f"Cabine: {resposta_final} para o veículo {veiculo['placa']}")


def simular_pedagio():
    try:
        while True:
            veiculo = gerar_veiculo()
            logging.info(
                f"Cabine: Enviando veículo {veiculo['placa']} para o servidor."
            )

            threading.Thread(target=enviar_veiculo, args=(veiculo,)).start()

            time.sleep(random.uniform(MIN_WAIT_TIME, MAX_WAIT_TIME))
    except KeyboardInterrupt:
        logging.info("Interrompendo e aguardando veículos restantes serem processados.")


if __name__ == "__main__":
    simular_pedagio()
