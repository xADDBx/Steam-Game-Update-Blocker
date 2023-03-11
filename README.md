# Don't update me
The project will modify Steam acf files to allow playing a Game without updating.
It will change the State flag to make Steam think the Game is already updated.

Changes StateFlags to 4.

Changes buildid to most recent one.

Iterates through all installed Depots and updates their Manifest to the most recent one.

Uses https://github.com/ValvePython/steam to get information
