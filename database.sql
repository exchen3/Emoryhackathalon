use emoryhackathon;

drop table if exists tutor;
drop table if exists student;
drop table if exists requests;

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

-- create request tutor_user_id, student_user_id,
CREATE TABLE requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    student_user_id VARCHAR(100) NOT NULL,
    tutor_user_id VARCHAR(100) NOT NULL,
    `status` ENUM('Pending', 'Accepted', 'Rejected') NOT NULL,
    message VARCHAR(1000) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_user_id) REFERENCES student(user_id),
    FOREIGN KEY (tutor_user_id) REFERENCES tutor(user_id)
);

select * from requests;

ALTER TABLE tutor
DROP COLUMN price_per_hour;

ALTER TABLE tutor
ADD COLUMN price_per_hour ENUM(
    'under 20',
    '20-30',
    '30-40',
    '40-50',
    '50-60',
    '60-70',
    '70-80',
    '80-90',
    '90-100',
    'over 100'
) DEFAULT NULL;

ALTER TABLE requests
ADD COLUMN completed BOOLEAN DEFAULT FALSE;

select * from requests;