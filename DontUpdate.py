import steam.client
from steam.client.cdn import CDNClient
import acf
from findSteam import findSteam
import os
from gevent import timeout
from requests import ConnectionError


steamdir = findSteam()
mySteam = steam.client.SteamClient()
username = input("Enter Username: ")
password = input("Enter Password: ")
appID = input("Enter AppID of Game: ").strip()

tries = 0
retry = True

while retry:
    try:
        retry = False
        res = mySteam.login(username=username, password=password)
    except ConnectionError:
        print("Connection error! Retrying...")
        tries += 1
        if tries < 5:
            retry = True
        else:
            print("Couldn't build a connection. Aborting...")
            quit()

if res == steam.client.EResult.InvalidPassword:
    print("Invalid password or too many login attempts!")
    quit()


@mySteam.on(mySteam.EVENT_AUTH_CODE_REQUIRED)
def auth_code_prompt(is_2fa, _):
    if is_2fa:
        code = input("Enter 2FA (Stema Guard) Code: ")
        if mySteam.login(username, password, two_factor_code=code) == steam.client.EResult.OK:
            print("Login successful")
    else:
        code = input("Enter Email Code: ")
        if mySteam.login(username, password, two_factor_code=code) == steam.client.EResult.OK:
            print("Login successful")


myCDN = CDNClient(mySteam)
repeat = True
while repeat:
    try:
        repeat = False
        response = myCDN.get_app_depot_info(app_id=int(appID))
    except timeout.Timeout:
        repeat = True

with open(os.path.join(steamdir, f"appmanifest_{appID}.acf"), "r") as inp:
    file = acf.load(inp)

print(f"Modyfing {file['AppState']['name']}")

file["AppState"]["StateFlags"] = 4
for depot in file["AppState"]["InstalledDepots"].keys():
    file["AppState"]["InstalledDepots"][depot]["manifest"] = response[depot]['manifests']['public']

targetBranch = 'public'
if file["AppState"].get("TargetBuildID") is not None:
    targetBuildID = file["AppState"].get("TargetBuildID")
    for branch in response['branches'].keys():
        if response['branches'][branch]['buildid'] == targetBuildID:
            targetBranch = branch
            break

targetBranchBuildID = response['branches'][targetBranch]['buildid']
file["AppState"]["buildid"] = targetBranchBuildID
if file["AppState"].get("TargetBuildID") is not None:
    file["AppState"]["TargetBuildID"] = targetBranchBuildID


with open(os.path.join(steamdir, f"appmanifest_{appID}.acf"), "w") as out:
    acf.dump(file, out)
