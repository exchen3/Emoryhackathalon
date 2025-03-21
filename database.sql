use emoryhackathon;

drop table if exists tutor;

CREATE TABLE tutor (
    user_id VARCHAR(100) PRIMARY KEY,
    `password` VARCHAR(255) NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    university VARCHAR(100) NOT NULL,
    graduation_year INT NOT NULL,
    major VARCHAR(100) NOT NULL,
    employed_status BOOLEAN NOT NULL,
    internships BOOLEAN NOT NULL,
    grad_school BOOLEAN NOT NULL,
    gpa_range VARCHAR(100) NOT NULL,
    classes_teaching VARCHAR(255) NOT NULL,
    bio VARCHAR(1000) NOT NULL
);

CREATE TABLE student (
    user_id VARCHAR(100) PRIMARY KEY,
    `password` VARCHAR(255) NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    university VARCHAR(100) NOT NULL,
    graduation_year INT NOT NULL,
    major VARCHAR(100) NOT NULL,
    employed_status BOOLEAN NOT NULL,
    internships BOOLEAN NOT NULL,
    grad_school BOOLEAN NOT NULL,
    gpa_range VARCHAR(100) NOT NULL,
    classes_taking VARCHAR(255) NOT NULL,
    bio VARCHAR(1000) NOT NULL
);