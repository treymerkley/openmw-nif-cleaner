# OpenMW NIF Cleaner
OpenMW NIF Cleaner edits mods made for the original engine to remove the shiny texture problem and re-implement *most* normal maps by fixing their naming convention.

ONC is in **alpha**. There are missing and broken features to be added. 

## Install
ONC depends on:

+ Python 3.7
+ Pyffi version 2.2.2. Note that higher versions are incompatible with NIF files used for Morrowind, but 2.2.2 is perfectly stable. If you need newer versions of Pyffi for editing meshes in new Bethesda games, you should be able to set this up in a venv.
+ (Optional) PySide2 >= 5.13.0-2

## Running
You can run this on any directory to get clean NIFs at the end. However, it's important to know that this can break some mods. Better clothes, for instance, breaks from using this. To mitigate that, use `ori` in the console to find where a broken mod comes from and re-add it to your mod directory.

Once you have these installed, simply clone the files and run either the console version or the Qt version for a GUI.
