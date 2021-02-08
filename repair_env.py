#!/usr/bin/env python3

# Repair virtual env in *nix systems after moving to new path.

# Since the absolute path is used for shebang in each script,
# this tool replaces the old path to new path in each script.

# Typical Usage:
# 1. Move the env to the new location
# 2. Run ./repair_env.py <PATH>

import os
import sys

def file_replace(filepath: str, old_string: str, new_string: str) -> bool:
    """
    Replace all instances of old string in file with new string
    Returns true if any updates were made, false otherwise
    """

    if old_string == new_string:
        return False

    with open(filepath, 'r') as infile:
        content = infile.read()
        if old_string not in content:
            return False
    
    with open(filepath, 'w') as outfile:
        outfile.write(content.replace(old_string, new_string))
        return True

def autodetect(envpath: str) -> str:
    """
    Autodetect the old path from shebang line of pip script
    Returns the detected path if found, null otherwise
    """
    scriptpath = os.path.join(envpath, 'bin', 'pip')

    if not os.path.isfile(scriptpath):
        return

    with open(scriptpath, 'r') as infile:
        pypath = infile.readline().strip()[2:]
        envpath = os.sep.join(pypath.split(os.sep)[:-2])
        return envpath

if __name__ == '__main__':
    stat = {
        'err': '\033[31;1m' + 'ERROR:' + '\033[0m',
        'ok': '\033[32;1m' + 'OK:' + '\033[0m',
    }

    if '--help' in sys.argv:
        print(f'Usage: ./repair_env.py <env-path>')
        exit()

    if len(sys.argv) < 2:
        print(stat['err'], 'Argument env-path missing')
        print('Use --help for usage instructions')
        exit()

    npath = sys.argv[1].rstrip('/')
    newpath = npath if npath.startswith('/') else os.path.join(os.getcwd(), npath)
    oldpath = autodetect(newpath)

    if not oldpath:
        print(stat['err'], 'cannot find pip inside bin directory')
        print('Please check if the given env path is correct')
        exit()

    if oldpath == newpath:
        print(stat['ok'], 'Already up-to-date')
        exit()

    binpath = os.path.join(newpath, 'bin')
    for filename in os.listdir(binpath):
        filepath = os.path.join(binpath, filename)
        if os.path.isfile(filepath) and not os.path.islink(filepath):
            res = file_replace(filepath, oldpath, newpath)

    print(stat['ok'], 'Updated')
