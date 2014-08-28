# RenPy archive unpacker 1.0
# Decompiles PRA archives from RenPy runtime.

# =============
# HOW TO USE IT
# =============
# 1. Put this file to your /game/ dir.
# 2. Run the game.
# 3. See /unpacked/ dir.

init 65535 python:
    import os
    import shutil
    
    _LB_GAME_DIR = os.path.join(config.basedir, "game")
    _LB_OUTPUT_DIR = os.path.join(config.basedir, "unpacked", "game")

    for fname in renpy.list_files():
        old_path = os.path.join(_LB_GAME_DIR, fname)
        new_path = os.path.join(_LB_OUTPUT_DIR, fname)
        if  not os.path.exists(old_path) and not os.path.exists(new_path):
            dirname = os.path.dirname(new_path)
            if  not os.path.exists(dirname):
                os.makedirs(dirname)
            with open(new_path, "wb") as new:
                orig = renpy.file(fname)
                shutil.copyfileobj(orig, new)
                orig.close()
