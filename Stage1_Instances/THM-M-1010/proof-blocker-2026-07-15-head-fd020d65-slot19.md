# THM-M-1010 proof recheck at `fd020d65`

Item: `S56-M-1010-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T13:42:00+08:00`

Base revision: `fd020d65a412e2c870f4bac1fefb9ea4ed5f5fd8`

Base tree: `5fce2f82823f95e5aa2ce97bd08b22091f96aeda`

## Verdict

`blocked`. No placeholder-free proof body for the exact root
`Stage1Instances.THM_M_1010.Target` is available in this checkout or its
pinned dependency sources. The proof item must remain `[ ]`; the root vector
remains `[H1, M3, R3]`.

The existing checked declarations do not close the requested phase:

- `ObligationTree.target_of_couplingPackage` consumes an assumed
  `CouplingPackage S`; it verifies exact final composition but does not
  construct that package.
- `representation_of_constant_laws` and
  `target_for_constant_sequence` prove only the constant-law boundary case.

The root requires one convergence-compatible realization of every prescribed
law in an arbitrary Polish space. Pinned mathlib provides exact single-law
realization on the unit interval
(`Measure.exists_measurable_map_eq`), small measurable partitions
(`SeparableSpace.exists_measurable_partition_diam_le`), null-frontier and
Portmanteau interfaces, product/disintegration infrastructure, and a.e.
subsequence extraction after common-space convergence in measure. None of
these constructs the required compatible full sequence. Independently
realizing each law proves exact marginals but supplies no pointwise convergence
relationship; the subsequence theorem assumes a common-space convergence
hypothesis and returns only a subsequence.

There is also a frozen universe constraint: `Representation.sample : Type u`
must live in the same universe as `S`. A direct use of the library's
`unitInterval : Type 0` realization therefore does not typecheck for arbitrary
`u` without an additional universe-lifted probability-space construction and
law transport. This is an extra implementation obligation, not a reason to
weaken the theorem.

The first open construction is `M1010-N-PARTITIONS`, feeding the
root-blocking `M1010-C-COUPLING`. The frozen remaining proof cut set is
`M1010-N-PARTITIONS`, `M1010-C-INTERVAL`,
`M1010-L-MEASURABLE`, `M1010-L-LAWS`, and
`M1010-L-AE-STABILIZE`. A local proof would need refining Borel partitions
with shrinking mesh and limit-law-null frontiers, compatible interval
allocations for every law, measurable representatives with exact pushforwards,
and eventual agreement of codes at each level. This is the missing
Skorokhod construction, not a wrapper around an available result.

The only immutable external candidate already recorded by the owned anchor
audit is restricted to `Real` and ends in `by sorry`; it is both a theorem
mismatch and an ineligible placeholder. A merely Borel measurable equivalence
to a real subset cannot repair the mismatch because it need not preserve the
Polish topology and therefore cannot transport pointwise convergence.

Retry requires either placeholder-free implementations of the five open
leaves above or an immutable exact arbitrary-Polish-space Lean 4 proof that
can be pinned, imported, and kernel checked. Because the requested positive
proof phase is incomplete, no proof receipt or
`.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided `Formalizations/Lean/.lake` symlink was treated as
read-only. No `lake update`, `lake build`, clone, fetch, or dependency
mutation was performed. Temporary Lean objects were written under `/tmp`
and removed by a shell trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 ordered targets at the L0/rework-required baseline passed. |
| `python3 scripts/stage1_target.py show THM-M-1010` | 0 | Rank 290, planned hard-mathlib anchor/wrapper lane, theorem incomplete. |
| direct isolated trust-zero three-module replay shown below | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated with Lean 4.29.0; the conditional composer and both constant-law declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`. Temporary object hashes were `2675f2bc...f3df` and `a11e8641...ca7`. |
| `timeout 180 python3 -B Stage1_Instances/THM-M-1010/check_obligation_tree.py` | 124 | The checker reached its nested Lake environment query and timed out without output; direct replay bypassing Lake metadata succeeded. |
| prohibited-construct scan over owned `*.lean` files | 1 expected | No `sorry`, `admit`, `axiom`, `sorryAx`, unsafe/oracle construct, or equivalent bodyless declaration was found. |
| complete pinned-package scan for `skorokhod\|skorohod\|probability coupling\|coupling theorem` | 1 expected | No matching proof candidate was found. |
| direct tool and mathlib identity checks | 0 | Lean 4.29.0 commit `98dc76e3...ab16740`; mathlib `8a178386...ea95`, tree `bdc39a31...c2b`, clean worktree. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse --verify HEAD` | 128 | The shared canonical `flt-regular` artifact has no resolvable `HEAD`; this independently blocks the Lake-driven checker and was not repaired because workers must not mutate `.lake`. |

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
  Stage1_Instances/THM-M-1010/Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lib" timeout 180 "$lean" --trust=0 -t0 -R "$repo" \
  -o "$tmp/Stage1_Instances/THM-M-1010/ObligationTree.olean" \
  Stage1_Instances/THM-M-1010/ObligationTree.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lib" timeout 180 "$lean" --trust=0 -t0 -R "$repo" \
  Stage1_Instances/THM-M-1010/Proof.lean
```

This target-scoped artifact is current-base blocker evidence only. It does not
satisfy `S56-M-1010-PROOF`, propose a checklist transition, or claim audit,
theorem, validation, release, or master-acceptance completion.
