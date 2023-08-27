SELECT Students.FirstName, Students.LastName
FROM Students
JOIN Groups ON Students.GroupID = Groups.GroupID
WHERE Groups.GroupName = 'EYE';