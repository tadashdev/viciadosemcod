import os
import requests
import threading
import uuid

# proxyzin
proxy_url = "http://spsqykt77n:o4x7Olsbo=D5Tu0Qjn@br.smartproxy.com:10000"
proxies = {
    "http": proxy_url,
    "https": proxy_url
}

# Cabeçalhos de reqeust de cada plata nessa bct
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

# essa def vai monitorar a porra da req de cada palta
def build_payload(platform, email, password):
    # Gerando um device id único
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

# Função que realiza a requisição de login e extrai o token
def process_login(platform, email, password):
    payload = build_payload(platform, email, password)
    if not payload:
        print(f"Plataforma {platform} não suportada.")
        return None
    info = api_info.get(platform.lower())
    if not info:
        print(f"Informações API para {platform} não encontradas.")
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
                print(f"{platform} - Falha no login para {email}: {data.get('msg')}")
                return None
        else:
            print(f"{platform} - Erro HTTP para {email}: {response.status_code}")
            return None
    except Exception as e:
        print(f"{platform} - Exceção para {email}: {e}")
        return None

# bct de funcao paia pra armazenar
results = []
results_lock = threading.Lock()

# se n saber oq faz e burro tmnc 
def process_group(platform, credentials):
    for email, password in credentials:
        token = process_login(platform, email, password)
        if token:
            with results_lock:
                results.append((platform, token, email, password))

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
            print(f"Linha inválida: {linha}")
            continue
        plataforma = partes[0].strip().lower()
        email = partes[1].strip()
        senha = partes[2].strip()
        if plataforma in grupos:
            grupos[plataforma].append((email, senha))
        else:
            print(f"Plataforma desconhecida: {plataforma}")

    threads = []
    for plat, creds in grupos.items():
        if creds:
            t = threading.Thread(target=process_group, args=(plat, creds))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

    # Organiza os tokens na ordem: braqqq, playpp, pttwin
    ordenados = []
    for plat in ["braqqq", "playpp", "pttwin"]:
        ordenados.extend([r for r in results if r[0].lower() == plat])

    # Cria a pasta tokenstotal se não existir e grava os tokens no arquivo tokens.txt
    tokens_dir = "tokenstotal"
    if not os.path.exists(tokens_dir):
        os.makedirs(tokens_dir)
    tokens_file = os.path.join(tokens_dir, "tokens.txt")
    with open(tokens_file, "w", encoding="utf-8") as f:
        for plataforma, token, email, senha in ordenados:
            f.write(f"{plataforma} : {token} : {email} : {senha}\n")

    print("Processamento concluído. Tokens salvos em", tokens_file)

if __name__ == "__main__":
    main()
