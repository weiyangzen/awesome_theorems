# THM-M-0115 statement recheck: blocked

Item: `S56-M-0115-STATEMENT`

Base revision: `69662621a19907de342801b09124e8dfe3495e40` (tree
`fbfbc07e2045accdd0144baf892481a9bb6717f8`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 62.

## Decision

The exact-statement gate remains blocked. The intake freezes the classical
Grothendieck-Riemann-Roch formula for a proper morphism `f : X -> Y` of nonsingular
quasi-projective varieties over an arbitrary field and every `alpha in K_0(X)`:

`ch(f_* alpha) cap td(T_Y) = f_*(ch(alpha) cap td(T_X))`

in rational Chow homology of `Y`. The left pushforward is on `K_0`; the right pushforward is on
Chow homology. Empty varieties and `alpha = 0` are included. The statement therefore requires
concrete compatible representations of the field-relative variety domain, nonsingularity,
quasi-projectivity, both pushforwards, Chern character, tangent bundles, Todd classes, and cap
action.

The pinned closure still does not expose these objects and maps together. Six bounded exact-topic
searches found no Grothendieck-Riemann-Roch, Chow group/ring, Chern-character, Todd-class, scheme
K-theory, or quasi-projective declaration in pinned mathlib. This is local surface evidence only,
not a global absence claim or the downstream anchor audit.

No authoritative `THM-M-0115` input changed after the previous recheck. The target manifest,
catalog and Stage0 records, legacy Stage1 blueprint, execution skill, guidelines, intake dossier,
legacy Lean module, toolchain, and dependency lock are unchanged. The rev-5.6 blueprint and
execution DAG changed only for unrelated item states; their `THM-M-0115` entries are unchanged.
The previous probe and recheck artifacts were integrated without a state transition.

The legacy `AwesomeTheorems.Stage1.S1_M_023.StatementShape` is not an admissible target because it
receives the desired `grrIdentity : Prop` as an input. `CandidateAStatementShape` and
`CandidateBStatementShape` quantify over arbitrary carriers and functions without the frozen
field-relative variety, quasi-projectivity, `K_0`, Chow, tangent, or characteristic-class semantics.
Their successful elaboration cannot identify the received claim.

The intake itself also retains statement-consistency debt: `instance.json` says "rational Chow
ring" in `canonical_statement` but rational Chow homology in `conclusion`, while the displayed
formula needs an explicit cap/fundamental-class convention. Resolving that discrepancy requires an
accountable source-scope review; this statement worker cannot silently choose a different theorem.

Consequently there is no canonical Lean expression whose imports can be minimized or whose
expression and environment can be fingerprinted. Checked transports and the four required mutation
classes remain undefined. The first failed gate is
`canonical_claim_to_concrete_lean_surface_mapping`. Lifecycle remains `planned`; the root vector
remains `H4 / M5 / R4`; the statement node remains `[ ]`; accepted receipt IDs remain empty. No
proof, debt change, audit completion, theorem completion, or master acceptance is claimed.

## Pinned Lean Boundary

`StatementProbe.lean` remains the strongest honest adjacent substrate. Its two direct imports are
`Mathlib.AlgebraicGeometry.Morphisms.Proper` and
`Mathlib.AlgebraicGeometry.Morphisms.Smooth`. It elaborates a field-relative scheme boundary with
smooth source and target structure morphisms and a proper morphism over the base. It deliberately
omits quasi-projectivity and every GRR-specific object and map. These imports are minimal only for
the probe, not for the absent canonical target.

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided `.lake` symlink was reused
read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was performed.

## Validation Record

Commands ran from this isolated worker clone unless another working directory is stated.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0115` | 0 | rank 23; planned; legacy slot `S1-M-023`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `Formalizations/Lean/.lake` symlink; base revision and tree match this record |
| scoped standard, source, intake, legacy-module, prior-blocker, and prior-recheck inspection | 0 | the frozen claim, exclusions, and source/API blockers remain unchanged |
| scoped `git diff ccab17a70dd799a6c34193b21d360a8f94611417..HEAD` | 0 | no target source, intake, legacy Lean, toolchain, or lock change; blueprint/DAG deltas are unrelated item states |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0115/StatementProbe.lean` | 0 | adjacent substrate elaborated; stdout 9 lines/656 bytes, SHA-256 `d7e1c9239e7597ff61115502aedc32611fd2968e91b8d2ec8af44f104fd57ca3`; stderr empty |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_023.lean` | 0 | legacy abstract module elaborated; stdout 111 lines/8807 bytes, SHA-256 `d38eb2772d093be737f7b41389d7aa8edc47f74ee200e55767800275c09be5e2`; no exact target validated |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | Lean and Lake versions match the pinned environment above |
| mathlib package status and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean at the pinned revision and tree above |
| six declaration-aware `rg` searches over pinned mathlib | 1 each, expected no match | no exact-topic GRR, Chow, Chern-character, Todd-class, scheme-K-theory, or quasi-projective declaration found |
| `python3 -m json.tool` on the paired recheck JSON | 0 | structured current-HEAD blocker record parsed |
| scoped blocker invariant assertions | 0 | item/base identity, blocked state, unchanged vector, null target/import/hash fields, undefined mutations, current hashes, two-file scope, and self-test absence agree |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` occurrence |
| scoped tracked and per-new-file `git diff --check` | 0 | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| final standard and target checks | 0 | target-set, projection, lifecycle, rank, and uniform-L0 invariants still pass |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the exact-statement gate failed |

## Retry Condition And Boundary

Retry after the intake is master-accepted, accountable reviewers preserve and approve an exact
source definition chain, the Chow codomain and cap convention are reconciled, and the pinned closure
gains concrete compatible APIs for the frozen variety domain, `K_0`, rational Chow homology, both
pushforwards, Chern character, tangent bundle, Todd class, and cap action. A fresh worker can then
encode only the same claim, minimize imports, fingerprint the elaborated expression and environment,
compile every transport, and distinguish all four mutation classes.

This is fresh current-HEAD blocker evidence only. Because the positive statement deliverable did
not pass, `.stage1-worker-selftest.json` is intentionally absent and no worker `[_]` or master
acceptance is requested.
