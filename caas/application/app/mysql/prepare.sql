CREATE DATABASE tododb CHARACTER SET utf8mb4;
CREATE TABLE tododb.tasks (
    id int(10) unsigned NOT NULL AUTO_INCREMENT,
    item varchar(255),
    is_done boolean NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);

CREATE USER user IDENTIFIED BY 'password';
GRANT ALL ON *.* TO user;