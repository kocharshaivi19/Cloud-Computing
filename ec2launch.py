import os
import boto.ec2
import random
import sys

'''
1. Creating a connection with AWS. Specify the region where you want to setup ec2 along with your security credentials.
2. Generate a new Key Pair
3. Add a Security group
4. Create the instance using Key and Security group
5. Print the instances having Instance ID, Region, Public key, Private key.
6. Stop the instance
7. Terminate the instance 
'''

class Instance(object):
	def __init__(self, conn):
		self.conn = conn

	def newkeycreate(self):
		'''
		1. Generates a random key and checks if that exists or not using create_key_pair function
		'''
		keyname=None
		try:
			keyname=str(random.random())
			key=self.conn.create_key_pair(keyname)
			cwd=os.getcwd()
			key.save(cwd)
			print key
			self.key = str(key).split(':')[1]
		except:
			print "Key Pair {0} alreadt exist".format(key)
			return None

	def newsecgrpcreate(self):
		'''
		2. Creates a new security group for the generated key
		'''
		grpname=None	
		try:
			grpname = str(random.random())
			desc = "Randolmly Generated Security Group"
			secgrp = self.conn.create_security_group(grpname,desc)
			print secgrp
			self.secgrp = str(secgrp).split(':')[1] 
		except:
			print "This Security group {0} already exist".format(secgrp)
			return None

	def instancecreate(self):
		'''
		3. Launching the ec2 instance. 
		This requires AMI image id and instance type. 
		Setup the key-pair and security group before launching.
		'''
		# keyname = self.newkeycreate()
		# security_grp_name = self.newsecgrpcreate()
		print self.key, self.secgrp
		if self.key!=None and self.secgrp!=None:
			inst = self.conn.run_instances(
				'ami-7172b611',
				key_name = self.key,
				instance_type = 't2.micro',
				security_groups = [self.secgrp])
			print "New instance has been created sucessfully"
			print type(str(inst.instances[0]))
		return inst

	def printdetails(self):
		'''
		4. Print Details of newly created instances
		'''
		reservations = self.conn.get_all_instances()
		instances = [i for r in reservations for i in r.instances]
		print "Instance ID\t"+"Region\t"+"Public IP Address\t"+ "Private IP Address"
		for i in instances:
			myd=i.__dict__			
			st=str(myd['_state'])
			if st.encode('ascii','ignore')=='running(0)' or st.encode('ascii', 'ignore') == 'pending(0)':
				print str(myd['id']).encode('ascii','ignore')+"\t"+str(myd['region']).encode('ascii','ignore') \
					+"\t"+str(myd['ip_address']).encode('ascii','ignore')+"\t"+str(myd['private_ip_address']).encode('ascii','ignore')


	def printalldetails(self):
		'''
		4. Print Details of all the instances currently present in the ec2 account
		'''
		reservations = self.conn.get_all_instances()
		instances = [i for r in reservations for i in r.instances]
		print "Instance ID\t"+"Region\t"+"Public IP Address\t"+"Private IP Address"
		for i in instances:
			myd=i.__dict__	
			print str(myd['id']).encode('ascii','ignore')+"\t"+str(myd['region']).encode('ascii','ignore')+"\t"+str(myd['ip_address']).encode('ascii','ignore')+"\t"+str(myd['private_ip_address']).encode('ascii','ignore')
		
	def instancestop(self, inst_val=None):
		'''
		5. Stop running the instance that we is created now by checking the status, either running or pending. 
		'''
		if inst_val:
			instances = [inst_val]
		else:
			reservations = self.conn.get_all_reservations()
			instances = [i for r in reservations for i in r.instances]
		print instances
		for i in instances:
			try:
				myd=i.__dict__			
				st=str(myd['_state'])
				if st.encode('ascii','ignore')=='running(16)' or st.encode('ascii', 'ignore') == 'pending(0)':
					self.conn.stop_instances(instance_ids=myd['id'])
					print "Instance {0} is now stopped.".format(myd['id'])
				elif st.encode('ascii', 'ignore') == 'stopped(80)' or st.encode('ascii', 'ignore') == 'terminated(48)':
					print "Instance"+myd['id']+" has alread stopped or terminated."
				else:
					pass
			except Exception, self.conn:
				error2 = "Error2: %s" % str(self.conn)
				print(error2)
				sys.exit(0)

	def terminateinstance(self, inst_val=None):
		'''
		6. Terminate only the instance that has stopped
		'''
		if inst_val:
			instances = [inst_val]
		else:
			reservations = self.conn.get_all_reservations()
			instances = [i for r in reservations for i in r.instances]

		for i in instances:
			try:
				myd=i.__dict__
				st=str(myd['_state'])
				if st.encode('ascii','ignore')=='stopped(80)':
					self.conn.terminate_instances(instance_ids=myd['id'])
					print "Instance {0} is now terminated.".format(myd['id'])
				elif st.encode('ascii', 'ignore') == 'terminated(48)':
					print "Instance"+myd['id']+" already terminated."
				else:
					pass
			except Exception, self.conn:
				error2 = "Error2: %s" % str(self.conn)
				print(error2)
				sys.exit(0)