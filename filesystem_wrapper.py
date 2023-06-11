import os
import subprocess
from text_processing import evaluateEnvironmentVariables, printLine

def recursivelyCreateDirectory(currentDirname):
  if not os.path.isdir(currentDirname):
    recursivelyCreateDirectory(os.path.dirname(currentDirname))
    os.mkdir(currentDirname)

def recursivelyCreateDirectoryForFile(filepath):
  recursivelyCreateDirectory(os.path.dirname(filepath))

def clearOtherHardLinks(fileToClearHardLinks):
  inodeNumber = subprocess.check_output(['ls', '-i', fileToClearHardLinks]).decode().split()[0]
  homeDirectory = evaluateEnvironmentVariables('~')
  hardLinkReferences = subprocess.getoutput(f"find {homeDirectory} /etc -inum {inodeNumber} 2> /dev/null").split()

  for fileReference in hardLinkReferences:
    if os.path.realpath(fileReference) == os.path.realpath(fileToClearHardLinks):
      print('Retain:', fileReference)
    else:
      print('Delete:', fileReference)
      subprocess.call(['sudo', 'rm', fileReference])

def createHardLink(configFileSrcPath, configFileDstPath):
  # TODO: Only use sudo if absolutely necessary

  recursivelyCreateDirectoryForFile(configFileDstPath)

  # TODO: Get the prompt of this to print properly
  subprocess.getoutput(f'sudo ln -i {configFileSrcPath} {configFileDstPath}')

def hardLinkConfigFile(configFileSrcPath, configFileDstPath):
  if os.path.isfile(configFileSrcPath):
    print("1) Clearing residual hard links for", configFileSrcPath + '.')
    clearOtherHardLinks(configFileSrcPath)
    print()

    print("2) Creating hard link")
    createHardLink(configFileSrcPath, configFileDstPath)
  else:
    print(configFileSrcPath, 'does not exist, skipping.')

def tryHardLinkConfigFileIfRequired(configFileSrcPath, configFileDstPath, configFileRequired):
  if configFileRequired:
    printLine()
    print(f"{configFileSrcPath} -> {configFileDstPath}")
    printLine()

    hardLinkConfigFile(configFileSrcPath, configFileDstPath)
  else:
    printLine()
    print(f"Skipping: {configFileSrcPath} -> {configFileDstPath}")
    printLine()