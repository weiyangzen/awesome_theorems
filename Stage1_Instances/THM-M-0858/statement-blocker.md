# Exact-statement gate: blocked

Item: `S56-M-0858-STATEMENT`

Theorem: `THM-M-0858`

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d` (tree
`43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The source-shaped `SimpleGraph` envelope elaborates, but it cannot yet be promoted to the exact
canonical Lean target. Brooks's printed theorem on page 194 concerns a "network (or linear graph)"
and separately rules out a line whose two ends are the same node. It does not explicitly prohibit
two distinct lines from joining the same pair of nodes. Lean's `SimpleGraph` is loopless and cannot
represent parallel lines. Selecting it as the root without an admitted model decision and checked
transport would therefore restrict the received domain rather than elaborate it exactly.

There is a plausible mathematical reduction: collapse parallel lines to one simple edge. Connected
components and proper vertex colorings are unchanged, and degrees weakly decrease. If a collapsed
component were `K_(n+1)`, each vertex would already have `n` distinct incident lines; the source
degree bound would then rule out extra parallel lines, so the original component would itself be
the forbidden `n`-simplex. That argument is not yet a Lean transport and has not received the
required source or graph-model review. It is recorded as a retry route, not assumed here.

The intake also has only provisional worker state `[_]`, not master-accepted `[x]`. Its receipt is
unsigned, non-content-addressed, has `accepted: false`, and contains no accepted receipt ID. The
historical intake checker now fails closed because it freezes the former authoritative intake state
`[ ]`, while the integrated DAG records `[_]`. This statement attempt preserves rather than rewrites
that historical evidence.

The publisher currently exposes the first-page preview but reports no full-text access for this
worker. The complete pages 194-197, proof-premise crosswalk, and independent source/model review
therefore remain unavailable. The page reports no linked corrections, but that metadata is not a
substitute for a complete source and errata audit.

Consequently rev-5.6 sections 5 and 5.1 fail before canonical expression serialization. There is no
approved exact root whose imports can be certified minimal, no canonical expression or environment
fingerprint, no credited alternate transport, and no meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary-case mutation certificate. No `Statement.lean`,
axiom, placeholder, finite-only theorem, connected-only theorem, or familiar modern-form
substitution was added.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates against the pinned environment. It defines only this
noncanonical candidate:

```lean
forall {V : Type u} (G : SimpleGraph V) [G.LocallyFinite] (n : Nat),
  2 < n ->
  (forall v, G.degree v <= n) ->
  (forall c : G.ConnectedComponent,
    Not (IsNSimplex c.toSimpleGraph n)) ->
  G.Colorable n
```

The probe's two direct imports are
`Mathlib.Combinatorics.SimpleGraph.Coloring` and
`Mathlib.Combinatorics.SimpleGraph.Finite`. They authenticate only the intake candidate. Neither is
claimed minimal for the exact network-domain target, because that target has not been selected or
transported.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

A bounded repository-local and pinned-mathlib Lean search found no named Brooks declaration or
degree-to-colorability target. This is statement-feasibility evidence only, not the downstream
immutable anchor audit or a global absence claim.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root unless
a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0858` | 0 | rank 1412; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped read-only inspection of the manifest, blueprint, skill, catalog, Stage0, and intake | 0 | the intake deliberately leaves the exact source/model target, imports, expression hash, transports, and mutations open |
| read-only Crossref API and Cambridge publisher-page requests for DOI `10.1017/S030500410002168X` | 0 | bibliographic identity and first-page preview confirmed; the page exposes a `Get access` boundary, no full content to this worker, and no linked correction relation |
| `sha256sum` on the exact authority, intake, toolchain, lockfile, probe, and pinned-mathlib paths listed in the structured blocker | 0 | digests agree with `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0858/check_intake.py` | 1 | historical replay stops because it freezes intake state `[ ]` while the integrated authoritative DAG records `[_]`; the checker was preserved rather than weakened |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree agree; dependency worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0858/IntakeProbe.lean` | 0 | nine pinned graph APIs plus `IsNSimplex` and `Brooks1941SourceEnvelope` elaborated; stdout SHA-256 `ae01b6d6...f716ca`; no theorem or proof body |
| bounded Brooks/degree-colorability search over repository-local and pinned-mathlib Lean | 0 | no exact target declaration located; only unrelated `FiveWheelLike` clique-free/minimum-degree colorability hits; discovery only |
| prohibited Lean construct scan over the owned path | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| blocker JSON parse/invariants, scoped whitespace checks, and root self-test absence check | 0 | blocker identity, null canonical fields, unchanged debt vector, false completion flags, exact two-file scope, file hygiene, and intentional self-test absence agree; blocker consistency only |

## Retry Condition

The integration lane must first revalidate and master-accept refreshed intake evidence. Accountable
reviewers must lawfully admit the complete Brooks source, independently approve the exact theorem,
proof boundary, assumptions, corrections and errata, and decide the source network model. If
parallel lines remain in scope, a future worker must formalize and kernel-check the collapse-to-
`SimpleGraph` transport above, or use a faithful multigraph target, without changing the degree,
component, simplex, infinite-carrier, or colorability semantics.

Only then can a fresh statement worker freeze the ordered binders and boundary cases, certify
minimal pinned imports, serialize and hash the exact elaborated expression and environment, compile
every credited alternate transport, and run all four required mutation classes.

This is a truthful blocked-attempt record. Lifecycle remains `planned`; the item remains `[ ]`; the
root remains `[H1, M3, R4]`; `audit_complete: false` and `theorem_complete: false`; no debt change is
proposed. Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, proof credit, or master acceptance is claimed.
