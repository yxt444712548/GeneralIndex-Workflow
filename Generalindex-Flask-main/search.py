import psycopg2 as p
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pydoi
import time

def search(query, search_within, start_year, end_year, export):
    start_time = time.time()
    results = {'dkey':[], 'doi':[], 'title':[], 'author':[], 'year':[],'journal':[]}
    if start_year != 'all_start_year' and end_year != 'all_end_year':
        if start_year > end_year:
            info = "end year must greater than start year"
            return results, info
    if start_year == 'all_start_year':
        start_year = 1960
    else:
        start_year = int(start_year) - 1
    if end_year == 'all_end_year':
        end_year = 2024
    else:
        end_year = int(end_year) + 1
    con = p.connect('postgresql://rccuser:password@localhost:5432/generalindex_metadata')
    cur = con.cursor()
    query = query.lower()
    if search_within == 'title':
        sql = "select dkey,doi,title,author,year,journal from metadata_recent where title_lwr like '%{query}%' and year > '{start_year}' and year < '{end_year}' limit 10000".format(query=query, start_year=start_year, end_year=end_year)
    elif search_within == 'author':
        sql = "select dkey,doi,title,author,year,journal from metadata_recent where author_lwr like '%{query}%' and year > '{start_year}' and year < '{end_year}' limit 10000".format(query=query, start_year=start_year, end_year=end_year)
    elif search_within == 'doi':
        sql = "select dkey,doi,title,author,year,journal from metadata_recent where doi like '%{query}%' and year > '{start_year}' and year < '{end_year}' limit 10000".format(query=query, start_year=start_year, end_year=end_year)
    elif search_within == "journal":
        sql = "select dkey,doi,title,author,year,journal from metadata_recent where journal like '%{query}%' and year > '{start_year}' and year < '{end_year}' limit 10000".format(query=query, start_year=start_year, end_year=end_year)
    else:
        sql = "select dkey,doi,title,author,year,journal from metadata_recent limit 10000;"
    cur.execute(sql)
    data = cur.fetchall()
    i = 0
    end_time = time.time()
    print(end_time - start_time)
    start_time = time.time()
    for item in data:
        results['dkey'].append(item[0])
        results['doi'].append(item[1])
        results['title'].append(item[2])
        results['author'].append(item[3])
        results['year'].append(item[4])
        results['journal'].append(item[5])
    # use pandas dataframe to store results for later use, you can use the dataframe to create plot.
    end_time = time.time()
    print(end_time - start_time)
    metadata_df = pd.DataFrame(data=results) 
    
    cur.close()
    con.close()
    
    #plot settings
    fig, ax = plt.subplots()
    metadata_df['year'].value_counts().sort_index().plot(ax=ax, kind='bar')
    ax.bar_label(ax.containers[0])
    ax.set_ylabel('Frequency')
    fig.suptitle("Frequency over time")
    fig.savefig("static/IMG/year_plot.png")
    
    info = ''
    return metadata_df, info
