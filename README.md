# ✅ Monitor de Rede Doméstica
Este projeto tem como objetivo monitorizar os dispositivos conectados à rede local (LAN), verificando se estão online ou offline e registando os resultados num ficheiro histórico.

---

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

✔ Histórico em ficheiros CSV

- Cria um ficheiro diário com o nome historico_YYYY-MM-DD.csv.
- Guarda: Data e Hora, IP, Hostname, Estado, Latência.

✔ Resumo no final de cada varredura

- Exibe quantos dispositivos estão ativos vs total.

---

## 🖥 Exemplo de Saída no Terminal

```
--- Nova Varredura ---
192.168.1.1      | router.local                   | ONLINE ✅   | Latência: 2ms
192.168.1.20     | Desconhecido                  | OFFLINE ❌  | Latência: --
192.168.1.50     | servidor.local                | ONLINE ✅   | Latência: 3ms

Total: 2 ativos / 254 no total

[INFO] A aguardar 86400 segundos para a próxima varredura...
```

---

## 📂 Estrutura dos Ficheiros de Histórico
Cada varredura é registada no ficheiro:

    historico_2025-08-27.csv

Com os dados:

    2025-08-27 10:00:00,192.168.1.1,router.local,ONLINE ✅,2ms
    2025-08-27 10:00:01,192.168.1.20,Desconhecido,OFFLINE ❌,--

---

## ✅ Como funciona o código

1. Define a faixa de IPs e intervalo entre varreduras.
2. Para cada IP:
- Faz ping.
- Resolve o hostname.
- Mostra no terminal o estado e a latência.
- Regista os dados no CSV diário.
3. Após varrer todos os IPs:
- Mostra o total de dispositivos ativos.
- Aguarda o intervalo definido e repete.