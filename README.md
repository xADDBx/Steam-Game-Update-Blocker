# Don't update me
The project will modify Steam acf files to allow playing a Game without updating.
You need a steam Account and the AppID of the game. You can get the AppID by visiting the Steam shop page of the game. The link will look like:

https://store.steampowered.com/app/{AppID}/{GameName}/

You just need to copy the AppID.

- Changes StateFlags to 4.
- Changes buildid to most recent one (if a targetBuild exists it takes that into account).
- Iterates through all installed Depots and updates their Manifest to the most recent one.

To undo this either reinstall the game or just verify the Game Files.

This will probably cause errors when used for Online Games.
