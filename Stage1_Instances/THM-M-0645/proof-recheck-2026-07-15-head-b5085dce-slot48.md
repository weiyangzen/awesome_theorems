# THM-M-0645 proof-phase blocker recheck

Item: `S56-M-0645-PROOF`

Theorem: `THM-M-0645`

Intent: `prove`

Verdict: `blocked`

State: `[ ]`

Recorded at: `2026-07-15T23:59:53+08:00`

Base revision: `b5085dcef95933c753b6877bce0f634c1082a98d`

Base tree: `c9baed8c952fce6f884a6ee997845c0ec979b52b`

## Exact blocker

The assigned positive proof cannot be implemented truthfully for the frozen target. In
`Statement.lean`, `Provable` specializes `Derivation`'s free-variable type to `Empty`, while the
`allIntro` constructor requires an explicit eigenvariable `x : alpha`. Universal introduction is
therefore unavailable in every closed derivation.

`Counterexample.lean` gives exact kernel evidence rather than a conjectural diagnosis. Its
structural induction proves that every closed derivation satisfies `proofInvariant`, in which every
universal formula is false. It then constructs the universe-polymorphic symbol-free sentence
`forall x, x = x`, proves it valid in every nonempty structure, proves it is not derivable, and
exports the exact countertheorem

```text
Stage1Instances.THM_M_0645.not_completenessTarget :
  Not Stage1Instances.THM_M_0645.CompletenessTarget
```

The conditional bodies in `Proof.lean` do not repair this conflict.
`builder_of_countermodel` and `completenessTarget_of_countermodel` both require an explicit
`CountermodelProperty` premise; neither constructs that premise or closes the positive root. The
pinned mathlib snapshot contains no syntactic completeness theorem for this custom calculus. The
audited external Foundation theorem uses a different proof system and toolchain and cannot be
transported consistently into a proposition whose negation is kernel checked.

The first failed gate is exact-target truth and consistency at `M0645-D-CALCULUS`, before the
Henkin or term-model route. The proof-phase diagnosis is `M5`, but this worker does not rewrite the
predecessor statement, registry, graph, or authoritative `[H2, M4, R4]` vector. The defect refutes
only this frozen custom Lean calculus and target, not Goedel's mathematical completeness theorem.
No obligation or receipt is closed, and no audit, validation, release, theorem completion, or
master acceptance is claimed. Because the requested positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

The semantic target inputs are byte-identical to the preceding integrated blocker-report base
`87ffd1cab865c5d4e1f6828412182c2069c87fde`. This recheck nevertheless replayed every narrow gate
on the current base.

## Current-base validation

