
import subprocess

def runCommand(command, printOutput=False):
	output = subprocess.getoutput(command)

	if printOutput:
		print(output)

	return output
