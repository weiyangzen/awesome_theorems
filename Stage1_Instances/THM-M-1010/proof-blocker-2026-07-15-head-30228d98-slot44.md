# THM-M-1010 proof recheck at `30228d98` (slot44)

Item: `S56-M-1010-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T13:06:31+08:00`

Base revision: `30228d98c98c401cb60a3dfa09eec01bb904053f`

Base tree: `773a33c6344fb9787649fbc5edea99092ea68856`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_1010.Target`. The root vector remains
`[H1, M3, R3]`, and the proof item remains `[ ]`.

The exact root quantifies over every weakly convergent sequence of probability
measures on every Polish space. It requires one common probability space,
exact prescribed laws, and almost-sure convergence of the full sequence. The
checked declarations under the owned path do not prove that claim:

- `ObligationTree.target_of_couplingPackage` consumes an assumed
  `CouplingPackage S`; it checks final composition but does not construct the
  package.
- `representation_of_constant_laws` and `target_for_constant_sequence` prove
  only the constant-law boundary case.

The first unavailable construction is `M1010-N-PARTITIONS`, and the resulting
root-blocking node is `M1010-C-COUPLING`. Pinned mathlib supplies useful
ingredients but not the missing construction:

- `MeasurableSpace.countablePartition` gives refining finite measurable
  partitions that generate the sigma algebra, but no shrinking-diameter or
  limit-law-null-frontier control.
- `SeparableSpace.exists_measurable_partition_diam_le` gives a small-diameter
  measurable partition at one scale, but not a compatible refining family or
  null frontiers.
- The null-frontier and Portmanteau interfaces give boundary selection and
  mass convergence, but not a convergence-compatible coupling.
- `Measure.exists_measurable_map_eq` and
  `Kernel.exists_measurable_map_eq_unitInterval` realize one prescribed law at
  a time; independently selected realizations impose no convergence relation,
  and their standard-Borel transport need not preserve the target topology.
- `exists_hasLaw_indepFun` puts exact laws on one product probability space,
  but independence supplies no almost-sure convergence.
- `TendstoInMeasure.exists_seq_tendsto_ae` starts with functions already on
  one measure space and returns only a subsequence.

There is no Skorokhod- or Skorohod-named result, Strassen theorem, or equivalent
compatible-coupling theorem in the available pinned dependency source. The
only immutable public candidate recorded by the owned dossier is
`facebookresearch/atlas-lean` revision
`34ffed396f376454c1a9b297f3fd74c5c801fb50`; it is restricted to `Real` and
its body is `by sorry`, so it is both a statement mismatch and an ineligible
placeholder. The legacy `S1_M_290.lean` file likewise records only a future
coupling route, not a root proof.

The frozen remaining root cut set is `M1010-N-PARTITIONS`,
`M1010-C-INTERVAL`, `M1010-L-MEASURABLE`, `M1010-L-LAWS`, and
`M1010-L-AE-STABILIZE`. Those leaves must close before the internal metric-
convergence and coupling nodes, followed by the checked composer, can close
the exact root.

Because the requested proof phase is incomplete, no proof receipt or
`.stage1-worker-selftest.json` is emitted. Retry requires placeholder-free
implementations of the five frozen leaves, or an immutable exact Polish-space
Lean 4 proof that can be pinned and checked.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned artifacts was reused read-only. No dependency update, build,
clone, fetch, or `.lake` mutation was performed. Generated Lean outputs were
isolated under `/tmp` and removed.

The canonical root Lake environment has a separate current-snapshot failure:
the `flt-regular` checkout has no valid `HEAD`, contains no tracked files, and
Lake cannot resolve it. The manifest-pinned commit object
`56161b6e...11a27` is present, but worker policy forbids
repairing or fetching the dependency. Consequently `check_obligation_tree.py`
completed its structural assertions and then failed at its nested
`lake env lean` call. Because this target imports only Mathlib, I also ran the
same pinned Lean through the mathlib Lake environment against the canonical
root precompiled package objects. That narrower replay passed, but it is not
presented as a repair of or substitute for the failing canonical gate.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all` | 0 | Base `30228d98c98c401cb60a3dfa09eec01bb904053f`, tree `773a33c6344fb9787649fbc5edea99092ea68856`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | The 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 ordered targets at the L0/rework-required baseline passed. |
| `python3 scripts/stage1_target.py show THM-M-1010` | 0 | Rank 290; planned hard-mathlib anchor/wrapper lane; theorem incomplete. |
| `timeout 600 python3 -B Stage1_Instances/THM-M-1010/check_obligation_tree.py` | 1 | Structural assertions completed; nested Lake validation failed because `flt-regular` could not resolve `HEAD`; the script then raised `AssertionError`. No pass is claimed. |
| Isolated pinned three-module mathlib-Lake replay shown below | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated with `--trust=0 -t0`; the conditional composer and both constant-law declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`. Log hashes were `e3b0c442...b855`, `cbee87b9...9abb`, and `940c65d9...9673`; temporary statement/tree object hashes were `2675f2bc...3df` and `a11e8641...ca7`. |
| Prohibited-construct scan over owned `*.lean` files | 1 expected | No `sorry`, `admit`, `axiom`, `sorryAx`, unsafe/oracle construct, or equivalent declaration form was found. |
| `rg -ni 'skorokhod\|skorohod' Formalizations/Lean/.lake/packages --glob '*.lean' --glob '*.md' --glob '*.tex'` | 1 expected | No match in the complete available pinned package source tree. |
| Pinned tool and dependency identity checks | 0 aggregate; invalid-`HEAD` subchecks fail as expected | Lean `4.29.0` commit `98dc76e3...ab16740`; Lake `5.0.0-src+98dc76e`; mathlib `8a178386...ea95`, tree `bdc39a31...c2b`, clean dependency worktree. The `flt-regular` pin object exists, while its expected `HEAD` checks fail because the checkout is invalid. |
| Root-input freshness against `4338dcf8` | 0 | `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and the seven listed structured root inputs are byte-unchanged; later integrations added blocker evidence only. |
| Structured artifact and worktree hygiene checks | 0 | The JSON parses and matches the assigned item/base/open boundary; both new artifacts have no whitespace diagnostics; no completion self-test or generated Lean output is present. |

