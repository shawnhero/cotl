# this script is supposed to be called only once
# to create the table schemas in HBase
import happybase

connection = happybase.Connection('ec2-54-67-86-242.us-west-1.compute.amazonaws.com')
print connection.tables()