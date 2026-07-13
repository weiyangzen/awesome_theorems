# THM-M-0498 proof-phase validation

Item: `S56-M-0498-PROOF`. Base revision:
`3bb4cb3ae15dff8b48c93242019edec3bf858e48`.

## Implemented body

`Proof.lean` supplies a genuine local proof body for the arithmetic-to-analytic
Dirichlet-series bridge intended by frozen node `M0498-A-DIRICHLET`. At every
`s` with `1 < s.re`, it identifies the complex L-series of the von Mangoldt
function with `-deriv riemannZeta s / riemannZeta s`, using the terminal body
`ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div` from the
pinned mathlib revision.

The frozen node currently has a planned rather than elaborated statement
fingerprint. This receipt therefore records the checked declaration as a
supported subbranch and conservatively claims no whole frozen obligation
closed. The root remains `M4`; the minimal open mathematical cut is
`M0498-T-ANALYTIC`.

No specialized Perron bridge for `Chebyshev.psi`, zero-avoiding contour
displacement with zeta estimates, residue package, trivial-zero series, or
nontrivial-zero convergence result is asserted here. Pinned mathlib does have
generic Mellin and rectangular-contour infrastructure, but it does not supply
the exact analytic package. The conditional `root_of_analytic_package` remains
only a composition interface, not a proof of that package or canonical target.

Pinned mathlib also has no proof that `NontrivialZeroEnumeration` is inhabited.
The target quantifies over every such enumeration, so a later root claim must
keep its realizability/nonvacuity obligation visible rather than obtaining
credit from a potentially empty input type.

## Commands and results

Validation ran in the worker clone on 2026-07-14. The pre-existing untracked
`Formalizations/Lean/.lake` link points to the canonical pinned artifacts and
was reused read-only. No Lake update/build, dependency clone/fetch, or other
`.lake` mutation was run.

```text
bash Stage1_Instances/THM-M-0498/check_proof.sh
  exit 0
  Statement.lean and ObligationTree.lean were compiled into a temporary
  directory; Proof.lean then elaborated against those temporary oleans and
  the pinned dependency path. Both the pinned terminal and local wrapper were
  transitively sorry-free. Both axiom reports contained only propext,
  Classical.choice, and Quot.sound. The structural receipt checker passed.

python3 Stage1_Instances/THM-M-0498/check_obligation_tree.py
  exit 0
  PASS THM-M-0498 obligation tree: 15 obligations, 33 typed edges
  registry denominator sha256:
  8a964cd4c13dc98d9bfa75e22cf5bab2af31d96d83bde13600049c669d88f144
  root closure: open (M4); analytic explicit-formula package remains M4

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0498
  exit 0: rank 258, planned, hard_mathlib_anchor_and_wrapper,
  theorem_complete=false

rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe|extern)\b|implemented_by|native_decide' \
  Stage1_Instances/THM-M-0498/Proof.lean
  exit 1 with empty output: no prohibited proof device

python3 -m json.tool Stage1_Instances/THM-M-0498/proof-receipt.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-0498/proof-blocker.json >/dev/null
python3 -m json.tool .stage1-worker-selftest.json >/dev/null
  exit 0 for all three JSON documents

git diff --check -- Stage1_Instances/THM-M-0498 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The available executable is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`. Mathlib is exactly revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, and its worktree was clean.

This is self-tested partial proof execution. Master acceptance, exact frozen
node reconciliation, all remaining analytic proof bodies, H0/R0, downstream
validation/release, hermetic replay, independent verification, and theorem
completion remain open.
