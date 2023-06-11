import os

from command_wrapper import runCommand
from text_processing import getRepoNameFromGitUrl, printTitle

def synchronizeWithRepo(repoHttpUrl):
    repoName = getRepoNameFromGitUrl(repoHttpUrl)
    pullOrCloneRepo(repoName, repoHttpUrl)

    return repoName

def pullOrCloneRepo(repoFileName, repoHttpUrl):
    if os.path.isdir(repoFileName):
        print("1) Repo already exists, pulling")
        runCommand(f'cd {repoFileName} && git pull && cd ..', printOutput=True)
    else:
        print("1) Repo doesn\'t exist, cloning")
        runCommand(f"git clone {repoHttpUrl}", printOutput=True)
