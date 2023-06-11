import os

from text_processing import evaluateEnvironmentVariables

class ConfigFile:
	def __init__(self, configDirectoryCsvLine, originRepoName):
		self.parseConfigDirectoryCsvLine(configDirectoryCsvLine)
		self.inferFields(originRepoName)

	def parseConfigDirectoryCsvLine(self, configDirectoryCsvLine):
		configDirectoryCsvLineValues = configDirectoryCsvLine.strip().split(',')

		assert len(configDirectoryCsvLineValues) == 3, \
	  	"There must only be 3 values in each line of the config_directory.csv file"

		self.configFileSrcName 			   = configDirectoryCsvLineValues[0]
		self.configFileDstPathWithVars = configDirectoryCsvLineValues[1]
		self.configFileRequiredText 	 = configDirectoryCsvLineValues[2]
	
	def inferFields(self, repoName):
		self.configFileSrcPath 	= os.path.join(repoName, "config_files", self.configFileSrcName)
		self.configFileDstPath  = evaluateEnvironmentVariables(self.configFileDstPathWithVars)
		self.configFileRequired = True if self.configFileRequiredText == 'y' else False
	
	def getName(self):
		return self.configFileSrcName
	
	def getSrcPath(self):
		return self.configFileSrcPath
	
	def getDstPath(self):
		return self.configFileDstPath
	
	def isRequired(self):
		return self.configFileRequired

