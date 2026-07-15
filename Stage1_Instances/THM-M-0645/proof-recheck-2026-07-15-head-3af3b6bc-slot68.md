# THM-M-0645 Proof-Phase Recheck

Item: `S56-M-0645-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T16:55:34+08:00`

Base revision: `3af3b6bc58d308bda7dc1cb164a9a258512b8c53`

Base tree: `65dce2e2ba00c806bf25b436c98caf996c1c56d2`

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

The scheduler projects the intake through obligation-tree predecessors as `[_]`, not accepted
`[x]`. Target-local structured projections also predate the refutation: `task-dag.json` remains
more conservative, while `typed-graphs.json` labels the conditional assembly node `M0-L` without
an evidence ID. Neither projection supplies proof credit. Reconciliation belongs to the master and
must follow an authorized statement repair; this proof worker does not rewrite predecessor state.

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
| Isolated direct `lake env which lean` replay below | 0 | `Statement`, `ObligationTree`, `Proof`, and `Counterexample` elaborated in dependency order under `--trust=0 -t0`. |
| Comment-stripped proof-device and diagnostic scan | 0 | No `sorry`, `admit`, `sorryAx`, declared `axiom`, `constant`, `opaque`, `unsafe`, `extern`, `implemented_by`, or `native_decide`; audited axioms are within `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0645/check_obligation_tree.py` | 0 | 15 obligations and 43 typed edges passed; denominator `ade5c7f4...7fc01`; predecessor root remains open M4. |
| `python3 Stage1_Instances/THM-M-0645/check_anchor_audit.py` | 0 | Anchor receipt `d61ebc24...1506` and pinned mathlib revision passed. |
| Two independent read-only audits | 0 | Both identified the `Empty` eigenvariable defect and independently concluded that no positive proof of the exact root exists. |

Exact successful replay command from the worker root:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0645
tmp=$(mktemp -d /tmp/thm-m-0645-head3af3b6bc-slot68.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target"/{Statement,ObligationTree,Proof,Counterexample}.lean "$tmp"/
lean=$(cd "$root/Formalizations/Lean" && env -u LEAN_PATH lake env which lean)
base_path=$(cd "$root/Formalizations/Lean" && env -u LEAN_PATH lake env printenv LEAN_PATH)
for mod in Statement ObligationTree Proof Counterexample; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" \
    timeout --foreground --kill-after=5s 300s "$lean" \
    --trust=0 -t0 -R "$tmp" -o "$tmp/$mod.olean" "$tmp/$mod.lean" \
    >"$tmp/$mod.out" 2>&1
done
```

The replay put the fresh target directory first in `LEAN_PATH`, so the local modules, rather than
same-named project artifacts, were imported. An exploratory invocation through `lake env lean`
itself resolved stale same-named build artifacts during `Proof.lean` and failed; no evidence is
credited to that run. This is a validation-recipe robustness warning about generic module names,
not a source-syntax defect. Directly invoking the executable returned by `lake env which lean`
against the fresh path produced:

| Artifact | SHA-256 |
|---|---|
| `Statement.olean` | `25eb67ade92875261cb4dafa5ae9075c3fe28e1e657ac763d2b7624430e04024` |
| `ObligationTree.olean` | `6c98e1bb9243a0930eae92822ff4d7a1043165662164476f7c47f7b0894bc614` |
| `Proof.olean` | `7c54139cf4e0d1fc38e44d2f6c1cca225e2fd83bd46dc35daa60ab86b344e7ce` |
| `Counterexample.olean` | `8dcfbde337211b11b3eb525b6f3cc2a5a191f3abfd60fc7d312725382d300c32` |
| `Proof` output | `bfd3e14def163e4418a27cd1c1890dbe8e26ff0cf2c2589ff3631541c48b5e2b` |
| `Counterexample` output | `80fb95cd6ab7948cfd7822889b590175b38af7d6180dd61103cbc634e37f48c1` |

The environment used pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). `#print axioms` reported exactly
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
