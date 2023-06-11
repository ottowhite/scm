import os
import subprocess
from text_processing import printLine

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
        print(f"{configFileSrcPath} -> {configFileDstPath}")
        printLine()

        hardLinkConfigFile(configFileSrcPath, configFileDstPath)
    else:
        printLine()
        print(configFileSrcPath, 'not required, skipping.')
        printLine()