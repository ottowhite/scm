#!/usr/bin/env python3
import os
import sys

from git_wrapper import synchronizeWithRepo
from filesystem_wrapper import hardLinkConfigFile
from text_processing import parseConfigDirectoryCsvLine, printTitle

def main(repoHttpUrl):
  printTitle(f"Getting latest changes from {repoHttpUrl}")
  repoName = synchronizeWithRepo(repoHttpUrl)

  configDirectoryCsvPath = os.path.join(repoName, "config_directory.csv")

  with open(configDirectoryCsvPath) as configDirectoryCsvFile:
    for configDirectoryCsvLine in configDirectoryCsvFile:

      (configFileSrcName, 
       configFileDstPath, 
       configFileRequired) = parseConfigDirectoryCsvLine(configDirectoryCsvLine)

      configFileSrcPath = os.path.join(repoName, "config_files", configFileSrcName)

      if configFileRequired:
        printTitle(configFileSrcName)
        hardLinkConfigFile(configFileSrcPath, configFileDstPath)
      else:
        printTitle(f"{configFileSrcName} (skipping)")

if __name__ == '__main__':
  main(sys.argv[1])

# TODO: Add windows from WSL support (With copying perhaps)
# TODO: Add --set-repo flag and write the value to a file
# TODO: Add support for backing up overwritten files
# TODO: Add safety step for when privilege is required to overwrite