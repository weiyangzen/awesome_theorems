# THM-M-1200 proof phase blocked on the current base

Item: `S56-M-1200-PROOF`. Base revision:
`6bf9ee93a322e7d25cf9249226222095f95d1cff`. Base tree:
`24acf86e69ab2e6fca9480c6269b6429874ba295`.

## Verdict

`blocked`. The exact frozen positive target cannot be proved. Fresh trust-zero
elaboration checks the existing placeholder-free declarations

```lean
Stage1Instances.THM_M_1200.Counterexample.not_rankineHugoniotTarget :
  Not Stage1Instances.THM_M_1200.RankineHugoniotTarget

Stage1Instances.THM_M_1200.not_nonzeroTracePackage :
  Not Stage1Instances.THM_M_1200.NonzeroTracePackage
```

The statement requires `ContDiff Real top phi`. In the pinned calculus API this
is analytic order `omega`, not smooth order `infinity`. Analytic uniqueness and
compact support force every admissible `phi` to be zero. Consequently every
interface defect vanishes, including at `f = 0`, `uL = 0`, `uR = 1`, `s = 1`,
where the requested jump law is false. The conditional root composer cannot
help because its `NonzeroTracePackage` premise is itself kernel-refuted.

This refutes only the frozen Lean encoding, not the mathematical
Rankine-Hugoniot theorem with smooth compactly supported tests. Correcting the
regularity order would change the target and invalidate predecessor evidence,
so it is outside this proof-phase assignment. The assigned item remains `[ ]`.
No positive proof receipt, state transition, audit completion, theorem
completion, validation completion, or release decision is claimed.
`.stage1-worker-selftest.json` is deliberately absent.

## Dependency Audit

The required schema-1.1 ledger is
`Stage1_Instances/THM-M-1200/dependency-reuse-ledger.json`, SHA-256
`4165312f498bb5b89c483eccc04a8ddb766587bbfd60c36999fe22d1a94d54cf`.
It binds graph digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`,
target context digest
`7cc9e6deceb544e7ebd0faafc5b046cb2cf33b5c4a62f06a23b782b17e027007`,
and this worker base.

There are no hard parents, transitive ancestors, hard edges, or reuse hints.
Both weak shared-module groups were inspected. THM-M-1227 uses
`Bochner.Basic` for an unrelated Leray-Hopf interface and zero-datum branch;
THM-M-1464 only probes `integral_piecewise` during a discontinuous-Galerkin
intake with no frozen statement. Neither supplies a shared terminal body or
repairs this target. Both decisions are `not_applicable`; no proof credit or
unresolved compatibility obligation is recorded. The scheduler's actual
`validate_dependency_reuse_ledger` function accepted the ledger with exit 0.

## Failed Gates

The first acceptance gate is already unavailable because prerequisite
`S56-M-1200-OBLIGATION_TREE` remains provisional `[_]`, not accepted `[x]`.
Independently, the semantic failure is exact-target consistency at
`M1200-S-BOUNDARIES`. The invalidated or open chain is
`M1200-S-BOUNDARIES`, `M1200-C-TEST`, and `M1200-ROOT`; the positive root cut
remains `M1200-C-TEST`, now proved impossible for the frozen test class.

Positive proof work requires authorized predecessor rework using
`ContDiff Real infinity-notation phi` after opening the `ContDiff` scope,
equivalently `ContDiff Real ((top : ENat) : WithTop ENat) phi`; a versioned or
transitively unfolded statement fingerprint; an order-sensitive mutation; and
fresh statement, anchor-audit, registry, and typed-graph acceptance. Otherwise
the scheduler must explicitly redirect work to a checked counterexample or
barrier target.

## Validation

All credited commands ran in this worker clone on 2026-07-16. The canonical
pinned `.lake` link was read only. No `lake update`, `lake build`, dependency
clone/fetch, network operation, or dependency mutation was run. Lean outputs
were confined to a fresh `/tmp` directory and removed by a trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 1 | Pre-existing global mismatch: the checked-in v2 theorem DAG differs from fresh deterministic generation. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | Same checked-in/fresh v2 DAG mismatch; workers may not edit either authority. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all uniform L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1200` | 0 | Rank 394; planned L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1200/check_statement.py` | 0 | Expression SHA-256 `b77d79ed6acc61642c8288a004f1023d65a71367415ac90fd6a6c5e8af77ca93`; four mutations killed. |
| `python3 Stage1_Instances/THM-M-1200/check_obligation_tree.py` | 0 | 14 obligations and 54 typed edges passed structurally; root and construction remain recorded open at M4. |
| Exact scheduler ledger-validator invocation below | 0 | `stage1-dependency-reuse-ledger/1.1 THM-M-1200 2`. |
| Isolated pinned `lake env lean --trust=0 -t0` recipe below | 0 | Statement, countermodel, conditional composer, and package refutation elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Prohibited-token scan below | 1 | Expected no-match: no prohibited proof device or declaration in the scoped Lean sources. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` plus mathlib revision query | 0 | Lean 4.29.0, Lake 5.0.0-src, mathlib `8a178386...`, tree `bdc39a31...`. |
| Inline blocker-record/ledger binding check | 0 | `PASS THM-M-1200 current-base blocker record/ledger bindings`. |
| Scoped whitespace checks | 0 | No whitespace errors in the three new owned artifacts. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Incomplete proof phase correctly emitted no completion packet. |

