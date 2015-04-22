#!/usr/bin/env python
#
# This file is part of lava-ci.  lava-ci is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# Copyright Tyler Baker 2015

import os
import shutil
import json


def write_file(file, name, directory):
    with open(os.path.join(directory, name), 'w') as f:
        f.write(file)


def write_json(name, directory, data):
    with open(os.path.join(directory, name), 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)


def load_json(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)


def mkdir(directory):
    if not ensure_dir(directory):
        shutil.rmtree(directory)
        os.makedirs(directory)


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    else:
        return False


def is_key(key, iterable):
    if key in iterable:
        return True
    else:
        return False