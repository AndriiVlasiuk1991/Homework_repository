SELECT Subjects.SubjectName
FROM Students
JOIN Grades ON Students.StudentID = Grades.StudentID
JOIN Subjects ON Grades.SubjectID = Subjects.SubjectID
JOIN Professors ON Subjects.ProfessorID = Professors.ProfessorID
WHERE Students.FirstName = 'Brian' AND Students.LastName = 'Bean'
  AND Professors.FirstName = 'Peter' AND Professors.LastName = 'Jones';