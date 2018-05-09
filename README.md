In order to run the code, you will need to have these views: 

1. CREATE VIEW titlecount AS SELECT subquery.title, COUNT(*) FROM (SELECT path, slug, articles.title FROM log LEFT JOIN articles ON path LIKE '%' || slug || '%') as subquery GROUP BY subquery.title ORDER BY COUNT(*) DESC OFFSET 1;
> This view sorts through the log table and groups the articles by slug/title. This is done this way because the log table sometimes has names such as "/article/goats-eat-googlesh" and "/article/goats-eat-googlesy" where these are links to the same article "goats-eat-googles" but are slightly different paths. 

		
2. CREATE VIEW authortitlecount AS SELECT articles.author, articles.title, count FROM titlecount JOIN articles ON titlecount.title = articles.title;
> This view holds the author IDs, the title of the article, and the number of times each article was hit.
	
3. CREATE VIEW authoridsum AS SELECT authortitlecount.author, SUM(count) FROM authortitlecount GROUP BY author ORDER BY SUM(count) DESC;
> This view holds the author IDs and the sum of the counts of each author IDs articles.
  
4. CREATE VIEW daylogstotal AS SELECT date_trunc('day', time) as "day", count(*) as "Total_Logs" FROM log GROUP BY "day";
> This view holds then total number of logs grouped by day.


5. CREATE VIEW daylogs200ok AS SELECT date_trunc('day', time) as "day", count(*) as "200_oks" FROM log WHERE status = '200 OK' GROUP BY "day";
> This article holds the total number of 200OKs grouped by day. 
