# Task 3: API Architecture & Advanced SQL Aggregation

## I. RESTful API Architecture
A **REST API** (Representational State Transfer) is a set of rules for how machines talk to each other over HTTP.

### 1. The Core Principles
- **Statelessness:** Each request from a client (the user) must contain all the information needed to understand the request. The server doesn't "remember" previous requests.
- **Client-Server Separation:** The backend handles data (logic), and the frontend handles the UI (presentation).
- **Uniform Interface:** Resources are identified by URLs (e.g., `/movies/top-rated`).

### 2. HTTP Methods
- `GET`: Retrieve data (Read).
- `POST`: Create data.
- `PUT/PATCH`: Update data.
- `DELETE`: Remove data.

---

## II. The Theory of SQL Joins
To create an "Insight" endpoint, we almost always need data from multiple tables.

### 1. Inner Join vs. Outer Join
- **Inner Join:** Returns rows only when there is a match in **both** tables.
- **Left (Outer) Join:** Returns **all** rows from the left table and any matches from the right. If there's no match, the right columns are `NULL`.

**Interview Strategy:** "When should you use a Left Join?"
- **Answer:** "When I want to see all entries, even those with no related records. For example, to find 'Movies with zero ratings,' I would Left Join Movies to Ratings and filter `WHERE ratings.id IS NULL`."

---

## III. SQL Aggregation & Filtering Logic
How does SQL process a complex query? Understanding the **Execution Order** is critical for performance tuning.

### 1. The Logical Execution Order
1. `FROM` (Get the tables)
2. `JOIN` (Combine them)
3. `WHERE` (Filter individual rows **before** grouping)
4. `GROUP BY` (Aggregate rows into groups)
5. `HAVING` (Filter groups **after** aggregation)
6. `SELECT` (Choose columns)
7. `ORDER BY` (Sort results)
8. `LIMIT` (Truncate the output)

**Example Code Theory:**
```sql
SELECT category, AVG(price) 
FROM products 
WHERE stock > 0 -- Pre-grouping filter
GROUP BY category 
HAVING AVG(price) > 50 -- Post-grouping filter
```

---

## IV. The Theory of SQL Injections & Parameter Binding
**SQL Injection** is a major security vulnerability where an attacker "injects" SQL commands through a user input field.

**The Theory:** 
- If you use an f-string: `f"SELECT * FROM users WHERE name = '{user_input}'"`
- An attacker can enter: `' OR 1=1; --`
- The resulting SQL becomes: `SELECT * FROM users WHERE name = '' OR 1=1; --'` (which returns all users).

**The Solution: Prepared Statements (Parameter Binding)**
SQLAlchemy's `text(":id")` and `params={"id": user_id}` sends the query and the data separately. The database treats the data as a literal value, not as a command.

---

## V. Advanced Concept: Explain Plans
**The Concept:** When you send a query, the Database Engine (the **Query Optimizer**) creates an "Execution Plan." 
- It decides whether to use an index or scan the whole table.
- **Interview Answer:** "If a query is slow, the first thing I do is run `EXPLAIN QUERY PLAN` to see if the DB is using the indexes I've defined."
