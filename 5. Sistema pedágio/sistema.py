import random
import socket
import threading
import queue
import time
import json
import logging

# Configuração Servidor
# SERVER_ADDRESS = ("localhost", 12345)
SERVER_ADDRESS = ("10.20.221.235", 12345)
MIN_WAIT_TIME = 5
MAX_WAIT_TIME = 8

# Configuração Logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("servidor_pedagio.log"),
        logging.StreamHandler(),
    ],
)

filas = {
    "Sem Parar": queue.Queue(),
    "ConectCar": queue.Queue(),
    "Veloe": queue.Queue(),
    "Move Mais": queue.Queue(),
    "C6 Taggy": queue.Queue(),
}


def processar_fila(servico, fila):
    while True:
        veiculo, connection = fila.get()
        logging.info(f"Servidor: Processando {veiculo['placa']} no serviço {servico}.")

        time.sleep(random.uniform(MIN_WAIT_TIME, MAX_WAIT_TIME))  # Atraso de pagamento

        liberar_veiculo(veiculo, connection)
        log_estado_fila(servico)


def liberar_veiculo(veiculo, connection):
    resposta = f"Veículo {veiculo['placa']} processado com sucesso. Valor pago: {veiculo['valor']}"  # Resposta final

    logging.info(f"Servidor: {resposta}")

    try:
        connection.sendall(resposta.encode("utf-8"))
    except BrokenPipeError:
        logging.error(
            f"Servidor: Falha ao enviar resposta para o veículo {veiculo['placa']}. A conexão foi fechada."
        )
    finally:
        connection.close()


def recebe_veiculo(connection, address):
    try:
        mensagem = connection.recv(1024).decode("utf-8")
        veiculo = json.loads(mensagem)
        logging.info(
            f"Servidor: Recebido veículo {veiculo['placa']} da cabine {address[0]}"
        )

        filas[veiculo["servico"]].put((veiculo, connection))
        log_estado_fila(veiculo["servico"])

        connection.sendall(b"Aguardando processamento")  # Resposta inicial

    except Exception as e:
        logging.error(f"Servidor: Erro ao lidar com o cliente {address}: {e}")
        connection.close()


def iniciar_servidor():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(SERVER_ADDRESS)
            server_socket.listen(5)
            logging.info("Servidor: Aguardando conexões...")

            for servico, fila in filas.items():
                threading.Thread(
                    target=processar_fila, args=(servico, fila), daemon=True
                ).start()

            while True:
                connection, address = server_socket.accept()
                threading.Thread(
                    target=recebe_veiculo, args=(connection, address), daemon=True
                ).start()
    except KeyboardInterrupt:
        logging.info("Interrompendo sistema.")


def log_estado_fila(servico):
    fila = filas[servico]
    veiculos_fila = list(fila.queue)
    placas_fila = [veiculo[0]["placa"] for veiculo in veiculos_fila]
    logging.info(f"Estado da fila {servico}: {placas_fila}")


if __name__ == "__main__":
    iniciar_servidor()
