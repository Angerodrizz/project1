import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine("postgresql://okbazksspizzvy:ed42cf8e50a9824eebc6e21d4d9ac34f0250eaeb75f6cc4d16ca9a41a31a7de1@ec2-54-217-204-34.eu-west-1.compute.amazonaws.com:5432/dacegb38d1f5r2")
db = scoped_session(sessionmaker(bind=engine))



db.execute('CREATE TABLE reviews (isbn VARCHAR NOT NULL, review VARCHAR NOT NULL, rating INTEGER NOT NULL, username VARCHAR NOT NULL)')
db.execute('CREATE TABLE booksE (isbn VARCHAR PRIMARY KEY, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year VARCHAR NOT NULL)')

f = open('books.csv')
reader =csv.reader(f) 

for isbn,title,author,year in reader:
    
    db.execute('INSERT INTO booksE (isbn, title, author, year) VALUES (:a,:b,:c,:d)', 
                {'a':isbn,'b':title,'c':author,'d':year})
    print('success')
    db.commit()
    
    