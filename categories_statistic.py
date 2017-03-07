# from flask import Flask, jsonify, render_template, redirect, request, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask_sqlalchemy import SQLAlchemy
from model import connect_to_db, db, OpportunityCategory, Category


# db = SQLAlchemy()
# from if_available_now import if_available_now

# def categories_stat():
#     f = open('categories_stat.txt', 'w')
#     cat_stat = {}
#     print("IN FN")
#     all_categories = db.session.query(OpportunityCategory.category_id).all()
#     for cat in all_categories:
#         cat = str(cat).replace('(','').replace(')','').replace(',','').rstrip()
#         f.write(cat+'\n')
#     file = open('categories_stat.txt','r')
#     for line in file:
#         if line in cat_stat:
#             cat_stat[line] = cat_stat[line]+1
#         else:
#             cat_stat[line] = 1
#     print cat_stat

file = open('cat_stat.txt', 'r')

for line in file:
    print line.split('\t')[0]
cat_id = db.session.query(Category.vm_id, Category.category_name)
for cat in cat_id:
    print cat.vm_id+"\t"+cat.category_name

if __name__ == "__main__":
    from server import app
    print app
    connect_to_db(app)
    print "Connect do db", app.config['SQLALCHEMY_DATABASE_URI']
#     categories_stat()
