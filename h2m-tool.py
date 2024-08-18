import os
import requests
import json
import bs4
import pyfiglet
import colorama
from colorama import Fore, Style
from colorama.ansi import Back
import subprocess
import hashlib

if __name__ == '__main__':
    colorama.init()

    # Version info
    version_name = "good enough edition"
    version_tag = 'v1.0'
    spacer = "------------------------------------------------------------------------------ \n"

    client = 'h2m-mod.exe'

    def check_version():
        # Header
        header = pyfiglet.figlet_format("zom's funny server fetcher", font='chunky')
        print(Fore.GREEN + Style.BRIGHT + header + '[' + version_name + '] ' + Fore.WHITE + version_tag + "\n \n"
                + Fore.GREEN + Style.BRIGHT + "https://github.com/z6m/h2m-tool \n" + Fore.WHITE + "Download from this repo yourself, close this if someone just sent you the file \n" 
                + Fore.GREEN + Style.BRIGHT + spacer + Fore.WHITE)
                
        try:
            response = requests.get("https://api.github.com/repos/z6m/h2m-tool/releases/latest")
            latest_version = response.json()["tag_name"]
            if latest_version != version_tag:
                print(Fore.RED + Style.BRIGHT + "[!] A new version is out\n"
                    "[!] Download it here: " + "https://github.com/z6m/h2m-tool/releases/latest\n")
                input("[*] Press ENTER to ignore and continue...")
        except:
            print(Fore.RED + Style.BRIGHT + "[!] Rate limit exceeded, skipping update check \n")

    

    def check_hash():
        # Clean Build: 9a961df9be3826b2c77e46193454af385add6adb581d4848f7319b2da9a3e33e
        # Old Leaked Build: 9dcfda29748e29e806119cb17847bb3617c188b402ed743bd16e770401f9e127
        sha256_hash = hashlib.sha256()
        with open(client,"rb") as f:
            for byte_block in iter(lambda: f.read(4096),b""):
                sha256_hash.update(byte_block)

        print(Fore.WHITE + "[*] Build Hash [SHA256]: " + sha256_hash.hexdigest())
        if sha256_hash.hexdigest() == "9a961df9be3826b2c77e46193454af385add6adb581d4848f7319b2da9a3e33e":
            trust_level = "SAFE"
            print("[*] " + Fore.GREEN + Style.BRIGHT + trust_level + Fore.WHITE + " Build\n")
            print(Fore.GREEN + Style.BRIGHT + "[*] You are on the final early access binary of h2m that was produced before the team disbanded")
        
        elif sha256_hash.hexdigest() == "9dcfda29748e29e806119cb17847bb3617c188b402ed743bd16e770401f9e127": 
            trust_level =  "OLDER"
            print("[*] " + Fore.YELLOW + Style.BRIGHT + trust_level + Fore.WHITE + " Build \n")
            print(Fore.YELLOW + Style.BRIGHT + "[!] You are on a known older leak from the early access before the final build went out \n[!] May not be malicious, but you may be missing certain features \n"
            + Fore.WHITE + "[*] The last official binary was [9a961df9be3826b2c77e46193454af385add6adb581d4848f7319b2da9a3e33e] \n \n"
            + "[*] It's recommended you go out and find that one before continuing\n" + Fore.YELLOW + Style.BRIGHT + spacer)
            input("Press Enter to ignore this warning and continue, otherwise close this launcher and come back...")
            print (spacer + Fore.WHITE)
        
        else:
            trust_level = "UNKNOWN"
            print("[*] " + Fore.RED + Style.BRIGHT + trust_level + Fore.WHITE + " Build \n")
            print(Fore.RED + Style.BRIGHT +"[!] You are using an unknown binary that was modified after the leak by an untrusted third party \n[!] Nothing about its safety can be assured and continuing is potentially dangerous \n"
            + Fore.WHITE + Style.BRIGHT + "[*] The final official binary was 9a961df9be3826b2c77e46193454af385add6adb581d4848f7319b2da9a3e33e \n \n"
            + "[*] For your security, it's recommended you go out and find that one before continuing \n"
            + Fore.RED + Style.BRIGHT + spacer)
            input("It is strongly advised you close this window and find a clean version, press Enter to ignore this warning and continue...")
            input("Are you SURE?")
            print("Alright, I'm not your dad, if anything happens it's on you \n" + spacer + Fore.WHITE)

        print(Fore.WHITE + "[!] Reminder, there is no required h2m-launcher.msi or other files that require an install other than the game itself\n"
                + "[!] If you installed anything like that, your build being safe doesn't matter and you are still at risk\n")

        return 
    
    def fetch_servers():
        print("[*] Fetching servers...")

        output_file = "./players2/favorites.json"
        url = "https://master.iw4.zip/servers"
        
        try:
            scraped_page = requests.get(url, timeout=10)
            soup = bs4.BeautifulSoup(scraped_page.text, "lxml")
            h2m_servers = soup.find('div', {'class': 'game-server-panel d-none', 'id': 'H2M_servers'})
            server_rows = h2m_servers.find_all('tr', {'class': 'server-row'})
            
            servers = []
            for s in server_rows:
                server = (f"{s.get('data-ip')}:{s.get('data-port')}")
                servers.append(server)

            server_list = list(set(servers))
            favorites_list = json.dumps(server_list)
            with open(output_file,"w") as file:
                file.write(favorites_list)
            
            print(Fore.GREEN + "[*] Servers updated \n" + Fore.WHITE)

        except:
            print(Fore.RED + Style.BRIGHT +"[!] Error Fetching servers, skipping... \n" + spacer + Fore.WHITE)

        return
        
    # Run
    def run():
        check_version()
        if os.path.isfile(client) == False:
            input(Fore.RED + Style.BRIGHT + "[!] Move me into your game folder next to your h2m-mod.exe")
        else:
            check_hash()
            fetch_servers()
            print("[*] Launching H2M...")
            subprocess.run([client])
        return 

    run()
