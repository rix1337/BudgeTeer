# -*- coding: utf-8 -*-
# BudgeTeer
# Projekt von https://github.com/rix1337
# Dieses Modul startet den BudgeTeer.

import multiprocessing

from budgeteer import run

if __name__ == '__main__':
    multiprocessing.freeze_support()
    run.main()
