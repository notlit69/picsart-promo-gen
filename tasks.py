
import random,string,httpx,time

def solve(clientkey:str,service:str) -> dict:
    
    if 'capsolver' in service:
        # Uses httpx to get results from capsolver instead of the capmonster lib idk why but this works really better and really less bot errors
        resp = httpx.post('https://api.capsolver.com/createTask',json={
    "clientKey": clientkey,
    "task": {
        "type": "ReCaptchaV3TaskProxyLess",
        "websiteURL": "https://picsart.com",
        "websiteKey": "6LdM2s8cAAAAAN7jqVXAqWdDlQ3Qca88ke3xdtpR",
        "pageAction": "signup",
        }
    }).json()

        taskId = resp.get('taskId')
        if not taskId:
            return {
            "solved" : False,
            "excp" : f"{resp.get('errorCode')} : {resp.get('errorDescription')}"
        }
        for j in range(30):

            getTask = httpx.post('https://api.capsolver.com/getTaskResult',json={
    "clientKey": clientkey,
    "taskId": taskId
}).json()

            getTaskStatus = getTask.get('status')
            if getTaskStatus == 'ready':
            
                return {
                "solved" : True,
                "gcap" : getTask.get('solution').get("gRecaptchaResponse")
            }
            time.sleep(2)
        else:
            return {
            "solved" : False,
            "excp" : "Captcha Timeout!"
        }
    elif 'capmonster' in service:
        resp = httpx.post('https://api.capmonster.cloud/createTask',json={
    "clientKey":clientkey,
    "task":
    {
        "type":"RecaptchaV3TaskProxyless",
        "websiteURL":"https://picsart.com",
        "websiteKey":"6LdM2s8cAAAAAN7jqVXAqWdDlQ3Qca88ke3xdtpR",
        "pageAction": "signup"
    }
}).json()
        taskId = resp.get('taskId')
        if not taskId:
            return {
            "solved" : False,
            "excp" : resp.get('errorCode')
        }
        for j in range(30):
            getTask = httpx.post('https://api.capmonster.cloud/getTaskResult',json={
    "clientKey":clientkey,
    "taskId": taskId
}).json()
            if getTask.get('errorCode'):
                return {
                    "solved" : False,
                    "excp" : resp.get('errorCode')
                }
                
            getTaskStatus = getTask.get('status')
            if getTaskStatus == 'ready':
                return {
                "solved" : True,
                "gcap" : getTask.get('solution').get("gRecaptchaResponse")
            }
            time.sleep(2)
        else:
            return {
            "solved" : False,
            "excp" : "Captcha Timeout!"
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

def formatProxy(proxy) -> str:
    if '@' in proxy:
        return proxy
    elif len(proxy.split(':')) == 2:
        return proxy
    else:
        if '.' in proxy.split(':')[0]:
            return ':'.join(proxy.split(':')[2:]) + '@' + ':'.join(proxy.split(':')[:2])
        else:
            return ':'.join(proxy.split(':')[:2]) + '@' + ':'.join(proxy.split(':')[2:])    

class Logger:
    def __init__(self,lock) -> None:
        self.lock = lock

    def log(self,msg:str):
        with self.lock:
            print(msg)
