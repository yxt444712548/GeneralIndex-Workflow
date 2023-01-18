from flask import Flask, render_template, request, redirect, url_for, session
from search import search
import sqlite3

app = Flask(__name__)
app.secret_key = "#$%#$%^%^BFGBFGBSFGNSGJTNADFHH@#%$%#T#FFWF$^F@$F#$FW"

def init_database():
	import csv, sqlite3

	con = sqlite3.connect("metadata.db")
	cur = con.cursor()
	cur.execute("CREATE TABLE t (dkey, title, doi, author, year);")  # use your column names here

	with open('metadata_test.csv', 'r') as fin:  # `with` statement available in 2.5+
		# csv.DictReader uses first line in file for column headings by default
		dr = csv.DictReader(fin)  # comma is default delimiter
		to_db = [(i['dkey'], i['title'], i['doi'], i['author'], i['year']) for i in dr]

	cur.executemany("INSERT INTO t (dkey, title, doi, author, year) VALUES (?, ?, ?, ?, ?);", to_db)
	con.commit()
	con.close()


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/search", methods=["POST", "GET"])
def searchr():
	if request.method == "POST":
		query = request.form["query"]
		search_within = request.values.get("type")
		start_year = request.values.get("start")
		end_year = request.values.get("end")
		results, info = search(query, search_within, start_year, end_year)
	return render_template("search.html", results=results, info=info, query=query)


if __name__ == '__main__':
	# init_database()
	app.run(debug=True)