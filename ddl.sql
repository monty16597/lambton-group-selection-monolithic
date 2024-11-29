CREATE TABLE group_selection (
    group_id VARCHAR(255) PRIMARY KEY,
    remaining_seats INT NOT NULL
);

CREATE TABLE student_selection (
    student_id VARCHAR(255) PRIMARY KEY,
    group_id VARCHAR(255) NOT NULL,
    CONSTRAINT fk_group_selection FOREIGN KEY (group_id) REFERENCES group_selection (group_id),
    CONSTRAINT student_group_uc UNIQUE (student_id, group_id)
);