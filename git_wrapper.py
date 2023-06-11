import os
import subprocess

def pullOrCloneRepo(repoFileName, repoHttpUrl):
    if os.path.isdir(repoFileName):
        print("1) Repo already exists, pulling")
        pullConfigRepo(repoFileName, repoHttpUrl)
    else:
        print("1) Repo doesn\'t exist, cloning")
        cloneConfigRepo(repoHttpUrl)

def pullConfigRepo(repoFileName, repoHttpUrl):
    os.chdir(repoFileName)
    print(f"\t{subprocess.getoutput('git pull')}")
    os.chdir('..')

def cloneConfigRepo(repoHttpUrl):
    print(f"\t{subprocess.getoutput(f'git clone {repoHttpUrl}')}")

