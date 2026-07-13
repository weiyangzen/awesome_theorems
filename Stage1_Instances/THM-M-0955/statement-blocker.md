# THM-M-0955 exact-statement gate: blocked

Item: `S56-M-0955-STATEMENT`

Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d` (tree
`0d6c1fdf06d1573c256af331c6b198e5a787af43`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0955-INTAKE` has only provisional worker
state `[_]`: `intake-receipt.json` is unaccepted, is not content-addressed, lists no accepted receipt
IDs, and binds older blueprint and execution-DAG hashes. There is no master-accepted dependency
receipt.

Independently and decisively, the exact-statement gate fails. The complete catalog claim is the
name `Bose-Chowla定理`, the attribution `Bose/Chowla`, the unexplained year `1960`, and the gloss
`Sidon集的构造`, or "construction of Sidon sets." It contains no formula, definition, ordered
binder, hypothesis, conclusion, source locator, proof boundary, correction, or erratum. Stage0
explicitly leaves exact definitions and premises open, and intake therefore freezes a null
canonical claim and null formal target.

Publisher and Crossref records identify R. C. Bose and S. Chowla, *Theorems in the additive theory
of numbers*, *Commentarii Mathematici Helvetici* 37 (1962), 141-147, DOI
`10.1007/BF02566968`. The inspected publisher access was only a subscription preview: it identifies
the `B_2` family but exposes no exact numbered theorem, incorporated definition, formula, proof
passage, correction, or erratum. Its 1962 publication date also conflicts with the catalog's 1960.
No immutable full primary text or independent source review has been admitted.

The name can denote a `B_2` Sidon construction or a general `B_h` construction. Even a `B_2` root
must choose the prime or prime-power parameter, cyclic group and its order versus an integer
interval, ordered pairs versus unordered multisets, diagonal and repeated summands, existential
versus explicit finite-field-logarithm construction, and exact cardinality, lower-bound,
optimality, or asymptotic conclusion. Choosing the familiar size-`q` cyclic construction would
therefore invent, narrow, broaden, or substitute proposition-changing mathematics.

There is no canonical Lean expression whose imports can be minimized, no expression or environment
fingerprint, no approved alternate encoding, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation. All four mutation classes are undefined, not
passed. No `Statement.lean`, theorem declaration, proof body, weakened special case, or broadened
interface was added. The root remains `[H1, M4, R4]`.

## Source And Lean Boundary

An exact statement still must select and map one source result; define the Sidon or `B_h` predicate;
fix the field, group or interval, parameters, equality and representation semantics, witness and
cardinality clauses; and resolve the smallest prime powers, `h = 0`, `h = 1`, `h = 2`, empty and
singleton sets, diagonal and swapped representations, zero residues, endpoints, and modular
wraparound. It must also preserve the ownership boundary with `THM-M-0956`, whose catalog gloss is
identical but whose attribution and construction are distinct.

The existing `IntakeProbe.lean` imports pinned Freiman-homomorphism, additive-energy, finite-field,
and cyclic-group modules. It checks six adjacent interfaces, but defines no Sidon predicate,
Bose-Chowla witness, canonical target, checked source transport, or proof body. Its four imports
cannot be certified minimal for an absent target. A bounded exact-topic search over repo-local Lean
and pinned mathlib located no Sidon, Bose-Chowla, or `B_h` target. This is narrow feasibility
evidence, not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0955` | 0 | rank 1489; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| authority and null-target assertions over the manifest, execution DAG, and `instance.json` | 0 | rank, dependency, intake `[_]`, statement `[ ]`, null canonical claim and target, and H1/M4/R4 agree |
| `git blame -L 6973,6978 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-0955/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`, while integration now records provisional `[_]`; this phase records rather than rewrites stale intake evidence |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0955/IntakeProbe.lean` | 0 | six adjacent APIs elaborated; 927 stdout bytes; SHA-256 `42fa9e5d42318c702ec5c11eb0aea0bcb387392eb8a34ca41ebac0078a5e5196`; no target or proof body declared |
| bounded exact-topic Lean search | 1, expected no relevant match | no Sidon, Bose-Chowla, `BhSet`, or `B_h` target; Unicode `b₂` matches were unrelated elliptic-curve notation and were excluded from the assessment |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured blocker
beside this report.

## Retry Condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and admit a full immutable primary or approved authoritative source, independently
select one exact `B_2` or `B_h` result, reconcile the 1960/1962 date and `THM-M-0956` ownership, and
approve every incorporated definition, ordered binder, hypothesis, conclusion, construction,
cardinality clause, proof boundary, correction, erratum, and degenerate case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
