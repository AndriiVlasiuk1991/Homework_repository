SELECT Professors.FirstName AS ProfessorFirstName, Professors.LastName AS ProfessorLastName, Students.FirstName
    AS StudentFirstName, Students.LastName AS StudentLastName, AVG(Grades.Grade) AS AverageGrade
FROM Grades
JOIN Students ON Grades.StudentID = Students.StudentID
JOIN Subjects ON Grades.SubjectID = Subjects.SubjectID
JOIN Professors ON Subjects.ProfessorID = Professors.ProfessorID
WHERE Professors.FirstName = 'Paula' AND Professors.LastName = 'Donaldson' AND Students.FirstName = 'Paula'
    AND Students.LastName = 'Donaldson'
GROUP BY Professors.FirstName, Professors.LastName, Students.FirstName, Students.LastName;
