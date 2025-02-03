import mysql.connector as connector

user = 'root'
password = 'Tituskiprono123*'
host = 'localhost'
database_name = 'Openheimer'

connection = connector.connect(user = "root", password = "Tituskiprono123*", host = 'localhost')

cursor = connection.cursor()

drop_database = """DROP DATABASE IF EXISTS Openheimer"""
cursor.execute(drop_database)

create_database = """CREATE DATABASE Openheimer"""
cursor.execute(create_database)

drop_table = """DROP TABLE IF EXISTS Books"""

create_Books_table = """
b_id INT AUTO_INCREMENT PRIMARY KEY,
b_name CHAR(50) NOT NULL,
b_author VARCHAR(255) NOT NULL,
email VARCHAR(255),
sales INT,
likes INT;
"""

cursor.execute(create_Books_table)

my_sql = """"
INSERT INTO Books(b_name,b_author,email,sales,likes) 
VALUES
('ELON MUSK','ASHLEE VANCE','ashle321@gmail.com',500000,100000),
('ZERO TO ONE','PETER THIEL', 'thiel23@gmail.com',1000000,200000),
('BRIDES OF THE KINDRED','EVANGELINE','evangeline24@gmail.com',600000,400000),
('CHAINED','ANDERSON','anderson4@gmail.com',3000000,10000000),
('OBSIDIAN','UNKNOWN',NULL,400000,20000000),
('H.I.V.E','MARK WALDEN','walden@gmail.com',1000000,50000000),
('EARTHFALL','MARK WALDEN','walden@gmail.com',500000,60000001),
('ALCHEMIST','PAULO COELHO','paul@gmail.com',800000,34000234);
"""

connection.commit()

read_data = """SELECT * FROM Books"""

cursor.execute(read_data)

result = cursor.fetchall()
print(result)

cursor.close()
connection.close()