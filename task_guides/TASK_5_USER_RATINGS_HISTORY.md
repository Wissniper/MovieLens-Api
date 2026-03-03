# Task 5: Time-Series Analysis & SQL Window Function Theory

## I. The Theory of Window Functions
**Window Functions** (Analytical Functions) are a "Senior SQL" skill.

### 1. The Core Concept: The "Frame"
Unlike `GROUP BY`, which aggregates rows into a single value, a window function defines a **Frame** (a sliding window of rows) that is relative to the current row.

**The Theory:** 
- `OVER (PARTITION BY ...)` defines the **groups** (the "window").
- `ORDER BY ...` defines the **sequence** of rows within the window.
- `ROWS BETWEEN ...` defines the **boundaries** of the frame.

### 2. Moving Average Theory (Smoothing)
A moving average is a type of **Low-Pass Filter**. It "filters" out high-frequency noise (outliers) and preserves the low-frequency trend (the signal).

**Generic Example Theory:** 
- A user rates 5, 5, 1, 5, 5. 
- The 1 is an outlier. 
- A "Moving Average of 3" would show: `5.0 -> 5.0 -> 3.6 -> 3.6 -> 3.6`. 
- The sudden drop is "smoothed" out.

---

## II. Cumulative vs. Sliding Windows

### 1. Cumulative Windows (Running Totals)
Used to calculate "Total sales to date."
- `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

### 2. Sliding Windows (Moving Averages)
Used to calculate "Average of the last 7 days."
- `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`

---

## III. Time-Series Data in Databases

### 1. Unix Epoch vs. ISO 8601
- **Unix Epoch (Integer):** 1709424000. Fast to sort, easy to calculate differences (e.g., `t2 - t1`).
- **ISO 8601 (String):** "2024-03-03T00:00:00Z". Human-readable, standard in APIs.

**The Strategy:** Store as integers for performance; convert to strings in the API for readability.

### 2. Time-Series Sampling
**The Theory:** "Downsampling" is the process of reducing the frequency of data points.
- **Generic Example:** If you have 1 rating every second, you might downsample to 1 rating every hour by taking the `MEAN`.

---

## IV. Interview Question: "Explain a Window Function"
**Interview Mastery:** 
"A window function allows me to perform calculations across a set of rows while keeping the individual rows intact. In `GROUP BY`, if I have 100 rows, I might get back 1 summary row. In a window function, if I have 100 rows, I get back 100 rows, each with its own contextual calculation."

---

## V. Advanced Concept: Non-Stationary Data
**The Concept:** A time-series is **Stationary** if its statistical properties (mean, variance) are constant. 
- **The Data Science Insight:** Moving averages are used to identify **Trends** (a change in the mean) or **Seasonality** (periodic patterns). If a user's moving average is always increasing, their data is non-stationary.
