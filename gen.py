from tasks import *
from traceback import print_exc
from colorama import Fore
import tls_client

bad = Fore.RED+'[!] '+Fore.RESET
good = Fore.GREEN+'[+] '+Fore.RESET

def genr(key : str,proxy_:str,logr:Logger,lock,service) -> None:
    session = tls_client.Session(
        client_identifier="chrome112",
        random_tls_extension_order=True
    )
    if proxy_:
        proxy = f"http://{formatProxy(proxy_)}"
    else:
        proxy = None
    captcha = solve(key,service)
    
    if not captcha.get('solved'):
        captcha_excp = captcha.get('excp')
        logr.log(f"{bad}Failed to solve captcha! Error : {captcha_excp}")
        return
    
    gcap_resp = captcha.get('gcap')
    passw = rnd_passw()
    mail = rnd_email()

    sheaders = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'connection': 'keep-alive',
    'g-recaptcha-action': 'signup',
    'g-recaptcha-token': gcap_resp,
    'origin': 'https://picsart.com',
    'platform': 'website',
    'pragma': 'no-cache',
    'referer': 'https://picsart.com/',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'token': rnd_letters(15),
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}

    sdata = {
    'password': passw,
    'email': mail,
    'consents': [],
}

    try:
        sresp = session.post('https://api.picsart.com/user-account/auth/signup', headers=sheaders, json=sdata, proxy=proxy)
    except Exception as excp:
        logr.log(f"{bad}Failed To Do Request. Error : {str(excp)}")
        return
    
    sjson : dict = sresp.json()

    sstatus = sjson.get('status')

    if sstatus == 'error':
        sfailmsg = sjson.get('message')

        if 'Bot' in sfailmsg:
            logr.log(f'{bad}Bot Behaviour Detected!')
        else:
            logr.log(f'{bad}Signup Failed! Message : {sfailmsg}')

        return
    access_token = sjson['token']['access_token']
    api_key = sjson['key']

    pheaders = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': f'Bearer {access_token}',
    'cache-control': 'no-cache',
    'connection': 'keep-alive',
    'content-type': 'application/json',
    'origin': 'https://picsart.com',
    'platform': 'website',
    'pragma': 'no-cache',
    'referer': 'https://picsart.com/',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76',
    'x-api-key': api_key,
}

    try:
        presp = session.get('https://api.picsart.com/discord/link', headers=pheaders, proxy=proxy)
    except Exception as excp:
        logr.log(f"{bad}Failed To Do Request. Error : {str(excp)}")
        return

    pjson : dict = presp.json()

    pstatus = pjson.get('status')

    if pstatus == 'success':
        plink = pjson.get('response')
        logr.log(f"{good}Successfully Generated Promo -> {mail}:{passw}")
        with lock:
            open('promos.txt','a').write(f"{plink}\n")  

    else:
        logr.log(f"{bad}Unknown Error While Claiming Promo. Response : {pjson}")

def genr_(*args):
    while True:
        try:
            genr(*args)
        except:
            print_exc()
            continue