import boto.ec2
import sys
import time
from ec2launch import Instance



if __name__ == '__main__':
	'''
	Create key pair value
	'''
	conn = boto.ec2.connect_to_region("<your-region>",
		aws_access_key_id = '<your-key>',
		aws_secret_access_key = '<your-secret-access-key>')
	inst = Instance(conn)

	print "Randomly creating a new Key Pair"
	inst.newkeycreate()
	'''
	Create Security group
	'''
	print"Randomly creating a new Security Group"
	inst.newsecgrpcreate()
	'''
	Create the instance
	'''
	print"Randomly creating a new instance"
	new_instance = inst.instancecreate()
	'''
	Printing the details of the running instance, and all present instances in the stack
	'''
	print"Printing Instance details"
	inst.printdetails()
	print"Print all Running Instances"
	inst.printalldetails()
	'''
	Stopping the instance created now. Let instance be intialised properly
	'''
	time.sleep(200)
	print"Stopping this Instance"
	inst.instancestop(new_instance)
	'''
	Terminate the instance created now. Let Stop processes execute completely
	'''
	time.sleep(200)
	print"Terminating the Instance"
	inst.terminateinstance(new_instance)

	'''
	Stopping all the running instance.
	'''
	time.sleep(200)
	print"Stopping this Instance"
	inst.instancestop()
	'''
	Terminate all the stopped instance.
	'''
	time.sleep(200)
	print"Terminating the Instance"
	inst.terminateinstance()	
