# Links Awakening ROM Hack toolbox

This tool is intended at the goto tool for creating custom ROMs based of Links Awakening DX.

# Supported features

This toolbox is build of the features of [LADXR](https://github.com/daid/LADXR). But expands on it to allow people to create really unique experiences.

* Any item can be placed anywhere. Chest can contain any item without limits. The base game can only put a specific list of items into the game, these patches enable all items to put anywhere.
* Ceiling keys (keys dropped in dungeons), heart pieces, heart containers, secret seashells can be replaced with any item.
* The whole map can be edited, any room including dungeon rooms can be modified.
* "Entities" (enemies, NPCs, various other things) can be placed almost anywhere. With the exception that some enemies cannot be combined in the same room due to graphics conflicts.

# Installation

LADX-Hackers-Toolbox uses [Python](https://www.python.org/) for conversion and [Tiled](https://www.mapeditor.org/)

1) Install python3.9 (or newer) from https://www.python.org/, be sure to check "Add python to environment variables" to make your life easier later.
2) Install Tiled map editor from https://www.mapeditor.org/
3) Get the latest toolbox code from https://github.com/daid/LADX-Hackers-Toolbox/archive/refs/heads/master.zip and extract it somewhere.

# Usage

LADX-Hackers-Toolbox works by the following steps:

1) Get a "Links Awakening DX 1.0 English" ROM. You will need to dump this yourself from a cartridge. Name this rom `origonal.gbc` and place it within the extracted toolbox in the `/roms/` folder.
2) Run `export.bat`, this will read all data from the origonal rom and create a data folder with a lot of files.
3) Edit the files in the `/data/` folder to modify the game how you want. See [TODO] for information on how to edit various things.
4) Run `build.bat`, this will take the data from `/data/` and create a `result.gbc` in `/roms/` with all your modifications.
