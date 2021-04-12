create table teachers (id INTEGER, first_name TEXT, last_name TEXT, PRIMARY KEY(id));

create table topics (
    id INTEGER,
    name TEXT,
    PRIMARY KEY (id)
);

create table courses (
    id INTEGER,
    name TEXT,
    topic_id INTEGER,
    PRIMARY KEY(id),
    FOREIGN KEY (topic_id) REFERENCES topics(id)
);

create table classes (
    id INTEGER,
    course_id INTEGER,
    teacher_id INTEGER,
    period INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

create table work (
    id INTEGER,
    class_id INTEGER,
    created_on DATE DEFAULT CURRENT_TIMESTAMP,
    due_by DATE DEFAULT CURRENT_TIMESTAMP,
    name TEXT,
    description TEXT,
    url TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (class_id) references classes(id)
);