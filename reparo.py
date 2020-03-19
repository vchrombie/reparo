#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CHAOSS
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#     Venu Vardhan Reddy Tekula <venuvardhanreddytekula8@gmail.com>
#

import requests
import json

from string import Template

REPO = "chaoss/grimoirelab-perceval/"
PATH_TO_FILE = "perceval/backend.py"

data = requests.get("https://api.github.com/repos/" + REPO + "commits?path=" + PATH_TO_FILE)
data = json.loads(data.content)

authors_data = {}

for item in reversed(data):
    data = item['commit']['author']
    if data['name'] not in authors_data.keys():
        authors_data[data['name']] = data['email']

authors = [key + " <" + value + ">" for key, value in authors_data.items()]

# print(authors)

template_file = open("gpl-v3.tmpl")

src = Template(template_file.read())

years = "2015-2020"
owner = "Bitergia"

sub_dict = {
    'years': years,
    'owner': owner,
    'authors': '\n#     '.join(authors)
}

result = src.substitute(sub_dict)

# print(result)

with open('./backend.py', 'r') as f:
    contents = f.readlines()
    i = 0
    for item in contents:
        if item.startswith('#'):
            i += 1

with open('./backend.py', 'w') as f:
    f.writelines(contents[i:])

with open('./backend.py', 'r') as f:
    contents = f.readlines()
    contents.insert(0, result+"\n")

with open('./backend.py', 'w') as f:
    contents = "".join(contents)
    f.write(contents)
