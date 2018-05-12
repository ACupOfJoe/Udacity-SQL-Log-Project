#!/usr/bin/env python

import psycopg2

DBNAME = "news"


def execute_query(query):
    """
    execute_query takes an SQL query as a parameter,
    executes the query and returns the results as a lits of tuples

    args:
        query - (string) an SQL query statemnt to be executed.

    returns:
        A list of tuple containg the results of the query.
    """

    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        c.execute(query)
        rows = c.fetchall()
        db.close()
        return rows
    except (Exception, psyocopg2.DatabaseError) as error:
        print(error)


def get_answer_1():
    """This method opens up the news database, finds out how often each article
    has been been pathed to, orders the articles from most paths to least paths
    ,and then prints the results"""

    query = """SELECT * FROM titlecount LIMIT 3;"""
    rows = execute_query(query)
    print('{:<50} {:<30} \n').format('Article Name', '# of hits')
    for row in rows:
        print ('{:<50} {:<30}').format(row[0], row[1])
    print("\n")


def get_answer_2():
    query = """ SELECT authors.name, authoridsum.sum
                FROM authoridsum
                LEFT JOIN authors ON authors.id = authoridsum.author
                GROUP BY authors.name, authoridsum.sum
                ORDER BY authoridsum.sum DESC;"""
    rows = execute_query(query)
    print('{:<50} {:<30} \n').format('Author Name', '# of hits')
    for row in rows:
        print ('{:<50} {:<30}').format(row[0], row[1])
    print("\n")


def get_answer_3():
    query = """ SELECT day, error_count, totallogs, percentlogs as percent_error
            FROM (SELECT ROUND(error_count*100.00/totallogs, 1) as percentlogs,
            day, totallogs, error_count
            FROM (SELECT daylogs404errors.day as day, daylogs404errors.error_count
            as error_count, daylogstotal.Total_Logs as totallogs
            FROM daylogstotal LEFT JOIN daylogs404errors
            ON daylogstotal.day = daylogs404errors.day) as subquery) as subquery2
            WHERE percentlogs > 1;"""
    rows = execute_query(query)
    print('{:<40} {:<20} {:<20} {:<20} \n'
          .format('Day', '# of 404 Errors Logs', '# of Total Logs',
                  'Percent of Errors'))
    for row in rows:
        print ("{:<40} {:<20} {:<20} {:<20}"
               .format(str(row[0]), row[1], row[2], row[3]))
    print("\n")


def main():
    get_answer_1()
    get_answer_2()
    get_answer_3()

if __name__ == "__main__":
    main()
