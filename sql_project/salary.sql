-- Table: Students
DROP TABLE IF EXISTS Students;
CREATE TABLE Students (
    StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    BirthYear INT NOT NULL,
    GroupID INT,
    FOREIGN KEY (GroupID) REFERENCES Groups(GroupID)
);

-- Table: Groups
DROP TABLE IF EXISTS Groups;
CREATE TABLE Groups (
    GroupID INTEGER PRIMARY KEY AUTOINCREMENT,
    GroupName VARCHAR(50) NOT NULL
);

-- Table: Professors
DROP TABLE IF EXISTS Professors;
CREATE TABLE Professors (
    ProfessorID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL
);

-- Table: Subjects
DROP TABLE IF EXISTS Subjects;
CREATE TABLE Subjects (
    SubjectID INTEGER PRIMARY KEY AUTOINCREMENT,
    SubjectName VARCHAR(50) NOT NULL,
    ProfessorID INT,
    FOREIGN KEY (ProfessorID) REFERENCES Professors(ProfessorID)
);

-- Table: Grades
DROP TABLE IF EXISTS Grades;
CREATE TABLE Grades (
    GradeID INTEGER PRIMARY KEY AUTOINCREMENT,
    StudentID INT,
    SubjectID INT,
    Grade INT NOT NULL,
    GradeDate DATE NOT NULL,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID)
);