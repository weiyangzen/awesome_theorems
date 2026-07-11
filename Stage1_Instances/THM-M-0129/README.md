# THM-M-0129 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Shimura lifting theorem. The short legacy
label "modular-form lifting" is not precise enough to silently choose among the original lift,
level refinements, plus-space correspondence, and eigenform corollaries. This intake selects the
classical coefficient-defined Shimura lift as the root family while keeping convention-sensitive
level, character, parity, and normalization choices open for the source and statement gates.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | half-integral cusp form to weight-`2k` Shimura lift, including coefficient formula and Hecke compatibility | Exact source variant and normalized Lean expression remain open |
| Source objects | half-integral weight, level, character, cusp condition, squarefree parameter, Fourier coefficients | None is represented by a credited bundled Lean object yet |
| Target objects | integral-weight modular/cusp form, target level and character, q-expansion | Existing mathlib ordinary cusp-form API is only a candidate target interface |
| Construction | divisor-sum coefficient definition and proof of modularity/cuspidality | Proof architecture and obligation registry belong to later phases |
| Hecke branch | compatibility away from the level and eigenform consequences | Operator normalizations and bad-prime behavior require exact crosswalks |
| Exclusions | bare existence of a zero cusp form; period/width lemmas; Kohnen correspondence treated as the root | These do not imply the canonical theorem |
| Foundations | Lean 4 kernel with versioned complex analysis, modular-form, character, and arithmetic dependencies | Environment and trust fingerprints remain open |

The historical file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_047.lean` is discovery input.
Its `StatementShape` stores the essential transformation and coefficient claims as unconstrained
`Prop` fields and omits the squarefree parameter and exact formula. It therefore receives no
statement or proof credit.

## Open task DAG

1. `S56-M-0129-STATEMENT`: select and elaborate one exact primary-source convention, including all
   level, parity, character, coefficient, and operator normalizations; mutation-test its scope.
2. `S56-M-0129-ANCHOR_AUDIT`: audit pinned mathlib and external Lean 4 candidates without treating
   ordinary modular-form infrastructure as terminal closure.
3. `S56-M-0129-OBLIGATION_TREE`: freeze typed construction, modularity, cuspidality, coefficient,
   Hecke, provenance, trust, documentation, and workflow obligations.
4. `S56-M-0129-PROOF`: implement or immutably integrate exact proof bodies.
5. `S56-M-0129-VALIDATION`: run exact-type, kernel, axiom, provenance, composition, hermetic, and
   independent checks.
6. `S56-M-0129-RELEASE`: reconcile accepted evidence and decide theorem completion.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact statement gate: there is no accepted source-variant selection, elaborated expression
hash, environment fingerprint, checked transport, or mutation result. The theorem is not complete.

The commands in `validation.md` establish manifest membership, standard consistency, dossier JSON
syntax, and local reference integrity only.
