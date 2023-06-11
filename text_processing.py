import os

from command_wrapper import runCommand

def printLine():
	columns = os.getenv('COLUMNS', runCommand("tput cols").strip())
	print('-' * int(columns))

def getRepoNameFromGitUrl(repoHttpUrl):
	return os.path.splitext(os.path.basename(repoHttpUrl))[0]
	
def parseConfigDirectoryCsvLine(configDirectoryCsvLine):
	configDirectoryCsvLine = configDirectoryCsvLine.strip()
	configDirectoryCsvLineValues = configDirectoryCsvLine.split(',')

	assert len(configDirectoryCsvLineValues) == 3

	configFileName     		 		 = configDirectoryCsvLineValues[0]
	configFileDstPathWithVars  = configDirectoryCsvLineValues[1]
	configFileRequired 			   = configDirectoryCsvLineValues[2]

	return (
		configFileName,
		evaluateEnvironmentVariables(configFileDstPathWithVars),
		True if configFileRequired == 'y' else False
	)

def evaluateEnvironmentVariables(inputString):
  return runCommand(f"eval \"echo {inputString}\"")
