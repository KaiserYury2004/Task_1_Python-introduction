#Для postgres
SELECT rooms.name, AVG(EXTRACT(year FROM AGE(CURRENT_DATE, students.birthday))) AS Average_Age
FROM rooms
JOIN students ON rooms.id = students.room
GROUP BY rooms.name
ORDER BY Average_Age
LIMIT 5;
