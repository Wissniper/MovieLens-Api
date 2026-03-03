# Task 1: Relational Database Design & SQLAlchemy Mechanics

## I. The "Object-Relational Impedance Mismatch"

Before writing a single line of code, you must understand the problem an ORM (Object-Relational Mapper) solves.

**The Theory:**

- **Python** is Object-Oriented (data is stored in objects with state and behavior, using pointers and graphs).
- **SQL** is Relational (data is stored in tables with flat rows and columns, using foreign keys and set theory).
- **The Mismatch:** How do you map a nested Python object into a flat SQL table? This is the "Impedance Mismatch."

**The Solution:** SQLAlchemy acts as a translation layer. It maps Python classes to SQL tables, and instances of those classes to rows.

---

## II. Database Normalization (The Interview Core)

Data Science interviews often test your knowledge of "Normal Forms."

### 1. First Normal Form (1NF)

Each column must contain atomic values (no lists or sets).

- **Generic Example:** Instead of a `tags` column containing `"python,data,sql"`, you would ideally have a separate row for each tag.

### 2. Second Normal Form (2NF)

It must be in 1NF, and all non-key attributes must be fully dependent on the primary key. This eliminates partial dependencies.

### 3. Third Normal Form (3NF)

It must be in 2NF, and there should be no "transitive dependencies."

- **Generic Example:** If a `Sales` table has `store_id` and `store_address`, the `store_address` depends on `store_id`, not the `sale_id`. To reach 3NF, you move `store_address` to a `Stores` table.

**The Data Science Trade-off:**
For **Analytics** (Data Science), we often **Denormalize** (break these rules) to 3NF or even 2NF because `JOINs` are expensive. Flat tables are faster for reading large batches of data.

---

## III. SQLAlchemy Architecture: Engine, Session, and Registry

### 1. The Engine (The Connector)

The Engine is the home of the **Connection Pool**. Creating a new connection to a database is slow (it requires a network handshake). The Engine keeps a pool of "hot" connections ready.

- **Generic Code Theory:**

```python
from sqlalchemy import create_engine
# The engine doesn't connect yet; it's "lazy."
engine = create_engine("sqlite:///example.db", pool_size=10, max_overflow=20)
```

### 2. The Declarative Base & Mapping

The `Base` class is a **Registry**. Every class that inherits from `Base` is tracked. When you run a command like `Base.metadata.create_all()`, SQLAlchemy looks through its registry and generates the SQL `CREATE TABLE` commands.

### 3. Data Types & Storage Efficiency

- **Integer (32-bit):** -2.1B to +2.1B.
- **BigInteger (64-bit):** Massive numbers. Essential for high-frequency logs or global IDs.
- **Numeric(precision, scale):** Fixed-point decimal. **Mandatory** for money (`Numeric(10, 2)`). Never use `Float` for currency due to rounding errors.

---

## IV. The Theory of Indexing (B-Trees)

Why do we add `index=True`?

**The Mechanics:**
Without an index, the database does a **Sequential Scan** (Big O: $O(N)$).
With an index, the database builds a **B-Tree** (Balanced Tree). When you search for an ID, the DB traverses the tree. This reduces search time to **Logarithmic** (Big O: $O(\log N)$).

**Interview Question:** "What is the cost of an index?"

- **Answer:** Indexes make **Read** faster but **Write** slower (the DB has to update the B-Tree every time a row is inserted) and take up extra **Disk Space**.

---

## V. Database Migrations (Alembic)

Why not just use `Base.metadata.create_all()`?

**The Theory:**
Database schema is **stateful**. If you add a column to your Python class, `create_all()` won't add it to the existing DB; it only creates tables if they don't exist.
**Alembic** provides "Version Control" for your DB. Each migration script has:

- `upgrade()`: The SQL to apply the change.
- `downgrade()`: The SQL to undo the change (rollback).

---

## VI. Advanced Concept: ACID Properties

Relational databases (like Postgres or SQLite) follow ACID:

1. **Atomicity:** "All or nothing." If a transaction has 5 steps and step 4 fails, the whole thing rolls back.
2. **Consistency:** The DB follows all rules (constraints) after the transaction.
3. **Isolation:** Concurrent transactions don't interfere with each other.
4. **Durability:** Once committed, data survives even if the power goes out.