Exact prohibited-construct scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide|^[[:space:]]*(?:constant|opaque|extern|external)[[:space:]]' \
  Stage1_Instances/THM-M-1010 --glob '*.lean'
```

Exact narrow replay, run from the repository root:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-1010"
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1010-lake-env-slot44-30228d98.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/Stage1_Instances/THM-M-1010"
lean_path="$lean_root/.lake/packages/mathlib/.lake/build/lib/lean:$lean_root/.lake/packages/batteries/.lake/build/lib/lean:$lean_root/.lake/packages/Qq/.lake/build/lib/lean:$lean_root/.lake/packages/aesop/.lake/build/lib/lean:$lean_root/.lake/packages/proofwidgets/.lake/build/lib/lean:$lean_root/.lake/packages/importGraph/.lake/build/lib/lean:$lean_root/.lake/packages/LeanSearchClient/.lake/build/lib/lean:$lean_root/.lake/packages/plausible/.lake/build/lib/lean:$lean_root/.lake/build/lib/lean"
(
  cd "$lean_root/.lake/packages/mathlib"
  LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 lake env lean --trust=0 -t0 \
    -R "$repo" -o "$tmp/Stage1_Instances/THM-M-1010/Statement.olean" \
    "$target/Statement.lean"
) >"$tmp/statement.log" 2>&1
(
  cd "$lean_root/.lake/packages/mathlib"
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 lake env lean --trust=0 -t0 \
    -R "$repo" -o "$tmp/Stage1_Instances/THM-M-1010/ObligationTree.olean" \
    "$target/ObligationTree.lean"
) >"$tmp/obligation.log" 2>&1
(
  cd "$lean_root/.lake/packages/mathlib"
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 lake env lean --trust=0 -t0 \
    -R "$repo" "$target/Proof.lean"
) >"$tmp/proof.log" 2>&1
sha256sum "$tmp/statement.log" "$tmp/obligation.log" "$tmp/proof.log" \
  "$tmp/Stage1_Instances/THM-M-1010/Statement.olean" \
  "$tmp/Stage1_Instances/THM-M-1010/ObligationTree.olean"
```

This is current-base nonrelease blocker evidence only. It is not a proof
receipt, does not satisfy `S56-M-1010-PROOF`, proposes no checklist
transition, and makes no audit-completion, theorem-completion, validation,
release, or master-acceptance claim.
