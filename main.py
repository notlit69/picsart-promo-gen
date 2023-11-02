from gen import genr_
from colorama import Fore,init
from tasks import load_config
from concurrent.futures import ThreadPoolExecutor

qs = Fore.BLUE+'[?] '+Fore.RESET

def main():
    config = load_config()
    key = config.get('capsolver_key')
    thread_count = config.get('threads')

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for _ in range(thread_count-1):executor.submit(genr_,key)

if __name__=="__main__":
    init(autoreset=True)
    main()