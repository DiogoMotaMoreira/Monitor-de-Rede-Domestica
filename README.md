# ✅ Monitor de Rede Doméstica
Este projeto tem como objetivo monitorizar dispositivos conectados à rede local (LAN), verificando se estão online ou offline, recolhendo informações como hostname, latência, e gravando tudo em histórico (CSV e JSON).


## 📌 Funcionalidades Implementadas
✔ Varredura da rede local

- Faz ping a todos os IPs dentro do intervalo 192.168.1.1 até 192.168.1.254.

✔ Resolução de hostname

- Tenta obter o nome associado ao IP (quando disponível).

✔ Deteção do estado do dispositivo

- Mostra se o dispositivo está ONLINE ✅ ou OFFLINE ❌.

✔ Medição de latência

- Exibe o tempo de resposta do ping (quando disponível).

✔ Execução periódica

- Corre automaticamente de 24 em 24 horas (interval = 86400 segundos).

✔ Histórico em ficheiros CSV e JSON

- Cria um ficheiro diário com o nome historico_YYYY-MM-DD.csv.
- Guarda: Data e Hora, IP, Hostname, Estado, Latência.

✔ Resumo no final de cada varredura

- Exibe quantos dispositivos estão ativos vs total.


## 🛠 Dependências
- Todas as dependências encontram-se no ficheiro requirements.txt com a devida instalação

## ✅ Como funciona o código

1. Define a faixa de IPs e intervalo entre varreduras.
2. Para cada IP:
- Faz ping.
- Resolve o hostname.
- Mostra no terminal o estado e a latência.
- Regista os dados no histórico.
3. Após varrer todos os IPs:
- Mostra o total de dispositivos ativos.
- Aguarda o intervalo definido e repete.


## 🖥 Exemplo de Saída no Terminal

```
--- Nova Varredura ---
                              Scanner de Rede
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ IP          ┃ Hostname               ┃ Status    ┃ Latência              ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ 192.168.1.1 │ NOSdrive               │ ONLINE ✅ │ 61ms                  │
│ 192.168.1.5 │ EPSON228706            │ ONLINE ✅ │ 124ms                 │
│ 192.168.1.3 │ zc4430kno-6CA604A54945 │ ONLINE ✅ │ 58ms                  │
│ 192.168.1.2 │ Desconhecido           │ ONLINE ✅ │ latência desconhecida │
│ 192.168.1.4 │ Desconhecido           │ ONLINE ✅ │ latência desconhecida │
└─────────────┴────────────────────────┴───────────┴───────────────────────┘
Total: 5 ativos / 5 no total
```


## ▶ Como Executar

    python monitor.py --subnet 192.168.1. --start 1 --end 5 --interval 60 --csv --json

### ⚙ Parâmetros Disponíveis
    Parâmetro	Descrição

    --subnet	Sub-rede base (ex.: 192.168.1.)
    --start	    IP inicial (ex.: 1)
    --end	    IP final (ex.: 254)
    --interval	Intervalo entre varreduras em segundos (ex.: 30)
    --once	    Executa apenas uma varredura
    --csv	    Salva histórico em CSV
    --json	    Salva histórico em JSON


## 🚀 Próximas Funcionalidades

- Obter MAC Address e identificar fabricante (Vendor).
- Criar Whitelist para dispositivos autorizados.
- Alertar sobre dispositivos desconhecidos/intrusos.
- Enviar notificações (Email, Telegram).
- Dashboard com interface gráfica (Web ou Terminal interativo).
- Logs detalhados.


## ✅ Tecnologias Utilizadas

- Python 3
- rich (para saída colorida no terminal)
- asyncio (execução assíncrona para rapidez)