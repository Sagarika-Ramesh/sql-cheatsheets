-- Sample data for every cheat-sheet example: a small online bookshop.
-- Loaded as TEMP tables in a fresh session for each query, so nothing persists in your database.
CREATE TEMP TABLE customers (customer_id int PRIMARY KEY, name text, city text, signup_date date, email text, referred_by int);
INSERT INTO customers VALUES
 (1,'Asha','Pune','2024-01-05','asha@mail.com',NULL),
 (2,'Ben','Leeds','2024-01-20','ben@mail.com',1),
 (3,'Chen','Pune','2024-02-11',NULL,1),
 (4,'Dee','Austin','2024-02-28','dee@mail.com',2),
 (5,'Eli','Leeds','2024-03-15','eli@mail.com',NULL),
 (6,'Fay','Austin','2024-03-30','fay@mail.com',4);
CREATE TEMP TABLE products (product_id int PRIMARY KEY, title text, category text, price numeric(6,2));
INSERT INTO products VALUES
 (1,'The Night Library','Fiction',18.00),
 (2,'Data Made Simple','Data',32.00),
 (3,'SQL in Pictures','Data',27.50),
 (4,'Moon Bears','Kids',12.00),
 (5,'Quiet Rivers','Fiction',15.00),
 (6,'Graph Theory Gently','Data',40.00);
CREATE TEMP TABLE orders (order_id int PRIMARY KEY, customer_id int, product_id int, qty int, amount numeric(8,2), status text, order_date timestamp);
INSERT INTO orders VALUES
 (101,1,2,1,32.00,'paid','2024-01-06 10:15'),
 (102,2,1,2,36.00,'paid','2024-01-21 14:02'),
 (103,1,4,3,36.00,'paid','2024-02-03 09:40'),
 (104,3,3,1,27.50,'refunded','2024-02-12 18:25'),
 (105,4,2,1,32.00,'paid','2024-02-29 11:00'),
 (106,2,5,1,15.00,'paid','2024-03-02 16:45'),
 (107,5,3,2,55.00,'paid','2024-03-16 08:30'),
 (108,1,1,1,18.00,'paid','2024-03-20 20:10'),
 (109,4,4,2,24.00,'pending','2024-04-02 12:00'),
 (110,3,2,1,32.00,'paid','2024-04-05 15:20');
CREATE TEMP TABLE employees (employee_id int PRIMARY KEY, name text, dept text, salary int, manager_id int);
INSERT INTO employees VALUES
 (1,'Maya','Eng',120000,NULL),(2,'Omar','Eng',95000,1),(3,'Priya','Eng',95000,1),
 (4,'Liam','Sales',70000,1),(5,'Noor','Sales',82000,4),(6,'Raj','Sales',65000,4);
CREATE TEMP TABLE logins (user_id int, day date);
INSERT INTO logins VALUES
 (1,'2024-03-01'),(1,'2024-03-02'),(1,'2024-03-03'),(1,'2024-03-04'),(1,'2024-03-06'),(1,'2024-03-07'),
 (2,'2024-03-01'),(2,'2024-03-03'),(2,'2024-03-04'),(2,'2024-03-05');
CREATE TEMP TABLE events (event_id int, data jsonb);
INSERT INTO events VALUES
 (1,'{"type":"signup","email":"asha@mail.com","address":{"city":"Pune"}}'),
 (2,'{"type":"purchase","amount":32,"address":{"city":"Leeds"}}'),
 (3,'{"type":"signup","email":"dee@mail.com","address":{"city":"Austin"}}');
CREATE TEMP TABLE posts (post_id int, title text, tags text[]);
INSERT INTO posts VALUES (1,'Joins explained','{sql,joins}'),(2,'Pandas tips','{python}'),(3,'Window magic','{sql,window}');
CREATE TEMP TABLE stock (sku text PRIMARY KEY, qty int);
INSERT INTO stock VALUES ('A1',5),('B2',0);
