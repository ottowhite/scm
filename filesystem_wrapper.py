import os
from command_wrapper import runCommand
from text_processing import evaluateEnvironmentVariables

def recursivelyCreateDirectory(currentDirname):
  if not os.path.isdir(currentDirname):
    recursivelyCreateDirectory(os.path.dirname(currentDirname))
    os.mkdir(currentDirname)

def recursivelyCreateDirectoryForFile(filepath):
  recursivelyCreateDirectory(os.path.dirname(filepath))

def clearOtherHardLinks(configFile):
  inodeNumber = runCommand(f"ls -i {configFile.getSrcPath()}").split()[0]

  homeDirectory = evaluateEnvironmentVariables('~')
  hardLinkReferences = runCommand(f"find {homeDirectory} /etc -inum {inodeNumber} 2> /dev/null").split()

  for fileReference in hardLinkReferences:
    if os.path.realpath(fileReference) == os.path.realpath(configFile.getSrcPath()):
      print('\tRetaining', fileReference)
    else:
      print('\tDeleting ', fileReference)
      runCommand(f"sudo rm {fileReference}")

def createHardLink(configFile):
  # TODO: Only use sudo if absolutely necessary
  name = configFile.getName()
  srcPath = configFile.getSrcPath()
  dstPath = configFile.getDstPath()

  recursivelyCreateDirectoryForFile(dstPath)

  print(f"\t{name} -> {dstPath}")

  # TODO: Get the prompt of this to print properly
  runCommand(f'sudo ln -i {srcPath} {dstPath}')

def hardLinkConfigFile(configFile):
  if os.path.isfile(configFile.getSrcPath()):
    print("1) Clearing residual hard links for", configFile.getName())
    clearOtherHardLinks(configFile)
    print()

    print("2) Creating hard link")
    createHardLink(configFile)
  else:
    print(configFile.getSrcPath(), 'does not exist, skipping.')
