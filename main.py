import sys
import requests
import json
import time

print("Getting wordlist...")
badwordlist = requests.get("https://raw.githubusercontent.com/dariusk/corpora/master/data/words/common.json").json()["commonWords"]
print("Starting...")
print("\n\n\n")
print("   ____   _____   _   _     ByzantineProcess'   _____ _               _             ")
print("  / __ \ / ____| | \ | |                       / ____| |             | |            ")
print(" | |  | | |  __  |  \| | __ _ _ __ ___   ___  | |    | |__   ___  ___| | _____ _ __ ")
print(" | |  | | | |_ | | . ` |/ _` | '_ ` _ \ / _ \ | |    | '_ \ / _ \/ __| |/ / _ \ '__|")
print(" | |__| | |__| | | |\  | (_| | | | | | |  __/ | |____| | | |  __/ (__|   <  __/ |   ")
print("  \____/ \_____| |_| \_|\__,_|_| |_| |_|\___|  \_____|_| |_|\___|\___|_|\_\___|_| ")
print("\nloading...\n\n")

wordlist = []

for x in badwordlist:
    if x.__len__() > 2:
        wordlist.append(x)
 

wordlist.sort()

print("What kind of test should I perform?")
print("1. Basic ")
print("2. Advanced (shows names that will be available soon)")

availNames = []

def printAvailableNames():
    print("\n\n\n")
    print("Available names:")
    for x in availNames:
        print(x)


def runservicebasic(service:bool, ask:str):
    if ask == "1":
        for x in wordlist:
            try:
                sys.stdout.write("Attempting " + x + "...")
                res = json.loads(requests.get("https://playerdb.co/api/player/minecraft/" + x).text)
                if res["code"] == "minecraft.api_failure":
                    sys.stdout.write("\nFound username! " + x)
                    availNames.append(x)
                elif res["code"] == "player.found":
                    sys.stdout.write("  failed.\n")
                    pass
                else:
                    pass
            except KeyboardInterrupt:
                exit()
            time.sleep(0.2)
        printAvailableNames()
    if ask == "2":
        for x in wordlist:
            sys.stdout.write("Attempting " + x + "...")
            res = json.loads(requests.get("http://api.minetools.eu/uuid/" + x).text)
            if res["status"] == "ERR":
                sys.stdout.write("\nFound username! " + x)
                availNames.append(x)
            elif res["status"] == "OK":
                sys.stdout.write("  failed.\n")
                pass
            else:
                pass
        printAvailableNames()
    if ask == "3":
        count = int(0)
        postBuf = []
        nameList = []
        for x in wordlist:
            rn = time.time()
            if count == 10:
                for z in postBuf:
                    sys.stdout.write("Attempting " + z + "...\n")
                badres = requests.post("https://api.mojang.com/profiles/minecraft", json=postBuf, headers={"Content-Type": "application/json"})
                res = json.loads(badres.text)
                for y in res:
                    nameList.append(y)
                for a in postBuf:
                    if nameList.count(a) != 0:
                        sys.stdout.write("\nFound username! " + y["name"])
                        availNames.append(str(y["name"]))
                postBuf = []
                count = 0
                time.sleep(0.7)
            else:
                postBuf.append(x)
                count += 1
        printAvailableNames()



def askservicebasic(type:bool):
    print("\n\nWhich service should I use?")
    print("[1] PlayerDB (will show names that are available later)")
    print("[2] MineTools (will !NOT! show names that are available later, also kinda slow)")
    print("[3] Mojang (will show names that are available later, fastest despite deing ratelimited)")
    ask = input("\n[1/2/3]: ")
    runservicebasic(type, ask)

if __name__ == "__main__":
    def run():
        ask = input("[1/2]: ")
        if ask == "1":
            askservicebasic(False)
        elif ask == "2":
            print("currently indev lol")
            run()
        else:
            print("Invalid input")
            exit()
    run()
