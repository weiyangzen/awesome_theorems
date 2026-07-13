# THM-M-0441 proof-phase validation

Item: `S56-M-0441-PROOF`

Intent: `prove`

Base revision: `8f22279fd1216cdfb5676c758e6bdb08e0ba3e01`

Base tree: `d2e9e68da52ecfcfe15a9c48ac2262400e602667`
Date: `2026-07-14` (`Asia/Shanghai`)

## Implemented Proof Bodies

`Proof.lean` contains fourteen genuine placeholder-free bodies. In addition to
the existing algebraic-part laws, bounded-height finiteness, and empty
transcendental-part results, this execution adds two bodies:

- `ncard_transcendentalRationalPoints_le_height_slice` checks the exact
  cardinal monotonicity from the canonical slice to the finite height slice.
- `countingConclusion_zero_dimensional` closes the exact affine-dimension-zero
  branch for every set and every positive exponent. There is at most one point
  in `Fin 0 -> Rat`; `c = 1` is positive, and `T ^ epsilon >= 1` for `T >= 1`.
- `pilaWilkie_zero_dimensional` preserves the language, structure,
  o-minimality, definability, set, and exponent binders of the frozen target's
  `n = 0` specialization.

This is partial progress toward `M0441-B-ZERO`, not closure of that frozen
obligation: `M0441-B-ZERO` requires counting zero-dimensional blocks in
arbitrary ambient dimension, while this theorem specializes the ambient space
itself to dimension zero. The other elementary bodies make partial progress
toward `M0441-S-HEIGHT`, `M0441-S-ALG`, `M0441-B-POS`, and
`M0441-L-COUNT`. No frozen obligation is credited closed from these cases.

The exact general root remains `[H1, M3, R4]`. No proof body inhabits the four
premises used by `ObligationTree.engine_compose`. Uniform parameterization,
the determinant estimate, general semialgebraic block construction, and
dimension induction remain formalization debt. The local `CountingEngine`
interface is conditional and is not proof provenance for those packages.

## Narrow Validation

All commands ran in this worker clone. The automation-provided canonical
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 standard, 15 assurance groups, and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0441` | 0 | Rank 87; planned hard-mathlib lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0441/check_obligation_tree.py` | 0 | `PASS THM-M-0441 obligation freeze: 21 obligations, 18 proof edges; root open`. |
| Concatenate the three target Lean modules with local imports removed, then pipe to `cd Formalizations/Lean && LEAN_NUM_THREADS=1 lake env lean --trust=0 /dev/stdin` | 0 | Exact target, conditional composition, all fourteen proof bodies, and every axiom probe elaborated. Axiom sets were subsets of `propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx` occurred. |
| `python3 Stage1_Instances/THM-M-0441/check_proof.py` | 0 | Receipt hashes, frozen scope, pin, provisional branch closure, open-root boundary, and worker packet agreed. |
| `python3 Stage1_Instances/THM-M-0441/check_proof.py` source scan after stripping Lean comments | 0 | No prohibited construct occurs in the executable owned Lean source. |
| `python3 -m json.tool Stage1_Instances/THM-M-0441/proof-receipt.json >/dev/null` | 0 | Provisional node receipt parsed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0441/proof-blocker.json >/dev/null` | 0 | Remaining-root blocker parsed. |
| `python3 -m json.tool .stage1-worker-selftest.json >/dev/null` | 0 | Worker handoff packet parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0441 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics. |

The narrow Lean recipe is:

```bash
set -o pipefail
{
  sed '/^import Statement$/d' Stage1_Instances/THM-M-0441/Statement.lean
  sed '/^import Statement$/d' Stage1_Instances/THM-M-0441/ObligationTree.lean
  sed '/^import ObligationTree$/d' Stage1_Instances/THM-M-0441/Proof.lean
} | (cd Formalizations/Lean &&
  LEAN_NUM_THREADS=1 lake env lean --trust=0 /dev/stdin)
```

Lean is `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib is pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Boundary

This is a self-tested proof-phase delta proposed as `[_]`, not accepted state.
The first open general gate is `M0441-C-PARAM`; the remaining root cut set is
`M0441-C-PARAM`, `M0441-L-DET`, `M0441-C-BLOCKS`, `M0441-B-INDUCT`,
`M0441-SOURCE`, and `M0441-TRUST`. Validation, release, `AUDIT-Z`, `THEOREM-Z`,
and theorem completion are not claimed.
