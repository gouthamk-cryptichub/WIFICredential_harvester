import subprocess

def mail_it():


cmd = "echo Hacker here!!"
result= subprocess.check_output(cmd, shell=True)
result = network.decode('utf-8')

mail_it(result)