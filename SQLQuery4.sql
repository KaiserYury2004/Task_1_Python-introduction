#Для postgres и MSSMS
SELECT DISTINCT r.name
FROM rooms r 
INNER JOIN students s ON r.id = s.room 
GROUP BY r.name
HAVING COUNT(DISTINCT s.sex) > 1;
