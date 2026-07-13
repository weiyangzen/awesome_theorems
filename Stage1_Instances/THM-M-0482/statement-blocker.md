# Exact-statement gate: blocked

Item: `S56-M-0482-STATEMENT`

Theorem: `THM-M-0482` (Chebyshev estimates)

Base revision: `be8701e88e791545c16a262edd1909486d5cef4b` (tree
`78b0a751473bf6d71f453a6aad18b130268a3428`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0482-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. Rev-5.6 permits
dependency-ordered inspection after a provisional predecessor, but master acceptance remains
necessary before any future statement transition can be accepted. The intake receipt itself says
`accepted: false`, is not content-addressed, and has no accepted receipt ID.

Independently, the exact-statement gate cannot pass from the received claim. The complete catalog
wording is only `素数分布的上下界估计` (upper and lower estimates for the distribution of primes),
with Chebyshev attribution and the year 1850. It does not determine:

- the ordinary prime-counting function, Chebyshev `theta`, Chebyshev `psi`, or a linked package;
- an exact inequality, eventual inequality, two-sided linear comparison, asymptotic comparison,
  Big-O/Theta statement, or a normalized ratio;
- the constants, their quantification, threshold, and strict or weak inequalities;
- natural or real arguments, floor conventions, logarithm normalization, and endpoint policy; or
- ordered binders, hypotheses, conclusion, one combined root versus two statements, and finite or
  degenerate cases.

These choices produce materially different propositions. The historical memoir cited by the intake
is a credible immutable lead, but no exact displayed proposition and definition package has been
selected, transcribed, crosswalked through its proof boundary and errata, or independently approved.
Choosing a familiar pair of Chebyshev bounds would therefore invent or substitute mathematics.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. There is no canonical expression whose import can honestly
be certified minimal, no credited alternate form to transport, and no meaningful
removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation. Those four
tests are undefined rather than passed. The root vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` imports `Mathlib.NumberTheory.Chebyshev` and checks
`Nat.primeCounting`, `Chebyshev.theta`, `Chebyshev.psi`, three explicit upper bounds, a
theta-to-prime-counting identity, and an eventual prime-counting upper bound. It re-elaborated under
the pinned environment and printed the representative axiom set `propext`, `Classical.choice`, and
`Quot.sound`. It declares no proposition or proof body for `THM-M-0482`.

Pinned `Mathlib.NumberTheory.Chebyshev` explicitly lists `Prove Chebyshev's lower bound` as a TODO.
The checked upper bounds cannot replace the catalog's promised upper-and-lower root, and the probe
import cannot be certified minimal for an absent canonical target. This is narrow feasibility
evidence, not the downstream exhaustive anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink
was used read-only. No update, build, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran
from `Formalizations/Lean`; all other commands ran from the repository root unless noted.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0482` | 0 | rank 1363; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before edits | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| source, Stage0, manifest, blueprint, execution DAG, and complete intake-dossier inspection | 0 | found only an underspecified estimate-family gloss; intake leaves the canonical human and Lean targets null |
| `sha256sum` over authority, intake, toolchain, lockfile, probe, and pinned mathlib inputs | 0 | exact current hashes are recorded in `statement-blocker.json` |
| `lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `lake env lean ../../Stage1_Instances/THM-M-0482/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; output SHA-256 `10e9505f0e987def5214385adcaac25a563d08afca14a4d4f4aebe69a9d5164f`; no target or proof body was declared |
| focused lower-bound declaration search in the pinned Chebyshev module | 0 | found only `theta_le_psi`; the module's lower-bound TODO remains; discovery only |
| `python3 -B Stage1_Instances/THM-M-0482/check_intake.py` | 1 | historical intake replay stops because it expects the intake DAG item at `[ ]`, while integration has provisionally advanced it to `[_]`; this phase records rather than rewrites historical intake evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | identity, dependency boundary, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-0482` plus per-new-file no-index checks | 0; 1 each | no whitespace diagnostics; both no-index exits are only the expected new-file differences |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake validator binds the predecessor's earlier DAG state and original nine-file
inventory. Adding this phase's two blocker reports also makes that inventory historical. This run
does not rewrite `check_intake.py`, the intake receipt, instance, target-local DAG, generated
blueprint, or authoritative execution DAG merely to manufacture agreement.

## Retry Condition And Status Boundary

Accountable source reviewers must preserve and hash an immutable primary or approved authoritative
source, select and independently approve one exact Chebyshev-estimate proposition, and transcribe
every incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, translation choice, and boundary case. The decision must fix the function or checked
function package, both bound directions, exact or asymptotic relation, constants, thresholds,
domain, coercions, floors, logarithms, and endpoints.

A fresh statement worker can then encode precisely that claim, minimize pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and execute
all four required mutation classes. The integration lane must also revalidate and master-accept the
intake dependency before accepting that later transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
