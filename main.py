import os
import colorama
from colorama import Fore, Style
from colorama.ansi import Back
import subprocess
from h2mgui import gui
import h2mfunctions as h2m
import threading


if __name__ == '__main__':
    colorama.init()
    def run():
        if os.path.isfile(h2m.client) == False:
            input(Fore.RED + Style.BRIGHT + "[!] Move me into your game folder next to your h2m-mod.exe")
        else:
            if not os.path.exists("./players2"):
                os.makedirs("./players2")
            if not os.path.exists(h2m.favorites_file):
                open(h2m.favorites_file, 'w').close()
            h2m.check_version()
            h2m.check_hash()
            print(Fore.GREEN + h2m.spacer + "\n"
            + Fore.WHITE)
            print("[*] Launching H2M...")
            print("[*] Launching server browser...\n")
            
            def run_subprocess():
                subprocess.run([h2m.client])
            subprocess_thread = threading.Thread(target=run_subprocess)
            subprocess_thread.start()
            
            h2m.fetch_servers()
            server_browser = gui()
            server_browser.mainloop()

    run()
