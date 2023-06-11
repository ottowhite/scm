#!/usr/bin/env python3
import os
import sys

from git_wrapper import pullOrCloneRepo
from filesystem_wrapper import tryHardLinkConfigFileIfRequired
from text_processing import (
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
             configFileDstPath, 
             configFileRequired) = parseConfigDirectoryCsvLine(configDirectoryCsvLine)

            tryHardLinkConfigFileIfRequired(
                os.path.join(repoName, "config_files", configFileSrcName), 
                configFileDstPath, 
                configFileRequired)


if __name__ == '__main__':
    main(sys.argv[1])