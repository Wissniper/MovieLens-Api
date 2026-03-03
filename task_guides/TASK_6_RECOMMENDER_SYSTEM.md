# Task 6: Recommender Systems & Similarity Metrics Theory

## I. The Vector Space Model (VSM)
In Data Science, we treat information as **Vectors** in high-dimensional space.

**The Theory:** 
Every movie is a "point" in space. If the space is "Comedy" and "Action," a movie like *Deadpool* might be at coordinate (0.8, 0.9). A movie like *Die Hard* might be at (0.1, 1.0).

---

## II. TF-IDF (Term Frequency-Inverse Document Frequency)
How do we turn words/genres into vectors?

### 1. Term Frequency (TF)
How many times does the word "Action" appear in this specific movie's tags?
- $TF(t, d) = \frac{\text{Count of term } t \text{ in document } d}{\text{Total terms in document } d}$

### 2. Inverse Document Frequency (IDF)
How "rare" is the word "Action" in the entire database (the "Corpus")?
- $IDF(t) = \log\left(\frac{\text{Total documents}}{\text{Documents containing term } t}\right)$

### 3. The TF-IDF Score
- $TF\text{-}IDF = TF \times IDF$

**The Strategy:** Words that appear in almost all movies (like "Movie") get a low IDF, so their TF-IDF score is zero. Words that are unique to a few movies (like "Film-Noir") get a high IDF, making them strong "features" for similarity.

---

## III. Distance Metrics: Why Cosine Similarity?
Once we have vectors, how do we measure the distance between them?

### 1. Euclidean Distance
The "straight-line" distance ($L2$ norm). 
- **The Problem:** It is sensitive to "Magnitude." If Movie A has 10 tags and Movie B has 100 tags (but they are the same tags), the Euclidean distance will be huge.

### 2. Cosine Similarity
Measures the **Angle** between the two vectors. It doesn't care about the magnitude (the number of tags), only the "direction" (the content).
- $\text{sim}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$

**Interview Answer:** "I used Cosine Similarity because it is **Scale-Invariant**. It correctly identifies that two movies with the same genre profile are similar, even if one has many more tags than the other."

---

## IV. Recommender Architectures

### 1. Content-Based Filtering
Recommends items similar to those a user has liked in the past. 
- **Advantage:** No "Cold Start" problem for items.
- **Disadvantage:** "Serendipity" is low. It only suggests what the user already likes.

### 2. Collaborative Filtering (CF)
"Users who liked X also liked Y." 
- **Advantage:** Can discover new interests for the user.
- **Disadvantage:** "Cold Start" problem for new items and new users.

---

## V. Advanced Concept: The "Cold Start" Problem
**The Concept:** When a new user joins, we have no ratings. 
**The Data Science Strategy:** 
1. Ask the user for their favorite genres (Content-Based).
2. Show them "Top Rated" movies (Popularity-Based).
3. Use **Hybrid Filtering** (combining Content + Collaborative).
