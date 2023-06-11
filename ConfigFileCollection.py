from ConfigFile import ConfigFile


class ConfigFileCollection:
  def __init__(self, configDirectoryCsvPath, repoName):
    self.configFiles = []

    with open(configDirectoryCsvPath) as configDirectoryCsvFile:
      for configDirectoryCsvLine in configDirectoryCsvFile:
        self.configFiles.append(ConfigFile(configDirectoryCsvLine, repoName))
  
  def forEach(self, function):
    for configFile in self.configFiles:
      function(configFile)
  
