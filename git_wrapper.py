import os
import subprocess

def pullOrCloneConfigRepo(repoFileName, repoHttpUrl):
    if os.path.isdir(repoFileName):
        pullConfigRepo(repoFileName, repoHttpUrl)
    else:
        cloneConfigRepo(repoHttpUrl)

def pullConfigRepo(repoFileName, repoHttpUrl):
    os.chdir(repoFileName)
    print('Pulling config file changes from:', repoHttpUrl)
    subprocess.call(['git', 'pull'])
    os.chdir('..')

def cloneConfigRepo(repoHttpUrl):
    print('Cloning repository at:', repoHttpUrl)
    subprocess.call(['git', 'clone', repoHttpUrl])
