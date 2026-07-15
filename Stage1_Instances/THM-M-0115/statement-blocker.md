# Exact-statement gate: blocked

Item: `S56-M-0115-STATEMENT`

Theorem: `THM-M-0115`

Base revision: `fd995645725ec3633e4da7e6d759deb14f530861` (tree
`5846121ab94ff0502b98217f643539881bc9c045`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0115-INTAKE` has provisional state `[_]`
in the authoritative execution projection and is still unaccepted in the target-local task DAG.
Dependency-ordered investigation is possible, but an accepted statement transition must remain
ordered after master acceptance of that intake.

The intake freezes a classical human formula: for a proper morphism `f : X -> Y` of nonsingular
quasi-projective varieties over a field and `alpha in K_0(X)`,

`ch(f_* alpha) cap td(T_Y) = f_*(ch(alpha) cap td(T_X))`

in rational Chow homology. It also explicitly requires exact Lean representations for the
variety/base-field relation, nonsingularity, quasi-projectivity, `K_0`, rational Chow homology, the
two distinct pushforwards, Chern character, tangent bundle, Todd class, and product or cap action.
The pinned dependency closure does not provide these objects and maps together, so this run cannot
elaborate a backend expression that maps to the frozen mathematical claim.

The legacy file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_023.lean` is not an admissible
substitute. Its `StatementShape` receives `grrIdentity : Prop` as an input field and concludes that
pre-supplied proposition. Its `CandidateAStatementShape` spells an equality over arbitrary carrier
types and arbitrary functions but does not encode a field, varieties, rational Chow homology,
tangent bundles, or the required semantic compatibility. The file itself identifies these layers
as missing and calls the compiled route a weak wrapper, not Grothendieck-Riemann-Roch closure.

A fresh conclusion-free typed interface could be useful future `M3` statement/interface work, but
it would need a reviewed mapping for every frozen notion and boundary. Inventing that mapping now,
or treating unconstrained types and functions as actual `K_0` and Chow theory, would broaden or
substitute the assigned theorem. Accordingly the canonical Lean module, expression, minimal
imports, expression fingerprint, checked transports, and four mutation outcomes remain undefined.
The first failed gate is `canonical_claim_to_concrete_lean_surface_mapping`.

## Pinned Lean Boundary

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only; no dependency update, build, clone, fetch, or other mutation was run.

A bounded exact-topic search of pinned mathlib returned no Grothendieck-Riemann-Roch, scheme
K-theory, Chow group/ring, Chern-character, or Todd-class Lean declaration. Repo-local matches
include other legacy abstract boundaries, especially `S1_M_121.lean` for the distinct target
`THM-M-0177`; they likewise say that the concrete APIs are absent and supply no checked transport
to this target's nonsingular quasi-projective variety scope. This is local negative surface evidence
only, not a global absence claim and not the downstream anchor audit.

The legacy module was re-elaborated successfully with
`lake env lean AwesomeTheorems/Stage1/S1_M_023.lean`. That command reached its scheme, properness,
sheaf, cohomology, derived-category, audit-table, and weak-boundary declarations. It did not reach
an exact GRR target: the module's own printed records report that all GRR-specific closure flags are
false and that its validation record is not terminal GRR evidence.

## Validation Record

Commands ran from this worker clone on 2026-07-15 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0115` | 0 | rank 23; legacy slot `S1-M-023`; planned; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit tree had only the automation-provided untracked `Formalizations/Lean/.lake` symlink; base revision and tree appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status check | 0 | pinned revision and tree recorded above; package worktree clean |
| exact-topic `rg` over pinned mathlib for GRR, Chow, Chern character, Todd class, and scheme K-theory declarations | 1 | expected no-match exit; no exact pinned surface was located by this bounded search |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_023.lean` | 0 | legacy weak-boundary module elaborated; its output exposes adjacent support and expressly false GRR-closure records, not an exact target |
| `python3 -m json.tool Stage1_Instances/THM-M-0115/statement-blocker.json` | 0 | structured blocker parsed as valid JSON after finalization |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-0115` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| `git diff --check -- Stage1_Instances/THM-M-0115` plus per-new-file no-index checks | 0 / expected difference | no whitespace diagnostics in the owned blocker artifacts |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest intentionally absent because the assigned deliverable did not pass |

## Retry Condition And Status Boundary

The statement gate can be retried after accountable source/formal reviewers select and preserve an
exact definition chain and approve a conclusion-free Lean representation of the base-field variety
domain, nonsingularity and quasi-projectivity, `K_0`, rational Chow homology, both pushforwards,
Chern character, tangent bundle, Todd class, and product/cap action. A fresh run must then minimize
the pinned imports, elaborate and serialize the complete formula, bind its environment fingerprint,
compile every credited transport, and distinguish removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations. The intake dependency must be master-accepted
before the statement can be accepted.

This is an owned, fail-closed blocker report. It is not an elaborated statement, a statement-node
receipt, worker `[_]` completion, anchor audit, proof, audit completion, theorem completion, or
master acceptance. Lifecycle remains `planned`; the root vector remains `H4 / M5 / R4`; accepted
receipt IDs remain empty; no `.stage1-worker-selftest.json` is emitted.
