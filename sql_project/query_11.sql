SELECT AVG(Grades.Grade) AS AvgGrade
FROM Students
JOIN Grades ON Students.StudentID = Grades.StudentID
JOIN Subjects ON Grades.SubjectID = Subjects.SubjectID
JOIN Professors ON Subjects.ProfessorID = Professors.ProfessorID
WHERE Students.FirstName = 'Paula' AND Students.LastName = 'Donaldson'
  AND Professors.FirstName = 'Peter' AND Professors.LastName = 'Jones';
