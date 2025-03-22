use emoryhackathon;

drop table if exists tutor;
drop table if exists student;

CREATE TABLE tutor (
    user_id VARCHAR(100) PRIMARY KEY,
    `password` VARCHAR(255) NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    university VARCHAR(100),
    graduation_year INT,
    major VARCHAR(100),
    employed_status BOOLEAN,
    internships BOOLEAN,
    grad_school BOOLEAN,
    gpa_range VARCHAR(100),
    classes_teaching VARCHAR(255),
    bio VARCHAR(1000),
    email varchar(100)
);

CREATE TABLE student (
    user_id VARCHAR(100) PRIMARY KEY,
    `password` VARCHAR(255) NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    university VARCHAR(100),
    graduation_year INT,
    major VARCHAR(100),
    employed_status BOOLEAN,
    internships BOOLEAN,
    grad_school BOOLEAN,
    gpa_range VARCHAR(100),
    classes_taking VARCHAR(255),
    bio VARCHAR(1000),
    email VARCHAR(100)
);

select * from emoryhackathon.student;

CREATE USER 'lynne'@'%' IDENTIFIED BY 'lynne';
GRANT ALL PRIVILEGES ON emoryhackathon.* TO 'lynne'@'%';

SELECT host FROM mysql.user;

-- create request tutor_user_id, student_user_id, 