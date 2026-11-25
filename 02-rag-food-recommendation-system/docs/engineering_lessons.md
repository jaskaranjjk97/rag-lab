# Engineering Lessons & Troubleshooting

While building this Vanilla RAG project, I faced several issues related to data preparation, ChromaDB, retrieval, testing, and Python environment configuration.

This document records what went wrong, why it happened, how I fixed it, and what I learned from each issue.

## 1. Semantic Similarity Does Not Guarantee Constraint Satisfaction

**Problem:**

During testing, I asked the system:

> Show me non-vegetarian options. List me 4 options.

The dietary filter was disabled, so the retriever searched across the entire food collection.

Although the query specifically requested non-vegetarian food, the retrieved results also included vegetarian records. The LLM could recommend only one non-vegetarian option from the retrieved context.

**Why it happened:**

Semantic search finds records that are similar in meaning to the user's query. It does not automatically enforce requirements such as vegetarian or non-vegetarian classification.

**How I fixed it:**

I added dietary classification to the food metadata and connected it to the ChromaDB retrieval filter.

When the user selects the non-vegetarian filter, ChromaDB applies:

```python
{
    "dietary_type": {
        "$eq": "non_vegetarian"
    }
}
```

This restricts the search to records classified as non-vegetarian.

**Result:**

With the filter enabled, the system retrieved four non-vegetarian options:

- Chicken Dum Biryani
- Beef Stew
- Chicken Tikka Masala
- Pad Thai

Without the filter, only one matching option was available in the retrieved context.

**What I learned:**

- Semantic search finds relevant information.
- Metadata filters help enforce specific requirements.
- Combining both makes retrieval more useful when users have clear constraints.

## 2. Combined Metadata Filters Were Not Working Together

**Problem:**

When I applied multiple filters, such as cuisine and maximum calories, the system did not apply all the selected conditions together.

**Why it happened:**

I initially used `elif` statements to build the filter conditions.

When a cuisine filter was provided, the calorie condition was skipped because the `elif` branch was not checked.

**How I fixed it:**

I replaced the dependent `elif` statements with independent `if` statements.

This allowed the system to collect all selected conditions and combine them using ChromaDB's `$and` operator.

**What I learned:**

- Use independent conditions when multiple filters can be active at the same time.
- Test individual filters as well as combinations of filters.
- A filter working on its own does not mean combined filtering is working correctly.

## 3. Duplicate IDs During ChromaDB Ingestion

**Problem:**

The food dataset contained duplicate food IDs. This could cause records to overwrite each other when they were added to ChromaDB.

**Why it happened:**

The duplicate ID counter used a fixed dictionary key instead of the original ID variable.

As a result, the counter did not correctly track occurrences of each original ID.

**How I fixed it:**

I added a counter for each original ID and used it to generate unique IDs for ChromaDB.

**What I learned:**

- Database IDs should be unique.
- Source datasets can contain duplicate identifiers.
- Check ID uniqueness before adding records to a vector database.

## 4. Python Function Return-Order Mismatch

**Problem:**

Documents, metadata, and IDs were assigned incorrectly when unpacking the values returned by a function.

**Why it happened:**

The order of values returned by the function did not match the order expected by the calling code.

**How I fixed it:**

I made the return order consistent between the data preparation function and the code that calls it.

**What I learned:**

Always check what a function returns and keep its return order consistent across modules.

## 5. ChromaDB API Compatibility

**Problem:**

I encountered errors while using ChromaDB methods and configuring the vector store.

**Why it happened:**

Some method names and API usage did not match the installed ChromaDB version.

**How I fixed it:**

I checked the installed ChromaDB version and inspected the available method names and constructor parameters.

**What I learned:**

- Different library versions can have different APIs.
- Check the installed version when an API call fails.
- Verify method names and parameters instead of assuming they are correct.

## 6. Incorrect Retrieval Response Key

**Problem:**

A `KeyError` occurred when accessing the distance values returned by ChromaDB.

**Why it happened:**

I used `distance` instead of the actual response key `distances`.

**How I fixed it:**

I corrected the key used to access the returned distance values.

**What I learned:**

When working with a third-party library, inspect its response structure before accessing values.

## 7. Incorrect Assertion in Retrieval Tests

**Problem:**

A calorie-filter test was passing an assertion that did not actually check every retrieved result.

**Why it happened:**

I used a generator expression without wrapping it in `all()`.

This meant the test was not checking that every result satisfied the calorie condition.

**How I fixed it:**

I used `all()` to check the condition for every retrieved record and added checks to make sure the result list was not empty.

**What I learned:**

Tests can also contain mistakes. Make sure the test checks the actual requirement, not just that some result looks correct.

## 8. Python Interpreter Mismatch in VS Code

**Problem:**

VS Code showed unresolved imports even though the required packages were installed in the virtual environment.

**Why it happened:**

VS Code was using a different Python interpreter from the one used in the terminal.

**How I fixed it:**

I selected the correct Python interpreter in VS Code.

I also used the following command to check which Python executable was active:

```python
import sys

print(sys.executable)
```

**What I learned:**

The terminal and code editor should use the same Python environment. Always check the active interpreter when imports behave unexpectedly.

## 9. Separating Ingestion from Retrieval

**Problem:**

The original workflow had document indexing and retrieval logic too closely connected.

This made it harder to understand which part of the application was responsible for preparing the data and which part handled user queries.

**How I improved it:**

I separated the ingestion and retrieval workflows.

- **Ingestion:** Loads the food dataset, prepares documents and metadata, generates embeddings, and stores records in ChromaDB.
- **Retrieval:** Takes a user query, applies the selected filters, and retrieves matching records from ChromaDB.

**What I learned:**

Data preparation and indexing are different from answering user queries. Keeping them separate makes the code easier to understand, test, and maintain.

---

## Final Takeaways

These issues helped me understand some important parts of building a RAG application:

1. Semantic search and metadata filtering solve different problems.
2. Multiple filters must be combined correctly.
3. Data should be checked before inserting it into a vector database.
4. Functions should have clear and consistent return values.
5. Library APIs should be checked against the installed version.
6. Tests must verify the actual expected behaviour.
7. Python environments should be configured consistently.
8. Ingestion and retrieval should have separate responsibilities.

These lessons came from problems I actually faced while developing and testing this project.