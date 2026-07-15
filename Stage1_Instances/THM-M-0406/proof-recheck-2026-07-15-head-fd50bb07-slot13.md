# THM-M-0406 proof-phase recheck at `fd50bb07`

Item: `S56-M-0406-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `fd50bb07f6632a2ad0bdc17737c200432ee242c8`

Base tree: `ed66432029954bfa5b17e0afda5f3817eeb32d48`

## Verdict

`blocked`. A consistent positive proof body cannot be implemented for the
exact frozen Lean proposition. The existing placeholder-free declaration

```text
Stage1Instances.THMM0406.not_corvajaZannierTheoremOne :
  Not (Stage1Instances.THMM0406.CorvajaZannierTheoremOne.{0, 0} (k := Rat))
```

kernel-checks against the current pinned Lean closure. Its model uses
`boundaryDivisor := Fin 4`, all four components, unit weights and intersection
numbers, true geometric premises, and `curve := Empty`. Thus every frozen
premise holds while the conclusion would produce an inhabitant of `Empty`.

This refutes the disconnected abstract encoding, not the mathematical
Corvaja--Zannier theorem. `SurfaceData` does not intrinsically relate its
scheme, curve, point, divisor, or predicate fields. The
`SurfaceDegeneracyEngine` in `ObligationTree.lean` is definitionally the same
refutable proposition; its conditional adapters add no positive proof body.

The frozen transcription also omits source-required diagonal intersection
equations. The dossier-pinned `math/0206100` source requires
`p_i p_j (D_i . D_j) = c` for every pair, including `i = j`, while
`HasTheoremOneBoundary` guards the equation by `D1 != D2`. Its finite-place
set also omits the source's archimedean places, and its geometric interfaces
are arbitrary fields rather than intrinsic objects.

No proof body or receipt was added, no obligation was closed, and the proof
item remains `[ ]`. The frozen vector remains `[H1, M4, R3]`; the checked
negative evidence supports a fail-closed `[H1, M5, R3]` proposal, but this
worker does not modify authority or promote state. Audit and theorem
completion are false. `.stage1-worker-selftest.json` is deliberately absent.

The blueprint projects the obligation-tree predecessor as worker-provisional
`[_]`, while target-owned `task-dag.json` still records it `open`. There were
already 96 `proof-recheck-*` artifacts before this packet. The five-unresolved-
tick split trigger has long fired, so another identical proof retry cannot
progress without upstream repair.

## Failed gate and retry

The first failed gate is `M0406-S-DEFINITIONS` / exact-target consistency and
source fidelity. The remaining root cut set is `M0406-S-DEFINITIONS` and
`M0406-ROOT`.

Master/integration must stop identical proof retries, reopen and split at
`M0406-S-DEFINITIONS`, and authorize a source-faithful proposition whose
intrinsic, noncircular geometric semantics rule out the checked model and
include all source-required intersection cases. It must then freeze a new
exact expression and obligation registry and rerun statement, anchor-audit,
and obligation-tree gates. Adding only `Nonempty X.curve`, assuming the proof
engine, or proving a realizable specialization would substitute the target.

## Validation

All commands ran in this worker clone. No `lake update`, `lake build`,
dependency clone/fetch, checkout, or intentional `.lake` mutation was
performed. Temporary Lean objects were written under `/tmp` and removed. The
automation-provided untracked `Formalizations/Lean/.lake` symlink makes this
nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| Read the rev-5.6 standard, execution skill, manifest/DAG entry, guidelines, and target artifacts | 0 | Ownership, dependency, proof, blocker, split-trigger, evidence, and no-overclaim rules reviewed. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | Rank 19; planned; L0/rework-required; theorem incomplete. |
| Pre-write `git status --short --untracked-files=all`; `git rev-parse HEAD HEAD^{tree}` | 0 | Only `?? Formalizations/Lean/.lake`; base `fd50bb07...42c8`, tree `ed664320...2d48`. |
| `python3 Stage1_Instances/THM-M-0406/check_obligation_tree.py` | 0 | Fourteen obligations and 26 typed edges passed; denominator `46deb9e2...d90a7`; root open M4. |
| `python3 Stage1_Instances/THM-M-0406/check_anchor_audit.py` | 0 | Six candidates and immutable pins passed; root open. |
| Isolated pinned `lake env lean --trust=0 -t0` replay | 0 | Statement/proof exits `0/0`; both declarations report exactly `[propext, Classical.choice, Quot.sound]`. |
| Broad prohibited-construct scan over owned Lean files | 1 | Expected no-match exit after reviewing multiline theorem hits; no prohibited proof escape occurs. |
| Final structured and whitespace checks | 0 | Companion JSON and blocker invariants passed; no whitespace errors; completion manifest remains absent. |

The isolated replay ran from `2026-07-15T19:24:13+08:00` through
`19:24:28+08:00`. Its hashes were:

| Input or output | SHA-256 |
|---|---|
| `Statement.lean` | `9d6e2a94131455eedcee2ae75765746958988f23f6398cc5c4ea3fbc193258ec` |
| `Proof.lean` | `afeb346ab8f1ff9e41b87395744faa7a352509d28ef842f10f18a3ec00874aaf` |
| statement output | `d75f6cfbd79a8f89ce74c827ba028608c5372e5299dceb94826e344c1ce7e022` |
| proof output | `861dd4c4de6e32c51877e23ba740e355ac9f23b79cdb61d79e03985c16f3eada` |
| temporary `Statement.olean` | `deafda332045568236e3354ba2870233cfdfd906e0105c9eb67b8fc575004a27` |
| temporary `Proof.olean` | `0657062f860c3291123f44bf3ece712003e49c6025427b0ccecd837dbe5a0c58` |

The structured companion binds the exact source hashes, environment pins,
countermodel, failed gate, retry condition, and status boundary. This packet
is durable blocker evidence only, not proof or completion credit.
