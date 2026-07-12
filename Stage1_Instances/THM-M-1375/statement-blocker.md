# Exact-statement gate: blocked

Item: `S56-M-1375-STATEMENT`

Theorem: `THM-M-1375`

Base revision: `1fc66febfddf404bb914cec34962d66862b96f2b` (tree
`49ae48302378d63f3c54b2a43eeca26433c6b7c5`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the family name Liouville theorem, Joseph Liouville, 1838, and the gloss
"phase-space volume conservation." It supplies no cited proposition, incorporated definitions,
ordered binders, hypotheses, conclusion, proof boundary, corrections, or boundary cases. Stage0
explicitly leaves the exact definitions and premises, proof route, equivalent forms, axioms,
machine status, and artifacts open. The catalog's verified label is untrusted metadata under
rev-5.6.

The omission is mathematically material. An exact statement must choose canonical Euclidean
coordinates, a symplectic vector space, or a symplectic manifold; dimension and volume
normalization; Hamiltonian regularity and autonomous or time-dependent status; a local or complete
flow and its domain; and one root among zero divergence, Jacobian determinant one, preservation of
the symplectic or Liouville volume form, equality of volumes of evolved regions,
`MeasurePreserving`, or a density equation. It must also fix every required implication or
equivalence transport and the set and boundary conventions. These related formulations are not
definitionally interchangeable.

The repository independently schedules `THM-M-1520` with the same Joseph Liouville attribution,
1838 date, and phase-space-volume gloss. Its later `Statement.lean` chooses a global
canonical-coordinate `MeasurePreserving` proposition for a `C^2` Hamiltonian and a flow whose time
orbits are `C^1`.
The legacy `S1_M_189.lean` instead stores abstract proposition fields, assumes symplectic-flow data,
and explicitly denies terminal completion. Both artifacts belong to `THM-M-1520`; adopting either
for this target before an accepted alias, deduplication, distinct-root, canonical-root, and evidence
ownership decision would be an unauthorized substitution.

The intake consequently leaves the canonical statement, Lean module and expression, expression
hash, and canonical-target environment fingerprint null at `[H1, M4, R4]`. Without a canonical
expression, no imports can be certified minimal, no alternate encoding can receive a checked
transport, and the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary
case mutations are undefined rather than passed. No `Statement.lean`, placeholder, assumed volume
preservation field, weakened special case, or broadened theorem was introduced.

The intake prerequisite currently has provisional worker state `[_]`, not master-accepted state
`[x]`. Its receipt is non-content-addressed, declares `accepted: false`, and has no accepted receipt
ID. Rev-5.6 permits this provisional later-node attempt, but dependency acceptance remains
independently necessary before a future statement transition can be accepted. The first substantive
failure is the missing exact source-statement and duplicate-root decision.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with the pinned environment. Its six
direct imports expose ten adjacent smoothness, gradient, ODE, flow, volume, measure-preservation,
and symplectic-matrix interfaces. All checks pass. The probe defines no source-selected phase space,
Hamiltonian system, evolution contract, volume transport, or Liouville proposition. Its successful
elaboration therefore receives no statement, minimal-import, anchor, or proof credit.

A bounded exact-topic search of repo-local Lean and pinned mathlib found no terminal Hamiltonian
phase-volume theorem after unrelated Liouville families and neighboring recurrence and quantum
records were excluded. It did find the separately owned legacy `S1_M_189` boundary described
above. This is narrow discovery evidence, not the downstream immutable anchor audit or a claim of
global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` link to the canonical pinned artifacts was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root unless
a different working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1375` | 0 | rank 985; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before editing | 0 | only the automation-provided untracked `.lake` link existed; the base revision and tree are recorded above |
| `sha256sum` over the authority, source, intake, duplicate, probe, toolchain, manifest, and relevant pinned mathlib inputs | 0 | hashes agree with `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, target `x86_64-unknown-linux-gnu`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e`, Lean 4.29.0 |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree agree with the fingerprint; package worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1375/IntakeProbe.lean` | 0 | ten adjacent pinned APIs elaborated; no canonical target or proof body was declared; complete output SHA-256 `c65fa987d8d9df7133e44eddec3b2bb1d38efb83432b7f27839420bce05c8069` |
| `rg -n -i --glob '*.lean' '(Liouville theorem\|phase[- _]?space.{0,100}volume\|volume.{0,100}Hamilton\|Hamilton.{0,100}(volume\|measure)\|MeasurePreserving.{0,100}Hamilton\|Hamilton.{0,100}MeasurePreserving)' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib Stage1_Instances/THM-M-1375 \| rg -v '<documented unrelated and separately inspected boundary filter>'` | 1 | expected no-match after the exclusions listed exactly in `statement-blocker.json`; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-1375/check_intake.py` | 1 | historical intake checker stops at stale receipt input hash `Docs/Stage1_Blueprint_rev-5.6.md`; this statement phase records rather than rewrites historical evidence |
| `rg -n '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-1375 --glob '*.lean'` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1375/statement-blocker.json` | 0 | the finalized structured blocker parsed as valid JSON |
| scoped statement-blocker invariant assertions | 0 | IDs, open blocked state, null target and imports, unchanged vector, four undefined mutations, false completion flags, exact two-file change scope, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-1375` plus `git diff --no-index --check -- /dev/null <each blocker artifact>` | 0 for the scoped check; expected added-file status 1 with empty output for each no-index check | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | the self-test manifest is absent because the exact-statement deliverable did not pass |

The observed historical intake-checker run stops at its stale blueprint hash. Independently, the
checker also freezes the original nine-file intake inventory, so a refreshed run would reject these
two phase-specific artifacts unless the historical validator were changed. This statement run
records both incompatibilities instead of rewriting the intake checker, intake receipt, instance,
task DAG, generated blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
lawfully preserve and hash one complete primary or authoritative source edition, select and
transcribe one exact result with every incorporated definition and assumption, audit genealogy,
translation, corrections, errata, and proof boundary, and independently approve the crosswalk. They
must also reconcile `THM-M-1375` with `THM-M-1520` and assign canonical-root and evidence ownership.
The exact phase space, Hamiltonian, evolution, regularity and domain, volume encoding, set class,
root conclusion, transports, binders, hypotheses, foundation profile, and every boundary case must
then be frozen.

A later statement worker can encode that same claim, minimize its pinned imports, serialize and
hash the elaborated expression and environment, compile every credited transport, and run all four
mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H1, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, node receipt, worker `[_]`, or master acceptance is claimed.
