#Karthikeyan Rajamani #UTA Id:1001267157
#CSE6331 -Cloud Computing
#Programming Assignment4
#references
#https://www.maxmind.com/en/free-world-cities-database
#http://stackoverflow.com/questions/2234204/latitude-longitude-find-nearest-latitude-longitude-complex-sql-or-complex-calc
#https://www.scribd.com/doc/2569355/Geo-Distance-Search-with-MySQL
#http://stackoverflow.com/questions/3635166/how-to-import-csv-file-to-mysql-table
#http://stackoverflow.com/questions/868690/good-examples-of-python-memcache-memcached-being-used-in-python

from flask import Flask,render_template,request,jsonify
import pymysql
import time
import memcache
import hashlib
import json
memc=memcache.Client(['xxxx:11211'],debug=0)
memc.set('val','one')

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def root():
     if request.method == "GET":
        #return memc.get('val')
        return render_template('index.html',queriedtime=0,totaltime=0)

@app.route("/distance",methods=['POST','GET'])
def querydis():
    #return "distance"
    if request.method == "POST":
        city=request.form['city']
        country=str(request.form['country'])
        region=str(request.form['region'])
        dist=float(request.form['N'])
        results=[]
        querytime=0
        starttime=0
        myConnection=''
        origLat="(SELECT latitude FROM cityinfo where city='"+city+"'and region='"+region+"'and country='"+country+"')"
        origLon= "(SELECT longtitude FROM cityinfo where city='"+city+"'and region='"+region+"'and country='"+country+"')"
        query1="SELECT city, latitude, longtitude, 3956 * 2 * ASIN(SQRT( POWER(SIN((" +str(origLat)+" - latitude)*pi()/180/2),2)+COS("+str(origLat)+"*pi()/180 )*COS(latitude*pi()/180)*POWER(SIN(("+str(origLon)+"-longtitude)*pi()/180/2),2))) as distance FROM cityinfo WHERE longtitude between ("+str(origLon)+"-"+str(dist)+"/cos(radians("+str(origLat)+"))*69) and ("+str(origLon)+"+"+str(dist)+"/cos(radians("+str(origLat)+"))*69) and latitude between ("+str(origLat)+"-("+str(dist)+"/69)) and ("+str(origLat)+"+("+str(dist)+"/69)) having distance < "+str(dist)+" ORDER BY distance"
        #return query1
        key1 = hashlib.sha256(query1).hexdigest()
        starttime=time.time()
        resultset=memc.get(key1)
        qtime=time.time()
        querytime=qtime-starttime
        status="Returned from memcache"
        if not resultset:
            hostname = 'xxxx52r4wudge.us-west-2.rds.amazonaws.com'
            username = 'xxxx'
            password = 'xxxx'
            database = 'mycitydb'
            myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database )

            cur = myConnection.cursor()
            cur0=myConnection.cursor()
            starttime=time.time()
            cur.execute(query1)
            #cur.execute( "SELECT city,latitude FROM cityinfo1 where city='Arlington' and region='TX' and country='us'")
            qtime=time.time()
            querytime=qtime-starttime
            resultset=cur.fetchall()#contains all the results
            status="Queried results from RDS"
            memc.set(key1,resultset)
            cur.close()
            myConnection.close()
        listingtime=time.time()
        querytime=qtime-starttime
        ttime=listingtime-starttime
        count=0
        for row in resultset:
            count=count+1
            #results.append(row)
            results.append(str(count)+": "+"    City:  "+str(row[0])+"      Latitude:"+str(row[1])+"      Longitude:"+str(row[2])+"      Distance:"+str(row[3]))
        return render_template('index.html',results=results,queriedtime=querytime,totaltime=ttime,status=status)


@app.route("/neighbours",methods=['GET','POST'])
def queryneigbours():
    if request.method == "GET":
        #return memc.get('val')
        return render_template('index1.html',queriedtime=0,totaltime=0)
    #return "distance"
    if request.method == "POST":
        city=request.form['city']
        country=str(request.form['country'])
        region=str(request.form['region'])
        rcount=int(request.form['K'])
        dist=3
        results=[]
        querytime=0
        starttime=0
        x=''
        resultset=''
        origLat="(SELECT latitude FROM cityinfo where city='"+city+"'and region='"+region+"'and country='"+country+"')"
        origLon= "(SELECT longtitude FROM cityinfo where city='"+city+"'and region='"+region+"'and country='"+country+"')"
        query1="SELECT city, latitude, longtitude, 3956 * 2 * ASIN(SQRT( POWER(SIN((" +str(origLat)+" - latitude)*pi()/180/2),2)+COS("+str(origLat)+"*pi()/180 )*COS(latitude*pi()/180)*POWER(SIN(("+str(origLon)+"-longtitude)*pi()/180/2),2))) as distance FROM cityinfo WHERE longtitude between ("+str(origLon)+"-"+str(dist)+"/cos(radians("+str(origLat)+"))*69) and ("+str(origLon)+"+"+str(dist)+"/cos(radians("+str(origLat)+"))*69) and latitude between ("+str(origLat)+"-("+str(dist)+"/69)) and ("+str(origLat)+"+("+str(dist)+"/69)) having distance < "+str(dist)+" ORDER BY distance"
        key1 = hashlib.sha256(query1).hexdigest()
        starttime=time.time()
        resultset=memc.get(key1)
        qtime=time.time()
        querytime=qtime-starttime
        status="Returned from memcache"
        if not resultset:
             hostname = 'xxxxcom52r4wudge.us-west-2.rds.amazonaws.com'
             username = 'xxxx'
             password = 'xxxx'
             database = 'mycitydb'
             myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database )
             dist=0;
             while True:
              cur = myConnection.cursor()
              starttime=time.time()
              dist=dist+2
              query1="SELECT city, latitude, longtitude, 3956 * 2 * ASIN(SQRT( POWER(SIN((" +str(origLat)+" - latitude)*pi()/180/2),2)+COS("+str(origLat)+"*pi()/180 )*COS(latitude*pi()/180)*POWER(SIN(("+str(origLon)+"-longtitude)*pi()/180/2),2))) as distance FROM cityinfo WHERE longtitude between ("+str(origLon)+"-"+str(dist)+"/cos(radians("+str(origLat)+"))*69) and ("+str(origLon)+"+"+str(dist)+"/cos(radians("+str(origLat)+"))*69) and latitude between ("+str(origLat)+"-("+str(dist)+"/69)) and ("+str(origLat)+"+("+str(dist)+"/69)) having distance < "+str(dist)+" ORDER BY distance"
              cur.execute(query1)
              qtime=time.time()
              querytime=qtime-starttime
              resultset=''
              resultset=cur.fetchall()#contains all the results
              status="Queried results from RDS"
              memc.set(key1,resultset)
              listingtime=time.time()
              querytime=qtime-starttime
              ttime=listingtime-starttime
              results=[]
              if(len(resultset)>rcount):
                  break;
        count=0
        for row in resultset:
            if count<rcount:
             count=count+1
             results.append(str(count)+": "+"    City:  "+str(row[0])+"      Latitude:"+str(row[1])+"      Longitude:"+str(row[2])+"      Distance:"+str(row[3]))
        if status=="Returned from memcache":
            ttime=time.time()-starttime
        return render_template('index1.html',results=results,queriedtime=querytime,totaltime=ttime,status=status)

if __name__ == '__main__':
    app.run(debug=True)


