import os
import platform
import subprocess
import socket
import asyncio
from datetime import datetime
import time

range_min = 1
range_max = 254
interval = 86400

def ping(host):
    param1 = '-n' if platform.system().lower() == 'windows' else '-c'
    param2 = '-w' if platform.system().lower() == 'windows' else '-W'
    tempo = '11000' if platform.system().lower() == 'windows' else '1'
    command = ['ping', param1, '1', param2, tempo, host]
    try:
        output = subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
        for line in output.splitlines():
            if 'time=' in line:
                time_part = line.split('time=')[-1].split()[0]
                return True, time_part
        return True, 'latência desconhecida'
    except subprocess.CalledProcessError:
        return False, None

def resolve_host(host):
    try:
        return socket.gethostbyaddr(host)[0]
    except socket.herror:
        return None

async def tarefa(host):
    hostname = await asyncio.to_thread(resolve_host, host)
    status, latency = await asyncio.to_thread(ping, host)
    status_text = "ONLINE ✅" if status else "OFFLINE ❌"
    name_text = hostname if hostname else "Desconhecido"
    latency_text = latency if latency else "--"

    print(f"{host:<15} | {name_text:<30} | {status_text:<10} | Latência: {latency_text}")

    timestamp = datetime.now().strftime("%Y-%m-%d")
    with open(f"historico_{timestamp}.csv", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()},{host},{name_text},{status_text},{latency_text}\n")
    
    return status

async def main():
    tasks = []
    for number in range(range_min, range_max+1):
        host = f'192.168.1.{number}'
        tasks.append(tarefa(host))
    resultados = await asyncio.gather(*tasks)
    ativos = sum(1 for r in resultados if r)
    total = len(resultados)
    return total, ativos


async def run_forever():
    while True:
        print("\n--- Nova Varredura ---")
        n_total, n_ativo = await main()
        print(f'Total: {n_ativo} ativos / {n_total} no total')
        print(f"\n[INFO] A aguardar {interval} segundos para a próxima varredura...\n")
        await asyncio.sleep(interval)

if __name__ == "__main__":
    asyncio.run(run_forever())
