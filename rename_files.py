import os
for dirpath, dirs, files in os.walk('/mnt/storage/Linux/Morrowind Archive/Mods/final'):
    for filename in files:
        if '_nm' in filename:
            print(filename)
            os.rename(
                os.path.join(dirpath, filename),
                os.path.join(dirpath, filename.replace('_nm.dds', '_n.dds'))
            )
        if '_NM' in filename:
            print(filename)
            os.rename(
                os.path.join(dirpath, filename),
                os.path.join(dirpath, filename.replace('_NM.dds', '_n.dds'))
            )
        if '_NM_n' in filename:
            print(filename)
            os.rename(
                os.path.join(dirpath, filename),
                os.path.join(dirpath, filename.replace('_NM_n.dds', '_n.dds'))
            )
