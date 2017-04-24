CREATE TABLE IF NOT EXISTS 
user2(
    id SERIAL PRIMARY KEY,
    fname char(80),
    lname char(80),
    gender char(10),
    age integer,
    uname char(80),
    password char(300)
);