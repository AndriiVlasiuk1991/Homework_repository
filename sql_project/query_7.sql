SELECT Students.FirstName, Students.LastName, Grades.Grade
FROM Students
JOIN Groups ON Students.GroupID = Groups.GroupID
JOIN Grades ON Students.StudentID = Grades.StudentID
JOIN Subjects ON Grades.SubjectID = Subjects.SubjectID
WHERE Groups.GroupName = 'EVENT' AND Subjects.SubjectName = 'Take';