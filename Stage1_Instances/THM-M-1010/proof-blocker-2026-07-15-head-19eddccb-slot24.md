# THM-M-1010 proof recheck at `19eddccb` (slot24)

Item: `S56-M-1010-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T15:47:26+08:00`

Base revision: `19eddccb8988b4da9e007b60f4a25b6806877160`

Base tree: `1b5d55ad37802063bf31881e5e06faa0410bf21c`

## Verdict

`blocked`. No placeholder-free proof body for the exact root
`Stage1Instances.THM_M_1010.Target` is present in this checkout or its pinned
dependency closure. The proof item must remain `[ ]`; the root vector remains
`[H1, M3, R3]`.

The target quantifies over every weakly convergent sequence of Borel
probability measures on every Polish space. It requires one probability space,
exact prescribed laws for the whole sequence and its limit, and almost-sure
convergence of the full sequence. The checked declarations do not close it:

- `ObligationTree.target_of_couplingPackage` consumes an assumed
  `CouplingPackage S`; it is an exact conditional composer, not a construction
  of that package.
- `representation_of_constant_laws` and `target_for_constant_sequence` prove
  only the constant-law boundary case.

The first unavailable construction is `M1010-N-PARTITIONS`, feeding the
root-blocking `M1010-C-COUPLING`. Pinned mathlib provides small measurable
partitions, null-frontier Portmanteau interfaces, one-law realization on the
unit interval, product and independent realizations, and a.e. subsequence
extraction after common-space convergence in measure. None builds a compatible
common-space realization of the entire prescribed sequence. Separate marginal
realizations impose no convergence relation, and the a.e. result returns only
a subsequence after assuming a common-space convergence hypothesis.

The complete pinned package-source scan found no probability-theoretic
Skorokhod, Skorohod, Strassen, or coupling theorem that supplies the missing
construction. The sole Skorokhod-named public Lean candidate recorded by the
owned dossier is restricted to `Real` and has body `by sorry`; it is both a
statement mismatch and an ineligible placeholder. A merely Borel measurable
equivalence cannot repair that mismatch because it need not preserve the
Polish topology required by the convergence conclusion.

The frozen remaining root cut set is:

```text
M1010-N-PARTITIONS
M1010-C-INTERVAL
M1010-L-MEASURABLE
M1010-L-LAWS
M1010-L-AE-STABILIZE
```

Closing the phase requires placeholder-free implementations of these five
leaves and their checked internal composition, or an immutable exact
arbitrary-Polish-space Lean 4 proof that can be pinned, imported, provenance
audited, and kernel checked. The canonical root inputs are byte-unchanged from
revision `11a448c97289d30fe7c8c05dbac5a283a9d00896`; subsequent target changes
are blocker evidence only.

Because no eligible proof body was added and the exact root remains open, no
proof receipt or `.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation was performed. Narrow Lean outputs were isolated under
`/tmp` and removed by a shell trap.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all` | 0 | Base `19eddccb8988b4da9e007b60f4a25b6806877160`, tree `1b5d55ad37802063bf31881e5e06faa0410bf21c`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1010` | 0 | Rank 290; planned hard-mathlib anchor/wrapper lane; legacy artifacts unaccepted; theorem incomplete. |
| `timeout 240 python3 -B Stage1_Instances/THM-M-1010/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `8cf08f66...d16016`; the conditional composer reports `propext`, `Classical.choice`, and `Quot.sound`; root explicitly remains open at M3. |
| Isolated pinned `lake env lean --trust=0 -t0` replay below | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated. The conditional composer and both constant-law declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`. Log hashes are `e3b0c442...b855`, `cbee87b9...9abb`, and `940c65d9...9673`; object hashes are `2675f2bc...f3df` and `a11e8641...ca7`. |
| Prohibited-construct scan over owned `*.lean` files | 1 expected | No `sorry`, `admit`, `axiom`, `sorryAx`, unsafe/oracle construct, or equivalent bodyless declaration matched. |
| Pinned-package source scan for `skorokhod\|skorohod\|strassen\|probability coupling` | 0 | The sole match was documentation for Strassen matrix multiplication; no probability-theoretic candidate matched. |
| Pinned tool and dependency identity checks | 0 | Lean `4.29.0` commit `98dc76e3...ab16740`; Lake `5.0.0-src+98dc76e`; mathlib `8a178386...ea95`, tree `bdc39a31...c2b`, clean worktree; `flt-regular` `56161b6e...1a27`, tree `32c9eace...e520`, clean worktree; toolchain and manifest hashes match frozen evidence. |
| Root-input freshness against `11a448c97289d30fe7c8c05dbac5a283a9d00896` | 0 | `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and the seven structured root inputs are byte-unchanged. |

Exact prohibited-construct scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide|^[[:space:]]*(?:constant|opaque|extern|external)[[:space:]]' \
  Stage1_Instances/THM-M-1010 --glob '*.lean'
```

Exact narrow replay, run from the repository root:

```bash
set -euo pipefail
repo="$PWD"
tmp=$(mktemp -d /tmp/thm1010-slot24.XXXXXX)
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

This is fresh current-base nonrelease blocker evidence only. It does not
satisfy `S56-M-1010-PROOF`, change scheduler state, or claim audit completion,
theorem completion, validation, release, or master acceptance.
