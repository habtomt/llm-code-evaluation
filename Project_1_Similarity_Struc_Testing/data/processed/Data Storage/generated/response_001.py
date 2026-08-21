import mysql .connector
from pymongo import MongoClient

def setup_mysql_db ():

    try :

        db =mysql .connector .connect (
        host ='YOUR_HOST',
        user ='YOUR_USER',
        password ='YOUR_PASSWORD'
        )
        cursor =db .cursor ()

        cursor .execute ("CREATE DATABASE IF NOT EXISTS my_database")
        cursor .execute ("USE my_database")

        cursor .execute ("""
            CREATE TABLE IF NOT EXISTS my_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                email VARCHAR(100)
            )
        """)

        cursor .execute ("ALTER TABLE my_table ADD INDEX (name)")

        db .commit ()
        db .close ()
    except mysql .connector .Error as err :
        print ("Something went wrong: {}".format (err ))

def setup_mongodb ():

    try :
        client =MongoClient ('mongodb://localhost:27017/')
        db =client ['myDatabase']
        collection =db ['myCollection']

        collection .create_index ('name')

        client .close ()
    except Exception as e :
        print ("An error occurred: {}".format (e ))

def mysql_crud_operations ():
    try :
        db =mysql .connector .connect (
        host ='YOUR_HOST',
        user ='YOUR_USER',
        password ='YOUR_PASSWORD',
        database ='my_database'
        )
        cursor =db .cursor ()

        cursor .execute ("INSERT INTO my_table (name, age, email) VALUES ('John Doe', 30, 'john.doe@mail.com')")
        db .commit ()

        cursor .execute ("SELECT * FROM my_table WHERE name = 'John Doe'")
        result =cursor .fetchall ()
        for row in result :
            print (row )

        cursor .execute ("UPDATE my_table SET age = 31 WHERE name = 'John Doe'")
        db .commit ()

        cursor .execute ("DELETE FROM my_table WHERE name = 'John Doe'")
        db .commit ()

        db .close ()
    except mysql .connector .Error as err :
        print ("Something went wrong: {}".format (err ))

def mongodb_crud_operations ():
    try :
        client =MongoClient ('mongodb://localhost:27017/')
        db =client ['myDatabase']
        collection =db ['myCollection']

        collection .insert_one ({'name':"John Doe",'age':30 ,'email':"john.doe@mail.com"})

        result =collection .find ({'name':"John Doe"})
        for document in result :
            print (document )

        collection .update_one ({'name':"John Doe"},{'$set':{'age':31 }})

        collection .delete_one ({'name':"John Doe"})

        client .close ()
    except Exception as e :
        print ("An error occurred: {}".format (e ))

if __name__ =="__main__":
    setup_mysql_db ()
    setup_mongodb ()
    mysql_crud_operations ()
    mongodb_crud_operations ()