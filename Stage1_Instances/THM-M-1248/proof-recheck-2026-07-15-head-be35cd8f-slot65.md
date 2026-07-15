# THM-M-1248 proof recheck at `be35cd8f`

Item: `S56-M-1248-PROOF`  
Date: `2026-07-15`  
Base revision: `be35cd8f5123e9d06247b12859f3843bdd90c66f`

## Verdict

`blocked`. The exact target remains open. The existing `Proof.lean` bodies were replayed at trust
level zero and still close only the parameter split (`M1248-N-PARAM`) and the lower-order `a = 0`
endpoint (`M1248-B-A0`). They do not construct `CKNAnalyticPackage`, so the immediate root cut
remains `M1248-T-ALL-PARAMS` and the assigned proof phase remains `[ ]`.

The first failed gate remains `M1248-L-ORIGIN`: the pinned closure has no checked package for the
measurability, integrability, cutoff, and limiting facts needed at singular radial weights. The
weighted Sobolev/Hardy endpoint, its `a = 1` branch, and the interior Holder/real-power construction
therefore remain open. The nearest mathlib theorem is unweighted and cannot receive proof credit.

No definitional shortcut closes the target. Bochner integration evaluates a nonintegrable
integrand to zero, but admissible compactly supported smooth functions include genuinely integrable,
nontrivial Sobolev and interpolation cases. `Real.rpow` has its ordinary non-collapsing behavior.
The statement's raw `Fin n -> Real` radial norm is the Pi sup norm while `u` is evaluated after an
`L2` `WithLp` transport; this is a fidelity issue to review, not a proof of the frozen proposition.

No `.stage1-worker-selftest.json` was written because the proof phase is not complete. This record
is blocker evidence only and does not propose provisional or accepted completion.

## Validation

All checks used the automation-provided pinned `.lake` artifacts read-only. No Lake update/build,
dependency clone/fetch, network action, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed |
| `python3 scripts/stage1_target.py show THM-M-1248` | 0 | Rank 428; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1248/check_obligation_tree.py` | 0 | 18 obligations and 43 typed edges passed; root open M3; analytic package M4 |
| isolated trust-zero replay of `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `AnchorAudit.lean` | 0 | All modules elaborated; three partial bodies were sorry-free and used only `propext`, `Classical.choice`, and `Quot.sound` |
| prohibited-construct scan over owned Lean files | 1 | Expected no-match exit; no placeholder, bodyless axiom, unsafe/oracle, or native shortcut was found |
| JSON checks for the existing receipt and prior blocker | 0 | Both structured records parsed |
| `git diff --check -- Stage1_Instances/THM-M-1248` | 0 | No whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest correctly absent |

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Reopen Condition

Resume after placeholder-free implementations of the singular-weight boundary package, the exact
weighted Sobolev/Hardy endpoint, and the interior Holder/real-power construction, followed by exact
composition into `CKNAnalyticPackage`; alternatively, pin an immutable compatible terminal Lean 4
proof and validate its exact transport and provenance without changing the dependency lock.

