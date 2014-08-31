# RenPy archive unpacker 1.1
# Decompiles PRA archives from RenPy runtime.
# Compatible with games using old versions of RenPy 6.x

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

    if  hasattr(renpy,"list_files"):
        _LB_list_files = renpy.list_files
    else:
        # for RenPy before 6.11.0
        _LB_list_files = lambda: [fn for dir, fn in renpy.loader.listdirfiles() if dir != renpy.config.commondir]

    # for removing invisible "archived" folder
    renpy.loader.walkdir = (lambda f: lambda dir: f(dir) if os.path.exists(dir) else [])(renpy.loader.walkdir)

    if  hasattr(renpy,"file"):
        _LB_file = renpy.file
    else:
        # for RenPy before 6.3.0
        _LB_file = renpy.loader.load

    for fname in _LB_list_files():
        old_path = os.path.join(_LB_GAME_DIR, fname)
        new_path = os.path.join(_LB_OUTPUT_DIR, fname)
        if  not os.path.exists(old_path) and not os.path.exists(new_path):
            dirname = os.path.dirname(new_path)
            if  not os.path.exists(dirname):
                os.makedirs(dirname)
            new = open(new_path, "wb")
            orig = _LB_file(fname)
            shutil.copyfileobj(orig, new)
            orig.close()
            new.close()