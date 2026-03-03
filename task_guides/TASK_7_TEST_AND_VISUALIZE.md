# Task 7: Data Visualization & Testing Theory

## I. Data Visualization Principles
As a Data Scientist, your goal is to **Communicate Insights**, not just show data.

### 1. The Tufte Principles
- **Maximize Data-Ink Ratio:** Remove anything that doesn't represent data (like heavy grids or 3D effects).
- **Avoid Chart-Junk:** Don't use fancy icons or complex themes that distract from the main trend.

### 2. Visualization Types for APIs
- **Bar Charts:** Compare categorical data (e.g., average rating per genre).
- **Line Charts:** Show changes over time (e.g., user rating history).
- **Scatter Plots:** Show relationships between two variables (e.g., movie count vs. average rating).

---

## II. The Theory of Testing in Data Science
Why test code if it "looks" correct?

### 1. The "Silent Failure" Problem
In standard software, a bug crashes the app. In Data Science, a bug might just return a "Wrong Number."
- **Example:** A join that duplicates rows will double your "Total Sales" without throwing an error.

### 2. The Pyramid of Testing
- **Unit Tests:** Test a single small function (e.g., your TF-IDF math).
- **Integration Tests:** Test how components work together (e.g., API -> DB -> Pandas).
- **End-to-End (E2E) Tests:** Test the entire system from the user's perspective.

**The Strategy:** Focus on **Integration Tests** for this project to ensure the data flows correctly.

---

## III. Test Isolation & Mocking
How do you test a database without modifying your real data?

### 1. In-Memory Databases
Use a temporary SQLite database (`sqlite:///:memory:`) that only exists during the test run.

### 2. Mocking
Replace a complex component (like an external API) with a "Fake" one that returns a predictable response.

---

## IV. Interview Mastery: "How do you test a Data Pipeline?"
"I use a 3-step approach:
1. **Schema Validation:** Ensure the data has the right columns and types.
2. **Value Validation:** Ensure values are in a reasonable range (e.g., ratings between 0.5 and 5.0).
3. **Integration Testing:** Call the API with known test data and verify that the output matches a 'Golden Dataset' (pre-calculated expected results)."

---

## V. Advanced Concept: Data Drift
**The Concept:** A model's performance might drop over time as the real-world data changes. 
- **The Data Science Insight:** We use "Monitoring" to detect **Data Drift** (when the distribution of incoming data shifts away from what the model was trained on).
- **Generic Example:** If a news event makes "Documentary" movies more popular, our recommender might need to be retrained.
