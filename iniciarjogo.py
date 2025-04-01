import os
import requests
import threading
import uuid
import base64
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuração do proxy
proxy_url = "http://spe8t07tai:et6m+l9uqWiCaFJ2q5@br.smartproxy.com:10000"
proxies = {
    "http": proxy_url,
    "https": proxy_url
}

# Cabeçalhos base para a requisição gameUp (serão ajustados conforme plataforma)
headers_template = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-type": "application/x-www-form-urlencoded",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/134.0.0.0"
}

# Informações da API gameUp para cada plataforma
gameup_api = {
    "pttwin": {
       "url": "https://api.pttwinz9t5t.com/other_game/gameUp",
       "origin": "https://www.pttwin.com",
       "referer": "https://www.pttwin.com/"
    },
    "playpp": {
       "url": "https://api.playppttxy3.com/other_game/gameUp",
       "origin": "https://www.playpp.com",
       "referer": "https://www.playpp.com/"
    },
    "braqqq": {
       "url": "https://api.braqqq2t22t.com/other_game/gameUp",
       "origin": "https://www.braqqq.com",
       "referer": "https://www.braqqq.com/"
    }
}

# Cabeçalhos para a API de SSO login
sso_headers = {
    "accept": "application/json, text/javascript, text/plain",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://wbgame.tadagaming.com",
    "referer": "https://wbgame.tadagaming.com/",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/134.0.0.0"
}

# Função para ler o arquivo tokens.txt na pasta tokenstotal e extrair os dados
def read_tokens(filename=os.path.join("tokenstotal", "tokens.txt")):
    tokens = []
    if not os.path.exists(filename):
        print("Arquivo tokens.txt não encontrado na pasta tokenstotal.")
        return tokens
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Espera-se o formato: plataforma : token : email : senha [saldo : <valor> ...]
            parts = [p.strip() for p in line.split(":")]
            if len(parts) < 4:
                continue
            platform = parts[0].lower()
            token_val = parts[1]
            email = parts[2]
            senha = parts[3]
            saldo = 0.0
            if "saldo" in line:
                try:
                    saldo_str = line.split("saldo :")[1].split()[0]
                    saldo = float(saldo_str)
                except:
                    saldo = 0.0
            tokens.append({"platform": platform, "token": token_val, "email": email, "senha": senha, "saldo": saldo})
    return tokens

# Função para processar a API gameUp e extrair o ssoKey
def process_gameup(token_record):
    platform = token_record["platform"]
    token_val = token_record["token"]
    api_conf = gameup_api.get(platform)
    if not api_conf:
        print(f"API gameUp não definida para a plataforma {platform}")
        return None
    url = api_conf["url"]
    headers = headers_template.copy()
    headers["origin"] = api_conf["origin"]
    headers["referer"] = api_conf["referer"]
    payload = {
        "token": token_val,
        "language": "pt-pt",
        "gid": "1010",
        "sub_gid": "421",
        "direction": "1",
        "type": "101"
    }
    try:
        resp = requests.post(url, data=payload, headers=headers, proxies=proxies, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("code") == 0:
                game_url = data.get("data", {}).get("url")
                if game_url:
                    # A URL possui um parâmetro "url" que é Base64
                    parsed = urllib.parse.urlparse(game_url)
                    qs = urllib.parse.parse_qs(parsed.query)
                    if "url" in qs:
                        base64_str = qs["url"][0]
                        try:
                            decoded = base64.b64decode(base64_str).decode("utf-8")
                            # A URL decodificada possui um parâmetro "ssoKey"
                            parsed_decoded = urllib.parse.urlparse(decoded)
                            qs_decoded = urllib.parse.parse_qs(parsed_decoded.query)
                            if "ssoKey" in qs_decoded:
                                ssoKey = qs_decoded["ssoKey"][0]
                                print(f"[{platform}] ssoKey extraído: {ssoKey}")
                                return {"platform": platform, "ssoKey": ssoKey}
                        except Exception as e:
                            print(f"Erro ao decodificar Base64 para {platform}: {e}")
                            return None
            else:
                print(f"GameUp API retornou erro para {platform}: {data.get('msg')}")
                return None
        else:
            print(f"GameUp API HTTP {resp.status_code} para {platform}")
            return None
    except Exception as e:
        print(f"Exceção na chamada gameUp para {platform}: {e}")
        return None

# Função para processar a API SSO login e extrair o token final
def process_sso_login(ssoKey):
    url = f"https://wbwebapi.tadagaming.com/sso-login.api?key={ssoKey}&lang=pt-BR"
    payload = {
        "key": ssoKey,
        "lang": "pt-BR"
    }
    try:
        resp = requests.post(url, data=payload, headers=sso_headers, proxies=proxies, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            final_token = data.get("token")
            if final_token:
                print(f"SSO login token obtido para ssoKey {ssoKey}: {final_token}")
                return final_token
            else:
                print(f"SSO login não retornou token para ssoKey {ssoKey}")
                return None
        else:
            print(f"SSO API HTTP {resp.status_code} para ssoKey {ssoKey}")
            return None
    except Exception as e:
        print(f"Exceção na SSO API para ssoKey {ssoKey}: {e}")
        return None

def main():
    # Passo 1: Ler tokens.txt da pasta tokenstotal e ordenar tokens por saldo decrescente
    tokens = read_tokens()
    if not tokens:
        print("Nenhum token encontrado no arquivo tokens.txt.")
        return
    tokens.sort(key=lambda x: x.get("saldo", 0), reverse=True)
    print(f"{len(tokens)} tokens carregados (ordenados por saldo).")
    
    # Passo 2: Processar a API gameUp para extrair os ssoKey (concorrente)
    sso_keys = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(process_gameup, rec): rec for rec in tokens}
        for future in as_completed(futures):
            result = future.result()
            if result and "ssoKey" in result:
                sso_keys.append(result["ssoKey"])
    
    # Salvar as ssoKeys no arquivo ssokey.txt
    with open("ssokey.txt", "w", encoding="utf-8") as f:
        for key in sso_keys:
            f.write(key + "\n")
    print(f"Total de ssoKeys coletadas: {len(sso_keys)}")
    
    # Passo 3: Para cada ssoKey, chamar a API SSO login e coletar o token final
    sso_tokens = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(process_sso_login, key): key for key in sso_keys}
        for future in as_completed(futures):
            token_final = future.result()
            if token_final:
                sso_tokens.append(token_final)
    
    # Salvar os tokens finais no arquivo tokenlj_g_r.txt
    with open("tokenlj_g_r.txt", "w", encoding="utf-8") as f:
        for t in sso_tokens:
            f.write(t + "\n")
    print(f"Total de tokens SSO obtidos: {len(sso_tokens)}")

if __name__ == "__main__":
    main()
