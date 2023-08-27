SELECT Students.FirstName, Students.LastName, Grades.Grade
FROM Students
JOIN Groups ON Students.GroupID = Groups.GroupID
JOIN Grades ON Students.StudentID = Grades.StudentID
JOIN Subjects ON Grades.SubjectID = Subjects.SubjectID
JOIN Professors ON Subjects.ProfessorID = Professors.ProfessorID
WHERE Groups.GroupName = 'EYE'
  AND Subjects.SubjectName = 'Clear'
  AND Professors.FirstName = 'Amanda'
  AND Professors.LastName = 'Roy'
  AND Grades.GradeDate = (SELECT MAX(GradeDate) FROM Grades);