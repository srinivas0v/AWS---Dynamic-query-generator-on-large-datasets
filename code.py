from flask import Flask, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
from random import randint
#import MySQLdb
import memcache
import time

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = '###########'
app.config['MYSQL_DATABASE_PASSWORD'] = '############'
app.config['MYSQL_DATABASE_DB'] = '############'
app.config['MYSQL_DATABASE_HOST'] = '##############'
app.config['local_infile'] = 1
mysql.init_app(app)

memc = memcache.Client(['sri-mem.x3eu3f.cfg.use2.cache.amazonaws.com:11211'], debug=1);
app = Flask(__name__)



fpath = 'C:/Users/srinivas venkatesh/Downloads/'

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
      if request.form['submit'] == 'count':
          return redirect('/count/')
      elif request.form['submit'] == 'state':
          st = request.form['statetext']
          return redirect('/state/'+st)
      elif request.form['submit'] == 'earth1':
          print 'earth1'
          mag1 = request.form['magnitude1']
          mag2 = request.form['magnitude2']
          long1 = request.form['logitude1']
          long2 = request.form['logitude2']
          lat1 = request.form['latitude1']
          lat2 = request.form['latitude2']
          no = request.form['times']
          var = request.form['var']
          para = mag1+'$$'+mag2+'$$'+long1+'$$'+long2+'$$'+lat1+'$$'+lat2+'$$'+no+'$$'+var
          print para
          return redirect('/earthquake1/'+para)

      elif request.form['submit'] == 'earth2':
          print 'earth2'
          no = request.form['time']
          var = request.form['va']
          para = no+'$$'+var
          return redirect('/earthquake2/' + para)
    return render_template('index.html')




@app.route('/count/',methods=['POST','GET'])
def count():
    print 'in func'
    cur = mysql.connect().cursor()
    query = ('select count(*) as count from MyDB.uc ')
    cur.execute(query)
    data = cur.fetchall()
    print data
    return render_template('count.html', flist=data)





@app.route('/earthquake1/<para>',methods=['POST','GET'])
def Q_earth1(para):

    print 'in func'

    mag1,mag2,long1,long2,lat1,lat2,no,var = para.split('$$')
    times = int(no)

    start_t = time.time()

    data2 =''
    if(var=='mem'):
        for num in range(times):
            key = mag1 + mag2 + long1 + long2 + lat1 + lat2
            data = memc.get(key)
            if not data:
                a = 'sql'
                print 'query in sql'
                cur = mysql.connect().cursor()
                query2 = ('select type,latitude,longitude,mag from MyDB.earthquake where (latitude between %s and %s) and (longitude between %s and %s) '
                          'and (mag between %s and %s)')
                cur.execute(query2,(lat1,lat2,long1,long2,mag1,mag2))
                data2 = cur.fetchall()
                cur.close()
              #  print data2
                memc.set(key, data2)
                end_t = time.time()
                total_t = str(end_t - start_t)

            else:
                a = 'memcache'
                print 'memcache data'
                data2 = data
                end_t = time.time()
                total_t = str(end_t - start_t)
        print 'end for loop'
        print data2

    else:
        for num in range(times):
            a = 'sql'
            print 'query in sql'
            cur = mysql.connect().cursor()
            query2 = (
            'select type,latitude,longitude,mag from MyDB.earthquake where (latitude between %s and %s) and (longitude between %s and %s) '
            'and (mag between %s and %s)')
            cur.execute(query2, (lat1, lat2, long1, long2, mag1, mag2))
            data2 = cur.fetchall()
            cur.close()
            end_t = time.time()
            total_t = str(end_t - start_t)

    return render_template('earth1.html', count=a, list = data2, time = total_t)





@app.route('/earthquake2/<para>',methods=['POST','GET'])
def Q_earth2(para):

    print 'in func'

    no,var = para.split('$$')
    times = int(no)

    start_t = time.time()

    data2 =''
    if(var=='mem'):
        for num in range(times):
            mag1 = randint(-1, 7)
            mag2 = randint(-1, 7)
            long1 = randint(-180, 180)
            long2 = randint(-180, 180)
            lat1 = randint(-70, 85)
            lat2 = randint(-70, 85)
            key = str(mag1 + mag2 + long1 + long2 + lat1 + lat2)
            data = memc.get(key)
            if not data:
                a = 'sql'
                print 'query in mem-sql'
                cur = mysql.connect().cursor()
                query2 = ('select type,latitude,longitude,mag from MyDB.earthquake where (latitude between %s and %s) and (longitude between %s and %s) '
                          'and (mag between %s and %s)')
                cur.execute(query2,(lat1,lat2,long1,long2,mag1,mag2))
                data2 = cur.fetchall()
                cur.close()
              #  print data2
                memc.set(key, data2)
                end_t = time.time()
                total_t = str(end_t - start_t)

            else:
                a = 'memcache'
                print 'memcache data'
                data2 = data
                end_t = time.time()
                total_t = str(end_t - start_t)
        print 'end for loop'
        print data2

    else:
        for num in range(times):
            mag1 = randint(-1, 7)
            mag2 = randint(-1, 7)
            long1 = randint(-180, 180)
            long2 = randint(-180, 180)
            lat1 = randint(-70, 85)
            lat2 = randint(-70, 85)
            print mag1,mag2,long1,long2,lat1,lat2
            a = 'sql'
            print 'query in mem'
            cur = mysql.connect().cursor()
            query2 = (
            'select type,latitude,longitude,mag from MyDB.earthquake where (latitude between %s and %s) and (longitude between %s and %s) '
            'and (mag between %s and %s)')
            cur.execute(query2, (lat1, lat2, long1, long2, mag1, mag2))
            data2 = cur.fetchall()
            cur.close()
            end_t = time.time()
            total_t = str(end_t - start_t)

    return render_template('earth1.html', count=a, list = data2, time = total_t)

@app.route('/state/<st>', methods=['POST', 'GET'])
def Q_state(st):

            print 'in func earthquake'
            key = st;
            start_t = time.time()
            print key
            data = memc.get(key)

            if not data:
                print 'query in sql'
                cur = mysql.connect().cursor()
                # query1=('select count(*) from MyDB.uc where STATE = %s')
                query2 = ('select Name from MyDB.uc where STATE = %s')
                # cur.execute(query1,(st))
                # data1 = cur.fetchall()
                # print data1
                cur.execute(query2, (st))
                data2 = cur.fetchall()
                print data2
                # value = data1+'$$$$'+data2
                memc.set(key, data2)
                end_t = time.time()
                total_t = str(end_t - start_t)
                return render_template('state.html', count='no count', list=data2, time=total_t)
            else:
                print 'memcache data'
                end_t = time.time()
                total_t = str(end_t - start_t)
                return render_template('state.html', count='no count', list=data, time=total_t)



if __name__ == '__main__':
    app.run(debug='true', port= 8080 )
