DROP TABLE IF EXISTS tasks;

CREATE TABLE IF NOT EXISTS tasks (
    id int(10) unsigned NOT NULL AUTO_INCREMENT,
    item varchar(255),
    is_done boolean NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);
