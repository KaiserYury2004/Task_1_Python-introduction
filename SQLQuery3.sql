#Для postgres
SELECT r.name, MAX(EXTRACT(year FROM AGE(CURRENT_DATE, s.birthday))) - MIN(EXTRACT(year FROM AGE(CURRENT_DATE, s.birthday))) AS Age_diff
FROM rooms r
INNER JOIN students s ON r.id = s.room
GROUP BY r.name
ORDER BY Age_diff DESC
LIMIT 5;
#Для MSSMS
SELECT TOP 5 r.name, MAX(DATEDIFF(YEAR, s.birthday, GETDATE())) - MIN(DATEDIFF(YEAR, s.birthday, GETDATE())) AS Age_diff 
FROM rooms r INNER JOIN students s ON r.id = s.room 
GROUP BY r.name 
ORDER BY Age_diff DESC 
