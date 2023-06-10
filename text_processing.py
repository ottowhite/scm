import subprocess
import os

def printLine():
    columns = os.getenv('COLUMNS', subprocess.check_output(['tput', 'cols']).decode().strip())
    print(' ' * int(columns))

def getRepoNameFromGitUrl(repoHttpUrl):
    return os.path.splitext(os.path.basename(repoHttpUrl))[0]

def getConfigDirectoryCsvPathFromRepoName(repoName):
    return os.path.join(repoName, 'config_directory.csv')
