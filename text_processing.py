import os

from command_wrapper import runCommand

def printLine():
	columns = os.getenv('COLUMNS', runCommand("tput cols").strip())
	print('-' * int(columns))

def getRepoNameFromGitUrl(repoHttpUrl):
	return os.path.splitext(os.path.basename(repoHttpUrl))[0]
	
def evaluateEnvironmentVariables(inputString):
  return runCommand(f"eval \"echo {inputString}\"")

def printTitle(title):
	print("\n")
	print(title)
	printLine()