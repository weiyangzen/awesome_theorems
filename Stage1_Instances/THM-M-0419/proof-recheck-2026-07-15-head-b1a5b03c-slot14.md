# THM-M-0419 proof-phase recheck at base b1a5b03c

Item: `S56-M-0419-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `b1a5b03c9eb85b0777b34f58df31029086acf260`

Base tree: `cb7fc5c4df1ed6cf6b1024492bf35bfa524a580b`

## Verdict

`blocked` at the exact root, with one self-tested partial proof body proposed
for provisional acceptance.

The dependency gate fails first: `S56-M-0419-OBLIGATION_TREE` is provisional
`[_]`, not master-accepted `[x]`. Independently, the mathematical proof
frontier remains open. The exact target is `Stage1.THM_M_0419.Statement`:
every number field `K` that is abelian Galois over `Q` embeds over `Q` into
some `CyclotomicField n Q` with `n != 0`.

There is no placeholder-free body for `LocalInductionPackage`, which requires
the local degree induction, complementary fixed-field reduction, and local
cyclotomic-compositum construction. No body inhabits the tame, odd-wild, or
2-adic-wild branch packages, and `GlobalizationPackage` is also uninhabited.
The frozen minimal mathematical proof cut is:

```text
M0419-B-INDUCTION
M0419-L-TAME
M0419-L-WILD-ODD
M0419-L-WILD-TWO
M0419-T-GLOBAL
```

`Proof.lean` now implements the intended
`M0419-C-CYCLOTOMIC-IDENTIFY` transport. Its local declaration maps an
abstract positive containment witness in a singleton cyclotomic extension to
the exact `ObligationTree.PositiveContainmentTarget`, using pinned mathlib's
`IsCyclotomicExtension.algEquiv` and composing its `AlgHom` with the supplied
embedding. A trust-zero replay checks the wrapper and upstream terminal
declaration with exactly `propext`, `Classical.choice`, and `Quot.sound`.

The obligation's frozen fingerprint is a `planned-v1` signature hash rather
than an elaborated Lean expression. Accordingly the receipt records a
candidate provisional closure for this node, not accepted closure; independent
master review must accept the checked interface mapping. This transport does
not remove any member of the five-node minimal root cut, and the root remains
`M3`.

A fresh trust-zero replay checked the exact statement and the conditional
interfaces in `ObligationTree.lean`. Those interfaces retain all substantive
mathematical packages as explicit premises. Returning `root_of_packages`, or
declaring a missing package as an axiom or bodyless constant, would substitute
a conditional theorem or prohibited placeholder for the requested root.

Pinned mathlib provides cyclotomic fields, the easy cyclotomic-to-abelian
direction, p-adics, fixed fields, conductor-adjacent APIs, and ramification
infrastructure. Exact-name and package searches of all 9,008 mathlib Lean
files and all 9,676 pinned-package Lean files found no converse, class-field
or global-reciprocity bridge, or inhabitant of the five open packages.

The existing local mathlib Git object store contains
`refs/remotes/origin/KroneckerWeber` at immutable commit
`0aaa73fbf982736ed441b55a3a067383b184e342`. This is an unfinished Lean
`4.17.0-rc1` development, not a closure candidate: its 18 Kronecker-Weber
files have 16 textual `sorry` matches in substantive compositum and odd-prime
work, `TamelyRamified.lean` ends with the bodyless declaration `def foo`, and
no terminal theorem exists. It was inspected without checkout, fetch, build,
or dependency mutation and receives zero proof credit. The audited Atlas
candidate at commit `34ffed396f376454c1a9b297f3fd74c5c801fb50`
likewise has 22 `sorry` occurrences and receives zero proof credit.

A partial proof body, proof-phase record, provisional receipt, checker, and
self-test handoff were added. No accepted obligation closure, dependency,
frozen graph, or scheduler authority changed. Lifecycle stays `planned`; the
accepted root vector stays `[H1, M3, R3]`; `audit_complete=false` and
`theorem_complete=false`.

## Scoped validation

All commands ran in this worker clone using the existing pinned Lake closure.
The automation-provided untracked `Formalizations/Lean/.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
checkout, network request, or `.lake` mutation ran. Temporary Lean objects
and logs were written under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}` | 0 | Commit `b1a5b03c9eb85b0777b34f58df31029086acf260`; tree `cb7fc5c4df1ed6cf6b1024492bf35bfa524a580b`. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0419` | 0 | Rank 74; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0419/check_anchor_audit.py` | 0 | The negative boundary, 13 Lean probes, mathlib pin, and external placeholder classification agree. |
| `python3 -B Stage1_Instances/THM-M-0419/check_obligation_tree.py` | 1 | The historical prerequisite validator stopped at its hardcoded original base `80f0191c...`, not current HEAD `b1a5b03c...`; no pass is claimed. |
| Isolated `lake env` resolved `lean --trust=0 -t0` replay | 0 | `Statement.lean` and `ObligationTree.lean` elaborated; conditional declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `bash Stage1_Instances/THM-M-0419/check_proof.sh` | 0 | The exact statement, obligation interfaces, and partial transport elaborated at trust zero; the wrapper and `IsCyclotomicExtension.algEquiv` reported exactly the allowed three axioms. |
| `python3 Stage1_Instances/THM-M-0419/check_proof.py` | 0 | Current base/tree, frozen hashes and planned fingerprint, candidate-only closure boundary, root cut, receipt/self-test agreement, and prohibited-device scan passed. |
| Exact-name and structural searches over repo-local and pinned Lean sources | expected no-match | No eligible exact proof, missing-package inhabitant, or global-reciprocity bridge was found. |
| Read-only inspection of mathlib ref `origin/KroneckerWeber` | 0 | Commit `0aaa73fb...` uses Lean `4.17.0-rc1`; 18 files have 16 textual `sorry` matches, a bodyless `def foo`, and no root theorem. |
| Environment, pin, tree, and package-cleanliness checks | 0 | Lean `4.29.0` (`98dc76e3...`), Lake `5.0.0-src+98dc76e`, mathlib `8a178386...` tree `bdc39a31...`, and flt-regular `56161b6e...` tree `32c9eace...`; both dependency worktrees were clean. |
| Frozen-input SHA-256 inspection | 0 | Statement, obligation, graph, pin, standard, manifest, and skill hashes were recorded in the paired JSON blocker. |
| `python3 -m json.tool` on proof-phase, receipt, blocker, and worker JSON plus the fail-closed proof checker | 0 | All records parse; identity, base/tree, eight changed paths, frozen hashes and planned fingerprint, candidate-only closure boundary, unchanged root cut/vector, receipt/self-test agreement, and prohibited-device scan pass. |
| `git diff --check -- Stage1_Instances/THM-M-0419 .stage1-worker-selftest.json`; new-file `git diff --no-index --check` | 0 / expected difference 1 | No whitespace diagnostics; the partial-proof self-test proposes only worker state `[_]`. |

The initial isolated replay used the Lake-resolved Lean executable and
`LEAN_PATH`, compiled from the owned target directory to a temporary
`Statement.olean`, prepended that temporary directory to `LEAN_PATH`, and then
compiled `ObligationTree.lean`. The statement stdout SHA-256 was
`d30ce90a242e9fe3900ec73e893184ad8878c5b90f5362a4f70ca3846342faeb`;
the obligation stdout SHA-256 was
`043ffeecbbd1d4b2f7574df4f0f23210d621e68982a2dab5d43773224b695a71`.
The temporary object hashes were respectively
`8aee5f584463bc1ac33c8498c2f45fd22a1002cb896905edc5535c3d345c4846`
and `7e0bdad9fee75626155511e7ad1b61da2d93eb3c06e2072208d36ffbc5094f3f`.

## Retry condition

First obtain master acceptance of `S56-M-0419-OBLIGATION_TREE`. Resume
positive proof work only after placeholder-free implementations of the five
minimal-cut packages and their frozen dependencies exist in the pinned
closure, or after an immutable, compatible, lawfully reusable no-placeholder
Lean 4 terminal proof is pinned/imported, exactly transported to the unchanged
target, and checked. Until then the item remains `[ ]`; validation, release,
master acceptance, `AUDIT-Z`, and `THEOREM-Z` remain open.
