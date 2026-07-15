# THM-M-1010 proof recheck at `860fc1b5` (slot56)

Item: `S56-M-1010-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T14:19:27+08:00`

Base revision: `860fc1b58d914171000ca0f981bf903c32ad5db2`

Base tree: `70bebf93650eba444a713c765f558a7087c0070f`

## Verdict

`blocked`. The exact root `Stage1Instances.THM_M_1010.Target` still has no
placeholder-free proof body in this checkout or in its pinned dependency
closure. The proof item must remain `[ ]`; the root vector remains
`[H1, M3, R3]`.

The frozen target quantifies over every weakly convergent sequence of Borel
probability measures on every Polish space. It requires one probability space,
exact laws for the entire sequence and its limit, and almost-sure convergence
of the full sequence. The available checked declarations do not prove that
claim:

- `ObligationTree.target_of_couplingPackage` consumes an assumed
  `CouplingPackage S`; it is an exact conditional composer, not a construction
  of the package.
- `representation_of_constant_laws` and `target_for_constant_sequence` prove
  only the constant-law boundary case.

The root inputs are byte-unchanged from accepted-base candidate revision
`11a448c97289d30fe7c8c05dbac5a283a9d00896` through this base. Later target
commits contain blocker evidence only. A fresh pinned-source audit confirms
that the nearest APIs remain ingredients rather than closure:

- `SeparableSpace.exists_measurable_partition_diam_le` constructs one small
  measurable partition, but not a refining family with limit-law-null
  boundaries.
- `ProbabilityMeasure.tendsto_measure_of_null_frontier_of_tendsto` supplies
  convergence of cell masses once the required null-boundary sets exist.
- `Measure.exists_measurable_map_eq` realizes one law on the unit interval;
  separate realizations do not give compatible representatives that converge.
- `measurePreserving_eval_infinitePi` and `exists_hasLaw_indepFun` realize all
  marginals independently, but independence supplies no almost-sure
  convergence relation.
- `TendstoInMeasure.exists_seq_tendsto_ae` assumes functions already living on
  one space and yields a subsequence, not the prescribed full sequence.

The complete pinned package-source scan found no Skorokhod-, Skorohod-, or
probability-coupling theorem. The immutable external candidate recorded by the
owned dossier is restricted to `Real` and ends in `by sorry`; it is both a
statement mismatch and an ineligible proof body. The legacy
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_290.lean` file likewise marks
all realization and convergence leaves as unchecked formalization debt.

The first failed construction gate is `M1010-N-PARTITIONS`, feeding the
root-blocking `M1010-C-COUPLING`. The frozen remaining root cut set is:

```text
M1010-N-PARTITIONS
M1010-C-INTERVAL
M1010-L-MEASURABLE
M1010-L-LAWS
M1010-L-AE-STABILIZE
```

Closing the phase requires placeholder-free implementations of those five
leaves and their checked internal composition, or an immutable exact
arbitrary-Polish-space Lean 4 proof that can be pinned, imported,
provenance-audited, and kernel checked. Independent marginals, a subsequence, a
`Real` specialization, or an assumed coupling package would weaken or
condition the frozen theorem and is rejected.

Because no eligible proof body was added and the exact root remains open, no
proof receipt or `.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation was performed. Narrow Lean outputs were isolated under
`/tmp` and deleted by shell traps.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1010` | 0 | Rank 290; planned `hard_mathlib_anchor_and_wrapper` lane; legacy artifacts unaccepted; theorem incomplete. |
| `timeout 180 python3 -B Stage1_Instances/THM-M-1010/check_obligation_tree.py` | 0 | `PASS THM-M-1010 obligation tree: 15 obligations, 31 typed edges`; denominator `8cf08f66...d16016`; conditional composer axioms `[propext, Classical.choice, Quot.sound]`; root explicitly open `M3`. |
| Isolated `lake env lean --trust=0 -t0` replay below | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated. The conditional composer and the two constant-law declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`. Log hashes are `e3b0c442...b855`, `cbee87b9...9abb`, and `940c65d9...9673`; object hashes are `2675f2bc...f3df` and `a11e8641...ca7`. |
| `rg -n --pcre2 '\b(?:sorry\|admit\|sorryAx\|native_decide)\b\|^[[:space:]]*(?:axiom\|unsafe\|external\|opaque\|constant\|extern)[[:space:]]\|implemented_by' Stage1_Instances/THM-M-1010 --glob '*.lean'` | 1 expected | No prohibited construct matched in owned Lean sources. |
| `rg -ni 'skorokhod\|skorohod\|probability coupling\|coupling theorem' Formalizations/Lean/.lake/packages --glob '*.lean' --glob '*.md' --glob '*.tex'` | 1 expected | No matching candidate in the complete pinned package source tree. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; clean worktree. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD HEAD^{tree}` | 0 | Revision `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`; tree `32c9eace926573a9981787ae97643e520353c893`; clean worktree. |
| `git diff --exit-code 11a448c97289d30fe7c8c05dbac5a283a9d00896..HEAD --` the ten listed root-input files | 0 | Canonical Lean sources and structured root inputs are unchanged. |

Exact narrow replay, run from the repository root:

```bash
set -euo pipefail
repo="$PWD"
tmp=$(mktemp -d /tmp/thm1010-slot56.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/Stage1_Instances/THM-M-1010"
cd Formalizations/Lean
LEAN_NUM_THREADS=1 timeout 240 lake env lean --trust=0 -t0 -R "$repo" \
  -o "$tmp/Stage1_Instances/THM-M-1010/Statement.olean" \
  "$repo/Stage1_Instances/THM-M-1010/Statement.lean" >"$tmp/statement.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp${LEAN_PATH:+:$LEAN_PATH}" timeout 240 \
  lake env lean --trust=0 -t0 -R "$repo" \
  -o "$tmp/Stage1_Instances/THM-M-1010/ObligationTree.olean" \
  "$repo/Stage1_Instances/THM-M-1010/ObligationTree.lean" >"$tmp/obligation.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp${LEAN_PATH:+:$LEAN_PATH}" timeout 240 \
  lake env lean --trust=0 -t0 -R "$repo" \
  "$repo/Stage1_Instances/THM-M-1010/Proof.lean" >"$tmp/proof.log" 2>&1
sha256sum "$tmp/statement.log" "$tmp/obligation.log" "$tmp/proof.log" \
  "$tmp/Stage1_Instances/THM-M-1010/Statement.olean" \
  "$tmp/Stage1_Instances/THM-M-1010/ObligationTree.olean"
```

This target-scoped artifact is fresh current-base blocker evidence only. It
does not satisfy `S56-M-1010-PROOF`, propose a scheduler state transition, or
claim audit, theorem, validation, release, or master-acceptance completion.
