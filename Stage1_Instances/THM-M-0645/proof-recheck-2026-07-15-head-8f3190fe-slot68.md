# THM-M-0645 Proof-Phase Recheck

Item: `S56-M-0645-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T17:18:13+08:00`

Base revision: `8f3190fed598f6cb4547035d0d96d460ba5fc5cc`

Base tree: `d8ca24ac4a840d07b81dcc099a4d31023046d649`

## Verdict

`blocked`. No positive proof body can truthfully close the exact frozen target because the
placeholder-free module `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0645.not_completenessTarget :
  Not Stage1Instances.THM_M_0645.CompletenessTarget
```

The defect is in the frozen custom calculus, not Goedel's mathematical completeness theorem.
`Provable` fixes `Derivation`'s free-variable type to `Empty`, while `Derivation.allIntro` requires
an explicit eigenvariable `x : alpha`. Universal introduction is therefore impossible in a closed
derivation. A structural induction proves that all remaining constructors preserve an invariant
under which every universal formula is false. The symbol-free sentence `forall x, x = x` is valid
in every nonempty structure but violates the invariant and is not provable. Instantiating the
exact root with that language and sentence gives the checked negation above.

The existing `Proof.lean` declarations are real but conditional. `builder_of_countermodel` requires
an explicit `CountermodelProperty` premise, and `completenessTarget_of_countermodel` merely composes
that conditional result with the frozen root wrapper. Neither declaration constructs the premise
or closes the positive root. A pinned-mathlib or external theorem cannot transport to this false
target in a consistent environment.

The first failed gate is exact-target truth and consistency at `M0645-D-CALCULUS`, before Henkin or
term-model proof execution. The proof item remains `[ ]`, the lifecycle remains `planned`, and the
accepted root vector remains `[H2, M4, R4]`; this recheck only confirms an `M5` proof-phase
diagnosis. No obligation, receipt, audit, validation, release, theorem completion, or master
acceptance is claimed. Because the assigned positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

The scheduler projects the predecessors as worker-self-tested `[_]`, not accepted `[x]`.
Target-local structured projections also predate the refutation: `task-dag.json` remains more
conservative, while `typed-graphs.json` records an old conditional assembly and M4 cut set. Neither
projection supplies proof credit. The older `proof-blocker.md` predates `Counterexample.lean` and
describes the later countermodel interface rather than the earlier exact-target failure; this
current-base report supersedes it as proof-phase blocker evidence. Reconciliation belongs to the
master and must follow an authorized statement repair.

## Current-Base Validation

All checks ran inside this worker clone. The automation-provided `.lake` symlink and existing pinned
packages were reused read-only. No update, build, clone, fetch, network operation, or `.lake`
mutation was performed. Lean sources and outputs were copied to disposable `/tmp` directories and
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at ranks 1 through 1546 and the uniform L0/rework-required baseline passed. |
| `python3 scripts/stage1_target.py show THM-M-0645` | 0 | Rank 691; planned `hard_statement_first_partial_verification` lane; theorem incomplete. |
| `cd Formalizations/Lean && timeout --foreground --kill-after=5s 30s env -u LEAN_PATH lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3...ab16740`. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0645/check_statement.py` | 0 | All four mutations were killed; canonical expression and pinned mathlib hashes matched. |
| Fresh `/tmp` replay through `lake env lean` | 1 | `Statement` and `ObligationTree` elaborated; `Proof` imported the stale project `ObligationTree.olean` and failed with invalid-universe and unknown-identifier errors. This run receives no proof credit. |
| Isolated direct `lake env which lean` replay below | 0 | `Statement`, `ObligationTree`, `Proof`, and `Counterexample` elaborated in dependency order under `--trust=0 -t0`. |
| Comment-stripped proof-device and diagnostic scan | 0 | No `sorry`, `admit`, `sorryAx`, declared `axiom`, `constant`, `opaque`, `unsafe`, `extern`, `implemented_by`, or `native_decide`; audited axioms are within `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0645/check_obligation_tree.py` | 0 | 15 obligations and 43 typed edges passed; denominator `ade5c7f4...7fc01`; predecessor root remains open M4. |
| `python3 Stage1_Instances/THM-M-0645/check_anchor_audit.py` | 0 | Anchor receipt `d61ebc24...1506` and pinned mathlib revision passed. |
| Three independent read-only audits or replays | 0 | All identified the `Empty` eigenvariable defect; two independently replayed the exact negation. |

`lake env lean` itself is not credited for the four-module replay. The existing project build output
contains a colliding top-level `ObligationTree.olean`, and Lake prepends that output to
`LEAN_PATH`. An independent attempt consequently failed while elaborating `Proof.lean`. Removing or
rebuilding that artifact would violate the worker's `.lake` policy. The successful narrow replay
instead used the pinned executable selected by Lake, excluded project build output, and reused only
already-existing package libraries plus the toolchain library:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0645
tmp=$(mktemp -d /tmp/thm-m-0645-head8f3190fe-slot68.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target"/Statement.lean "$target"/ObligationTree.lean \
  "$target"/Proof.lean "$target"/Counterexample.lean "$tmp"/
lean=$(cd "$root/Formalizations/Lean" && env -u LEAN_PATH lake env which lean)
paths=()
for path in "$root"/Formalizations/Lean/.lake/packages/*/.lake/build/lib/lean; do
  test -d "$path" && paths+=("$path")
done
paths+=("$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean")
base_path=$(IFS=:; printf '%s' "${paths[*]}")
for mod in Statement ObligationTree Proof Counterexample; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" \
    timeout --foreground --kill-after=5s 300s "$lean" \
    --trust=0 -t0 -R "$tmp" -o "$tmp/$mod.olean" "$tmp/$mod.lean" \
    >"$tmp/$mod.out" 2>&1
done
```

| Artifact | SHA-256 |
|---|---|
| `Statement.olean` | `25eb67ade92875261cb4dafa5ae9075c3fe28e1e657ac763d2b7624430e04024` |
| `ObligationTree.olean` | `6c98e1bb9243a0930eae92822ff4d7a1043165662164476f7c47f7b0894bc614` |
| `Proof.olean` | `7c54139cf4e0d1fc38e44d2f6c1cca225e2fd83bd46dc35daa60ab86b344e7ce` |
| `Counterexample.olean` | `8dcfbde337211b11b3eb525b6f3cc2a5a191f3abfd60fc7d312725382d300c32` |
| `Statement` output | `80b80b2744011d9ae27ea98f08ab5102c3cd0ed979091ae7b7adba4179c88e37` |
| `ObligationTree` output | `ac9cf82f5caed589ebd1d642f3860f4fd0e4ecd2adf07afcf36d603e6f363357` |
| `Proof` output | `bfd3e14def163e4418a27cd1c1890dbe8e26ff0cf2c2589ff3631541c48b5e2b` |
| `Counterexample` output | `80fb95cd6ab7948cfd7822889b590175b38af7d6180dd61103cbc634e37f48c1` |

The environment used Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, executable SHA-256
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. `#print axioms` reported exactly
`propext`, `Classical.choice`, and `Quot.sound` for `not_completenessTarget`.

## Retry Condition

Positive proof work may resume only after an authorized statement-phase repair replaces the
unusable universal-introduction interface with a source-faithful eigenvariable or context-extension
rule. The repaired calculus must derive the quantified empty-language equality boundary. The
integration lane must then accept a new statement fingerprint, publish an append-only obligation
registry delta, and rerun statement mutation testing, anchor audit, obligation-tree construction,
and proof execution in dependency order.

This current-base evidence changes no scheduler state and does not satisfy
`S56-M-0645-PROOF`.
