import psycopg2

DBNAME = "news"


def get_answer_1():
	db = psycopg2.connect(database=DBNAME)
	c = db.cursor()
	query = "SELECT subquery.title, COUNT(*) FROM (SELECT path, slug, articles.title FROM log LEFT JOIN articles ON path LIKE '%' || slug || '%') as subquery GROUP BY subquery.title ORDER BY COUNT(*) DESC OFFSET 1 LIMIT 3;"
	c.execute(query)
	rows = c.fetchall()
	print('{:<50} {:<30} \n').format('Article Name', '# of hits')
	for row in rows:
		print ('{:<50} {:<30}').format(row[0], row[1])
	print("\n")
	db.close()
	return rows

def get_answer_2():
	db = psycopg2.connect(database=DBNAME)
	c = db.cursor()
	query = "SELECT authors.name, authoridsum.sum FROM authoridsum LEFT JOIN authors ON authors.id = authoridsum.author GROUP BY authors.name, authoridsum.sum ORDER BY authoridsum.sum DESC;"
	c.execute(query)
	rows = c.fetchall()
	print('{:<50} {:<30} \n').format('Author Name', '# of hits')
	for row in rows:
		print ('{:<50} {:<30}').format(row[0], row[1])
	print("\n")
	db.close()
	return rows

def get_answer_3():
	db = psycopg2.connect(database=DBNAME)
	c = db.cursor()
	query = "SELECT day, \"200oks\", totallogs, percentlogs FROM (SELECT ROUND(\"200oks\"*100.00/totallogs, 1) as \"percentlogs\", day, totallogs, \"200oks\" FROM (SELECT daylogstotal.day as \"day\", daylogs200ok.\"200_oks\" as \"200oks\", daylogstotal.\"Total_Logs\" as \"totallogs\" FROM daylogstotal LEFT JOIN daylogs200ok ON daylogstotal.\"day\" = daylogs200ok.\"day\") as subquery) as subquery2 WHERE percentlogs < 99.0;"
	c.execute(query)
	rows = c.fetchall()
	print('{:<40} {:<20} {:<20} {:<20} \n').format('Day', '# of 200Oks Logs', '# of Total Logs', 'Percent of Errors')
	for row in rows:
		print ("{:<40} {:<20} {:<20} {:<20}").format(str(row[0]), row[1], row[2], row[3])
	print("\n")
	db.close()
	return rows


def main():
	get_answer_1()
	get_answer_2()
	get_answer_3()

if __name__ == "__main__": main()