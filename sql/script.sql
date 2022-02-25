DROP TABLE IF EXISTS Bibliography;

CREATE TABLE Bibliography ( id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
bib_id VARCHAR(255) NOT NULL, title TEXT NOT NULL, booktitle TEXT, 
month VARCHAR(50), year VARCHAR(50), address VARCHAR(255), 
publisher TEXT, url TEXT, doi VARCHAR(255), pages VARCHAR(50), 
abstract TEXT, author TEXT, editor TEXT, 
FULLTEXT (title, abstract)) ENGINE=InnoDB;

SELECT * FROM Bibliography;
SELECT COUNT(bib_id) FROM Bibliography;
SELECT COUNT(bib_id) FROM Bibliography WHERE year = 1971;
SELECT * FROM Bibliography WHERE year = 1971;
SELECT COUNT( ALL year ) FROM Bibliography;
SELECT year, count(year) AS CountOf FROM Bibliography GROUP BY year;
SELECT month, count(month) AS CountOf FROM Bibliography GROUP BY month;
SELECT * FROM Bibliography WHERE MATCH(title, abstract) AGAINST('covid' IN NATURAL LANGUAGE MODE);
SELECT year, count(year) AS CountOf  FROM Bibliography WHERE MATCH(title, abstract) AGAINST('covid' IN NATURAL LANGUAGE MODE)  GROUP BY year;
SELECT month, count(month) AS CountOf  FROM Bibliography WHERE MATCH(title, abstract) AGAINST('covid' IN NATURAL LANGUAGE MODE)  GROUP BY month;
SELECT COUNT(bib_id) FROM Bibliography WHERE MATCH(title, abstract) AGAINST('covid' IN NATURAL LANGUAGE MODE);
SELECT * FROM Bibliography WHERE MATCH(title, abstract) AGAINST('corona' IN NATURAL LANGUAGE MODE);
SELECT * FROM Bibliography WHERE MATCH(title, abstract) AGAINST('University of Stuttgart' IN NATURAL LANGUAGE MODE);
SELECT COUNT(bib_id) FROM Bibliography WHERE MATCH(title, abstract) AGAINST('University of Stuttgart' IN NATURAL LANGUAGE MODE);
SELECT * FROM Bibliography WHERE NOT abstract = '';
SELECT COUNT(bib_id) FROM Bibliography WHERE abstract = '';
SELECT COUNT(bib_id) FROM Bibliography WHERE NOT abstract = '';

