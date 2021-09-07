# Python program to demonstrate
# Ansible with command line arguments
 
 
import sys
 
# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)
 
# Arguments passed
print("Name of Python script:", sys.argv[0])
 
print("Host run against:", sys.argv[1])