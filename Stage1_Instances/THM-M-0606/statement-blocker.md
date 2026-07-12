# Exact-statement gate: blocked

Item: `S56-M-0606-STATEMENT`  
Theorem: `THM-M-0606`  
Base revision: `c299e0512fb2c1371ed98a055c95169a2c981ff6`

## Decision

No exact Lean 4 target can be truthfully selected or elaborated from the authoritative repository
record. The complete repository wording is "classification of homotopy spheres," attributed to
Michel Kervaire and John Milnor in 1963. As the accepted intake records, this is an umbrella phrase,
not a unique proposition. It can denote the group of oriented smooth homotopy spheres, its
finiteness or order, the subgroup of spheres bounding parallelizable manifolds, or an exact-sequence
comparison with stable homotopy groups. These alternatives have different dimension restrictions,
equivalence relations, binders, exceptional terms, and conclusions.

The intake identifies Kervaire and Milnor, *Groups of Homotopy Spheres: I*, Annals of Mathematics
77 (1963), 504-537, DOI `10.2307/1970128`, only as an uninspected discovery candidate. The dossier
does not select a numbered result or page, transcribe its assumptions, dispose of errata, or freeze
whether classes are taken up to oriented diffeomorphism or h-cobordism. It also leaves the indexing
of `Theta_n` and `bP_(n+1)`, the stable `J`-homomorphism quotient, and the Kervaire-invariant term
open. Choosing one result or conjoining several would invent mathematics not fixed by the source
record. Replacing the classification with the existence of an exotic seven-sphere, the generalized
Poincare theorem, an order table, or an abstract classifier assumed as a parameter would substitute
or weaken the target.

Consequently the gate fails before ordered binders, a canonical expression fingerprint, minimal
imports, checked transports, or meaningful removed-hypothesis, changed-domain, binder-scope, and
boundary mutations can be established. No canonical theorem declaration, axiom, placeholder, or
proxy statement was introduced. Machine status remains `M4`; statement acceptance, audit
completion, and theorem completion are false.

## Pinned Lean boundary

`StatementProbe.lean` checks only the nearest repository-pinned mathlib surface. The module
`Mathlib.Geometry.Manifold.PoincareConjecture` supplies homotopy-equivalence and smooth-sphere
statement vocabulary, including
`ContinuousMap.HomotopyEquiv.NonemptyDiffeomorphSphere`. It does not define homotopy-sphere classes,
connected sum, or the Kervaire-Milnor classification. Its exotic-seven-sphere declaration is a
`proof_wanted` and is also explicitly excluded as a substitute by intake.

`Mathlib.Geometry.Manifold.Bordism` describes itself as only the beginnings of unoriented bordism
theory. Its TODO leaves the bordism relation, bordism groups, and ring structure unimplemented.
Pinned-mathlib searches found no connected-sum, parallelizability, stable-homotopy,
`J`-homomorphism, Kervaire, or homotopy-sphere classification declaration. Thus the probe is
infrastructure evidence only; it is not an exact Lean target and receives no statement credit.

The environment reuses the canonical pinned `.lake` artifact and was not updated, built, fetched,
or otherwise mutated.

## Validation evidence

Commands ran inside this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0606` | 0 | rank 644, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0606/StatementProbe.lean` | 0 | the five nearby homotopy-equivalence and singular-manifold declarations elaborated and printed |
| pinned-mathlib `rg` searches for Kervaire/homotopy spheres, connected sum, parallelizability, stable homotopy, and the stable `J` homomorphism | 0/1 per search | zero matching files for every searched concept; no target-specific declaration or required classification infrastructure found |
| `git diff --check -- Stage1_Instances/THM-M-0606` | 0 | no whitespace errors |

There is no applicable `lake env lean <canonical-target>.lean` command: the exact human claim is
not identified. Elaborating an abstract interface that assumes the classification would be fake
statement evidence.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact numbered
result/page, record exact wording and errata, and freeze the smooth/oriented category, equivalence
relation, dimension range, `Theta` and `bP` indexing, stable `J` quotient, and every exceptional
term. It must crosswalk those choices independently to concrete Lean definitions. A later statement
run can then encode the proposition, minimize its pinned imports, fingerprint its elaborated
expression, and run structural and boundary mutations.

The assigned phase is not genuinely self-tested to completion, so no
`.stage1-worker-selftest.json` is emitted.
