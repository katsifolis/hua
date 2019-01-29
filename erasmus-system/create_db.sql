CREATE TABLE users(username TEXT, password TEXT, courses integer, year integer, language TEXT, uni1 text, uni2 text, uni3 text, type_of_user TEXT);
CREATE TABLE uni(name text, acceptances number, language TEXT);
CREATE TABLE submissions(uni TEXT, total_submits NUMBER, accepted NUMBER, remaining NUMBER);

/* Users */

insert into users values('vasilis', '0000', 30, 3, 'polish', 'uni of poland', 'uni of paris', 'uni of spain');
insert into users values('petran', '1111', 32, 4, 'bulgarian', 'uni of bulgaria', 'uni of paris', 'uni of germany');
insert into users values('kapalfa', '420', 28, 6, '', 'uni of ukraine', 'uni of paris', 'uni of spain');
insert into users values('afroxulanth', '4444', 20, 4, 'german', 'uni of germany', 'uni of paris', 'uni of spain');

/* Universities */
insert into users values('uni of poland', 5, 'polish');
insert into users values('uni of germany', 3, 'german');
insert into users values('uni of paris', 4, 'french');
insert into users values('uni of italy', 3, 'italian');
insert into users values('uni of london', 6, 'english');
insert into users values('uni of norway', 2, 'norwegian');

/* Submittances */
insert into users values('uni of poland', 0, 0, 5);
insert into users values('uni of germany', 0, 0, 3);
insert into users values('uni of paris', 0, 0, 4);
insert into users values('uni of italy', 0, 0, 3);
insert into users values('uni of london', 0, 0 6);
insert into users values('uni of norway', 0, 0, 2);
