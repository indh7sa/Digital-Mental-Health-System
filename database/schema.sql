-- Create Database

CREATE DATABASE IF NOT EXISTS mindcare_ai;

USE mindcare_ai;


-- ==========================
-- Student Table
-- ==========================

CREATE TABLE Student (

student_id INT AUTO_INCREMENT PRIMARY KEY,

name VARCHAR(100) NOT NULL,

email VARCHAR(100) UNIQUE NOT NULL,

department VARCHAR(100),

year INT,

phone VARCHAR(15),

password VARCHAR(255) NOT NULL,

profile_image VARCHAR(255),

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


-- ==========================
-- Counselor Table
-- ==========================

CREATE TABLE Counselor (

counselor_id INT AUTO_INCREMENT PRIMARY KEY,

name VARCHAR(100) NOT NULL,

email VARCHAR(100) UNIQUE NOT NULL,

specialization VARCHAR(100),

phone VARCHAR(15),

password VARCHAR(255) NOT NULL

);


-- ==========================
-- Admin Table
-- ==========================

CREATE TABLE Admin (

admin_id INT AUTO_INCREMENT PRIMARY KEY,

username VARCHAR(50) UNIQUE NOT NULL,

email VARCHAR(100) UNIQUE,

password VARCHAR(255) NOT NULL

);


-- ==========================
-- Assessment Table
-- ==========================

CREATE TABLE Assessment (

assessment_id INT AUTO_INCREMENT PRIMARY KEY,

student_id INT NOT NULL,

stress_score FLOAT,

anxiety_score FLOAT,

depression_score FLOAT,

risk_level VARCHAR(20),

assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

FOREIGN KEY (student_id)

REFERENCES Student(student_id)

ON DELETE CASCADE

);


-- ==========================
-- Mood Tracker Table
-- ==========================

CREATE TABLE Mood_Tracker (

mood_id INT AUTO_INCREMENT PRIMARY KEY,

student_id INT NOT NULL,

mood VARCHAR(30),

note TEXT,

mood_date DATE,

FOREIGN KEY (student_id)

REFERENCES Student(student_id)

ON DELETE CASCADE

);


-- ==========================
-- Emotion Detection Table
-- ==========================

CREATE TABLE Emotion_Detection (

emotion_id INT AUTO_INCREMENT PRIMARY KEY,

student_id INT NOT NULL,

input_text TEXT,

detected_emotion VARCHAR(50),

confidence_score FLOAT,

prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

FOREIGN KEY (student_id)

REFERENCES Student(student_id)

ON DELETE CASCADE

);


-- ==========================
-- Risk Prediction Table
-- ==========================

CREATE TABLE Risk_Prediction (

risk_id INT AUTO_INCREMENT PRIMARY KEY,

student_id INT NOT NULL,

stress_score FLOAT,

anxiety_score FLOAT,

depression_score FLOAT,

mood VARCHAR(30),

risk_level VARCHAR(20),

prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

FOREIGN KEY (student_id)

REFERENCES Student(student_id)

ON DELETE CASCADE

);


-- ==========================
-- Recommendation Table
-- ==========================

CREATE TABLE Recommendation (

recommendation_id INT AUTO_INCREMENT PRIMARY KEY,

student_id INT NOT NULL,

recommendation_type VARCHAR(100),

description TEXT,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

FOREIGN KEY (student_id)

REFERENCES Student(student_id)

ON DELETE CASCADE

);


-- ==========================
-- Counseling Table
-- ==========================

CREATE TABLE Counseling (

session_id INT AUTO_INCREMENT PRIMARY KEY,

student_id INT NOT NULL,

counselor_id INT NOT NULL,

appointment_date DATE,

appointment_time TIME,

status VARCHAR(30),

notes TEXT,

FOREIGN KEY (student_id)

REFERENCES Student(student_id)

ON DELETE CASCADE,

FOREIGN KEY (counselor_id)

REFERENCES Counselor(counselor_id)

ON DELETE CASCADE

);


-- ==========================
-- Emergency Alert Table
-- ==========================

CREATE TABLE Emergency_Alert (

alert_id INT AUTO_INCREMENT PRIMARY KEY,

student_id INT NOT NULL,

risk_level VARCHAR(20),

alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

alert_status VARCHAR(30),

FOREIGN KEY (student_id)

REFERENCES Student(student_id)

ON DELETE CASCADE

);