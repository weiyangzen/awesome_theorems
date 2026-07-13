# THM-M-1010 proof recheck

Item: `S56-M-1010-PROOF`. Base revision:
`823dfcd5e231e84436ac3d88948d8e669c168fdb`.

## Verdict

The exact `Stage1Instances.THM_M_1010.Target` remains blocked at `M3`.
The existing `Proof.lean` genuinely proves the constant-law boundary case,
and `ObligationTree.lean` genuinely checks the final conversion from a
`CouplingPackage` to the root. Neither file constructs that package for an
arbitrary weakly convergent sequence. No root-critical obligation or debt
vector changed in this recheck.

The first failed gate is the joint `M1010-N-PARTITIONS` /
`M1010-C-COUPLING` construction gate. Pinned mathlib has useful substrate:

- Portmanteau null-frontier and set-mass convergence lemmas;
- Levy-Prokhorov metricization of weak convergence;
- unit-interval and product-space realizations of prescribed laws.

Those declarations do not allocate the laws compatibly so that one full
sequence converges almost surely. Independent or one-law-at-a-time
realizations therefore do not close the coupling.

## External candidate

Fresh exhaustive Sourcegraph searches for both spellings, including archived
repositories and forks, found one Lean 4 file:
`facebookresearch/atlas-lean`, commit
`34ffed396f376454c1a9b297f3fd74c5c801fb50`, blob
`6678048a1e5d62f383390a185d6935d3c2237f7a`. Its declaration
`skorokhod_representation` is restricted to probability measures on `Real`
and terminates with `by sorry`. It cannot be imported: it both weakens the
arbitrary-Polish-space target and has no eligible proof body.

The retry condition is a placeholder-free implementation of the frozen
partition, interval-coupling, measurability, exact-law, a.e.-stabilization,
and metric-convergence packages, or discovery of an immutable exact
Polish-space Lean proof that can be pinned and checked.

## Validation

Commands ran on 2026-07-14 in this worker clone. The existing canonical
`.lake` symlink was reused read-only; no update, build, clone, fetch, or
dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | ordered 1546-target manifest passed |
| `python3 scripts/stage1_target.py show THM-M-1010` | 0 | rank 290; planned; theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-1010/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `8cf08f66...16016`; root open at M3 |
| isolated temporary-olean replay shown below | 0 | exact statement, conditional composer, and constant-law bodies elaborated; axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -n --pcre2 '\b(?:sorry\|admit\|axiom)\b\|sorryAx\|unsafe\|implemented_by' Stage1_Instances/THM-M-1010 --glob '*.lean'` | 1 expected | no prohibited Lean construct in the owned sources |
| pinned-source search for `skorokhod|skorohod` | 1 expected | no matching pinned declaration |
| exhaustive Sourcegraph search plus immutable source inspection | 0 | sole public hit is Real-only and ends in `sorry` |
| `python3 -m json.tool Stage1_Instances/THM-M-1010/proof-blocker-2026-07-14.json` | 0 | structured blocker parses |
| `git diff --check -- Stage1_Instances/THM-M-1010` | 0 | no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean replay command:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1010-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/Stage1_Instances/THM-M-1010"
LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH_PINNED=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_PATH="$LEAN_PATH_PINNED" "$LEAN_BIN" -R "$PWD" \
  -o "$tmp/Stage1_Instances/THM-M-1010/Statement.olean" \
  Stage1_Instances/THM-M-1010/Statement.lean
LEAN_PATH="$tmp:$LEAN_PATH_PINNED" "$LEAN_BIN" -R "$PWD" \
  -o "$tmp/Stage1_Instances/THM-M-1010/ObligationTree.olean" \
  Stage1_Instances/THM-M-1010/ObligationTree.lean
LEAN_PATH="$tmp:$LEAN_PATH_PINNED" "$LEAN_BIN" -R "$PWD" \
  Stage1_Instances/THM-M-1010/Proof.lean
```

This is blocker evidence only. It does not satisfy the proof item, propose
`[_]`, or claim audit completion, theorem completion, release, or master
acceptance.
