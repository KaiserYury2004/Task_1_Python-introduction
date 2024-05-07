#Для postgres и MSSMS
SELECT rooms.name, COUNT(students.id) 
FROM rooms LEFT JOIN students ON rooms.id = students.room 
GROUP BY rooms.name
