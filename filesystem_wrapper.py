import os
from command_wrapper import runCommand
from text_processing import evaluateEnvironmentVariables

def recursivelyCreateDirectory(currentDirname):
  if not os.path.isdir(currentDirname):
    recursivelyCreateDirectory(os.path.dirname(currentDirname))
    os.mkdir(currentDirname)

def recursivelyCreateDirectoryForFile(filepath):
  recursivelyCreateDirectory(os.path.dirname(filepath))

def clearOtherHardLinks(fileToClearHardLinks):
  inodeNumber = runCommand(f"ls -i {fileToClearHardLinks}").split()[0]

  homeDirectory = evaluateEnvironmentVariables('~')
  hardLinkReferences = runCommand(f"find {homeDirectory} /etc -inum {inodeNumber} 2> /dev/null").split()

  for fileReference in hardLinkReferences:
    if os.path.realpath(fileReference) == os.path.realpath(fileToClearHardLinks):
      print('\tRetaining', fileReference)
    else:
      print('\tDeleting ', fileReference)
      runCommand(f"sudo rm {fileReference}")

def createHardLink(configFileSrcPath, configFileDstPath):
  # TODO: Only use sudo if absolutely necessary

  recursivelyCreateDirectoryForFile(configFileDstPath)

  print(f"\t{configFileSrcPath} -> {configFileDstPath}")

  # TODO: Get the prompt of this to print properly
  runCommand(f'sudo ln -i {configFileSrcPath} {configFileDstPath}')

def hardLinkConfigFile(configFileSrcPath, configFileDstPath):
  if os.path.isfile(configFileSrcPath):
    print("1) Clearing residual hard links for", configFileSrcPath + '.')
    clearOtherHardLinks(configFileSrcPath)
    print()

    print("2) Creating hard link")
    createHardLink(configFileSrcPath, configFileDstPath)
  else:
    print(configFileSrcPath, 'does not exist, skipping.')
