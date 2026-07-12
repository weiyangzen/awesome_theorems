# S56-M-1270-PROOF worker evidence

Date: `2026-07-12`

Base revision: `d37af820f29f76421ee53b63322cae0e13bd731b`

Pinned environment: Lean `4.29.0`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Proof bodies admitted

`Proof.lean` repeats the exact transparent proposition from `Statement.lean` as `ProofTarget` and
checks proof bodies for the positive penalty slope, transitivity of the descent relation, the
finite-chain telescoping estimate, localization from the approximate-minimizer bound, strict
penalized minimality from descent maximality, witness packaging, and final root composition from an
explicit maximal-point constructor. The `#print axioms` results for every theorem are exactly
`propext`, `Classical.choice`, and `Quot.sound`; no theorem contains `sorryAx`.

The remaining hard premise of `target_of_maximalPoint` is not claimed or hidden: the pinned closure
still has no proof constructing a descent-maximal point from completeness and lower
semicontinuity. Thus `M1270-C-SEQUENCE`, `M1270-L-CAUCHY`, and `M1270-L-LIMIT` remain open along
with the registry nodes whose unconditional closure depends on them. The exact root remains `M3`,
and theorem completion is false. This receipt self-tests only the concrete proof bodies above,
pending master acceptance.

## Commands and exact results

Commands ran from the repository root unless noted. The existing pinned `.lake` artifacts were
reused; no update, build, clone, fetch, or dependency mutation was performed.

| command | exit | result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1270` | 0 | rank 163; planned; L0/rework-required; theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-1270/Statement.lean` from `Formalizations/Lean` | 0 | exact target and structural mutations elaborated |
| `lake env lean ../../Stage1_Instances/THM-M-1270/Proof.lean` from `Formalizations/Lean` | 0 | seven proof declarations elaborated; each printed only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-1270/check_obligation_tree.py` | 0 | 17 obligations and 41 typed edges passed; root reported open at M3 |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|(^\|[^[:alnum:]_])axiom[[:space:]]' Stage1_Instances/THM-M-1270/Proof.lean` | 1 | expected clean result: no prohibited proof token found |
| `git diff --check -- Stage1_Instances/THM-M-1270/Proof.lean` | 0 | no whitespace errors |

Source SHA-256 values during validation:

```text
2df3271cdc697f454a89304bdf766da6ec173aa86f84f31c403998f805c1f951  Stage1_Instances/THM-M-1270/Statement.lean
4ba20c9bceb7c458e3f5c10f2b534ba30cac56868b20cc58e1b57201f79756a1  Stage1_Instances/THM-M-1270/Proof.lean
```

The pre-existing untracked `Formalizations/Lean/.lake` link makes this worker evidence nonrelease.

