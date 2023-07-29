# -*- coding: utf-8 -*-
# BudgeTeer
# Projekt von https://github.com/rix1337
# Dieses Script prüft, ob Versionsnummern und Changelog gegenüber main geändert wurden.

import json
import re
import subprocess
import sys
from distutils.version import StrictVersion
from urllib.request import urlopen

if __name__ == '__main__':
    python_version = ""
    try:
        result = subprocess.run(['python', 'budgeteer/providers/version.py'], stdout=subprocess.PIPE)
        python_version = str(result.stdout.decode("utf-8")).strip()
    except:
        pass

    if not python_version:
        sys.exit('Version info missing in budgeteer/providers/version.py')

    vue_version = ""
    try:
        with open('budgeteer/web_interface/vuejs_frontend/package.json') as fp:
            data = json.load(fp)
            vue_version = str(data['version']).strip()
    except:
        pass

    if not vue_version:
        sys.exit('Version info missing in budgeteer/web_interface/vuejs_frontend/package.json')

    if not python_version == vue_version:
        sys.exit(
            'Version info mismatch in budgeteer/providers/version.py and budgeteer/web_interface/vuejs_frontend/package.json')

    online_changelog = urlopen(
        'https://raw.githubusercontent.com/rix1337/BudgeTeer/main/.github/Changelog.md').read()
    online_changelog = online_changelog.decode("utf-8")
    with open('.github/Changelog.md', encoding='utf8') as local_changelog:
        local_changelog = local_changelog.read()
    if online_changelog == local_changelog:
        sys.exit('.github/Changelog.md not updated')

    latest = urlopen('https://github.com/rix1337/BudgeTeer/releases/latest').read()
    latest_title = latest.decode("utf-8")
    latest_title_text = re.findall(r'<title>(.+)</title>', latest_title)[0]
    onlineversion = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3})', latest_title_text).group()
    if StrictVersion(python_version) > StrictVersion(onlineversion) and StrictVersion(vue_version) > StrictVersion(
            onlineversion):
        print("Proper version increase in branch detected.")
        sys.exit(0)
    else:
        sys.exit('Version not increased on branch')
