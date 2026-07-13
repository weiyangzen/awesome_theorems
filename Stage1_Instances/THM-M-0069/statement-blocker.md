# Exact-statement gate: blocked

Item: `S56-M-0069-STATEMENT`

Theorem: `THM-M-0069`

Base revision: `0d2c3bdcd192266bc255ac3d5186da604517145a` (tree
`eafbcb48efd51d9cda34f0fc1afe780434abad64`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0069-INTAKE` has provisional state `[_]`
in the authoritative execution DAG, not master-accepted state `[x]`. Dependency-ordered inspection
can proceed from that predecessor, but its worker receipt is unaccepted and non-content-addressed,
has no accepted receipt ID, and deliberately leaves the canonical mathematical statement and Lean
target null. Master acceptance remains required before any later statement transition can be
accepted.

Independently, the exact-statement gate fails at source identity. The repository supplies only the
gloss `p^a q^b`-order groups are solvable, with William Burnside and 1904 as metadata. It does not
bind finiteness, say that `p` and `q` are primes or distinct, choose the domains and zero policy for
`a` and `b`, define group order, fix the multiplication orientation or ordered binders, or select a
solvability convention. The untrusted `已验证` catalog label supplies none of those clauses.

Crossref metadata identifies W. Burnside, "On Groups of Order p-alpha q-beta," *Proceedings of the
London Mathematical Society* s2-1(1), 1904, pages 388-392, DOI
`10.1112/plms/s2-1.1.388`. The intake could not admit the article text because the publisher
endpoints returned HTTP 400/403. No exact theorem passage, incorporated definitions, proof
boundary, correction or errata disposition, immutable source packet, or independent review exists.

The familiar modern formulation with a finite group `G`, distinct natural primes `p` and `q`,
natural exponents `a` and `b`, an equality `Nat.card G = p ^ a * q ^ b`, and conclusion
`IsSolvable G` is recognizable, but the intake explicitly records it as uncredited. Selecting it
would resolve proposition-changing choices without authority. The alternatives involving
`Fintype.card`, a prime-support or divisibility condition, positive exponents, equality without
distinctness, or an unfolded derived-series conclusion are likewise not interchangeable without
source approval and checked transports.

Consequently there is no honest canonical expression for which minimal target imports, an
elaborated-expression fingerprint, alternate-form wrappers, or removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations can be certified. Those four
mutation classes are undefined rather than passed. The lifecycle remains `planned`, the vector
remains `[H1, M3, R4]`, and both audit and theorem completion remain false.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates in the pinned environment. Its imports expose
mathlib's `IsSolvable` definition, prime-power and Sylow interfaces, Burnside normal
p-complement theorem, and finite Z-group solvability substrate. All eight API checks pass; the
four inspected declarations report only `propext`, `Classical.choice`, and `Quot.sound`.

A bounded exact-topic search of pinned mathlib found no direct p-alpha q-beta solvability root.
The normal p-complement theorem, finite Z-group instance, prime-power interfaces, and Sylow
existence results are adjacent infrastructure, not substitutes for the catalog target. The probe
therefore validates only the already recorded M3 interface boundary. It declares no canonical
target, checked source transport, or proof body, and its imports cannot be certified minimal for an
absent target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation ran.

## Validation Record

Commands ran inside this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0069` | 0 | rank 1100; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` plus package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0069/IntakeProbe.lean)` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `af89feb80ce1dac575819b97c5e64ca24a5e3361b784c5c6f443cb314a039257`; no target or proof declared |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 0 | pinned search returned expected no-match exit 1; no direct p-alpha q-beta root was located |
| `python3 -B Stage1_Instances/THM-M-0069/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`, while current authority records provisional `[_]`; it is not statement evidence and was not modified |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0069/statement-blocker.json` and scoped blocker assertions | 0 | blocker JSON and its null-target, unchanged-vector, undefined-mutation, false-completion, and no-self-test boundaries agree |
| scoped whitespace checks over `Stage1_Instances/THM-M-0069` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker is historical: it freezes the intake-time authoritative state and original
nine-file inventory. The integration lane later promoted the intake row to provisional `[_]`, and
this phase adds two blocker reports. Rewriting the intake checker, instance, receipt, task DAG,
generated checklist, or authoritative execution DAG to manufacture agreement would be invalid.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash a lawful immutable primary or authoritative source,
select and independently approve one exact proposition, and map every incorporated definition,
ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, and boundary case.
They must explicitly decide finiteness, prime distinctness, exponent domains and zero cases,
cardinality encoding, multiplication orientation, solvability convention, and degenerate cases.
The integration lane must also master-accept the intake before accepting a later statement
transition.

A fresh statement worker can then encode precisely that source-mapped claim, minimize pinned
imports, serialize and fingerprint the elaborated expression and environment, compile every
credited transport, and execute all four required mutation classes.

This is the assigned phase's truthful blocker result, not completion of the statement node or any
downstream node. No statement receipt, worker `[_]`, `.stage1-worker-selftest.json`, proof credit,
audit completion, theorem completion, or master acceptance is claimed.
