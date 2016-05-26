# Cloud-Web-and-DatabaseGeo--Location-Services
from 22.	https://www.maxmind.com/en/free-world-cities-database,
Download worldcitypop.txt.
Rename it to worldcitypop.csv
In Amazon RDS create a database with name mycitydb.
create a table cityinfo (ref:RDS_MYSQl_Data_Import.docx)
load worldcitypop.csv in to mycitydb.cityinfo.
IN AWS ec2 create an ubuntu instance.
Install Apache server,Setup a flask app names sqlapp.
upload the sqlapp.py,static,teplates in the sqlapp folder in ubuntu
ref:http://www.datasciencebytes.com/bytes/2015/02/24/running-a-flask-app-on-aws-ec2/
Install pymysql python library
setup memcache in AWS & update memc=memcache.Client(['xxxx:11211'],debug=0) -xxxx in sqlapp.py
open the wesite with the ec2 url
Enter the city, country region & Query for the distance. 
If the query & results are repeted then the result is given from memcache way faster
Query for nieghbours similarly
