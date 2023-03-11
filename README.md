# Don't update me
The project will modify Steam acf files to allow playing a Game without updating.
It will change the State flag to make Steam think the Game is already updated.

Changes StateFlags to 4.

Changes buildid to most recent one (if a targetBuild exists it takes that into account).

Iterates through all installed Depots and updates their Manifest to the most recent one.

To undo this either reinstall the game or just verify the Game Files.

This will probably cause errors when used with Online Games.