The exact ledger validation was:

```bash
python3 - <<'PY'
from pathlib import Path
from scripts.stage1_execution_cron import validate_dependency_reuse_ledger
ledger = validate_dependency_reuse_ledger(
    Path('Stage1_Instances/THM-M-1200/dependency-reuse-ledger.json'),
    'THM-M-1200',
    expected_observed_graph_sha256='73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca',
    expected_repository_revision='6bf9ee93a322e7d25cf9249226222095f95d1cff',
)
print(ledger['schema_version'], ledger['consumer_theorem_id'],
      len(ledger['reuse_decisions']))
PY
```

The isolated kernel recipe was:

```bash
set -euo pipefail
repo=$PWD
canonical=$(readlink -f Formalizations/Lean/.lake)
packages=$canonical/packages
mathlib=$packages/mathlib
lean_bin=$(cd "$mathlib" && timeout --foreground --kill-after=10s 90 lake env which lean)
toolchain_lib=$(realpath "$(dirname "$lean_bin")/../lib/lean")
base_path=$toolchain_lib
for package in "$packages"/*; do
  if [ -d "$package/.lake/build/lib/lean" ]; then
    base_path="$base_path:$package/.lake/build/lib/lean"
  fi
done
tmp=$(mktemp -d /tmp/thm-m-1200-proof-head-6bf9ee93-slot31.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
for module in Statement Counterexample ObligationTree ProofRefutation; do
  cp "$repo/Stage1_Instances/THM-M-1200/$module.lean" "$tmp/$module.lean"
done
cd "$mathlib"
for module in Statement Counterexample ObligationTree ProofRefutation; do
  if [ "$module" = Statement ]; then
    module_path="$base_path"
  else
    module_path="$tmp:$base_path"
  fi
  LEAN_PATH="$module_path" LEAN_NUM_THREADS=1 \
    timeout --foreground --kill-after=10s 900 \
    lake env lean --trust=0 -t0 -R "$tmp" \
      -o "$tmp/$module.olean" "$tmp/$module.lean" \
      >"$tmp/$module.log" 2>&1
done
cat "$tmp/Statement.log" "$tmp/Counterexample.log" \
  "$tmp/ObligationTree.log" "$tmp/ProofRefutation.log" >"$tmp/kernel.log"
cat "$tmp/kernel.log"
sha256sum "$tmp/Statement.olean" "$tmp/Counterexample.olean" \
  "$tmp/ObligationTree.olean" "$tmp/ProofRefutation.olean" "$tmp/kernel.log"
```

Fresh output SHA-256 values were:

| Output | SHA-256 |
|---|---|
| `Statement.olean` | `74f5f45b992141e003cee16879671aea16eb7e14174374070dd37062f35276b0` |
| `Counterexample.olean` | `3f4ccc8963bc2e801b8d2ed33909e9ed67d34503008f3b210ae96049791b6485` |
| `ObligationTree.olean` | `c3ab556b8209466f1dcbf67faeec45834fa5bd9d242dc797b05f1f221a844044` |
| `ProofRefutation.olean` | `1ae262cb2c3a2a9c6657721427154adb08f87bd9eac9ad9f0ffd571917cf8d08` |
| Combined kernel log | `a91296be37b65fbe52ab3ec716c621079391b7ba096adb37d520cacf83b37aa0` |

The prohibited-token scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(?:axiom|unsafe|opaque|extern|external|constant)[[:space:]]' \
  Stage1_Instances/THM-M-1200 --glob '*.lean'
```

The no-match exit 1 is the passing outcome for that scan. This artifact and the
structured record are durable blocker evidence only; they do not complete the
assigned positive proof phase.
