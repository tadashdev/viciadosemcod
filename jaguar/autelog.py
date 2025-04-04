import os
import requests
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor

def log_error(message):
    with open("logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n\n")

errored_accounts = []
errored_lock = threading.Lock()

proxy_url = "seu proxy aqui"
proxies = {
    "http": proxy_url,
    "https": proxy_url
}

playpp_headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.playpp.com",
    "referer": "https://www.playpp.com/",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"
}

braqqq_headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.braqqq.com",
    "referer": "https://www.braqqq.com/",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"
}

pttwin_headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.pttwin.com",
    "referer": "https://www.pttwin.com/",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/134.0.0.0"
}

api_info = {
    "playpp": {
        "url": "https://api.playppttxy3.com/login/login",
        "headers": playpp_headers
    },
    "braqqq": {
        "url": "https://api.braqqq2t22t.com/login/login",
        "headers": braqqq_headers
    },
    "pttwin": {
        "url": "https://api.pttwinz9t5t.com/login/login",
        "headers": pttwin_headers
    }
}

wallet_info = {
    "playpp": {
        "url": "https://api.playppttxy3.com/user/getUserWallet",
        "headers": playpp_headers
    },
    "braqqq": {
        "url": "https://api.braqqq2t22t.com/user/getUserWallet",
        "headers": braqqq_headers
    },
    "pttwin": {
        "url": "https://api.pttwinz9t5t.com/user/getUserWallet",
        "headers": pttwin_headers
    }
}

def build_payload(platform, email, password):
    device_id = f"Windows_{str(uuid.uuid4())}"
    if platform.lower() == "playpp":
        return {
            "account": email,
            "password": password,
            "login_type": "2",
            "mainVer": "1",
            "subVer": "4",
            "pkgName": "h5_client",
            "platform": "Windows",
            "deviceid": device_id,
            "firstInstall": "false",
            "type": "101",
            "dataVersion": "1743171601",
            "nativeVer": "0",
            "language": "pt-pt",
            "domain": "https://api.playppttxy3.com",
            "device_id": device_id,
            "source_type": "",
            "os": "Windows",
            "login_source": "0"
        }
    elif platform.lower() == "braqqq":
        return {
            "account": email,
            "password": password,
            "login_type": "2",
            "mainVer": "1",
            "subVer": "4",
            "pkgName": "h5_client",
            "platform": "Windows",
            "deviceid": device_id,
            "firstInstall": "false",
            "type": "101",
            "dataVersion": "1743171601",
            "nativeVer": "0",
            "language": "pt-pt",
            "domain": "https://api.braqqq2t22t.com",
            "device_id": device_id,
            "source_type": "",
            "os": "Windows",
            "login_source": "0"
        }
    elif platform.lower() == "pttwin":
        return {
            "account": email,
            "password": password,
            "login_type": "2",
            "mainVer": "1",
            "subVer": "4",
            "pkgName": "h5_client",
            "platform": "Windows",
            "deviceid": device_id,
            "firstInstall": "false",
            "type": "101",
            "dataVersion": "1743171601",
            "nativeVer": "0",
            "language": "pt-pt",
            "domain": "https://api.pttwinz9t5t.com",
            "device_id": device_id,
            "source_type": "",
            "os": "Windows",
            "login_source": "0"
        }
    else:
        return None

def process_login(platform, email, password):
    payload = build_payload(platform, email, password)
    if not payload:
        err = f"Plataforma {platform} não suportada para {email}."
        print(err)
        log_error(err)
        return None
    info = api_info.get(platform.lower())
    if not info:
        err = f"Informações API para {platform} não encontradas para {email}."
        print(err)
        log_error(err)
        return None
    try:
        response = requests.post(info["url"], data=payload, headers=info["headers"], proxies=proxies)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0:
                token = data.get("data", {}).get("token")
                print(f"{platform} - Login bem-sucedido para {email}. Token: {token}")
                return token
            else:
                err = f"{platform} - Falha no login para {email}: {data.get('msg')}"
                print(err)
                log_error(err)
                return None
        else:
            err = f"{platform} - Erro HTTP para {email}: {response.status_code}"
            print(err)
            log_error(err)
            return None
    except Exception as e:
        err = f"{platform} - Exceção para {email}: {e}"
        print(err)
        log_error(err)
        if "522" in str(e) or "ProxyError" in str(e):
            with errored_lock:
                errored_accounts.append((platform, email, password))
        return None

def process_login_retry(platform, email, password):
    token = process_login(platform, email, password)
    if token:
        with results_lock:
            results.append((platform, token, email, password))

results = []
results_lock = threading.Lock()

def process_group(platform, credentials):
    for email, password in credentials:
        token = process_login(platform, email, password)
        if token:
            with results_lock:
                results.append((platform, token, email, password))

def reprocess_error_accounts():
    max_retries = 3
    retry = 0
    while retry < max_retries:
        with errored_lock:
            if not errored_accounts:
                break
            current_batch = errored_accounts.copy()
            errored_accounts.clear()
        print(f"Reenviando os com erro... Tentativa {retry+1}")
        with ThreadPoolExecutor(max_workers=len(current_batch)) as executor:
            futures = []
            for account in current_batch:
                plataforma, email, senha = account
                futures.append(executor.submit(process_login_retry, plataforma, email, senha))
            for future in futures:
                future.result()
        retry += 1
    if errored_accounts:
        print("Contas que ainda não puderam ser processadas:")
        for account in errored_accounts:
            print(account)

