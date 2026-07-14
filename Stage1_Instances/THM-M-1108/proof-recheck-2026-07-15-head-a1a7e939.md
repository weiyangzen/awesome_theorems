# THM-M-1108 proof-phase recheck at a1a7e939

Item: `S56-M-1108-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

Base tree: `d881fd9641fa3e5f3ebe5082b35672981e90adcf`

## Verdict

`blocked`. The exact target
`Stage1Instances.THM_M_1108.CanonicalStatement` has no proof body in the owned
source or pinned dependency closure. This recheck adds no proof body and closes
no obligation. The lifecycle remains `planned`, and the root vector stays
`[H2, M3, R3] -> [H2, M3, R3]`.

`ObligationTree.lean` contains one genuine placeholder-free composition body,
`canonicalStatement_of_poissonized_depoissonized`, but it consumes
`PoissonizedAsymptotics` and `DePoissonizationTransfer` as premises. Neither
premise has an inhabitant. Under the frozen proof graph, the remaining root cut
is therefore `M1108-T-POISSONIZED` plus `M1108-T-DEPOISSONIZE`.

The first unavailable proof package is `M1108-C-RSK`: neither the repository nor
pinned mathlib provides a checked Robinson-Schensted correspondence with the
required LIS/first-row identity. The subsequent Toeplitz determinant,
Riemann-Hilbert steepest descent, Hastings-McLeod identification, uniform error,
Poissonized convergence, monotonicity/tail, and de-Poissonization packages are
also absent. The prerequisite immutable anchor audit found no compatible public
Lean 4 theorem-level body to pin or import.

Assuming either terminal package, proving a weakened theorem, or reporting the
conditional composition as BDJ would introduce a placeholder or substitute the
frozen theorem. No such declaration was added.

## Failed Gate And Retry

The first failed implementation gate is `M1108-C-RSK`. Resume only after the
frozen combinatorial and analytic packages are implemented without placeholders,
or after an immutable compatible Lean 4 BDJ proof is available for exact-type,
terminal-body, dependency, trust, license, and provenance validation in the
pinned environment.

## Validation

All checks ran in this worker clone against the automation-provided pinned Lake
artifacts. The pre-existing untracked `Formalizations/Lean/.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch, network
operation, or `.lake` mutation was performed. Temporary Lean objects were
removed after replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1108` | 0 | Rank 548; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1108/check_obligation_tree.py` | 0 | 18 obligations and 36 typed edges passed; denominator `2defff91...0322c8e`; root open at M3 and both terminal packages open at M4. |
| Isolated two-module `lake env` replay with the resolved Lean binary, pinned `LEAN_PATH`, `--trust=0`, and `-t0` | 0 | `Statement.lean` and `ObligationTree.lean` both elaborated. The exact statement transport and conditional composer reported only `[propext, Classical.choice, Quot.sound]`. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom-like declaration, unsafe/oracle, or equivalent prohibited construct was found. |
| Pinned-mathlib topical source scan | 1 | Expected no-match exit; no BDJ, Tracy-Widom, Painleve, Hastings-McLeod, LIS, Riemann-Hilbert, or Robinson-Schensted terminal declaration was found. |
| Repo-local exact-declaration scan outside this owned target | 1 | Expected no-match exit; no declaration of `normalizedLISCDF`, `IsTracyWidomCDF`, `PoissonizedAsymptotics`, or `DePoissonizationTransfer` was found. |

The word `sorry` printed during `Statement.lean` elaboration is Lean's diagnostic
rendering inside the four expected `#check_failure` mutation probes. It is not
source syntax or an admitted proof. The token-anchored source scan above confirms
that distinction.

The isolated replay was:

```bash
set -u
tmp=$(mktemp -d .thm1108-proof-replay.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1108/{Statement,ObligationTree}.lean "$tmp"/
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 240 "$lean" --trust=0 -t0 \
  -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 240 "$lean" --trust=0 \
  -t0 -R "$tmp" "$tmp/ObligationTree.lean"
```

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does
not satisfy `S56-M-1108-PROOF`, change the task state, or claim audit completion,
theorem completion, validation, release, receipt acceptance, or master
acceptance. `accepted_receipt_ids=[]`. Because the assigned proof phase is
incomplete, `.stage1-worker-selftest.json` is deliberately absent.
