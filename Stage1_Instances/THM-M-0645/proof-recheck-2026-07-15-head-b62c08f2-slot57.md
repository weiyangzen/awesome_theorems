# THM-M-0645 Proof-Phase Recheck

Item: `S56-M-0645-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T14:05:50+08:00`

Base revision: `b62c08f262435e44a30ad3fc88a4712e3954afc7`

Base tree: `f7374dcf5690374a2e9e5d13ac124b34c7ecfab1`

## Verdict

`blocked`. A positive proof body cannot truthfully close the exact frozen target because its
negation is already kernel checked. `Counterexample.lean` proves, without placeholders,

```text
Stage1Instances.THM_M_0645.not_completenessTarget :
  Not Stage1Instances.THM_M_0645.CompletenessTarget
```

`Provable` specializes `Derivation` to the free-variable type `Empty`, but
`Derivation.allIntro` requires an explicit eigenvariable `x : alpha`. Universal introduction is
therefore impossible in a closed derivation. A structural invariant proves that all remaining
constructors preserve a syntactic interpretation in which universal formulas are false. The
symbol-free sentence `forall x, x = x` is semantically valid, violates that invariant, and is not
provable. Instantiating the exact root with this language and sentence yields the checked negation.

This diagnoses only the defective custom calculus and target frozen in `Statement.lean`; it does
not refute Goedel's mathematical completeness theorem. The proof item remains `[ ]`, the positive
root is open, and no `.stage1-worker-selftest.json` is written.

## Proof Boundary

The existing `Proof.lean` bodies are real but conditional. `builder_of_countermodel` converts an
explicit `CountermodelProperty` premise into `CompletenessDerivationBuilder`, and
`completenessTarget_of_countermodel` composes it with the exact-root wrapper. Neither declaration
constructs `CountermodelProperty`. They supply no positive root proof and are consistent with the
checked refutation.

The first failed gate is exact-target truth and consistency at `M0645-D-CALCULUS`, before Henkin
or term-model execution. The predecessor graph retains its accepted open `M4` architecture because
this proof worker cannot rewrite predecessor authority; the current proof evidence diagnoses an
`M5` statement/calculus mismatch.

## Validation

Preflight and structural commands run from the worker root:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0645` | 0 | rank 691; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0645/check_obligation_tree.py` | 0 | 15 obligations and 43 typed edges passed; predecessor root remains open `M4` |
| `python3 Stage1_Instances/THM-M-0645/check_anchor_audit.py` | 0 | pinned mathlib revision and anchor receipt hash passed |

At preflight, the automation-provided `.lake` symlink pointed to a shared `flt-regular` checkout
with no resolvable `HEAD`. Another concurrent actor populated that checkout during this run. This
worker did not run `lake update`, `lake build`, `git clone`, `git fetch`, or any dependency repair
or mutation command, so the changing shared checkout cannot support an immutability claim.

The narrow current-base replay copied `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and
`Counterexample.lean` to a fresh `/tmp` directory, assembled `LEAN_PATH` only from already-existing
compiled package directories, selected the Lean executable with `lake env which lean`, and
confirmed that executable matched the version pinned by `lean-toolchain`. It used
`LEAN_NUM_THREADS=1`, `--trust=0`, `-t0`, and `-R <tmp>`. All outputs were confined to the temporary
directory and removed. All four modules exited 0.

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0645
lake_root=$root/Formalizations/Lean/.lake
lean=$(cd "$root/Formalizations/Lean" && lake env which lean)
paths=()
for p in "$lake_root"/packages/*/.lake/build/lib/lean; do
  test -d "$p" && paths+=("$p")
done
paths+=("$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean")
lean_path=$(IFS=:; printf '%s' "${paths[*]}")
tmp=$(mktemp -d /tmp/thm-m-0645-headb62c08f2.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target"/{Statement,ObligationTree,Proof,Counterexample}.lean "$tmp"/
for mod in Statement ObligationTree Proof Counterexample; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" \
    --trust=0 -t0 -R "$tmp" -o "$tmp/$mod.olean" "$tmp/$mod.lean" \
    >"$tmp/$mod.out" 2>&1
done
```

The run then applied the comment-stripped prohibited-device scan and parsed each `#print axioms`
report, requiring it to be a subset of the three allowed axioms before hashing the temporary
outputs. No project build directory was placed on `LEAN_PATH`.

A comment-stripped scan found no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`,
`unsafe`, `extern`, `implemented_by`, or `native_decide` proof device. Output checks found no error
or sorry diagnostic. Every audited declaration had an axiom set contained in `propext`,
`Classical.choice`, and `Quot.sound`; `not_completenessTarget` used exactly those three.

| Artifact | SHA-256 |
|---|---|
| `Statement.olean` | `25eb67ade92875261cb4dafa5ae9075c3fe28e1e657ac763d2b7624430e04024` |
| `ObligationTree.olean` | `6c98e1bb9243a0930eae92822ff4d7a1043165662164476f7c47f7b0894bc614` |
| `Proof.olean` | `7c54139cf4e0d1fc38e44d2f6c1cca225e2fd83bd46dc35daa60ab86b344e7ce` |
| `Counterexample.olean` | `8dcfbde337211b11b3eb525b6f3cc2a5a191f3abfd60fc7d312725382d300c32` |
| `Proof` output | `bfd3e14def163e4418a27cd1c1890dbe8e26ff0cf2c2589ff3631541c48b5e2b` |
| `Counterexample` output | `80fb95cd6ab7948cfd7822889b590175b38af7d6180dd61103cbc634e37f48c1` |

The replay used Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, executable SHA-256
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). An independent subagent repeated the isolated
trust-zero `Statement` and `Counterexample` replay and obtained the same hashes and axiom reports.
This is narrow nonrelease blocker evidence, not hermetic release validation.

## Retry Condition

Positive proof work may resume only after an authorized statement-phase repair replaces the
unusable universal-introduction interface with a source-faithful eigenvariable or context-extension
rule. The repaired calculus must derive the quantified empty-language equality boundary. The
integration lane must then accept a new statement fingerprint, publish an append-only registry
delta, and rerun statement mutation testing, anchor audit, obligation-tree construction, and proof
execution in dependency order.

This current-base report changes no scheduler state and claims no proof completion, audit
completion, validation, release, theorem completion, receipt acceptance, or master acceptance.