def main():
    contas_dir = "contas"
    if not os.path.exists(contas_dir):
        print(f"Pasta '{contas_dir}' não encontrada.")
        return
    arquivos = os.listdir(contas_dir)
    if not arquivos:
        print(f"Nenhum arquivo encontrado na pasta '{contas_dir}'.")
        return
    print("Arquivos disponíveis na pasta 'contas':")
    for idx, arquivo in enumerate(arquivos):
        print(f"{idx + 1}. {arquivo}")
    escolha = input("Escolha o número do arquivo a ser processado: ")
    try:
        escolha = int(escolha)
        if escolha < 1 or escolha > len(arquivos):
            print("Escolha inválida.")
            return
    except ValueError:
        print("Entrada inválida.")
        return
    arquivo_selecionado = os.path.join(contas_dir, arquivos[escolha - 1])
    with open(arquivo_selecionado, "r", encoding="utf-8") as f:
        linhas = f.readlines()
    grupos = {"playpp": [], "braqqq": [], "pttwin": []}
    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        partes = linha.split(",")
        if len(partes) < 3:
            err = f"Linha inválida: {linha}"
            print(err)
            log_error(err)
            continue
        plataforma = partes[0].strip().lower()
        email = partes[1].strip()
        senha = partes[2].strip()
        if plataforma in grupos:
            grupos[plataforma].append((email, senha))
        else:
            err = f"Plataforma desconhecida: {plataforma} para {email}"
            print(err)
            log_error(err)
    threads = []
    for plat, creds in grupos.items():
        if creds:
            t = threading.Thread(target=process_group, args=(plat, creds))
            threads.append(t)
            t.start()
    for t in threads:
        t.join()
    with errored_lock:
        if errored_accounts:
            reprocess_error_accounts()
    ordenados = []
    for plat in ["braqqq", "playpp", "pttwin"]:
        ordenados.extend([r for r in results if r[0].lower() == plat])
    tokens_dir = "tokenstotal"
    if not os.path.exists(tokens_dir):
        os.makedirs(tokens_dir)
    tokens_file = os.path.join(tokens_dir, "tokens.txt")
    with open(tokens_file, "w", encoding="utf-8") as f:
        for plataforma, token, email, senha in ordenados:
            f.write(f"{plataforma} : {token} : {email} : {senha}\n")
    print("Processamento de logins concluído. Tokens salvos em", tokens_file)
    consulta = input("Deseja consultar os saldos? (s/n): ")
    if consulta.strip().lower().startswith("s"):
        wallet_results = []
        wallet_lock = threading.Lock()
        def process_wallet_for_result(result):
            plataforma, token, email, senha = result
            info = wallet_info.get(plataforma.lower())
            if not info:
                gold = "N/A"
                err = f"Informações de wallet não encontradas para {email} em {plataforma}"
                print(err)
                log_error(err)
            else:
                try:
                    payload = {"token": token, "type": "1", "language": "pt-pt"}
                    r = requests.post(info["url"], data=payload, headers=info["headers"], proxies=proxies)
                    if r.status_code == 200:
                        data = r.json()
                        if data.get("code") == 0:
                            gold = data.get("data", {}).get("gold", "N/A")
                        else:
                            gold = "Erro: " + data.get("msg", "Unknown")
                            err = f"{plataforma} - Wallet falhou para {email}: {data.get('msg')}"
                            print(err)
                            log_error(err)
                    else:
                        gold = "Erro HTTP " + str(r.status_code)
                        err = f"{plataforma} - Erro HTTP na wallet para {email}: {r.status_code}"
                        print(err)
                        log_error(err)
                except Exception as e:
                    gold = "Exceção: " + str(e)
                    err = f"{plataforma} - Exceção na wallet para {email}: {e}"
                    print(err)
                    log_error(err)
            with wallet_lock:
                wallet_results.append((plataforma, token, email, senha, gold))
        wallet_threads = []
        for res in results:
            t = threading.Thread(target=process_wallet_for_result, args=(res,))
            wallet_threads.append(t)
            t.start()
        for t in wallet_threads:
            t.join()
        ordenados_wallet = []
        for plat in ["braqqq", "playpp", "pttwin"]:
            ordenados_wallet.extend([r for r in wallet_results if r[0].lower() == plat])
        with open(tokens_file, "w", encoding="utf-8") as f:
            for plataforma, token, email, senha, gold in ordenados_wallet:
                f.write(f"{plataforma} : {token} : {email} : {senha} saldo : {gold}\n")
        print("Consulta de saldos concluída e tokens atualizados com saldos.")
        total_saldo = 0.0
        saldo_braqqq = 0.0
        saldo_playpp = 0.0
        saldo_pttwin = 0.0
        contas_abaixo_10 = 0
        saldo_acima_20 = 0.0
        for plataforma, token, email, senha, gold in wallet_results:
            try:
                saldo = float(gold)
            except Exception:
                saldo = 0.0
            total_saldo += saldo
            if plataforma.lower() == "braqqq":
                saldo_braqqq += saldo
            elif plataforma.lower() == "playpp":
                saldo_playpp += saldo
            elif plataforma.lower() == "pttwin":
                saldo_pttwin += saldo
            if saldo < 10:
                contas_abaixo_10 += 1
            if saldo >= 20:
                saldo_acima_20 += saldo
        print("\n--- Resumo dos Saldos ---")
        print(f"Total de saldo: {total_saldo:.2f}")
        print(f"Saldo do grupo braqqq: {saldo_braqqq:.2f}")
        print(f"Saldo do grupo playpp: {saldo_playpp:.2f}")
        print(f"Saldo do grupo pttwin: {saldo_pttwin:.2f}")
        print(f"Contas com saldo abaixo de 10 reais: {contas_abaixo_10}")
        print(f"Saldos total sem contas com saldo abaixo de 20: {saldo_acima_20:.2f}")
    else:
        print("Consulta de saldos ignorada.")

if __name__ == "__main__":
    main()
