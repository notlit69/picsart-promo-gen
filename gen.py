from tasks import *
from traceback import print_exc
from colorama import Fore

bad = Fore.RED+'[!] '+Fore.RESET
good = Fore.GREEN+'[+] '+Fore.RESET

def genr(key : str) -> None:
    
    session = session_()
    try:
        proxy = f"http://{GetProxy()}"
    except:
        proxy = None

    captcha = solve(key)
    
    if not captcha.get('solved'):
        captcha_excp = captcha.get('excp')
        print(f"{bad}Failed to solve captcha! Error : {captcha_excp}")
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
        print(f"{bad}Failed To Do Request. Error : {str(excp)}")
        return
    
    sjson : dict = sresp.json()

    sstatus = sjson.get('status')

    if sstatus == 'error':
        sfailmsg = sjson.get('message')

        if 'Bot' in sfailmsg:
            print(f'{bad}Bot Behaviour Detected!')
        else:
            print(f'{bad}Signup Failed! Message : {sfailmsg}')

        return
    
    access_token = sjson['token']['access_token']

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
    'x-api-key': '796e3b99-9bc0-4ec2-8a74-e7eaf0fbfa68',
}

    try:
        presp = session.get('https://api.picsart.com/discord/link', headers=pheaders, proxy=proxy)
    except Exception as excp:
        print(f"{bad}Failed To Do Request. Error : {str(excp)}")
        return

    pjson : dict = presp.json()

    pstatus = pjson.get('status')

    if pstatus == 'success':
        plink = pjson.get('response')
        print(f"{good}Successfully Generated Promo -> {mail}:{passw}")
        with open('promos.txt','a') as fl:
            fl.write(f"{plink}\n")   

    else:
        print(f"{bad}Unknown Error While Claiming Promo. Response : {pjson}")

def genr_(key:str):
    while True:
        try:
            genr(key)
        except:
            print_exc()
            continue