
import capsolver,random,string,tls_client,json

def solve(clientkey:str) -> dict:
    capsolver.api_key = clientkey
    try:
        soln = capsolver.solve({
    "type": "ReCaptchaV3M1TaskProxyLess",
    "websiteURL": "https://picsart.com",
    "websiteKey": "6LdM2s8cAAAAAN7jqVXAqWdDlQ3Qca88ke3xdtpR",
    "pageAction" : 'signup',
    "timeout" : 10
})
    except Exception as excp:
        return {
            "solved" : False,
            "excp" : str(excp)
        }
    return {
        "solved" : True,
        "gcap" : soln.get('gRecaptchaResponse')
    }

def rnd_letters(len : int) -> str:
    return ''.join(random.choices(string.ascii_letters,k=len))

def rnd_digits(len : int) -> str:
    return ''.join(random.choices(string.digits,k=len))

def rnd_email() -> str:
    domains = ['gmail.com','outlook.com','outlook.fr','hotmail.com']

    return rnd_letters(random.randint(10,20)) + rnd_digits(3) + '@' + random.choice(domains)

def rnd_passw() -> str:
    return rnd_letters(8) + rnd_digits(5)

def session_() -> tls_client.Session:
    return tls_client.Session(
        client_identifier="chrome112",
        random_tls_extension_order=True
    )

# https://github.com/Switch3301/Xbox-Bins-Gen/blob/main/main.py#L106
def GetProxy() -> str:
    with open('proxies.txt', "r") as f:
        proxy =  random.choice(f.readlines()).strip()
    if '@' in proxy:
        return proxy
    elif len(proxy.split(':')) == 2:
        return proxy
    else:
        if '.' in proxy.split(':')[0]:
            return ':'.join(proxy.split(':')[2:]) + '@' + ':'.join(proxy.split(':')[:2])
        else:
            return ':'.join(proxy.split(':')[:2]) + '@' + ':'.join(proxy.split(':')[2:])    

def load_config() -> dict:
    return json.load(open('config.json'))

