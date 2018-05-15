CREATE VIEW titlecount  
AS SELECT title, COUNT(*) as count 
FROM articles LEFT JOIN log 
ON log.path = concat('/article/', articles.slug) 
GROUP BY title
ORDER BY count
DESC;

CREATE VIEW authortitlecount 
AS SELECT articles.author, articles.title, count 
FROM titlecount JOIN articles 
ON titlecount.title = articles.title;

CREATE VIEW authoridsum AS 
SELECT authortitlecount.author, SUM(count) 
FROM authortitlecount 
GROUP BY author 
ORDER BY SUM(count) DESC;

CREATE VIEW daylogstotal AS 
SELECT date_trunc('day', time) as day, 
count(*) as Total_Logs 
FROM log GROUP BY day;

CREATE VIEW daylogs404errors 
AS SELECT time::date AS day, count(*) as error_count FROM log 
WHERE status = '404 NOT FOUND' GROUP BY day;