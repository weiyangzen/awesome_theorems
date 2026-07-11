# THM-M-0399 anchor audit

Item `S56-M-0399-ANCHOR_AUDIT`; search cutoff `2026-07-12` (Asia/Shanghai). This
is a frozen candidate inventory, not proof evidence. The comparison target is exactly
`Stage1Instances.THM_M_0399.RothStatement`, the constant-one, exponent-`2 + epsilon`
finite-set proposition fingerprinted in `statement.json`.

## Immutable boundary

The repository base is `72e8a2edc0088f19a59d40d8b64c51a5c9143981`. The Lake manifest pins
mathlib to `8a178386ffc0f5fef0b77738bb5449d50efeea95`, whose checked-out tree is
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; the manifest SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
The checked-out dependency HEAD matches the pin. No dependency was fetched, updated, built, or
otherwise changed.

The protocol searched repo-local Lean first, the complete pinned mathlib and `flt-regular` source
trees next, then the immutable tree of the credible Lean statement collection Formal Conjectures.
Anonymous GitHub repository searches for `Roth theorem Lean`, `Roth rational approximation Lean`,
and `Diophantine approximation Lean4` each returned zero repositories. GitHub code search requires
authentication, and grep.app returned a security-checkpoint page. Thus this is complete for the
recorded protocol, not a claim that every public Lean repository was exhaustively searched.

## Candidate ledger

| Candidate | Immutable location | Exact comparison | Decision |
|---|---|---|---|
| Local historical THM-M-0399 surface | repository base above; `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_012.lean`; `RothStatementShapeA`, `RothStatementShapeEpsilon`, `candidateA_implies_epsilon` | The epsilon shape is close to the exact target and Candidate A conditionally specializes to it. Both root shapes are `def : Prop`; the only bridge assumes Candidate A. The file explicitly records that no terminal proof exists. | Statement and conditional transport only; no machine credit. |
| Local THM-M-0398 overlap | same base; `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_011.lean`; `RothStatementShape` and conditional bridge lemmas | Uses a lower-bound/interface variant and proves useful normalization and `LiouvilleWith` bridges only after receiving the missing Roth hypothesis. It neither has the exact type nor closes it. Target identity also forbids borrowing credit from THM-M-0398. | Reject as root anchor; adjacent infrastructure only. |
| mathlib Diophantine approximation | pinned mathlib; `Mathlib.NumberTheory.DiophantineApproximation.Basic`; `Real.infinite_rat_abs_sub_lt_one_div_den_sq_of_irrational`, `Rat.finite_rat_abs_sub_lt_one_div_den_sq`, `Real.infinite_rat_abs_sub_lt_one_div_den_sq_iff_irrational` | These classify exponent-two approximation: irrational real targets have infinitely many good approximants, while rational targets have finitely many. The exact root instead needs finiteness for algebraic irrational targets at every exponent strictly above two. | Reject due to statement mismatch; useful P1 infrastructure only. |
| mathlib `LiouvilleWith` and height APIs | pinned mathlib; `Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleWith`, `Mathlib.NumberTheory.Height.Basic`, `Mathlib.NumberTheory.Height.NumberField` | Supplies predicates and object models for a future proof architecture, but no theorem deriving the exact finite exceptional set for algebraic irrational reals was found. | No terminal anchor. |
| mathlib `Roth` name hits | pinned mathlib; `Mathlib.Combinatorics.Additive.Corner.Roth`; `roth_3ap_theorem`, `roth_3ap_theorem_nat` | These are Roth's additive-combinatorics theorem on three-term arithmetic progressions, not rational approximation. | Reject as name collision. |
| Formal Conjectures | `google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c`; complete commit tree | No path matching Roth, rational approximation, or Diophantine approximation was present. Therefore there is no declaration, type, body, axiom profile, or dependency feasibility to credit. | No candidate to integrate. |

The historical local files contain no `sorry`, `axiom`, or other root-closing declaration for this
target; their checked theorem bodies are transports or conditional consequences. No external proof
candidate was found, so there is no actionable `repo_local_integration_debt`. Importing any listed
candidate would not close the exact proposition.

## Validation record

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets with ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0399` | exit 0; rank 12, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; exact manifest pin |
| scoped `rg` searches over repo-local Lean, pinned mathlib, and pinned `flt-regular` | exit 0/1 as expected; only the candidates and name collisions listed above were found |
| GitHub immutable Formal Conjectures tree query and three repository queries | exit 0; commit recorded above, no matching path, repository totals `0, 0, 0` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0399/RothStatement.lean` | exit 1; `unknown module prefix 'Mathlib'` because the canonical reused cache lacks `Mathlib.olean` |
| `python3 Stage1_Instances/THM-M-0399/check_anchor_audit.py` | exit 0; pins, candidate invariants, negative-result boundary, and source witnesses passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0399/anchor-audit.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0399 .stage1-worker-selftest.json` | exit 0; no output |

The failed Lean replay is a recorded cache limitation. Worker policy forbids repairing it with a
build, update, clone, or fetch. It does not turn the already frozen statement into proof evidence and
does not prevent a source/provenance audit of candidates.

## Verdict

This anchor-audit phase is self-tested. The exact root remains `[H1, M4, R4]`, with
`theorem_complete=false`. The primary paper is identified but lacks theorem/page, errata, and
independent-review closure, so H0 is not claimed. The remaining root cut begins with a genuine local
proof architecture or a future immutable exact external proof, followed by obligation-tree,
validation, and release gates. Master acceptance remains outstanding.
