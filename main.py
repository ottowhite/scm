#!/usr/bin/env python3
import os
import sys
import subprocess

from git_wrapper import pullOrCloneRepo
from filesystem_wrapper import tryHardLinkConfigFileIfRequired
from text_processing import (
    getRepoNameFromGitUrl,
    parseConfigDirectoryCsvLine
)

def main(repoHttpUrl):
    repoName = getRepoNameFromGitUrl(repoHttpUrl)
    pullOrCloneRepo(repoName, repoHttpUrl)

    configDirectoryCsvPath = os.path.join(repoName, "config_directory.csv")

    with open(configDirectoryCsvPath) as configDirectoryCsvFile:
        for configDirectoryCsvLine in configDirectoryCsvFile:

            (configFileSrcName, 
             configFileDstPath, 
             configFileRequired) = parseConfigDirectoryCsvLine(configDirectoryCsvLine)

            configFileSrcPath = os.path.join(repoName, "config_files", configFileSrcName)

            tryHardLinkConfigFileIfRequired(
                configFileSrcPath, 
                configFileDstPath, 
                configFileRequired)

if __name__ == '__main__':
    main(sys.argv[1])

# TODO: Add windows from WSL support (With copying perhaps)
# TODO: Add --set-repo flag and write the value to a file
# TODO: Add support for backing up overwritten files
# TODO: Add safety step for when privilege is required to overwrite