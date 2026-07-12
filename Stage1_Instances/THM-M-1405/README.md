# THM-M-1405 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository target named
"Sinai theorem." The catalogue supplies only Yakov Sinai, the year 1959, and the gloss
`measure entropy's generator` (`测度熵的生成子`). Its `已验证` label is explicitly untrusted and
provides no human-source or machine-proof credit.

The wording most plausibly points to the Kolmogorov-Sinai generator theorem: the entropy of a
measure-preserving transformation is computed by a generating partition. An author-written
secondary source states that result, and Sinai's 1959 paper is a credible primary-source
candidate. Intake has not inspected and independently reviewed an immutable primary text,
however, so it does not freeze that interpretation as the canonical proposition. In particular,
finite versus countable partitions, invertibility, equality modulo null sets, and entropy
conventions remain material source decisions.

The provisional root vector is `[H1, M4, R3]`. `H1` records a named published proof candidate with
an unresolved statement and assumption crosswalk; it is not `H0`. A pinned Lean probe checks only
measure-preserving, ergodic, probability-measure, sigma-algebra-generation, and finite-partition
substrates. It is not a measure-entropy definition, a generating-partition statement, or a proof.

`scope-map.md` fixes the family boundary, `source-statement-crosswalk.md` records the source
candidates and open mappings, and `task-dag.json` leaves every dependent phase open. Exact commands
and results are in `validation.md` and `intake-receipt.json`. No accepted proof state, audit
completion, or theorem completion is claimed.
