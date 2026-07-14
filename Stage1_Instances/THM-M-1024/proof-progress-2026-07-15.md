# THM-M-1024 proof-phase progress

Item: `S56-M-1024-PROOF`

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

## Verdict

`blocked`; a real analytic proof body was added, but the assigned proof phase is not complete and
no item-state transition or theorem completion is claimed.

`Proof.lean` closes the compensated-exponent integrability part of frozen obligation
`M1024-N-EXPONENT` for every finite dimension.  It proves measurability, a pointwise bound by
`(2 + 3 * norm u ^ 2) * min 1 (norm x ^ 2)`, and Bochner integrability against every measure
satisfying the local `IsLevyMeasure` predicate.  The final theorem
`integrable_levyExponent_jump` is written in the exact integrand syntax used by `levyExponent`.
This is a repo-local, placeholder-free body, not a copied external theorem.

The exact root remains open.  The local conditional composition still requires
`ForwardExistencePackage`, `ConversePackage`, and `UniquenessPackage`, and neither pinned mathlib
nor the owned path supplies an inhabitant of any package.  Pinned mathlib has no
Levy-Khintchine/infinite-divisibility theorem family.  The audited `slink/LeanLevy` candidate is
only over `Real`, with scalar covariance and open-ball compensation, and therefore cannot prove
the all-finite-dimensional target.  The immediate root cut stays `M1024-T-FORWARD`,
`M1024-T-CONVERSE`, and `M1024-T-UNIQUENESS`.

The first failed frozen gate remains `M1024-N-EXPONENT`: compensated-integrand
integrability is now checked, but the complete exponent-normalization package is not.  Its
downstream forward/converse/uniqueness branches are therefore also open.

Because the deliverable says to implement or pin/import the required proof bodies and those root
packages remain absent, `.stage1-worker-selftest.json` is deliberately not written.  The root
vector remains `[H1, M3, R3]`; `proof_phase_complete=false` and `theorem_complete=false`.

## Narrow validation

All Lean commands use the existing pinned Lake environment.  The final command creates the
statement olean only in a temporary directory; it does not run `lake update`, `lake build`, clone
or fetch a dependency, or mutate `.lake`.

```bash
set -euo pipefail
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH="$LP" "$LEAN" --trust=0 -R Stage1_Instances/THM-M-1024 \
  -o "$tmp/Statement.olean" Stage1_Instances/THM-M-1024/Statement.lean
LEAN_PATH="$tmp:$LP" "$LEAN" --trust=0 -R Stage1_Instances/THM-M-1024 \
  Stage1_Instances/THM-M-1024/Proof.lean
```

The trust-zero Lean replay exited `0`.  Both exported analytic theorems reported only
`propext`, `Classical.choice`, and `Quot.sound`; `sorryAx` was absent.
An independent read-only review repeated that replay and audited the pointwise-domination and
`Integrable.mono'` arguments; it found no mathematical or Lean soundness issue.

The recorded supporting checks and their final results are:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1024` | 0 | rank 500; planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1024/check_obligation_tree.py` | 0 | Frozen 24-obligation/66-edge architecture passed |
| isolated `--trust=0` statement plus proof replay above | 0 | Exact source elaborated; analytic declarations have no `sorryAx` |
| prohibited-construct scan over owned Lean sources | 1 | Expected no-match result: no forbidden construct occurs |
| scoped tracked `git diff --check` plus `git diff --no-index --check /dev/null <fresh-file>` for each new artifact | 0 | No scoped whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest absent because proof phase remains blocked |

## Reopen condition

Resume by formalizing the remaining finite-dimensional forward, converse, and uniqueness packages
and composing them through `root_of_packages`, or by making an immutable exact all-dimensional
proof available for pinned local integration and trust/provenance checks.

## Status boundary

This is truthful partial proof progress and fresh blocker evidence for `S56-M-1024-PROOF`.  It is
not a proof receipt, completion self-test, accepted obligation-registry update, validation/release
packet, master acceptance, or theorem-completion claim.
