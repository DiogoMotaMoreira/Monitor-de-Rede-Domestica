import os
import platform
import subprocess
import socket
import asyncio
from datetime import datetime
import argparse
from rich.table import Table
from rich.console import Console
import csv
import json

console = Console()

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
    
def hist_csv(host, name_text, status_text, latency_text):
    timestamp = datetime.now().strftime("%Y-%m-%d")
    os.makedirs('historico_csv', exist_ok=True)
    escrever_cabecalho = not os.path.exists(f'historico_csv/historico_{timestamp}.csv')
    with open(f"historico_csv/historico_{timestamp}.csv", "a", encoding="utf-8") as f:
        writer = csv.writer(f)

        if escrever_cabecalho:
            writer.writerow(["Date", "Ip", "Hostname", "Satus", "Latency"])
        
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            host,
            name_text,
            status_text,
            latency_text
        ])

def hist_json(host, name_text, status_text, latency_text):
    timestamp = datetime.now().strftime("%Y-%m-%d")
    dados_json = {
        "timestamp": timestamp,
        "ip": host,
        "hostname": name_text,
        "status": status_text,
        "latency": latency_text
    }
    os.makedirs('historico_json', exist_ok=True)

    with open(f"historico_json/historico_{timestamp}.json", "a", encoding="utf-8") as f:
        json.dump(dados_json, f, ensure_ascii=False, indent=4)       
    

async def tarefa(host, table):
    hostname = await asyncio.to_thread(resolve_host, host)
    status, latency = await asyncio.to_thread(ping, host)
    status_text = "ONLINE ✅" if status else "OFFLINE ❌"
    name_text = hostname if hostname else "Desconhecido"
    latency_text = latency if latency else "--"

    table.add_row(host, name_text, status_text, latency_text)

    if args.csv:
        hist_csv(host, name_text, status_text, latency_text)

    if args.json:
        hist_json(host, name_text, status_text, latency_text)
    

    return status

async def main():
    tasks = []
    subnet = args.subnet
    range_min = args.start
    range_max = args.end

    table = Table(title='Scanner de Rede')
    table.add_column("IP", style="cyan")
    table.add_column("Hostname", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Latência", style="yellow")


    for number in range(range_min, range_max+1):
        host = f'{subnet}{number}'
        tasks.append(tarefa(host, table))
    
    resultados = await asyncio.gather(*tasks)

    console.print(table)

    ativos = sum(1 for r in resultados if r)
    total = len(resultados)
    return total, ativos


async def run_forever():
    while True:
        interval = args.interval
        print("\n--- Nova Varredura ---")
        n_total, n_ativo = await main()
        print(f'Total: {n_ativo} ativos / {n_total} no total')
        if args.once: break
        else:              
            print(f"\n[INFO] A aguardar {interval} segundos para a próxima varredura...\n")
            await asyncio.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scanner de rede')
    parser.add_argument("--subnet", type=str, default="192.168.1.", help="Sub-rede base (ex.: 192.168.0.)")
    parser.add_argument("--interval", type=int, default=30, help="Intervalo entre varreduras (segundos)")
    parser.add_argument("--start", type=int, default=1, help="Inicio de host")
    parser.add_argument("--end", type=int, default=254, help="Fim de host")
    parser.add_argument("--once",action='store_true', help="Uma varredura apenas")
    parser.add_argument("--json",action='store_true', help="Criar histórico em json")
    parser.add_argument("--csv",action='store_true', help="Criar histórico em csv")
    args = parser.parse_args()
    asyncio.run(run_forever())
