# RAG Evaluation Results

## 1. Baseline: Local Embeddings

| Configuration | Value |
|---|---|
| Embedding model | all-MiniLM-L6-v2 |
| Embedding dimensions | 384 |
| Vector database | ChromaDB |
| Dataset records | 179 |
| LLM | Configured OpenAI chat model |
| Retrieval top-k | 3 (generation test) |

## 2. Baseline Evaluation

The initial evaluation covered six core tests.

| Test | Result |
|---|---|
| Semantic retrieval | PASS |
| Cuisine filtering | PASS |
| Calorie filtering | PASS |
| Combined filters | PASS |
| Duplicate detection | PASS |
| Generation and citations | PASS |
| **Total** | **6/6 passed** |

### Baseline observed performance

| Metric | Result |
|---|---:|
| Retrieval latency | 0.06 seconds |
| Generation latency | 2.33 seconds |
| Total latency | 2.40 seconds |

**Note:** These timings represent one warm execution and are not benchmark averages.

## 3. Latest Evaluation

The evaluation suite was expanded to include a separate dietary filtering test.

**Command:**

```bash
python -m scripts.evaluate_rag
```

### Latest test results

| Test | Result |
|---|---|
| Semantic retrieval relevance | PASS |
| Indian cuisine filtering | PASS |
| Maximum calorie filtering | PASS |
| Dietary type filtering | PASS |
| Combined metadata filtering | PASS |
| Duplicate record detection | PASS |
| LLM generation and citations | PASS |
| **Total** | **7/7 passed** |

### Latest observed end-to-end performance

| Metric | Result |
|---|---:|
| Retrieved documents | 3 |
| Retrieval latency | 4.77 seconds |
| LLM generation latency | 3.60 seconds |
| Total request latency | 8.38 seconds |

**Note:** These timings represent one execution. They are not averages and should not be directly compared with the earlier warm execution because the test conditions and execution overhead may differ.

## 4. Evaluation Summary

The latest evaluation confirms that the main application features are working:

- Semantic retrieval returns relevant food records.
- Cuisine filtering works.
- Maximum calorie filtering works.
- Dietary type filtering works.
- Multiple metadata filters can be applied together.
- Duplicate records are handled during data preparation.
- LLM generation returns responses with source citations.

The evaluation checks core functionality. Passing these tests does not guarantee that every generated recommendation or