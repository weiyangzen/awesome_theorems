# THM-M-0012 Statement Validation

Item: `S56-M-0012-STATEMENT`
Base revision: `ec27eb0336c89f0aed87200fc7cbf03a09996597` (tree
`3fe77e381bf94ce1ed347bed17c94af25de8d543`)

## Frozen target

`Stage1Instances.THM_M_0012.FundamentalTheoremOfAlgebraTarget` says that every
`f : Polynomial Complex` outside the image of `Polynomial.C` has a root `z : Complex`. The
nonconstancy hypothesis precedes the existential root binder. The zero polynomial and every
constant polynomial are excluded; linear polynomials remain included. No monicity, irreducibility,
real-coefficient, degree-parity, or extension-field restriction is introduced.

The sole direct import is `Mathlib.Analysis.Complex.Polynomial.Basic`, the narrow pinned feature
module that owns `Complex.exists_root` and exports the statement vocabulary and transport lemmas.
The canonical target is checked equivalent both to its positive-`WithBot`-degree root shape and to
the direct evaluation-at-zero shape. The statement module does not invoke or credit
`Complex.exists_root` or any other proof of the target.

The catalog supplies no immutable primary edition, theorem/page, translation, assumption map,
errata record, or independent reviewer. This phase therefore freezes the conventional scope
selected at intake while retaining `H1`; it does not claim source-level `H0` fidelity.

## Commands and results

All commands ran inside this worker clone. Lean reused the automation-provided canonical `.lake`
symlink read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0012` | 0 | rank 1062, planned, no legacy slot, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386...ea95`, tree `bdc39a31...5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0012/Statement.lean)` | 0 | canonical target, three checked statement witnesses, four expected mutation type rejections, three boundary witnesses, axiom reports, and explicit expression elaborated |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0012/check_statement.py)` | 0 | expression SHA-256 `d14207f4...ba74`; source `fce52766...ee46`; all four mutations distinguished; pins and sole import matched |
| `python3 -B Stage1_Instances/THM-M-0012/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | expanded planned dossier, H1/M3/R4 boundary, artifact inventory, worker handoff, and six open tasks agree |
| `python3 -m json.tool` on every owned JSON and the root worker packet | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0012-pycache python3 -m py_compile ...` | 0 | both scoped Python validators compile without generating files in the owned path |
| scoped prohibited-construct scan over `Statement.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, axiom/bodyless/opaque/unsafe declaration, TODO, FIXME, or placeholder marker |
| `git diff --check -- Stage1_Instances/THM-M-0012 .stage1-worker-selftest.json` plus per-new-file checks | 0 | no whitespace diagnostics |

## Mutation and boundary policy

The removed-hypothesis mutation admits constants, the changed-domain mutation asks for real roots,
the binder-scope mutation chooses one root before every polynomial, and the boundary mutation
excludes linear polynomials. Lean rejects each mutation when offered as the canonical target, and
the validator confirms each fully explicit expression differs. Separate theorems check that zero
and every `C c` fail the antecedent while `X` satisfies it.

The three statement transports report only `propext`, `Classical.choice`, and `Quot.sound`. This is
a statement-level foundation observation, not a proof-body or full trust audit.

## Status boundary

This is provisional statement evidence pending master acceptance. Pinpoint source review, the
formal anchor and terminal proof-body provenance audit, discovery and obligation freezes, proof and
composition, readable reconstruction, hermetic replay, deterministic evidence bundling,
independent verification, release, audit completion, and theorem completion remain open.
