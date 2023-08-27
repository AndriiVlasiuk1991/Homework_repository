SELECT Groups.GroupName, AVG(Grades.Grade) AS AvgGrade
FROM Groups
JOIN Students ON Groups.GroupID = Students.GroupID
JOIN Grades ON Students.StudentID = Grades.StudentID
JOIN Subjects ON Grades.SubjectID = Subjects.SubjectID
WHERE Subjects.SubjectName = 'Future'
GROUP BY Groups.GroupID, Groups.GroupName;