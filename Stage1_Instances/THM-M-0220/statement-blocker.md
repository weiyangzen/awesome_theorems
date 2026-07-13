# Exact-statement gate: blocked

Item: `S56-M-0220-STATEMENT`

Theorem: `THM-M-0220`

Base revision: `c2e294becadae6ce784f27ee69f2e8dbf57e0b30` (tree
`3f567e7f76b189432b73444354070c0ff75925b9`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete record supplies only the Chinese title and gloss recorded at
`Docs/researches/math_theorems.md:1585-1590`, attribution to many mathematicians, and the
nineteenth century. It supplies no bibliographic source, exact formula, definition, ordered binder,
hypothesis, exact conclusion, proof boundary, correction, reviewer, or boundary case. Stage0
explicitly leaves the formal system, exact definitions and premises, proof route, alternate forms,
axioms, machine status, and artifacts open. The catalog status value is untrusted metadata under
rev-5.6.

The gloss identifies a classical theorem family, not one proposition. For a finite geodesic
triangle, the familiar curvature `-1` formula is
`Area = pi - (alpha + beta + gamma)`. Under curvature `-k^2`, a common scaled formula is
`Area = (pi - (alpha + beta + gamma)) / k^2`. These are not definitionally the same target, and
the catalog selects neither. It also does not fix:

- an upper-half-plane, disk, synthetic, or abstract constant-curvature geometry;
- a metric and curvature normalization;
- the geodesic-triangle object, enclosed region, area measure, or interior-angle definition;
- finite, ideal, partially ideal, ordered, oriented, or signed triangles; or
- repeated vertices, collinearity, self-intersection, orientation reversal, and zero-area cases.

Choosing any familiar variant would add, narrow, broaden, or substitute proposition-changing
mathematics. The inherited, unaccepted intake provisionally records `[H1, M4, R4]` while leaving
the canonical human statement, Lean module and expression, minimal imports, and expression and
environment fingerprints null. H1 itself remains pending source audit. Without a canonical target,
checked alternate transports and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are
undefined rather than passed. No `Statement.lean`, axiom, placeholder, assumed area identity,
weakened special case, or broadened theorem was introduced.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its three direct
imports expose upper-half-plane metric and invariant-measure interfaces together with Euclidean
angle vocabulary. All checks and instances elaborate, but the probe defines no hyperbolic
geodesic triangle, interior-angle bridge, curvature normalization, canonical target, transport,
or proof body. Its imports therefore cannot be certified minimal for an absent target, and the
successful check receives no statement, anchor, or proof credit.

A bounded exact-topic search over `Formalizations/Lean/AwesomeTheorems` and pinned mathlib found no
hyperbolic-triangle area-defect or Gauss-Bonnet declaration under the recorded terms. This is
narrow feasibility evidence, not the downstream anchor audit and not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided canonical `.lake` symlink
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation evidence

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository
root unless another working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0220` | 0 | rank 1233, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; the base revision and tree are recorded above |
| the exact inline Python command recorded in `statement-blocker.json` | 0 | the scoped checker verifies the authority, source, and intake hashes plus the fail-closed blocker invariants |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, and worktree inspection | 0 | revision and tree agree with the fingerprint; the package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0220/IntakeProbe.lean` | 0 | adjacent metric, measure, angle, and invariance APIs elaborated; no canonical target or proof body was declared; stdout SHA-256 `7d93b900abe98f89e98347ab858221f70fc684f68ccc3f04cdc6fbd5bfd2ff84` |
| bounded exact-topic `rg` over `Formalizations/Lean/AwesomeTheorems` and pinned mathlib | 1 | expected no-match exit; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-0220/check_intake.py` | 1 | the historical intake checker freezes the earlier authoritative intake item as `[ ]`, while the integrated DAG now records provisional `[_]`; this phase records rather than rewrites historical evidence |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-0220` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0220/statement-blocker.json` | 0 | the finalized structured blocker parses as valid JSON; the recorded inline checker supplies the scoped invariant assertions |
| `git diff --check` plus per-file `git diff --no-index --check` | 0; 1 expected difference | no whitespace diagnostics; the harness treated each no-index exit `1` as the expected new-file difference status |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The intake prerequisite has provisional worker state `[_]`, not master-accepted state `[x]`. Its
receipt explicitly has `accepted: false` and no accepted receipt ID. Under the enabled concurrent
worker workflow, rev-5.6 section 10.2 permits preparation of this later-node blocker, but dependency
acceptance independently remains necessary before a future statement transition can be accepted.
The first substantive failure is the missing exact source statement and normalization selection.

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash one immutable complete primary or approved authoritative source,
select and independently approve one exact proposition, and transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, and erratum. They
must freeze the hyperbolic geometry and metric scale, triangle and region objects, area measure,
angle convention, orientation, ideal-vertex policy, alternate encodings, and all boundary cases.

A later statement worker can then encode that same claim using real Lean definitions, minimize
its pinned imports, serialize and hash the elaborated expression and environment, check every
credited transport, and run all four mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
inherited provisional intake vector remains `[H1, M4, R4]`, with `audit_complete: false` and
`theorem_complete: false`; H1 remains unaccepted pending source audit, and no debt change is
proposed. Because the assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json`, node receipt, worker `[_]`, or master acceptance is claimed.
