This project uses psycopg2 to query a mock PostgreSQL database for a fictional news website. 

The news database contains three tables:
* authors
	* name - text 
	* bio -text 
	* id - integer 
* articles
	* author - integer 
	* title - text 
	* slug - text 
	* lead - text 
	* body - text 
	* time - timestamp with time zone 
	* id - integer 
* log
	* path - text 
	* ip - inet 
	* method - text 
	* status - text 
	* time - timestamp with time zone  
	* id - integer 

The python script "answers.py" answers three questions: 
	1. What are the most popular three articles of all time?
	2. Who are the most popular article authors of all time?
	3. On which days did more than 1% of requests lead to errors?


In order to run the code, you will need to have these views: 

1. CREATE VIEW titlecount AS SELECT subquery.title, COUNT(*) FROM (SELECT path, slug, articles.title FROM log LEFT JOIN articles ON path LIKE '%' || slug || '%') as subquery GROUP BY subquery.title ORDER BY COUNT(*) DESC OFFSET 1;

> This view sorts through the log table and groups the paths by article slug/title.

		
2. CREATE VIEW authortitlecount AS SELECT articles.author, articles.title, count FROM titlecount JOIN articles ON titlecount.title = articles.title;
> This view holds the author IDs, the title of the article, and the number of times each article was hit.
	
3. CREATE VIEW authoridsum AS SELECT authortitlecount.author, SUM(count) FROM authortitlecount GROUP BY author ORDER BY SUM(count) DESC;
> This view holds the author IDs and the sum of the counts of each author IDs articles.
  
4. CREATE VIEW daylogstotal AS SELECT date_trunc('day', time) as day, count(*) as Total_Logs FROM log GROUP BY day;
> This view holds then total number of logs grouped by day.


5. CREATE VIEW daylogs200ok AS SELECT date_trunc('day', time) as day, count(*) as ok_count FROM log WHERE status = '200 OK' GROUP BY day;
> This article holds the total number of 200OKs grouped by day. 
