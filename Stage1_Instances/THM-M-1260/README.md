# THM-M-1260 rev-5.6 intake

This is the planned intake dossier for the metadata label "pseudodifferential operators". The
repository's source wording, "generalization of differential operators", describes a class of
operators rather than a truth-valued theorem. It therefore does not yet determine an exact Lean 4
target. Intake preserves that ambiguity instead of substituting a convenient result about Fourier
transforms, differential operators, or symbols.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Source record | The historical development of pseudodifferential operators, dated 1965 and attributed by repository metadata to Kohn, Nirenberg, and Hormander | The metadata supplies no publication, theorem number, page, hypotheses, or conclusion |
| Operator data | A prospective symbol class, quantization convention, domain/codomain function spaces, and operator defined from that data | Every choice remains open; no one convention is canonical from the supplied wording |
| Candidate theorem families | Differential operators as a subclass; composition/symbol calculus; mapping or regularity results | These are alternatives, not conjuncts and not credited targets |
| Analytic foundations | Euclidean dimension, real/complex scalars, Schwartz/distribution or Sobolev spaces, Fourier normalization, oscillatory integrals | Must be fixed before a formal proposition can be frozen |
| Formal surface | Lean 4 plus pinned mathlib | No declaration, module, expression hash, or environment fingerprint is claimed |
| Exclusions | A mere definition of an operator, and any theorem selected only because mathlib can express it | Neither may silently replace the source claim |

The downstream statement phase must first obtain a pinpoint human source or explicitly choose and
justify a source-faithful theorem. It must then fix all parameters and conventions before Lean
elaboration. The subsequent open DAG is: exact statement, source/Lean anchor audit, obligation-tree
freeze, proof, validation, and release.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H3, M4, R4]`. The first failed gate is exact
source-statement identification. Audit completion and theorem completion are false. No historical
"verified" label, formal proof, or kernel closure is credited.

The structured authority is `intake.json`; source wording and candidate interpretations are kept in
`source_statement_crosswalk.md`. Intake validation is recorded in `validation.md`.
