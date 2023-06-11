#!/usr/bin/env python3
import os
import sys

from git_wrapper import pullOrCloneRepo
from filesystem_wrapper import hardLinkConfigFile
from text_processing import (
    getRepoNameFromGitUrl,
    parseConfigDirectoryCsvLine,
    printLine
)

def main(repoHttpUrl):
    repoName = getRepoNameFromGitUrl(repoHttpUrl)
    print("\n")
    print(f"Getting latest changes from {repoHttpUrl}")
    printLine()
    pullOrCloneRepo(repoName, repoHttpUrl)

    configDirectoryCsvPath = os.path.join(repoName, "config_directory.csv")

    with open(configDirectoryCsvPath) as configDirectoryCsvFile:
        for configDirectoryCsvLine in configDirectoryCsvFile:

            (configFileSrcName, 
             configFileDstPath, 
             configFileRequired) = parseConfigDirectoryCsvLine(configDirectoryCsvLine)

            configFileSrcPath = os.path.join(repoName, "config_files", configFileSrcName)

            if configFileRequired:
              print("\n")
              print(configFileSrcName)
              printLine()

              hardLinkConfigFile(configFileSrcPath, configFileDstPath)
            else:
              print("\n")
              print(configFileSrcName, "(skipping)")
              printLine()

if __name__ == '__main__':
    main(sys.argv[1])

# TODO: Add windows from WSL support (With copying perhaps)
# TODO: Add --set-repo flag and write the value to a file
# TODO: Add support for backing up overwritten files
# TODO: Add safety step for when privilege is required to overwrite