# Task 2: Data Engineering & The ETL Pipeline

## I. The ETL Lifecycle: A Theoretical Overview

**ETL (Extract, Transform, Load)** is the primary workflow for moving data from source systems to a target system (like a Data Warehouse or an API Database).

---

## II. Step 1: Extract (The Source)

**Extraction** is the process of retrieving data from sources (APIs, Databases, Files).

**Challenges:**

- **Rate Limiting:** If extracting from an API.
- **Data Integrity:** What if the CSV file is corrupted?
- **Incrementality:** Should you extract all data every time, or just the data that changed since the last run? (The "Last Modified" strategy).

---

## III. Step 2: Transform (The Core of Data Science)

Transformation is where "Cleaning" happens.

### 1. The Strategy: Vectorization over Iteration

**The Rule:** In Data Science, never iterate over rows in a for-loop.

- **Iteration:** $O(N)$ and slow (thousands of calls to the DB or disk).
- **Vectorization:** Leveraging CPU/GPU SIMD instructions (Single Instruction, Multiple Data). This is why Pandas/NumPy are fast.

**Example Theory:**

```python
# Iteration (BAD)
for row in df:
    if row['age'] > 20:
        row['category'] = 'adult'

# Vectorization (GOOD)
import numpy as np
df['category'] = np.where(df['age'] > 20, 'adult', 'minor')
```

### 2. Handling Missing Data (Imputation)

- **Deletion:** Removing rows with missing data (Loss of information).
- **Mean/Median Imputation:** Replacing missing values with average (Distorts variance).
- **Predictive Imputation:** Using a model to predict the missing value (Advanced).

---

## IV. Step 3: Load (The Target)

Loading data into the database.

### 1. Insert Strategies: Row-by-Row vs. Bulk

- **Row-by-Row:** The DB must parse the SQL, open a transaction, write, and commit for every single row.
- **Bulk Insert:** Sending a single massive binary block of data. SQLAlchemy's `df.to_sql()` uses high-performance bulk-insert mechanics.

### 2. The Concept of Idempotency

**Idempotency** is a crucial engineering concept. An operation is idempotent if running it multiple times has the same effect as running it once.

- **Non-idempotent:** Your ETL script duplicates all movies every time it runs.
- **Idempotent:** Your script checks if a movie exists before inserting, or uses a "Truncate and Load" strategy (`if_exists='replace'`).

---

## V. Validation & "Data Quality" (DQ)

In production, we use **Data Contracts**.

- **Expectation:** "The `rating` column must be between 0.5 and 5.0."
- **Check:** `assert df['rating'].between(0.5, 5.0).all()`
- **Interview Answer:** "I built data validation checks into my ETL script to ensure we don't load 'trash' data into our source-of-truth database."

---

## VI. Advanced Concept: ACID vs. BASE

When you load data, you're interacting with the DB's storage engine.

- **ACID:** (Relational DBs) Atomicity, Consistency, Isolation, Durability. Strict rules.
- **BASE:** (NoSQL DBs like MongoDB) Basically Available, Soft state, Eventually consistent. Faster, but "Consistency" might take a few seconds to propagate.
