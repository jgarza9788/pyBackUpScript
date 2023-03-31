

import os
import json5 as jason
import subprocess as sp


# https://github.com/elesiuta/backupy
import backupy # pip install BackuPy
from backupy.backupman import BackupManager
# from backupy.config import ConfigObject

from dataMan import DataManager

from logging import Logger
from logMan import createLogger


def run_cli(data):
    #if no enable ... default to True
    if data.get("enable",True) == False:
        return "this is not enabled"

    options = " "
    if data.get("noarchive",False):
        options += "--noarchive"
        options += " "
    if data.get("noprompt",False):
        options += "--noprompt"
        options += " "
    if data.get("nolog",False):
        options += "--nolog"
        options += " "

    try:
        cmd = f'start wt -p \"pwsh\" python -m backupy.cli \"{data["source"]}\" \"{data["dest"]}\" {options}'
        # print(cmd)
        os.system(cmd)
        return cmd
    except Exception as e:
        return str(e)


def main():
    dir = os.path.dirname(os.path.realpath(__file__))
    logger = createLogger(root=os.path.join(dir,'log'),useStreamHandler=False)

    dm = DataManager(file="data.json",root=dir)

    for d in dm.data:

        if d.get("enable",True) == False:
            logger.info(f'skip -> {str(d)} ')
            continue

        logger.info("START")
        logger.info(str(d))

        dfolder = d['source'].split('\\')[-1]
        d['dest'] = os.path.join(d['root_dest'],dfolder)

        if os.path.exists(d['dest']) == False:
            os.mkdir(d['dest'])

        # try:
        #     result = run_cli(d)
        #     logger.info(result)
        # except Exception as e:
        #     print(str(e))
        
        buman = BackupManager(d)
        buman.run()

        # print(*buman.log._log,sep='\n')
        for l in buman.log._log:
            logger.info(str(l))

        logger.info("END")

if __name__ == "__main__":
    main()