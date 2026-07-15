# THM-M-0645 proof recheck at current base

Item: `S56-M-0645-PROOF`

Intent: `prove`

Recorded at: `2026-07-16T04:50:59+08:00`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

## Verdict

`blocked`. The assigned proof phase remains `[ ]`; no completion self-test or proof receipt is
issued. The required schema-1.1 dependency ledger has been added first and validates as a genuinely
empty audit: this v2 node has no hard parent, transitive ancestor, incoming hard edge, reuse hint,
or shared group. The ledger therefore transfers no proof credit.

The exact frozen positive target cannot be proved truthfully because its negation is kernel checked:

```text
Stage1Instances.THM_M_0645.not_completenessTarget :
  Not Stage1Instances.THM_M_0645.CompletenessTarget
```

`Provable` specializes `Derivation`'s free-variable type to `Empty`, while
`Derivation.allIntro` requires an explicit eigenvariable `x : alpha`. Universal introduction is
therefore unusable for closed derivations. `Counterexample.lean` proves an invariant for every
remaining derivation constructor in which universally quantified formulas are false. It then shows
that the symbol-free sentence `forall x, x = x` is valid in every nonempty structure but is not
provable. Applying the frozen root to that language and sentence proves its exact negation.

This refutes only the defective custom Lean calculus and target, not Goedel's mathematical
completeness theorem. Lifecycle stays `planned`; authoritative debt stays `[H2, M4, R4]`;
`root_closed=false`, `audit_complete=false`, and `theorem_complete=false`.

## Proof Boundary

`Proof.lean` contains real, placeholder-free conditional bodies:

```text
builder_of_countermodel : CountermodelProperty -> CompletenessDerivationBuilder
completenessTarget_of_countermodel : CountermodelProperty -> CompletenessTarget
```

They retain `CountermodelProperty` as an explicit premise and construct no inhabitant of it. They
cannot close a proposition whose exact negation is checked. Pinned mathlib supplies first-order
syntax and semantics, not a completeness theorem for this custom calculus. The audited repo-local
legacy module uses a different calculus and leaves its semantic-to-derivability bridge uninhabited.
The external anchor is neither a pinned exact body nor a transport into this inconsistent target.

The first failed gate is exact-target truth/consistency at `M0645-D-CALCULUS`. The predecessor
registry still presents its pre-refutation M4 architecture and `M0645-T-CLASSICAL` cut; this proof
worker records an M5 diagnosis without rewriting predecessor authority.

## Dependency Ledger

`dependency-reuse-ledger.json` is bound to:

- theorem DAG SHA-256 `73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`;
- context SHA-256 `068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`;
- repository revision `6bf9ee93a322e7d25cf9249226222095f95d1cff`; and
- zero inspections, reuse decisions, and unresolved compatibility obligations.

The scheduler validator accepts this exact empty closure. There is a separate worker-artifact
bootstrap conflict: the v2 generator excludes the ledger from dependency discovery but inventories
target-owned JSON evidence. Thus the new ledger and structured blocker make a fresh in-memory DAG
differ from the checked-in projection only at `THM-M-0645.evidence_inventory`. The worker must not
edit the protected generated DAG, so the global DAG/standard/cron validators honestly report that
mismatch. The integration lane can regenerate the DAG after preserving this blocked packet. This
failure supplies no proof evidence and is not hidden as a passing gate.

## Narrow Validation

All commands ran inside the worker clone. The automation-provided `.lake` symlink and existing
pinned artifacts were reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
network request, or `.lake` mutation was performed. Lean sources and outputs were copied to a
fresh `/tmp` directory and removed on exit.

| Command | Exit | Result |
|---|---:|---|
| `sha256sum Docs/Stage1_Theorem_DAG_v2.json` | 0 | Graph digest `73e99d22...40eca` matched the scheduler context. |
| Schema-1.1 `validate_dependency_reuse_ledger` call | 0 | Empty closure passed with zero inspections, decisions, and unresolved obligations. |
| `python3 scripts/stage1_target.py check` | 0 | All 1,546 unique ordered L0/rework-required targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0645` | 0 | Rank 691; lifecycle planned; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0645/check_statement.py` | 0 | Expression hash `76fbce83...7c7ea68` matched; four structural mutations were distinguished. |
| Isolated four-module `lake env lean --trust=0 -t0` replay below | 0 | All modules elaborated; the exact negation used only allowed axioms; prohibited-device scans passed. |
| `python3 Stage1_Instances/THM-M-0645/check_obligation_tree.py` | 0 | 15 obligations and 43 typed edges passed; predecessor root remains open M4. |
| `python3 Stage1_Instances/THM-M-0645/check_anchor_audit.py` | 0 | Anchor receipt and pinned mathlib revision passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | First-ledger evidence-inventory bootstrap mismatch described above. |
| `python3 Docs/tools/check_stage1_standard.py` | 1 | Delegated DAG validator failed for the same mismatch. |
| `python3 scripts/stage1_execution_cron.py --validate-only --workers 0` | 1 | Delegated DAG validator failed for the same mismatch. |

Exact successful replay command:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0645
lean_dir=$root/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0645-slot46.XXXXXX)
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
rg -F 'Stage1Instances.THM_M_0645.completenessTarget_of_countermodel' "$tmp/Proof.out"
sha256sum "$tmp"/{Statement,ObligationTree,Proof,Counterexample}.olean \
  "$tmp"/{Statement,ObligationTree,Proof,Counterexample}.out
```

Replay SHA-256 values:

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

Lean is 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib is
`8a178386ffc0f5fef0b77738bb5449d50efeea95` at tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. `not_completenessTarget` reports
exactly `propext`, `Classical.choice`, and `Quot.sound`.

## Retry Condition

Positive proof work may resume only after an authorized statement repair replaces the unusable
universal-introduction interface with a source-faithful eigenvariable or context-extension rule.
The repaired calculus must derive the quantified empty-language equality boundary. The integration
lane must then accept the new statement fingerprint and regenerate the statement-dependent anchor,
obligation registry, typed graphs, validation specifications, and proof architecture in dependency
order.

This blocker changes no scheduler state, closes no obligation, accepts no receipt, and supports no
proof completion, validation, release, audit completion, theorem completion, or master acceptance.
Because `S56-M-0645-PROOF` is not complete, `.stage1-worker-selftest.json` is deliberately absent.
