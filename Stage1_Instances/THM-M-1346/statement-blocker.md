# Exact-statement gate: blocked

Item: `S56-M-1346-STATEMENT`

Theorem: `THM-M-1346`

Base revision: `b72c38f3df59ba12e643e0a20be2dd36c063eafc` (tree
`4b2126951b48faf4dd3d85dc1e81962ea29a7004`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1346-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. The intake receipt
also declares `accepted: false`, has no accepted receipt ID, and intentionally leaves the canonical
mathematical statement and Lean target null.

Independently, the repository record cannot support an exact Lean 4 target. It gives only the title
`稳定流形定理` (stable manifold theorem) and the noun phrase `双曲平衡点的稳定与不稳定流形`
(stable and unstable manifolds of a hyperbolic equilibrium). It cites no theorem and supplies no
phase space, dynamics, definition, ordered binder, hypothesis, conclusion, proof boundary, erratum,
or formal artifact. Stage0 explicitly leaves the precise definitions and premises open, and the
catalog label `已验证` is untrusted under rev-5.6.

The intake's inspection of Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*,
Section 9.2, confirms rather than resolves the ambiguity:

- Theorem 9.3 is a rate-indexed local graph result under shifted hyperbolicity;
- Theorem 9.4 constructs local stable and unstable `C^k` graphs with tangency and estimates; and
- Theorem 9.5 assumes hyperbolicity and identifies the constructed manifolds with local-orbit and
  global stable/unstable sets.

The catalog does not cite Teschl or select one theorem or conjunction. It also does not choose
continuous-time vector-field dynamics over a diffeomorphism, a finite-dimensional space over a
manifold or Banach space, the regularity class, the spectral splitting convention, local over
global leaves, embedded over immersed status, or which graph, tangency, dimension, invariance,
convergence, estimate, uniqueness, and stable-set-identification clauses belong to the conclusion.
Time-direction, completeness, trivial spectral subspaces, and boundary cases are likewise open.

Those choices produce inequivalent propositions. Selecting a familiar formulation, conjoining
Teschl 9.4 and 9.5, or assuming the desired stable/unstable manifolds in an input structure would
invent, broaden, or circularly package mathematics rather than elaborate the exact received target.
The first substantive failure is therefore the exact source-statement and scope-identity gate in
sections 5 and 5.1 of the rev-5.6 blueprint. Statement ambiguity and a missing expression
fingerprint are hard blockers there.

Consequently there is no honest canonical declaration for which minimal imports can be claimed.
No `Statement.lean`, exact expression, checked alternate transport, or mutation suite was created.
The required removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations are
undefined rather than passed. The intake vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the pinned environment. Its four direct imports
expose generic integral-curve, flow, invariant-set, fixed-point, orbit, and smooth-embedding APIs.
They do not define hyperbolicity, a stable/unstable spectral splitting, local or global stable sets,
the desired leaves, or a stable-manifold theorem. Their imports are discovery-only inputs and
cannot be certified minimal for a target that has not been selected.

A bounded exact-name search of pinned mathlib and the repository-local Lean sources found no
stable-, unstable-, or invariant-manifold declaration. This is feasibility evidence only, not the
downstream immutable anchor audit and not a claim of absence outside the searched closure.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1346` | 0 | rank 957; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository and source inspection for the target, title, gloss, and candidate family | 0 | found the sparse catalog record, explicit null intake target, and inequivalent source candidates; no source-selected proposition |
| `sha256sum` over authority, intake, source, probe, toolchain, and pinned mathlib inputs | 0 | hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-1346/check_intake.py` | 1 | the historical receipt's blueprint hash is stale after integration; the checker also freezes its old base, intake state, and nine-file inventory, so it is not rewritten by this statement phase |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1346/IntakeProbe.lean` | 0 | seven generic adjacent APIs elaborated; no canonical target was declared |
| bounded exact-name search for stable, unstable, or invariant manifolds | 1 | expected no-match result in pinned mathlib and repository-local Lean sources; discovery-only evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | blocker identity, null target and imports, unchanged vector, four undefined mutations, false completion flags, and absent-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-1346` plus per-new-file no-index checks | 0; 1 each | no whitespace diagnostics; both no-index exits are only the expected new-file differences |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must first accept the intake dependency. Accountable reviewers must then
preserve and hash an immutable primary or authoritative edition, select and independently approve
one exact root theorem or explicit conjunction, and transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, regularity and spectral convention, local/global and
time-direction choice, exceptional case, proof boundary, correction, and erratum. The selection
must preserve the boundaries with Hartman-Grobman, center-manifold, hyperbolic-system, Anosov, and
Pesin targets.

A fresh statement run can then encode precisely that source-selected claim, minimize pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport, and
run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
