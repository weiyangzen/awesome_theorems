# THM-M-1542 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Ward correspondence named by the source as
"twistors and self-dual Yang-Mills." The source wording denotes a family of theorems, not one
fully quantified proposition. Intake therefore preserves the intended geometric correspondence
while leaving the choice of variant explicit for the dependent statement phase.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Geometric root | Correspondence between anti-self-dual connections and holomorphic twistor data | Base space, signature, compactification, structure group, regularity, and framing are not yet selected |
| Gauge side | A bundle with connection, curvature equation `F_A = -*F_A`, and gauge equivalence | Sign convention must be reconciled with the source's use of "self-dual" |
| Twistor side | Holomorphic vector bundle, reality structure, and trivial restriction to the relevant twistor lines | Rank, determinant, stability, topology, and singular objects remain open choices |
| Forward transform | Construct holomorphic data from the connection through the twistor distribution | No well-definedness or functoriality is credited |
| Inverse transform | Reconstruct a connection from the family of trivializations | No existence, regularity, or uniqueness result is credited |
| Correspondence | Both transforms descend to equivalence classes and are mutually inverse | A bijection cannot be stated exactly until both object categories are frozen |
| Formal foundation | Lean 4 plus pinned mathlib | Required twistor and gauge-theory infrastructure has not been audited |

The Ward-Takahashi identity is expressly outside this target. So are physical claims that have not
been reduced to definitions of connections, curvature, holomorphic bundles, and equivalence.
`intake.json` is the authoritative structured scope record; `source_statement_crosswalk.md` records
why the historical source does not yet determine a unique Lean target.

## Open task DAG

1. `W1542-SOURCE`: pin a precise Ward theorem variant, edition, page range, conventions, and errata.
2. `W1542-MODEL`: choose the base geometry, twistor space, structure group, regularity, and equivalences.
3. `W1542-STATEMENT`: elaborate the exact Lean proposition and record its environment fingerprint.
4. `W1542-TRANSPORT`: check convention and compactification transports rather than assuming them.
5. `W1542-ANCHOR`: audit mathlib and external Lean 4 declarations at immutable revisions.
6. `W1542-GRAPHS`: freeze proof, provenance, evidence, trust, documentation, and workflow graphs.
7. `W1542-PROOF`: implement or pin the forward/inverse constructions and composition certificates.
8. `W1542-VALIDATE`: run exact-type, axiom, provenance, hermetic replay, and independent-review gates.

These are intake tasks, not accepted proof obligations; canonical obligation IDs and denominators
must be frozen only after the exact statement is selected.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed theorem gate is
exact source/statement identification: the source title and generated summary do not fix the
geometric setting needed for one proposition. No Lean declaration, proof, or theorem completion is
claimed.

## Validation

The exact commands and results establishing manifest membership, repository-standard consistency,
JSON syntax, and dossier-local integrity are recorded in `validation.md`. These checks validate the
intake artifact only.
