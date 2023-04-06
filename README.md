# Steam Game Update Blocker
The project will modify Steam acf files to allow playing a Game without updating. 
To be able to play the game you need to restart Steam after running the program. To prevent accidents it's best to just have Steam closed before running the program.
You need a steam Account and the AppID of the game. You can get the AppID by visiting the Steam shop page of the game. The link will look like:

https://store.steampowered.com/app/{AppID}/{GameName}/

You just need to copy the AppID.

- Changes StateFlags to 4.
- Changes buildid to most recent one (if a targetBuild exists it takes that into account).
- Iterates through all installed Depots and updates their Manifest to the most recent one.

To undo this either reinstall the game or just verify the Game Files.

This will probably cause errors when used for Online Games.

The following cases exist:

- Playing on the public branch, ignore an update and keep playing on the old public version (works)
- Playing on a non-public branch, switch to the public branch but keep playing on the non-public branch version (works)
- Playing on a non-public branch, ignore an update and keep playing on the old branch version (don't know; probably doesn't work)
- Playing on the public branch, switching to a non-public branch but keep playing on the public version (doesn't work)

The fix for the later two cases isn't hard but I have never needed those two myself so I'll do them sometime in the future.