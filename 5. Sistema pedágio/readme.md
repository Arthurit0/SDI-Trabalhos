# Configuração do código

Ambos os códigos, cliente (cabine.py) e servidor (sistema.py) possuem as variáveis `SERVER_ADDRESS`, `MIN_WAIT_TIME` e `MAX_WAIT_TIME`.

`SERVER_ADDRESS` configura o endereço e porta em que o sistema irá rodar e que o cliente irá conectar.

`MIN_WAIT_TIME` e `MAX_WAIT_TIME` funcionam para simular a aleatoriedade dos veiculos chegando na cabine, no caso do cliente, e o tempo de processar o pagamento, no caso do servidor, funcionando como tempo mínimo e máximo para a execução dessas tarefas, respectivamente.

# Execução do código

Atualmente, o sistema (servidor) está configurado para rodar na ENS5 (10.20.221.235) e as cabines (clientes) irão se conectar a ele através dos ENS1-4. Para executar o código, basta rodar os comandos em python:

sistema.py:

```
python3 sistema.py
```

cabine.py

```
python3 cabine.py
```

Logs das operações da cabine e do sistema serão exibidos no terminal, mas também serão gerados arquivos `.log`.
