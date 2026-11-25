# Embedding Benchmark Results

**Project:** Interactive Food Search and RAG Chatbot System (Vanilla RAG)  
**Dataset size:** 179 prepared food records  
**Evaluation date:** 2026-11-24  
**Retrieval configuration:** Top-K = 5; 4 manually labelled queries; 3 warm repetitions per query

## Summary

| Metric | Local: all-MiniLM-L6-v2 | OpenAI: text-embedding-3-small |
|---|---:|---:|
| Embedding dimensions | 384 | 1536 |
| First-query latency | 16.7406 s | 4.7627 s |
| Average warm retrieval latency | 0.0444 s | 0.3891 s |
| Average Precision@5 | 0.40 | 0.70 |
| Average Recall@5 | 0.54 | 0.94 |

Local MiniLM was approximately 8.8 times faster for warm retrieval in this run. OpenAI embeddings achieved higher average Precision@5 and Recall@5 on this small, manually labelled evaluation set.

## Per-query results

| Query | Local P@5 | Local R@5 | OpenAI P@5 | OpenAI R@5 |
|---|---:|---:|---:|---:|
| I want something sweet and chocolatey | 0.40 | 0.50 | 0.80 | 1.00 |
| Suggest a traditional Indian vegetarian meal | 0.40 | 0.67 | 0.60 | 1.00 |
| Recommend a healthy snack with nuts and dried fruits | 0.80 | 1.00 | 0.80 | 1.00 |
| I want a rich and filling meal | 0.00 | 0.00 | 0.60 | 0.75 |

## Interpretation

- Local embeddings provided substantially faster warm retrieval in this environment.
- OpenAI embeddings retrieved more of the manually labelled relevant foods for these four queries.
- Both models performed well for the nuts-and-dried-fruits query.
- Local MiniLM struggled with the subjective “rich and filling” query in this sample.
- The vegetarian query returned chicken dishes with both providers. Semantic similarity alone does not enforce dietary restrictions; this requires explicit, trustworthy metadata and filtering.

## Important limitations

1. This is a preliminary evaluation with only four manually labelled queries. It is not a statistically robust comparison or proof that one embedding model is generally superior.
2. The relevance labels are manually selected and partly subjective, especially for “rich and filling.” Review them against the food records before treating the scores as ground truth.
3. The current relevance calculation uses unique food names (a set). Duplicate names therefore count once. These scores are best described as unique-name Precision@5 and Recall@5, not standard rank-sensitive precision.
4. Duplicate food names appeared in retrieval results (for example, Chocolate Lava Cake). Inspect the corresponding food IDs and record contents before deciding whether these are true duplicates or distinct records.
5. “First-query latency” includes process/model/client/network/Chroma initialization and query work; it is not a pure model-loading measurement.
6. The timing comparison reflects this machine, network, software versions, and run. Repeat under controlled conditions for stronger conclusions.
7. The benchmark measures retrieval by food-name labels. It does not prove that all nutritional, dietary, or descriptive claims are correct.

## Configuration decision

For this dataset and the current preliminary evaluation, use `text-embedding-3-small` as the preferred/default provider if its API cost and network dependency are acceptable. Keep `all-MiniLM-L6-v2` available as a local, faster, offline-capable alternative.

Do not delete either provider-specific Chroma collection. Keep provider-specific collection names so embeddings from different models are never mixed in the same collection.

