DROP TABLE IF EXISTS friend;

CREATE TABLE friend
(
  id serial PRIMARY KEY,
  twitter varchar(15) UNIQUE NOT NULL
)
WITH (
  OIDS=FALSE
);
ALTER TABLE friend
  OWNER TO postgres;
