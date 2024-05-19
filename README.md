# BudgeTeer

<img src="https://raw.githubusercontent.com/rix1337/BudgeTeer/main/budgeteer/web_interface/vuejs_frontend/public/favicon.ico" data-canonical-src="https://raw.githubusercontent.com/rix1337/BudgeTeer/main/budgeteer/web_interface/vuejs_frontend/public/favicon.ico" width="64" height="64" />

Einfacher Überblick über das eigene Budget 

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/rix1337/BudgeTeer/CreateRelease.yml?branch=main)](https://github.com/rix1337/BudgeTeer/actions/workflows/CreateRelease.yml)
[![GitHub stars](https://img.shields.io/github/stars/rix1337/BudgeTeer.svg)](https://github.com/rix1337/BudgeTeer/stargazers)
[![GitHub all releases](https://img.shields.io/github/downloads/rix1337/BudgeTeer/total?label=github%20downloads)](https://github.com/rix1337/BudgeTeer/releases)

[![PyPI](https://img.shields.io/pypi/v/BudgeTeer?label=pypi%20package)](https://pypi.org/project/BudgeTeer/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/BudgeTeer?label=pypi%20downloads)](https://pypi.org/project/BudgeTeer/#files)

[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/rix1337/docker-BudgeTeer?label=docker%20image&sort=semver)](https://hub.docker.com/r/rix1337/docker-budgeteer/tags)
[![Docker Pulls](https://img.shields.io/docker/pulls/rix1337/docker-BudgeTeer)](https://hub.docker.com/r/rix1337/docker-budgeteer/)

[![GitHub license](https://img.shields.io/github/license/rix1337/BudgeTeer.svg)](https://github.com/rix1337/BudgeTeer/blob/main/LICENSE.md)
[![Python 3 Backend](https://img.shields.io/badge/backend-python%203-blue.svg)](https://github.com/rix1337/BudgeTeer/tree/main/BudgeTeer)
[![Vue.js 3 Frontend](https://img.shields.io/badge/frontend-vue.js%203-brightgreen.svg)](https://github.com/rix1337/BudgeTeer/tree/main/BudgeTeer/web_interface/vuejs_frontend)
[![GitHub last commit](https://img.shields.io/github/last-commit/rix1337/BudgeTeer)](https://github.com/rix1337/BudgeTeer/commits/main)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/rix1337/BudgeTeer)](https://github.com/rix1337/BudgeTeer/graphs/commit-activity)
[![Lines of code](https://img.shields.io/tokei/lines/github/rix1337/BudgeTeer)](https://github.com/rix1337/BudgeTeer/pulse)

[![Github Sponsorship](https://img.shields.io/badge/support-me-red.svg)](https://github.com/users/rix1337/sponsorship)
[![GitHub issues](https://img.shields.io/github/issues/rix1337/BudgeTeer.svg)](https://github.com/rix1337/BudgeTeer/issues)

***

## Installation

## Manuelle Installation

### Voraussetzungen

* [Python 3.8](https://www.python.org/downloads/) oder neuer (nur 2 [externe Abhängigkeiten](https://github.com/rix1337/BudgeTeer/blob/main/requirements.txt)!)

### Installation / Update durch [pip](https://pip.pypa.io/en/stable/installation/)

```pip install -U budgeteer```

### Lokaler Build
Benötigt [Node.js](https://nodejs.org/en/download/), [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) und [pip](https://pip.pypa.io/en/stable/installation/):

1. Frontend-Pfad aufrufen: `cd budgeteer/web_interface/vuejs_frontend`
2. Dependencies installieren: `npm ci`
3. [Vue.js 3](https://vuejs.org/) Frontend kompilieren: `npm run build`
4. Zurück in das Hauptverzeichnis wechseln: `cd ../../..`
5. BudgeTeer auf Basis der _setup.py_ installieren: `pip install .`

### Start

```budgeteer``` in der Konsole (Python muss im System-PATH hinterlegt sein)

### [Docker Image](https://hub.docker.com/r/rix1337/docker-budgeteer/)

```
docker run -d \
  --name="BudgeTeer" \
  -p port:2808 \
  -v /path/to/config/:/config:rw \
  --log-opt max-size=50m \
  rix1337/docker-budgeteer
  ```

* Der Betrieb als Docker-Container empfiehlt sich als Standardinstallation - vor allem für NAS-Systeme, Homeserver und
  sonstige Geräte die dauerhaft und möglichst wartungsfrei (headless) betrieben werden sollen.
* Bei jedem Release wird ein getaggtes Image erstellt. Damit kann man auf der Wunschversion verbleiben oder im Falle
  eines Bugs zu einer stabilen Version zurück kehren.
* Um immer auf dem aktuellen Stand zu sein, einfach das mit `latest` getaggte Image nutzen.
* Für UNRAID-Server kann das Image direkt über die Community Applications bezogen und der Container so eingerichtet
  werden.

Das Image `rix1377/docker-budgeteer` wird standardmäßig auf das `:latest`-Tag aufgelöst. Dieses wird mit jedem Release auf die neue Version aktualisiert. Mit jedem Release wird ebenfalls eine getaggte Version des Images erzeugt. Auf letztere kann man wechseln, um beispielsweise bei Fehlern in der neuen Version auf einen funktionierenden Stand zurück zu kehren.

Beispiel:

`docker pull rix1337/docker-budgeteer:0.0.2`

### Windows Build

* Jedem [Release](https://github.com/rix1337/BudgeTeer/releases) wird eine selbstständig unter Windows lauffähige
  Version des BudgeTeers beigefügt.
* Hierfür müssen weder Python, noch die Zusatzpakete installiert werden.
* Einfach die jeweilige Exe herunterladen und ausführen bzw. bei Updates die Exe ersetzen.