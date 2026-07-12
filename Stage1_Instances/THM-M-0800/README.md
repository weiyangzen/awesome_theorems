# THM-M-0800 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Ramsey
cardinal" (`拉姆齐基数`). The source inventory supplies only the gloss "properties of Ramsey
cardinals", a collective attribution, the period "20th century", and an untrusted `verified`
label. It does not state a proposition.

Even the usual partition-property definition requires choices absent from the record: whether
colorings range over all finite subsets at once or one arity at a time, the color set, whether a
single homogeneous set must work for all arities, the cardinality and infinitude conditions on the
cardinal, and the exact meaning of homogeneity. Other characterizations use measures, elementary
embeddings, or model-theoretic formulations and cannot be substituted without checked equivalence.
The word "properties" also gives no conclusion to prove.

This intake freezes that ambiguity rather than inventing a theorem. The root remains
`[H3, M4, R4]`. A pinned Lean probe confirms only that cardinal, finite-subset, and set APIs needed
for a later encoding are available; it is not a Ramsey-cardinal statement or proof. Exact checks
and the downstream boundary are recorded in `validation.md`.
