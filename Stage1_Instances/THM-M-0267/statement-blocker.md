# Exact-statement gate: blocked

Item: `S56-M-0267-STATEMENT`

Theorem: `THM-M-0267`

Base revision: `c2467750f2cdb3960045c83e819d96687253303d` (tree
`0f79eb697267dc28b29d41a1e282f319d758a2ac`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0267-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is not
content-addressed, and has no accepted receipt ID. It deliberately leaves the canonical
mathematical statement, Lean module and expression, expression hash, and target environment
fingerprint null. This dependency still requires master acceptance before a statement transition
can be accepted.

Independently, the exact Lean 4 target cannot be truthfully selected from the received source
record. The catalog supplies only the Arzela-Ascoli name, the Cesare Arzela and Giulio Ascoli
attribution, the year 1889, and the gloss "a criterion for compactness of sequences of functions."
It gives no formula, definitions, citation, ordered binders, assumptions, topology, conclusion,
direction, proof boundary, or correction history. Stage0 explicitly leaves the precise definitions
and premises open.

Those omissions conceal proposition-changing choices. The root does not decide a natural-number
sequence versus an arbitrary family; compact metric, compact Hausdorff, or locally compact domain;
scalar, metric, pseudo-metric, normed, or uniform codomain; continuous or bounded continuous maps;
uniform, compact-open, uniform-on-compacts, pointwise, or sequential convergence; uniform
boundedness, one common compact range, or pointwise relative compactness; the exact equicontinuity
quantifiers; closedness; compactness of the family or its closure, relative compactness, total
boundedness, or subsequence extraction; or sufficiency versus an equivalence criterion.

The intake's secondary source discovery also exposes an unresolved 1883/1889/1893 historical and
formulation mismatch. No immutable primary theorem passage, complete definition and assumption map,
proof boundary, translation, correction or errata disposition, historical reconciliation, or
independent review has been accepted. Selecting the familiar scalar sequential theorem or one
named mathlib declaration would therefore invent a source bridge or substitute one member of the
Arzela-Ascoli family for the unresolved catalog root.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. There is consequently no honest canonical expression whose direct imports can be
certified minimal. Checked alternate transports and the removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutation suites are undefined, not passed. The root vector
remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates two direct pinned imports:

- `Mathlib.Topology.ContinuousMap.Bounded.ArzelaAscoli`
- `Mathlib.Topology.UniformSpace.Ascoli`

The bounded-continuous-function declarations are materially different. One requires a compact
pseudo-metric codomain and a closed family, one requires a common compact range and a closed
family, and one adds a `T2Space` codomain and concludes compactness of the closure rather than of
the original family. The general uniform-space declarations instead use closed embeddings and a
family of compact subsets with pointwise compact-range hypotheses, or compactness of the
pointwise-image set. Mathlib's general module explicitly records compact-implies-equicontinuous as
a TODO, so the catalog word "criterion" cannot silently supply an equivalence there.

All six interfaces elaborate under pinned Lean. The three representative axiom reports are exactly
`propext`, `Classical.choice`, and `Quot.sound`. This is real candidate-interface evidence only:
the probe defines no canonical target, source-to-Lean transport, statement mutation, or proof body.
Its two imports are appropriate for discovery but cannot be certified as the minimal imports of an
absent target.

A bounded exact-topic search found the two mathlib modules, a Gromov-Hausdorff use, and the legacy
`S1_M_174` inventory. No source-identical root mapping was accepted. This observation is not the
downstream exhaustive anchor audit and makes no global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symbolic link was used read-only. No update, build, dependency clone or
fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0267` | 0 | rank 1046; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| repository source, Stage0, manifest, blueprint, intake dossier, task dependency, and source-boundary inspection | 0 | theorem family identified, but the proposition-changing choices and canonical target remain null |
| `sha256sum` over authority, intake, toolchain, probe, and pinned candidate sources | 0 | exact fingerprints are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree recorded above; package source worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0267/IntakeProbe.lean` | 0 | six materially different exact-topic APIs elaborated; three representative declarations reported the three axioms above; stdout SHA-256 `3d1f15292cd5965e6f59b3a924c93b087d06a9e492ac40049b224c17fccfbc7b` |
| bounded exact-topic `rg` search in pinned mathlib and repo-local Lean | 0 | candidate modules, one downstream use, and legacy inventory references found; no source-identical mapping credited |
| `python3 -B Stage1_Instances/THM-M-0267/check_intake.py` | 1 | historical intake replay stops at its frozen repository-base assertion: intake records `2612b21a0cd5f3f13bd2223af801c73511f950c0`, while this later statement worker is based at the revision above; intake evidence was not rewritten |
| `python3 -m json.tool Stage1_Instances/THM-M-0267/statement-blocker.json` plus scoped blocker invariants | 0 | structured blocker parses; identity, dependency, null target/imports, undefined mutations, unchanged vector, false completion flags, and no-self-test boundary agree |
| prohibited-declaration scan over owned Lean files | 1 | expected no-match result: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` commands are permitted |
| `git diff --check -- Stage1_Instances/THM-M-0267` plus direct byte checks on both new files | 0 | no whitespace, missing-newline, carriage-return, or NUL diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | the worker self-test manifest is intentionally absent because the exact-statement deliverable did not pass |

The intake checker freezes the intake run's original commit and nine-file artifact inventory. It is
historical evidence, not a later-phase validator. This run records its stale-base failure instead
of rewriting the intake instance, receipt, checker, target-local task DAG, generated blueprint, or
authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake dependency before accepting a later statement
transition. Accountable reviewers must preserve and hash an immutable source edition, transcribe
and independently approve one exact root proposition with every incorporated definition, ordered
binder, hypothesis, conclusion, direction, proof boundary, correction, erratum, translation,
historical attribution, and boundary case.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute the removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
