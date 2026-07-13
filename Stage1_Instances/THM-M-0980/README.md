# THM-M-0980 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`Bennett不等式` (Bennett's inequality). The catalog supplies only the gloss
`随机变量和的尾概率` ("tail probability of a sum of random variables"), the attribution George
Bennett, the year 1962, and an untrusted `已验证` label. It supplies no citation, formula, domains,
ordered binders, hypotheses, conclusion, constants, tail convention, or boundary cases.

The bibliographic metadata for George Bennett's 1962 article *Probability Inequalities for the
Sum of Independent Random Variables* matches the catalog name, author, year, and subject. Crossref
identifies DOI `10.1080/01621459.1962.10482149`, *Journal of the American Statistical Association*
57(297), pages 33-45. The article text was not available for statement-level inspection in this
worker run, and the catalog does not cite it. This is an `E5` source-family lead only, not an
admitted exact statement, proof, or `H0` record.

## Intake result

The conventional Bennett family includes several proposition-changing choices: finite or
countable summands; identical or individual upper bounds; variance or second-moment parameters;
one-sided, lower-tail, or two-sided events; a real-valued or extended-real probability codomain;
the exact Bennett rate function and its zero-variance extension; and strict versus non-strict tail
events. Intake records these choices in `scope-map.md` but does not select one from memory.

The canonical human statement and Lean target therefore remain null. The provisional vector is
`[H1, M4, R4]`: a matching published source family is identified but its exact statement,
assumptions, proof boundary, and errata are unaudited; no source-identical usable Lean target is
credited; and no readable proof reconstruction can attach to an unfrozen root.

## Formal boundary

`IntakeProbe.lean` authenticates pinned mathlib interfaces for moment-generating functions,
Chernoff bounds, independent finite sums, and variance. Those declarations are prospective
infrastructure only. They contain no source-selected Bennett root and receive no proof credit.
A bounded exact-topic search found no separately named Bennett tail theorem in repo-local Lean or
the pinned mathlib snapshot. That search is intake discovery, not the downstream exhaustive anchor
audit and not a global absence claim.

All six downstream phases remain open in `task-dag.json`. No canonical statement, expression
fingerprint, checked transport, H0, M0, R0, accepted proof state, audit completion, theorem
completion, accepted receipt, release evidence, or master acceptance is claimed.
