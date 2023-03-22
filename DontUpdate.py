import steam.client
from steam.client.cdn import CDNClient
import acf
from findSteam import findSteam
import os
from gevent import timeout


steamdir = findSteam()
print("Found Steam in: " + steamdir)
mySteam = steam.client.SteamClient()
mySteam.anonymous_login()

appID = input("Enter AppID of Game: ").strip()
myCDN = CDNClient(mySteam)

repeat = True

while repeat:
    try:
        repeat = False
        response = myCDN.get_app_depot_info(app_id=int(appID))
        if response is None:
            repeat = True
    except timeout.Timeout:
        repeat = True

with open(os.path.join(steamdir, f"appmanifest_{appID}.acf"), "r") as inp:
    file = acf.load(inp)

print(f"Modyfing for Game: {file['AppState']['name']}")

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

# TODO: Seems broken for other branches?
# To reproduce: Change to a Beta. Close Steam. -> Trying to apply program will not work?.
# Other direction works (If you are on a beta build, switching to the public build and then using the program
# Allows staying on beta files
print(f"Target Branch: {targetBranch}")

targetBranchBuildID = response['branches'][targetBranch]['buildid']
file["AppState"]["buildid"] = targetBranchBuildID
if file["AppState"].get("TargetBuildID") is not None:
    file["AppState"]["TargetBuildID"] = targetBranchBuildID


with open(os.path.join(steamdir, f"appmanifest_{appID}.acf"), "w") as out:
    acf.dump(file, out)
