#!/usr/bin/env python3
import os
import sys
import subprocess
from git_wrapper import pullOrCloneRepo

def printLine():
    columns = os.getenv('COLUMNS', subprocess.check_output(['tput', 'cols']).decode().strip())
    print(' ' * int(columns))

def recursivelyCreateDirectory(currentDirname):
    if not os.path.isdir(currentDirname):
        recursivelyCreateDirectory(os.path.dirname(currentDirname))
        os.mkdir(currentDirname)


def recursivelyCreateDirectoryForFile(filepath):
    recursivelyCreateDirectory(os.path.dirname(filepath))


def clearOtherHardLinks(fileToClearHardLinks):
    inodeNumber = subprocess.check_output(['ls', '-i', fileToClearHardLinks]).decode().split()[0]
    hardLinkReferences = subprocess.check_output(['find', '~', '/etc', '-inum', inodeNumber, '2>', '/dev/null']).decode().split()

    for fileReference in hardLinkReferences:
        if os.path.realpath(fileReference) == os.path.realpath(fileToClearHardLinks):
            print('Retain:', fileReference)
        else:
            print('Delete:', fileReference)
            subprocess.call(['sudo', 'rm', fileReference])


def createHardLink(configFileName, configFileDst):
    # TODO: Only use sudo if absolutely necessary

    # Evaluate ~
    configFileDst = os.path.expanduser(configFileDst)

    recursivelyCreateDirectoryForFile(configFileDst)
    src = os.path.realpath(configFileName)

    subprocess.call(['sudo', 'ln', '-i', src, configFileDst])


def hardLinkConfigFile(configFileName, configFileDst):
    if os.path.isfile(configFileName):
        print("1) Clearing residual hard links for", configFileName + '.')
        clearOtherHardLinks(configFileName)
        print()

        print("2) Creating hard link:", configFileName, '->', configFileDst)
        createHardLink(configFileName, configFileDst)
    else:
        print(configFileName, 'does not exist, skipping.')


def tryHardLinkConfigFileIfRequired(configDirectoryCsvLine, repoName):
    configFileName = os.path.join(repoName, 'config_files', configDirectoryCsvLine.split(',')[0])
    configFileDst = configDirectoryCsvLine.split(',')[1]
    configFileRequired = configDirectoryCsvLine.split(',')[2]

    if configFileRequired == 'y':
        printLine()
        print('Processing:', configFileName)
        print('Destination:', configFileDst)
        printLine()

        hardLinkConfigFile(configFileName, configFileDst)
    else:
        printLine()
        print(configFileName, 'not required, skipping.')
        printLine()

def getRepoNameFromGitUrl(repoHttpUrl):
    return os.path.splitext(os.path.basename(repoHttpUrl))[0]

def getConfigDirectoryCsvPathFromRepoName(repoName):
    return os.path.join(repoName, 'config_directory.csv')

def processConfigFiles(repoHttpUrl):
    repoName = getRepoNameFromGitUrl(repoHttpUrl)
    pullOrCloneRepo(repoName, repoHttpUrl)

    configDirectoryCsvPath = getConfigDirectoryCsvPathFromRepoName(repoName)

    with open(configDirectoryCsvPath) as configDirectoryCsv:
        for configDirectoryCsvLine in configDirectoryCsv:
            tryHardLinkConfigFileIfRequired(configDirectoryCsvLine.strip(), repoName)


if __name__ == '__main__':
    processConfigFiles(sys.argv[1])