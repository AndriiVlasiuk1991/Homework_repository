SELECT Professors.FirstName, Professors.LastName, AVG(Grades.Grade) AS AvgGrade
FROM Professors
JOIN Subjects ON Professors.ProfessorID = Subjects.ProfessorID
JOIN Grades ON Subjects.SubjectID = Grades.SubjectID
GROUP BY Professors.ProfessorID, Professors.FirstName, Professors.LastName
HAVING Professors.FirstName = 'Cassandra';