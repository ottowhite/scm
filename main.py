#!/usr/bin/env python3
import os
import sys
from ConfigFile import ConfigFile
from ConfigFileCollection import ConfigFileCollection

from git_wrapper import synchronizeWithRepo
from filesystem_wrapper import hardLinkConfigFile
from text_processing import printTitle

def main(repoHttpUrl):
  printTitle(f"Getting latest changes from {repoHttpUrl}")
  repoName = synchronizeWithRepo(repoHttpUrl)

  configFileCollection = ConfigFileCollection(
    os.path.join(repoName, "config_directory.csv"), 
    repoName)
  
  configFileCollection.forEach(processConfigFile)

def processConfigFile(configFile):
  if configFile.isRequired():
    printTitle(configFile.getName())

    hardLinkConfigFile(configFile)
  else:
    printTitle(f"{configFile.getName()} (skipping)")

if __name__ == '__main__':
  main(sys.argv[1])

# TODO: Add windows from WSL support (With copying perhaps)
# TODO: Add --set-repo flag and write the value to a file
# TODO: Add support for backing up overwritten files
# TODO: Add safety step for when privilege is required to overwrite