import requests
import json
import bs4
import pyfiglet
import hashlib
import re
from colorama import Fore, Style
from colorama.ansi import Back

# Version info
version_name = ' "Fine, I\'ll do it myself" Edition '
version_tag = 'v1.3'
spacer = "------------------------------------------------------------------------------ \n"

client = 'h2m-mod.exe'
output_file = "./players2/Servers.json"
favorites_file = "./players2/Favorites.json"

# Check version
def check_version():
    # Header
    header = pyfiglet.figlet_format("zom's funny server fetcher", font='chunky')
    print(Fore.GREEN + Style.BRIGHT + header + '[' + version_name + '] ' + Fore.WHITE + version_tag + "\n \n"
            + Fore.GREEN + Style.BRIGHT + "https://github.com/z6m/h2m-tool \n" + Fore.WHITE + "Download from this repo yourself, close this if someone just sent you the file \n" 
            + Fore.GREEN + Style.BRIGHT + spacer 
            + Fore.WHITE)
            
    try:
        response = requests.get("https://api.github.com/repos/z6m/h2m-tool/releases/latest")
        latest_version = response.json()["tag_name"]
        if latest_version != version_tag:
            print(Fore.RED + Style.BRIGHT + "[!] A new version is out\n"
                "[!] Download it here: " + "https://github.com/z6m/h2m-tool/releases/latest\n")
            input(Fore.WHITE + Style.BRIGHT + "[*] Press ENTER to ignore and continue...")
    except:
        print(Fore.RED + Style.BRIGHT + "[!] Rate limit exceeded, skipping update check \n")


# Check hash
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
        + "[*] It's recommended you go out and find that one before continuing\n" 
        + Fore.YELLOW + Style.BRIGHT + spacer)
    
    else:
        trust_level = "UNKNOWN"
        print("[*] " + Fore.RED + Style.BRIGHT + trust_level + Fore.WHITE + " Build \n")
        print(Fore.RED + Style.BRIGHT +"[!] You are using an unknown binary that was modified after the leak by an untrusted third party \n[!] Nothing about its safety can be assured and continuing is potentially dangerous \n"
        + Fore.WHITE + Style.BRIGHT + "[*] The final official binary was 9a961df9be3826b2c77e46193454af385add6adb581d4848f7319b2da9a3e33e \n \n"
        + "[*] For your security, it's recommended you go out and find that one before continuing \n"
        + Fore.RED + Style.BRIGHT + spacer 
        + Fore.YELLOW + "[!] These modified builds tend to be made with a server browser built into them, if you have one that YOU trust, you have no need to be using this tool anyway" + Fore.RED + Style.BRIGHT)
        input("It is strongly advised you close this window and find a clean version, press Enter to ignore this warning and continue...")
        input("Are you SURE?")
        print("Alright, I'm not your dad, if anything happens it's on you \n" + spacer + Fore.WHITE)

    print(Fore.WHITE + "[!] Reminder, there is no h2m-launcher.msi or other installable files required client-side other than the game itself\n"
            + "[!] If you installed anything like that, your build being safe doesn't matter\n")

# Fetch servers
def fetch_servers():
        print("[*] Fetching servers...")
        url = "https://master.iw4.zip/servers"
        
        scraped_page = requests.get(url, timeout=10)
        soup = bs4.BeautifulSoup(scraped_page.text, "lxml")
        h2m_servers = soup.find('div', {'class': 'game-server-panel d-none', 'id': 'H2M_servers'})
        server_rows = h2m_servers.find_all('tr', {'class': 'server-row'})
        
        servers = []
        for s in server_rows:
            ip = s.get('data-ip')
            port = s.get('data-port')
            name = s.find('td', {'class': 'server-hostname text-break'})
            name = name.get('data-hostname')
            gamemode = s.find('td', {'class': 'server-gametype text-break'})
            gamemode = gamemode.get('data-gametype').upper()
            map = s.find('td', {'class': 'server-map text-break'})
            map = map.get('data-map')
            clientnum = s.find('td', {'class': 'server-clientnum'})
            players = int(clientnum.get('data-clientnum'))
            maxplayers = int(clientnum.get('data-maxclientnum'))
            region_map = {
                "US": "NA",
                "USA": "NA",
                "NA": "NA",
                "UK": "EU",
                "SCOTLAND": "EU",
                "ITA": "EU",
                "EU": "EU",
                "AUS": "OCE",
                "AU": "OCE",
                "NZ": "OCE",
                "OCE": "OCE",
                "BR": "LAT",
                "MEX": "LAT",
                "LATAM": "LAT",
                "JPN": "SEA",
                "SEA": "SEA"  
            }
            region = ""
            for key in region_map:
                # Create a regex pattern to match the key as a whole word
                pattern = r'\b' + re.escape(key) + r'\b'
                if re.search(pattern, name):
                    region = region_map[key]
                    break
                
            category = "Regular"
            category_map = {
                "custom": "Custom",
                "menu": "Custom",
                "scripts": "Custom",
                "trickshotting": "Trickshotting", 
                "trickshot": "Trickshotting",
                "trickshots": "Trickshotting",
                "sniping": "Sniping",
                "sniper": "Sniping",
                "snipers": "Sniping",
                "x2 xp": "Double XP",
                "2xp": "Double XP",
                "double xp": "Double XP",
                "xp": "Double XP",
                "doublexp": "Double XP"
            }
            for key in category_map:
                if key in name.lower():
                    category = category_map[key]
                    break
            
            if ip and ip not in ("127.0.0.1", "localhost") and not ip.startswith("192.168"):
                servers.append({
                    'ip': f"{ip}:{port}",
                    'port': port,
                    'name': name,
                    'gamemode': gamemode,
                    'map': map,
                    'category': category,
                    'region': region,
                    'players': players,
                    'maxplayers': maxplayers
                })
            

        favorites_list = json.dumps(servers, indent=4)
        with open(output_file,"w+") as file:
            file.write(favorites_list)
            
        print(Fore.GREEN + "[*] Servers fetched \n" + Fore.WHITE)
        return