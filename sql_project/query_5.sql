SELECT Subjects.SubjectName
FROM Subjects
JOIN Professors ON Subjects.ProfessorID = Professors.ProfessorID
WHERE Professors.FirstName = 'Amanda';