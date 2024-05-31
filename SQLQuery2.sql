SELECT r.name, AVG(EXTRACT(year FROM AGE(CURRENT_DATE, s.birthday))) AS Average_Age
FROM rooms r
JOIN students s ON r.id = s.room
GROUP BY r.name
ORDER BY Average_Age
LIMIT 5;
