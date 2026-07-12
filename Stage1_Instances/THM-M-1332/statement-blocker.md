# Exact-statement gate: blocked

Item: `S56-M-1332-STATEMENT`

Theorem: `THM-M-1332`

Base revision: `5a057abd0705ba3f4cadbff1712f2bb7467e6354` (tree
`e6499183859cf75043a1ab13bcce0ca7470a2df6`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1332-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. The intake receipt
also declares `accepted: false`, has no accepted receipt ID, and leaves the canonical mathematical
statement and Lean target null. This is the earliest workflow blocker.

Independently, the exact-statement gate cannot be passed from the authoritative repository record.
The record supplies only the title Picard-Lindelof theorem, the attribution Picard/Lindelof, the
year 1894, and the gloss `ODE解的存在唯一性` ("existence and uniqueness of ODE solutions"). It
contains no source locator, formula, definitions, ordered binders, hypotheses, solution predicate,
uniqueness class, exceptional cases, or proof boundary. The catalog label `已验证` is explicitly
untrusted under rev-5.6.

The intake's Picard 1894 DOI is only a bibliographic lead. Its title concerns linear differential
equations, the complete primary text was not inspected, the catalog does not select it, and no
Lindelof source, translation audit, errata audit, or independent source review is present. The
following unresolved choices change the proposition rather than merely its notation:

- scalar, finite-dimensional, or complete normed state space, including the completeness premise;
- autonomous versus time-dependent vector field and the time-state domain of its assumptions;
- continuity in time and local or global Lipschitz continuity in state, including uniformity and
  the Lipschitz region;
- any norm bound and its quantitative relation to spatial and temporal radii;
- a fixed closed, open, one-sided, or two-sided interval versus an existential neighborhood;
- `HasDerivAt`, `HasDerivWithinAt`, or an integral-equation solution predicate, including endpoint
  semantics and curve regularity;
- one solution versus a local flow, and uniqueness among which curves on which common domain;
- whether compared solutions must remain in the controlled state region; and
- zero-width intervals, zero radii or constants, endpoint initial times, and a hypothesis center
  different from the actual initial value.

Selecting conventional answers would manufacture one modern textbook variant. It would also risk
duplicating `THM-M-1331`, the adjacent catalog target for existence and uniqueness under a
Lipschitz condition. The repository contains no approved distinction, alias/deduplication relation,
or correction for these two targets. `THM-M-1333` separately owns Peano existence and cannot supply
the missing uniqueness claim.

Section 5 of the rev-5.6 blueprint makes statement ambiguity and a missing expression fingerprint
hard blockers. There is consequently no canonical expression for which minimal imports, checked
alternate transports, or removed-hypothesis, changed-domain, changed-binder-scope, and boundary
mutations can be certified. Those mutation tests are undefined, not passed. No theorem, assumed
declaration, placeholder, weakened specialization, or broadened substitute was added. The root
remains `[H1, M3, R3]` and no statement or theorem completion is claimed.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. It confirms the
types of `IsPicardLindelof`, three local-existence interfaces, and five Gronwall uniqueness
interfaces. This is real discovery evidence, but it does not select a combined target.

The split is material. The Picard-Lindelof existence theorem uses a time-dependent field on a
complete normed real vector space, a bundled `IsPicardLindelof` hypothesis with nonnegative radii
and constants, a closed interval, and `HasDerivWithinAt`. The inspected uniqueness alternatives
instead use different combinations of open-interval `HasDerivAt`, closed-interval continuity,
range membership in time-indexed sets, global Lipschitz hypotheses, a left-endpoint initial value,
or a global domain. Mathlib's Picard-Lindelof module explicitly says that it proves existence only
and delegates uniqueness to `Mathlib.Analysis.ODE.Gronwall`.

Choosing and proving one compatibility bridge would resolve formal engineering only after a
source-faithful root has selected its interval, derivative, range, and uniqueness conventions. The
probe's two imports are therefore candidate-family imports, not certified minimal imports for an
absent canonical target. This statement phase does not inspect or credit the component proof
bodies and does not perform the downstream anchor audit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `Formalizations/Lean/.lake`
symlink was used read-only. No update, build, dependency clone or fetch, or other `.lake` mutation
was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1332` | 0 | rank 944; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all && git rev-parse HEAD && git rev-parse 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above |
| `sha256sum` over the blueprint, manifests, skill, repository source records, intake records, toolchain files, probe, and both pinned ODE sources | 0 | authority, source, intake, environment, probe, and ODE-source hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1332/IntakeProbe.lean` | 0 | ten pinned Picard-Lindelof existence and ODE uniqueness interfaces elaborated; no target theorem was declared |
| repository search for the target, gloss, neighboring targets, and ODE interfaces | 0 | found only underspecified catalog/Stage0 records, the intake dossier, and adjacent discovery uses; no source-selected combined proposition |
| `python3 Stage1_Instances/THM-M-1332/check_intake.py` (pre-edit) | 1 | the historical intake checker stops at its stale expectation that the generated execution-DAG intake state is `[ ]`; the current authoritative DAG has provisional `[_]`; it fails before checking the owned-file inventory |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1332/statement-blocker.json` and scoped `jq -e` invariant check | 0 each | blocker JSON parses; identity, null target/imports, undefined mutations, unchanged vector, false completion flags, and no-self-test state agree |
| `git diff --check -- Stage1_Instances/THM-M-1332` and no-index checks for both blocker files | 0 / 1 each | no whitespace diagnostics; no-index exit 1 is the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must first master-accept the intake dependency. Accountable reviewers must
then preserve and hash an immutable primary or authoritative source, pinpoint the exact theorem and
incorporated definitions, transcribe every ordered binder, hypothesis, conclusion, and exceptional
case, reconcile Picard and Lindelof provenance, audit translation and errata, resolve the identity
boundary with `THM-M-1331`, and independently approve the source-to-target mapping.

A later statement worker can then encode that same claim using concrete Lean definitions, minimize
its pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
