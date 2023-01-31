import pymysql

db=pymysql.connect(host="localhost",user="root",password="root@123",db="python_april")

obj=db.cursor()

obj.execute("SELECT VERSION()")

data=obj.fetchone()
print('your database version is',data)

obj.execute("show tables")
a=obj.fetchall()
print("your tables are:",a)




obj.execute('insert into student values(2,"arun",21,"datascience","alapuzha")')
obj.execute("select * from student")
output=obj.fetchall()
print(output)

# for i in output:
    # print(i)

