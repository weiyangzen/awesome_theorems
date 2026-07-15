# THM-M-1010 proof recheck at `d5ab961c`

Item: `S56-M-1010-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T13:56:04+08:00`

Base revision: `d5ab961cb3cd92c7febcf21fb9ab746fde231c24`

Base tree: `5f3d5abbfee8a0f11198a295ecf024aca301867f`

## Verdict

`blocked`. No placeholder-free proof body for the exact root
`Stage1Instances.THM_M_1010.Target` is present in this checkout or in the
pinned dependency sources inspected below. The proof item must remain `[ ]`;
the root vector remains `[H1, M3, R3]`.

The checked local declarations are genuine but nonterminal:

- `ObligationTree.target_of_couplingPackage` consumes an assumed
  `CouplingPackage S`; it checks exact child-to-parent composition but does not
  construct the package.
- `representation_of_constant_laws` and `target_for_constant_sequence` close
  only the constant-law boundary case.

The exact root needs a convergence-compatible joint realization of every
prescribed law on one probability space. The pinned product-measure API can
put all laws on one product space: `measurePreserving_eval_infinitePi` gives
the coordinate marginals, and `exists_hasLaw_indepFun` packages the same idea.
That independent construction does not give the required `ae_tendsto`. Even
for a constant non-Dirac law on a discrete two-point space, independent
coordinates do not converge almost surely to an independent limit. Replacing
the product measure by a joint law supported on convergent trajectories while
preserving every marginal is precisely the missing Skorokhod coupling, not a
wrapper-level shortcut.

Similarly, `Measure.exists_measurable_map_eq` realizes one law at a time on
the unit interval, while `TendstoInMeasure.exists_seq_tendsto_ae` assumes an
already common-space convergence-in-measure hypothesis and returns a
subsequence. Neither result constructs the prescribed full-sequence
coupling. The complete pinned-source name scan found no Skorokhod/Skorohod or
probability-coupling theorem to import. The previously audited external
candidate is Real-only and ends in `by sorry`, so it is both a statement
mismatch and an ineligible proof body.

The first open construction is `M1010-N-PARTITIONS`, feeding the
root-blocking `M1010-C-COUPLING`. The frozen remaining root cut set is:

```text
M1010-N-PARTITIONS
M1010-C-INTERVAL
M1010-L-MEASURABLE
M1010-L-LAWS
M1010-L-AE-STABILIZE
```

A valid local closure must implement refining Borel partitions with shrinking
mesh and limit-law-null frontiers, compatible allocations for every law,
measurable representatives with exact pushforward laws, and one null-set
argument yielding convergence of the full sequence. Implementing only
independent marginals, a subsequence, a Real specialization, or an assumed
`CouplingPackage` would broaden or weaken the frozen theorem and is rejected.

Retry requires placeholder-free implementations of these five frozen leaves,
or an immutable exact arbitrary-Polish-space Lean 4 proof that can be pinned,
imported, provenance-audited, and kernel checked. Because the positive proof
phase is incomplete, no proof receipt or `.stage1-worker-selftest.json` is
emitted.

## Validation

The automation-provided `Formalizations/Lean/.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed. Direct Lean outputs were isolated under `/tmp` and
removed by a shell trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1010` | 0 | Rank 290; planned hard-mathlib anchor/wrapper lane; legacy artifacts unaccepted; theorem incomplete. |
| `timeout 60 python3 -B Stage1_Instances/THM-M-1010/check_obligation_tree.py` | 1 | The structural assertions ran, then its Lake-driven Lean invocation failed because the shared canonical `flt-regular` package has no resolvable `HEAD`; the checker raised `AssertionError`. |
| Direct isolated trust-zero replay below | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated with Lean 4.29.0. The conditional composer and both constant-law declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`. Log hashes are `e3b0c442...b855`, `cbee87b9...9abb`, and `940c65d9...9673`; temporary object hashes are `2675f2bc...f3df` and `a11e8641...ca7`. |
| `rg -n --pcre2 '\b(?:sorry|admit|sorryAx|native_decide)\b|^[[:space:]]*(?:axiom|unsafe|external|opaque|constant|extern)[[:space:]]|implemented_by' Stage1_Instances/THM-M-1010 --glob '*.lean'` | 1 expected | No prohibited construct matched in the owned Lean sources. |
| `rg -ni 'skorokhod|skorohod|probability coupling|coupling theorem' Formalizations/Lean/.lake/packages --glob '*.lean' --glob '*.md' --glob '*.tex'` | 1 expected | No matching proof candidate was found in the complete pinned package source tree. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse --verify HEAD` | 128 | `fatal: Needed a single revision`; the shared artifact was not repaired or mutated. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |

Exact narrow replay, run from the repository root:

```bash
set -euo pipefail
repo="$PWD"
lean="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
lib="$repo/Formalizations/Lean/.lake/build/lib/lean"
for package in mathlib batteries Qq aesop proofwidgets LeanSearchClient importGraph plausible; do
  path="$repo/Formalizations/Lean/.lake/packages/$package/.lake/build/lib/lean"
  test ! -d "$path" || lib="$lib:$path"
done
tmp=$(mktemp -d /tmp/thm1010-direct.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/Stage1_Instances/THM-M-1010"
LEAN_NUM_THREADS=1 LEAN_PATH="$lib" timeout 180 "$lean" --trust=0 -t0 -R "$repo" \
  -o "$tmp/Stage1_Instances/THM-M-1010/Statement.olean" \
  Stage1_Instances/THM-M-1010/Statement.lean >"$tmp/statement.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lib" timeout 180 "$lean" --trust=0 -t0 -R "$repo" \
  -o "$tmp/Stage1_Instances/THM-M-1010/ObligationTree.olean" \
  Stage1_Instances/THM-M-1010/ObligationTree.lean >"$tmp/obligation.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lib" timeout 180 "$lean" --trust=0 -t0 -R "$repo" \
  Stage1_Instances/THM-M-1010/Proof.lean >"$tmp/proof.log" 2>&1
sha256sum "$tmp/statement.log" "$tmp/obligation.log" "$tmp/proof.log" \
  "$tmp/Stage1_Instances/THM-M-1010/Statement.olean" \
  "$tmp/Stage1_Instances/THM-M-1010/ObligationTree.olean"
```

This target-scoped artifact is current-base blocker evidence only. It does not
satisfy `S56-M-1010-PROOF`, propose a scheduler state transition, or claim
audit, theorem, validation, release, or master-acceptance completion.
