# Statement gate: blocked

Item: `S56-M-0552-STATEMENT`

Base revision: `bdfc69baefbe6cfce9a205be72f3d46cb31458e8`

## Gate decision

The exact Lean 4 target cannot be truthfully selected from the repository evidence. The only
claim-bearing source record is `Docs/researches/math_theorems.md:4093-4098`; it gives the label
"Pontryagin operation", the attribution Lev Pontryagin, the year 1947, and the gloss "stable
cohomology operations on integral cohomology". It provides no publication, theorem/page anchor,
definition, coefficient groups, degree, space category, hypotheses, or asserted law.

The closest conventional interpretation, the Pontryagin square, cannot be silently chosen. Its
usual typing has mod-2 input, mod-4 output, and doubles degree, while the metadata says integral
cohomology and stable. Pontryagin characteristic classes, the Pontryagin product, and Pontryagin
duality are distinct subjects and are excluded by the intake scope. Choosing any of these would be
a broadened or substituted theorem.

Consequently there is no justified canonical human statement, ordered binder list, Lean
declaration or expression, minimal import, normalized-expression hash, alternate encoding,
mutation suite, or boundary-case specification to elaborate. The section 5.1 statement gate fails
before proof or anchor evidence may be inspected. The provisional root remains `[H1, M4, R4]`;
this artifact claims neither statement completion nor theorem completion.

## Pinned environment inspection

The shared Lean project pins Lean `v4.29.0`, mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, and `flt-regular` revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. The worker clone's
`Formalizations/Lean/.lake` is a symlink to the canonical pinned artifacts and was not modified.
From `Formalizations/Lean`, `lake env lean --version` succeeds and reports Lean 4.29.0. A scoped
text search of the pinned sources finds Pontryagin duality APIs only, not a Pontryagin cohomology
operation. This is environment and blocker evidence, not the later anchor audit and not a basis for
inventing a target.

## Validation record

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0552` | exit 0; rank 604, L0/rework_required, lifecycle planned, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; `Lean (version 4.29.0, x86_64-unknown-linux-gnu, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740, Release)` |
| scoped `rg` for `pontryagin` spellings in pinned mathlib and `flt-regular` | exit 0; only mathlib Pontryagin-duality files matched; no cohomology-operation target found |

No `lake env lean` elaboration command is recorded for a target: there is no source-justified
expression to put in such a file. Elaborating a generic proposition or a guessed Pontryagin-square
signature would be fake statement evidence.

## Retry condition

Supply an immutable primary-source edition and exact proposition/page that resolves the operation,
coefficients, grading, domain, hypotheses, conclusion, attribution, and meaning of stability. Then
transcribe that proposition without merging variants, select the smallest import that provides its
actual primitives, elaborate it under fixed options, fingerprint the kernel expression and
environment, and run the required removed-hypothesis, changed-domain, changed-scope, and boundary
mutations.

Because the assigned deliverable did not pass its hard gate, no `.stage1-worker-selftest.json` is
created and no provisional `[_]` completion is requested.
