# Exact-statement gate: blocked

Item: `S56-M-0200-STATEMENT`

Theorem: `THM-M-0200`

Base revision: `27400857bccc93638c97e9c65859ddf5d5b5f4da` (tree
`3762537e0e5ae46cd70b086da49a69e2fd7b275c`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0200-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt has `accepted: false`, is
non-content-addressed, and provides no accepted receipt ID. Dependency-ordered inspection is
possible, but master closure remains dependency ordered.

The exact-statement gate also fails independently. The repository supplies only the title
`塞瓦定理` (Ceva's theorem), Giovanni Ceva attribution, the year 1678, and the gloss
`共点线的比例关系` (a ratio relation for concurrent lines). It supplies no formula, direction,
bibliography, definitions, ordered binders, hypotheses, proof boundary, boundary cases, correction
history, or reviewer. The catalog's `已验证` label is explicitly untrusted.

The intake correctly leaves the canonical human claim and Lean target null. Its inspected modern
source lead, Thomas Prince's arXiv `2406.08378v1`, Theorem 1, states an iff for a Euclidean triangle:
three cevians are concurrent exactly when a cyclic product of signed side ratios is one, including
points on produced sidelines. That lead has not been adopted as the catalog's authoritative source
or independently reviewed. Its signed-length convention, historical relationship, corrections,
errata, and precise boundary mapping remain open.

These proposition-changing decisions remain unresolved:

- forward implication, converse, or an iff;
- directed affine ratios, signed lengths, unsigned metric distances, or a division-free equality;
- the exact cyclic ratio order and reciprocal convention;
- closed or open side segments versus complete supporting lines;
- the Euclidean plane versus a general affine or normed affine domain and its dimension;
- triangle nondegeneracy, endpoint exclusions, zero denominators, and all coincident-point cases;
- a supplied finite concurrency witness versus an existence predicate or projective concurrency;
  and
- every external-point, parallel-cevian, orientation, relabeling, and other boundary case.

Selecting the convenient pinned forward theorem would silently discard the source lead's converse
and signed external-side semantics. Selecting the familiar iff from mathematical knowledge would
invent a source decision and require a converse that the located pinned declarations do not
provide. Rev-5.6 treats this ambiguity and the absent expression fingerprint as hard blockers.

Consequently there is no honest canonical declaration whose imports can be certified minimal. No
`Statement.lean`, exact expression, checked transport, or mutation fixture was created. The
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. The provisional vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with:

```lean
import Mathlib.Analysis.Normed.Affine.Ceva
```

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, it authenticates two
generalized affine-combination interfaces and four triangle-product declarations. The closest
metric quotient declaration assumes an affinely independent triangle, one point on each complete
opposite sideline, one supplied finite common point on all three cevians, and denominator endpoint
exclusions. It concludes an unsigned-distance product identity.

With `t.points 0 = A`, `1 = B`, `2 = C` and `p 0 = D`, `p 1 = E`, `p 2 = F`, mathlib's quotient is
`BD / DC * CE / EA * AF / FB = 1`. Prince displays its reciprocal,
`AE / EC * CD / DB * BF / FA = 1`, within an iff and with signed lengths on produced sidelines.
A checked reciprocal transport would need the relevant nonzero hypotheses, and no located pinned
declaration proves the converse.

All six interfaces elaborate. Four representative bodies report only `propext`,
`Classical.choice`, and `Quot.sound`. This is direct pinned feasibility evidence, not a
source-approved root, minimal-import result for a canonical target, downstream anchor audit, or
proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No update, build, clone, fetch, or other
dependency-mutation command was run, and the pinned mathlib worktree remained clean.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0200` | 0 | rank 1532; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink; base identifiers appear above |
| authority, source, scope, crosswalk, task DAG, receipt, and intake inspection | 0 | confirmed the provisional dependency, sparse catalog claim, null target, and unresolved direction/ratio/domain/boundary choices |
| `sha256sum` over authority, source, intake, toolchain, lock, and pinned Ceva inputs | 0 | exact digests are recorded in `statement-blocker.json` |
| `git blame -L 1443,1448 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and package status checks | 0 | revision/tree match the values above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0200/IntakeProbe.lean` | 0 | six pinned interfaces elaborated and four axiom reports printed; stdout 3,852 bytes, SHA-256 `8f6a5cf8f07cbdf476aaf775d7efc85607331448c4900996ed0aa94cad547e6a`; no canonical target declared |
| bounded exact-topic `rg` search over repo-local Lean and the two pinned defining modules | 0 | located the four direct triangle candidates and no separate repo-local canonical target; discovery only |
| `python3 -B Stage1_Instances/THM-M-0200/check_intake.py` | 1 | historical intake replay stops because it expects authoritative intake state `[ ]`, while integration now records `[_]`; this phase did not rewrite historical evidence |
| prohibited-declaration `rg` scan over owned Lean | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0200/statement-blocker.json` and scoped invariant/hash assertions | 0 | valid JSON; identity, current authority/input hashes, blocked open state, provisional dependency, null target/imports, unchanged vector, undefined mutations, false completion flags, exact change scope, and absent self-test agree |
| scoped `git diff --check` and per-new-file `git diff --no-index --check` | 0 aggregate | no whitespace diagnostics; each no-index command returned only expected new-file difference status 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |
| final standard validator, target-manifest validator, and target display rerun | 0 | all structural checks still pass; the target remains planned, L0/rework_required, and theorem incomplete |

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before accepting any statement
transition. Accountable reviewers must preserve and hash one lawful immutable primary or
authoritative source, select and independently approve one exact proposition, and map every
incorporated definition, binder, hypothesis, conclusion, proof boundary, correction, erratum, and
boundary case. They must decide direction, ratio order and sign, segment versus sideline scope,
ambient domain and dimension, nondegeneracy and endpoint policy, concurrency encoding, and all
degenerate cases.

A fresh statement attempt may then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and run all four mutation classes.

This blocker is the assigned phase's truthful result, not completion. Lifecycle remains `planned`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, proof credit, or master acceptance is claimed.
