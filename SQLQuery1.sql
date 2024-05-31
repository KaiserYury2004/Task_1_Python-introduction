SELECT r.name, COUNT(s.room) 
FROM rooms r LEFT JOIN students s ON r.id = s.room 
GROUP BY r.name
