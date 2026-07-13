# THM-M-0890 statement validation

## Frozen target

`Statement.lean` freezes the regular simple-graph form of Hoffman's ratio bound selected from
Willem H. Haemers, *Hoffman's ratio bound*, Section 2, Theorem 1. For a finite nonempty graph `G`
that is regular of positive degree `k`, it states

```text
(G.indepNum : Real) <= |V| * (-lambda_min / (k - lambda_min)),
```

where `lambda_min` is the last entry of mathlib's descending real eigenvalue enumeration for
`G.adjMatrix Real`. The exact binder order, hypotheses, conclusion, conventions, hashes, and
source-selection boundary are recorded in `statement.json`.

Haemers' paper says that Hoffman communicated but did not publish the independence-number bound
and identifies Hoffman's 1970 coloring paper as a wrong reference for it. The catalog's 1970 field
therefore receives no source credit here. This is an H1 canonicalization of the conventional
eponymous result, not H0 genealogy or proof-source acceptance.

The paper's displayed formula has no explicit denominator premise. A nonempty edgeless graph is
0-regular and has `k = lambda_min = 0`; the paper's algebraic derivation then divides by zero, while
Lean's total real division would make the displayed bound false. The formal target therefore
requires `0 < k`. This excludes exactly the regular edgeless boundary and retains degree one. The
later source audit must independently approve that explicit formalization boundary.

No equality consequence, weighted or arbitrary-graph extension, chromatic bound, Laplacian form,
strongly regular specialization, or division-free transport is credited. No proof body is present.

## Minimal Lean boundary

The two direct imports are:

- `Mathlib.Combinatorics.SimpleGraph.Clique`, for `SimpleGraph.indepNum`;
- `Mathlib.Combinatorics.SimpleGraph.LapMatrix`, for the Hermitian real adjacency matrix.

Deleting either import from a target-only fixture makes elaboration fail. `Spectrum` is not a
direct import because it is already available through `LapMatrix`'s public dependency closure.
The validator serializes the fully elaborated root with explicit arguments and universes, rejects
unresolved metavariables, and confirms four distinct mutation expressions: removed positive degree,
rational spectral domain, existential graph scope, and degree at least two. Lean boundary examples
check that the edgeless graph on `Fin 1` is 0-regular, zero degree fails the selected premise, and
degree one remains admitted.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Existing pinned `.lake` artifacts were used read-only.
No update, build, clone, fetch, or dependency mutation was run.

## Commands and results

Commands ran on 2026-07-13 (Asia/Shanghai). Lean commands ran from `Formalizations/Lean`; all
others ran from the repository root unless noted.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0890` | 0 | rank 1440; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base `46a0f2a3...`, tree `7b1b5269...` |
| immutable arXiv v2 PDF and Crossref metadata inspection | 0 | Haemers Theorem 1 and history rechecked; PDF SHA-256 `e2a90698...22bc` |
| `lake env lean ../../Stage1_Instances/THM-M-0890/Statement.lean` | 0 | root elaborated, four expected `#check_failure` rejections and explicit expression printed; output SHA-256 `429d47c...47d5` |
| `python3 ../../Stage1_Instances/THM-M-0890/check_statement.py` | 0 | expression SHA-256 `512ebe65...a54d`; four mutations distinct; both import deletions fail; toolchain and mathlib pin agree |
| Lean/Lake version and pinned mathlib revision/tree/status checks | 0 | expected versions and clean pinned mathlib worktree |
| historical `python3 -B Stage1_Instances/THM-M-0890/check_intake.py` | 1 | expected historical replay limitation: the integrated authority now records intake `[_]`, while the frozen intake checker asserts `[ ]`; it also predates statement files |
| JSON parse, statement invariant checker, and scoped prohibited-construct scan | 0 aggregate | metadata agrees with fresh elaboration; no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| scoped whitespace and changed-path checks | 0 | no diagnostics; only this target and the root worker packet changed |

The historical intake checker and receipt remain immutable evidence for the earlier intake snapshot.
This statement phase does not rewrite them merely to absorb later authority state and files.

## Status boundary

The proposed vector change is `[H1, M4, R4]` to `[H1, M3, R4]`: the exact interface now exists,
but no proof of the bound exists in this packet. Formal-anchor audit, obligation freeze, proof,
composition, trust and provenance closure, readable reconstruction, reproducibility, independent
verification, master acceptance, audit completion, and theorem completion all remain open.
