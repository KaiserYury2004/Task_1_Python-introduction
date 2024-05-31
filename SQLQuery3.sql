#Для postgres
SELECT r.name, MAX(EXTRACT(year FROM AGE(CURRENT_DATE, s.birthday))) - MIN(EXTRACT(year FROM AGE(CURRENT_DATE, s.birthday))) AS Age_diff
FROM rooms r
INNER JOIN students s ON r.id = s.room
GROUP BY r.name
ORDER BY Age_diff DESC
LIMIT 5;
