#!/usr/bin/env python3
import os
import sys
import subprocess

from git_wrapper import pullOrCloneRepo
from text_processing import (
    printLine,
    getConfigDirectoryCsvPathFromRepoName,
    getRepoNameFromGitUrl,
    parseConfigDirectoryCsvLine
)

def main(repoHttpUrl):
    repoName = getRepoNameFromGitUrl(repoHttpUrl)
    pullOrCloneRepo(repoName, repoHttpUrl)

    configDirectoryCsvPath = getConfigDirectoryCsvPathFromRepoName(repoName)

    with open(configDirectoryCsvPath) as configDirectoryCsv:
        for configDirectoryCsvLine in configDirectoryCsv:

            (configFileSrcName, 
             configFileDstPathWithVars, 
             configFileRequired) = parseConfigDirectoryCsvLine(configDirectoryCsvLine)

            configFileSrcPath = os.path.join(repoName, configFileSrcName)
            # Evaluate environment variables like $HOME or ~
            configFileDstPath = subprocess.getoutput(f"eval \"echo {configFileDstPathWithVars}\"")

            tryHardLinkConfigFileIfRequired(
                configFileSrcPath, 
                configFileDstPath, 
                configFileRequired)

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

def createHardLink(configFileSrcName, configFileDstPath):
    # TODO: Only use sudo if absolutely necessary

    # Evaluate ~
    configFileDstPath = os.path.expanduser(configFileDstPath)

    recursivelyCreateDirectoryForFile(configFileDstPath)
    src = os.path.realpath(configFileSrcName)

    subprocess.call(['sudo', 'ln', '-i', src, configFileDstPath])


def hardLinkConfigFile(configFileSrcName, configFileDstPath):
    if os.path.isfile(configFileSrcName):
        print("1) Clearing residual hard links for", configFileSrcName + '.')
        clearOtherHardLinks(configFileSrcName)
        print()

        print("2) Creating hard link:", configFileSrcName, '->', configFileDstPath)
        createHardLink(configFileSrcName, configFileDstPath)
    else:
        print(configFileSrcName, 'does not exist, skipping.')


def tryHardLinkConfigFileIfRequired(configFileSrcPath, configFileDstPath, configFileRequired):
    if configFileRequired:
        printLine()
        print('Processing:', configFileSrcPath)
        print('Destination:', configFileDstPath)
        printLine()

        hardLinkConfigFile(configFileSrcPath, configFileDstPath)
    else:
        printLine()
        print(configFileSrcPath, 'not required, skipping.')
        printLine()

if __name__ == '__main__':
    main(sys.argv[1])