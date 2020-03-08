import requests
import json

from string import Template

REPO = "chaoss/grimoirelab-perceval/"
PATH_TO_FILE = "perceval/backend.py"

data = requests.get("https://api.github.com/repos/" + REPO + "commits?path=" + PATH_TO_FILE)
data = json.loads(data.content)

authors_data = {}

for item in data:
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
