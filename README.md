# Get it DONE!
A crowd sourced homework management app!

### SQL Schemas
```sqlite
create table teachers (id INTEGER, first_name TEXT, last_name TEXT, PRIMARY KEY(id));

create table courses (id INTEGER, name TEXT, PRIMARY KEY(id));

create table classes (
    id INTEGER,
    course_id INTEGER,
    teacher_id INTEGER,
    period INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);
```