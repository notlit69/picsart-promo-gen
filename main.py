from gen import genr_
from colorama import Fore,init
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from tasks import Logger

import json,random

lock = Lock()

def main():
    config = json.load(open('config.json'))
    key = config.get('captcha_key')
    thread_count = config.get('threads')
    service = config.get('service')

    with open('proxies.txt', "r") as f:
        _proxy= f.readlines()

    logr = Logger(lock)

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for _ in range(thread_count-1):executor.submit(genr_,key,random.choice(_proxy) if not _proxy==[] else None,logr,lock,service)

if __name__=="__main__":
    init(autoreset=True)
    main()