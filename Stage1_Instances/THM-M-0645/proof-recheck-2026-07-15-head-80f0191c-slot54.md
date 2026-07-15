# THM-M-0645 proof recheck at `80f0191c` (slot54)

Item: `S56-M-0645-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T15:24:02+08:00`

Base revision: `80f0191c83a1bb4026c2d490be957cf109464de1`

Base tree: `b89a01cfc623bf97d1896fb3534a1ac24381fa71`

## Verdict

`blocked`. No positive proof body can truthfully close the exact frozen target because the owned,
placeholder-free module `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0645.not_completenessTarget :
  Not Stage1Instances.THM_M_0645.CompletenessTarget
```

The defect is in the frozen custom calculus. `Provable` specializes `Derivation`'s free-variable
type to `Empty`, while `Derivation.allIntro` requires an explicit eigenvariable `x : alpha`.
Universal introduction is therefore impossible in a closed derivation. A structural induction
shows that every remaining derivation constructor preserves `proofInvariant`, in which every
universally quantified formula is false. The universe-polymorphic symbol-free sentence
`forall x, x = x` is nevertheless semantically valid, violates that invariant, and is not
provable. Instantiating the exact root with this language and sentence yields the checked negation.

This refutes only the defective Lean target, not Goedel's mathematical completeness theorem. The
first failed gate is exact-target truth and consistency at `M0645-D-CALCULUS`, before Henkin or
term-model proof execution. The predecessor graph retains its authoritative open `M4` state; this
proof evidence diagnoses an `M5` statement/calculus mismatch without rewriting predecessor state.

The existing `Proof.lean` declarations are real but conditional. `builder_of_countermodel` takes an
explicit `CountermodelProperty` premise, and `completenessTarget_of_countermodel` composes it with
the exact-root wrapper. Neither declaration constructs that premise, so neither closes the positive
root. A repo-local and pinned-mathlib search found no terminal completeness theorem for this custom
`Derivation`; a consistent dependency could not prove the refuted target in any event.

The proof item remains `[ ]`, lifecycle remains `planned`, and the accepted root vector remains
`[H2, M4, R4]`. No proof receipt, audit completion, validation, release, theorem completion, or
master acceptance is claimed. Because the assigned positive proof phase is not complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Scoped Validation

All checks ran inside this worker clone. The automation-provided `.lake` symlink and already-built
pinned packages were reused read-only. No update, build, clone, fetch, network operation, or `.lake`
mutation was performed. Lean sources and outputs were copied to a disposable `/tmp` directory and
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at ranks 1 through 1546 and the uniform L0/rework-required baseline passed. |
| `python3 scripts/stage1_target.py show THM-M-0645` | 0 | Rank 691; planned `hard_statement_first_partial_verification` lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0645/check_statement.py` | 0 | Canonical expression hash `76fbce...7ea68`; all four required statement mutations were distinguished; pinned versions matched. |
| Isolated `lake env lean --trust=0 -t0` replay below | 0 | `Statement`, `ObligationTree`, `Proof`, and `Counterexample` elaborated in dependency order. |
| Comment-stripped source scan plus output/axiom assertions in the replay | 0 | No prohibited proof device or `sorryAx`; all audited axiom sets were subsets of `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0645/check_obligation_tree.py` | 0 | 15 obligations and 43 typed edges passed; denominator `ade5c7f4...7fc01`; predecessor root remains open M4. |
| `python3 Stage1_Instances/THM-M-0645/check_anchor_audit.py` | 0 | Anchor receipt `d61ebc24...1506` and pinned mathlib revision passed. |
| Independent trust-zero replay | 0 | A separate worker copied `Statement.lean` and `Counterexample.lean` to `/tmp`; both elaborated and the exact negation used only the three allowed axioms. |
| `python3 -m json.tool Stage1_Instances/THM-M-0645/proof-recheck-2026-07-15-head-80f0191c-slot54.json` plus source-hash and fail-closed status assertions | 0 | Blocker JSON parsed; all recorded source hashes matched; verdict stayed `blocked`, state `[ ]`, and all completion fields stayed false. |
| `git diff --check -- Stage1_Instances/THM-M-0645` | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test manifest exists. |

Exact successful replay command, run from the worker root:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0645
lean_dir=$root/Formalizations/Lean
lean=$(cd "$lean_dir" && env -u LEAN_PATH lake env which lean)
base_path=$(cd "$lean_dir" && env -u LEAN_PATH lake env printenv LEAN_PATH)
tmp=$(mktemp -d /tmp/thm-m-0645-head80f0191c.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target"/{Statement,ObligationTree,Proof,Counterexample}.lean "$tmp"/
for mod in Statement ObligationTree Proof Counterexample; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" \
    timeout --foreground --kill-after=5s 300 "$lean" \
    --trust=0 -t0 -R "$tmp" -o "$tmp/$mod.olean" "$tmp/$mod.lean" \
    >"$tmp/$mod.out" 2>&1
done
```

The run then stripped comments before scanning each source for `sorry`, `admit`, `sorryAx`,
declared `axiom`, `constant`, `opaque`, `unsafe`, `extern`, `implemented_by`, or `native_decide`;
rejected any error or `sorryAx` diagnostic; parsed every `#print axioms` result from `Proof.out` and
`Counterexample.out`; and required every axiom set to be a subset of `propext`,
`Classical.choice`, and `Quot.sound`.

| Artifact | SHA-256 |
|---|---|
| `Statement.olean` | `25eb67ade92875261cb4dafa5ae9075c3fe28e1e657ac763d2b7624430e04024` |
| `ObligationTree.olean` | `6c98e1bb9243a0930eae92822ff4d7a1043165662164476f7c47f7b0894bc614` |
| `Proof.olean` | `7c54139cf4e0d1fc38e44d2f6c1cca225e2fd83bd46dc35daa60ab86b344e7ce` |
| `Counterexample.olean` | `8dcfbde337211b11b3eb525b6f3cc2a5a191f3abfd60fc7d312725382d300c32` |
| `Proof` output | `bfd3e14def163e4418a27cd1c1890dbe8e26ff0cf2c2589ff3631541c48b5e2b` |
| `Counterexample` output | `80fb95cd6ab7948cfd7822889b590175b38af7d6180dd61103cbc634e37f48c1` |

Lean reported version 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib was pinned at
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

This current-base evidence changes no scheduler state. It does not satisfy `S56-M-0645-PROOF`,
close the positive root, or claim audit completion, validation, release, theorem completion,
receipt acceptance, or master acceptance.
