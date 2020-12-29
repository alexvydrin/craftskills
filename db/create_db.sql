
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

/* Структура БД */

DROP TABLE IF EXISTS student;
CREATE TABLE student (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32));

DROP TABLE IF EXISTS category;
CREATE TABLE category (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, category INTEGER, name VARCHAR (32));

DROP TABLE IF EXISTS course;
CREATE TABLE course (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, category INTEGER, name VARCHAR (32));

COMMIT TRANSACTION;

/* Тестовое наполнение данными */

BEGIN TRANSACTION;

INSERT INTO student (name) VALUES ("Ivanov");
INSERT INTO student (name) VALUES ("Petrov");
INSERT INTO student (name) VALUES ("Vydrin");

INSERT INTO category (name) VALUES ("Patterns");
INSERT INTO category (name) VALUES ("Antipatterns");

/* id = 1 Patterns */
INSERT INTO course (name, category) VALUES ("Adapter", 1);
INSERT INTO course (name, category) VALUES ("Bridge", 1);
INSERT INTO course (name, category) VALUES ("Composite", 1);
INSERT INTO course (name, category) VALUES ("Decorator", 1);
INSERT INTO course (name, category) VALUES ("Facade", 1);
INSERT INTO course (name, category) VALUES ("Proxy", 1);

COMMIT TRANSACTION;

PRAGMA foreign_keys = on;