All commands ran in the worker clone. The automation-provided `.lake` symlink and existing pinned
packages were reused without `lake update`, `lake build`, clone, fetch, network access, or
dependency mutation. Lean sources and outputs for the direct replay were confined to a disposable
`/tmp` directory and removed by a trap. The untracked automation symlink makes this nonrelease
evidence; no hermetic or release claim is made.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at ranks 1 through 1546 and the uniform L0/rework-required baseline passed. |
| `python3 scripts/stage1_target.py show THM-M-0645` | 0 | Rank 691; planned `hard_statement_first_partial_verification` lane; theorem incomplete. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0645/check_statement.py` | 0 | Canonical expression hash `76fbce83...7c7ea68` and pinned revisions matched; all four structural mutations were distinguished. |
| Isolated four-module `lake env lean --trust=0 -t0` replay below | 0 | `Statement`, `ObligationTree`, `Proof`, and `Counterexample` elaborated in dependency order. |
| Comment-stripped prohibited-device and Lean-diagnostic scans | 0 | No `sorry`, `admit`, declared axiom, unsafe/oracle device, or `sorryAx`; the exact negation uses only `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0645/check_obligation_tree.py` | 0 | 15 obligations and 43 typed edges passed; denominator `ade5c7f4...7fc01`; the stale predecessor graph still records an open M4 root. |
| `python3 Stage1_Instances/THM-M-0645/check_anchor_audit.py` | 0 | Anchor receipt `d61ebc24...1506` and pinned mathlib revision passed. |
| `git diff --quiet 87ffd1cab865c5d4e1f6828412182c2069c87fde..b5085dcef95933c753b6877bce0f634c1082a98d -- Stage1_Instances/THM-M-0645/{Statement.lean,ObligationTree.lean,Proof.lean,Counterexample.lean,statement.json,anchor-audit.json,obligation-registry.json,typed-graphs.json,proof-blocker.json}` | 0 | The nine semantic inputs are byte-identical to the preceding integrated blocker-report base. |
| `git status --short` | 0 | Only the pre-existing automation `.lake` symlink and this owned JSON/Markdown pair are untracked; there are no tracked changes. |
| `git diff --check -- Stage1_Instances/THM-M-0645` plus direct whitespace/EOF checks for the two untracked files | 0 | No whitespace, CRLF, or missing-final-newline error. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test is deliberately absent because this positive proof item is blocked. |

Three parallel read-only peer audits also inspected the requirements, exact proof/refutation, and
history/current-base handoff. They independently reproduced the trust-zero Lean hashes or checked
the relevant sources, and found no positive-closure route. These reviews are corroboration only,
not executable independent-verification or release receipts.

Exact successful Lean replay from the worker root:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0645
lean_dir=$root/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0645-headb5085dce-slot48.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target"/{Statement,ObligationTree,Proof,Counterexample}.lean "$tmp"/
base_path=$(cd "$lean_dir" && {
  for path in .lake/packages/*/.lake/build/lib/lean; do
    test -d "$path" && realpath "$path"
  done
  lean=$(env -u LEAN_PATH lake env which lean)
  realpath "$(dirname "$(dirname "$lean")")/lib/lean"
} | paste -sd:)
for mod in Statement ObligationTree Proof Counterexample; do
  (
    cd "$lean_dir"
    LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300s \
      env -u LEAN_PATH lake env env LEAN_PATH="$tmp:$base_path" \
      lean --trust=0 -t0 -R "$tmp" -o "$tmp/$mod.olean" "$tmp/$mod.lean"
  ) >"$tmp/$mod.out" 2>&1
done
for source in "$tmp"/{Statement,ObligationTree,Proof,Counterexample}.lean; do
  perl -0777 -pe 's!/\-.*?\-/!!gs; s/--[^\n]*//g' "$source"
done >"$tmp/scoped-stripped.lean"
! rg -n '\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe|extern|implemented_by|native_decide)\b' \
  "$tmp/scoped-stripped.lean"
! rg -n 'declaration uses .sorry|sorryAx' "$tmp"/*.out
rg -F "'Stage1Instances.THM_M_0645.not_completenessTarget' depends on axioms: [propext, Classical.choice, Quot.sound]" \
  "$tmp/Counterexample.out"
rg -F "'Stage1Instances.THM_M_0645.completenessTarget_of_countermodel' depends on axioms: [propext," \
  "$tmp/Proof.out"
rg -F " Classical.choice," "$tmp/Proof.out"
rg -F " Quot.sound]" "$tmp/Proof.out"
sha256sum "$tmp"/{Statement,ObligationTree,Proof,Counterexample}.olean \
  "$tmp"/{Statement,ObligationTree,Proof,Counterexample}.out
```

The explicit `LEAN_PATH` puts the copied modules before pinned package libraries and excludes
project build output, so no stale target olean can satisfy the check.

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

The replay used Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, executable SHA-256
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` at tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry condition

Positive proof work can resume only after an authorized statement-phase repair replaces the
unusable universal-introduction interface with a source-faithful rule that works for closed
sentences. The repaired calculus must derive the quantified equality boundary. The integration
lane must then accept the new statement fingerprint, publish an append-only obligation-registry
delta, and rerun statement testing, anchor audit, obligation-tree construction, and proof execution
in dependency order.

## Status boundary

This is fresh negative kernel evidence for `S56-M-0645-PROOF`, not a positive proof receipt. The
item remains `blocked` and `[ ]`; lifecycle remains `planned`; root closure, audit completion,
theorem completion, and master acceptance remain false.
