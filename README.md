# Dolly Trailers for ETS2

This project generates a drawbar configuration (dolly and trailer) for all of Euro Truck Simulator 2's basegames trailers. It is intended to be used with [Devil BDF Tandem Truck Pack](https://steamcommunity.com/sharedfiles/filedetails/?id=620915774&searchtext=bdf), but may or may not work with other rigid truck mods.

## Why use this mod

The open trailers in Devils BDF mod doesn't show any visible cargo, which I find very annoying. Since this mod uses the basegames trailer bodies, but only add a dolly as a sub-body, the cargo configurations still works. This means that every cargo that's in the game, as well as modded cargoes that's visible on the basegames trailer, will be visible.

## How to generate the mod from this repository

Run _generate_trailer_configs.py_ with the path to the extracted game archive (where folders such as _def_, _vehicle_ and _automat_ are) and the options for what to generate (`--trailer_owned` and `trailer_defs`).

```bash
python generate_trailer_configs.py "<path/to/game/archive>" --trailer_owned --trailer_defs
```

Then, run the [SCS packer](https://modding.scssoft.com/wiki/Documentation/Tools/Game_Archive_Packer).

```bash
<path/to/scs_packer.exe> create dolly_trailer.scs -root <this_repo>/mod/base
```

and copy _dolly_trailer.scs_ into the game's modfolder.
