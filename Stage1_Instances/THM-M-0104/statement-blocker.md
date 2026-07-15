# Exact-statement gate: blocked

Item: `S56-M-0104-STATEMENT`

Theorem: `THM-M-0104`

Base revision: `8400eb33dbc4ffb9ebd94456e4de9bfb8d28e005` (tree
`02fcb6bc0f0786ce18871dc9c2c0d2d3db071200`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0104-INTAKE`, has provisional worker
state `[_]`, not master-accepted state `[x]`. Its receipt says `master_acceptance: false`, is not
content-addressed, has no accepted receipt ID, and records the older base
`a8d6489fd935cd71fa4499f2f3f5b051998203f4`. Rev-5.6 section 10.2 permits a later worker to prepare
evidence, but master closure remains dependency ordered.

Independently and decisively, the exact-statement gate cannot pass from the received source record.
The repository supplies only the name "Bezout theorem," an Etienne Bezout attribution, the year
1779, and the gloss "an upper bound on the number of intersection points of algebraic curves."
It supplies no primary bibliography, edition, theorem or page, binder-complete proposition,
definition of curve or intersection point, coefficient field, dimension or projective/affine
setting, multiplicity convention, degree convention, hypotheses, treatment of points at infinity,
corrections, errata, or independent source approval. The `verified` label is explicitly untrusted
under rev-5.6.

The intake therefore selected only a **planned** standard scope: two projective plane curves over an
algebraically closed field, no common irreducible component, and equality between the sum of local
intersection multiplicities and the product of degrees, with the catalog's distinct-point bound as
a corollary. Its own README requires a pinpoint primary source before this choice may be frozen or
elaborated. Its `intake.yaml` leaves the module, expression, expression hash, environment
fingerprint, exact object model, degree, multiplicity, source pin, and toolchain pin unresolved.

Those choices materially change the proposition. In particular, the received gloss does not
select an affine count, projective count, count with multiplicity, distinct-point count, equality,
upper bound, homogeneous-polynomial model, scheme-theoretic length model, or a particular
proper-intersection hypothesis. Selecting the planned equality or any convenient Lean encoding
would invent, strengthen, narrow, or substitute mathematics rather than elaborate the exact
received target. Rev-5.6 sections 5 and 5.1 make this ambiguity and the missing expression
fingerprint hard blockers.

There is consequently no honest canonical Lean expression whose imports can be certified minimal,
no source-approved alternate encoding, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation suite. Those mutation results are undefined, not
passed. The lifecycle stays `planned`, and the root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The historical discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_029.lean` was re-elaborated against the pinned
environment. It imports ten broad algebraic-geometry and commutative-algebra modules and exposes
adjacent scheme, Proj, homogeneous-polynomial, ideal-sheaf, finite-length, and Hilbert-polynomial
interfaces. This is useful feasibility evidence only; its imports cannot be minimal for an absent
canonical target.

The module's `PlaneCurveIntersectionData` does not implement the requested geometry. It stores
`algebraicallyClosedBase`, `noCommonComponent`, projective-support facts, a local multiplicity
function, and the connection between local and total multiplicities as arbitrary fields or
propositions. Its `StatementShape` merely asserts the desired numeric equality for any record that
already packages this abstract data. The module expressly says that the curve/intersection payload
must be replaced before any terminal claim. It is therefore neither an exact source-faithful
statement nor a checked transport and receives no statement or proof credit. Its successful Lean
output has SHA-256 `3aa7c7c88bbd78e87b58596c17d60edf6355da4c6fdfc190929cb387923bd97a`.

A bounded pinned-source search for Bezout/intersection-multiplicity declarations found only
unrelated Bezout-ring and Bezout-identity uses, not a projective-plane Bezout theorem or a local
intersection-multiplicity API. This is a scoped discovery observation, not a whole-ecosystem absence
claim and not the downstream anchor audit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation ran.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-15 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0104` | 0 | rank 29; legacy slot `S1-M-029`; planned; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 767,772 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib status and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean; pinned revision and tree recorded above |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_029.lean` | 0 | historical discovery module elaborated; no source-faithful curve/intersection model or exact canonical target was established; stdout hash appears above |
| bounded Bezout/intersection search over pinned mathlib and `flt-regular` | 0 | only unrelated Bezout-ring/identity uses matched; no projective-plane Bezout or intersection-multiplicity declaration was located in the searched surfaces |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no owned Lean file, hence no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0104/statement-blocker.json` plus scoped invariants | 0 | valid JSON; identity, null target/imports, unchanged vector, four undefined mutations, false completion fields, exact two-file scope, and no-self-test boundary agree |
| scoped and per-new-file whitespace checks | 0 diagnostics | no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

An accountable source reviewer must lawfully preserve and hash one complete primary or approved
authoritative source, select and independently approve one exact proposition, and transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, and boundary case. The selection must resolve affine versus projective scope, coefficient
field and characteristic, curve representation and nonzero/reduced/irreducible conventions, common
components, degree, local multiplicity, finiteness, points at infinity, equality versus distinct
point bound, and the checked relationship between any credited forms. A later statement worker can
then encode precisely that claim, minimize pinned imports, serialize and hash the elaborated
expression and environment, compile all credited transports, and run all four mutation classes.
The integration lane must master-accept the intake before accepting that future transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
