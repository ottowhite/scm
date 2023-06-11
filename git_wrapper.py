import os

from command_wrapper import runCommand

def pullOrCloneRepo(repoFileName, repoHttpUrl):
    if os.path.isdir(repoFileName):
        print("1) Repo already exists, pulling")
        runCommand(f"git clone {repoHttpUrl}", printOutput=True)
    else:
        print("1) Repo doesn\'t exist, cloning")
        runCommand(f'cd {repoFileName} && git pull && cd ..', printOutput=True)
