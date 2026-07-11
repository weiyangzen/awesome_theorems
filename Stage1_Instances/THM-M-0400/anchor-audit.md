# THM-M-0400 formal-anchor audit

Audit item: `S56-M-0400-ANCHOR_AUDIT`. Search cutoff: `2026-07-12`
(Asia/Shanghai). The exact target is `Stage1Rev56.THMM0400.Statement` in
`Statement.lean`. This is a validated candidate inventory, not a proof receipt.

## Immutable search boundary

The local search used repository revision
`5093f20d511694e3a61ba1d6f425083e10ac2a00`, pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`), pinned `flt-regular` revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`, and Lean 4.29.0. The Lake lock
file SHA-256 was
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
No dependency was fetched, updated, built, or modified.

Queries covered `Schmidt`, `Schmidt subspace theorem`, `SubspaceTheorem`,
`subspace theorem`, `Thue-Siegel-Roth`, `Evertse`, `Schlickewei`,
`simultaneous approximation`, `DiophantineApproximation`, and product-of-linear-
forms phrases. Search order was repo-local Lean, every locally pinned mathlib and
`flt-regular` Lean source, Lean Reservoir, GitHub repository search, GitHub code
search, and grep.app.

## Candidate comparison

| Candidate | Exact immutable location | Comparison with the root | Verdict |
|---|---|---|---|
| Legacy shape | `AwesomeTheorems.Stage1.S1_M_013.StatementShape` at the repository revision above | Its algebraicity, independence, height, smallness inequality, and exceptional-subspace membership are abstract fields or predicates. It has no checked transport to the canonical proposition and no terminal proof body for it. | Rejected: statement mismatch; discovery only |
| One-dimensional Diophantine approximation | `Mathlib.NumberTheory.DiophantineApproximation.Basic` at the pinned mathlib revision; `Real.exists_int_int_abs_mul_sub_le`, `Real.exists_nat_abs_mul_sub_round_le`, `Real.exists_rat_abs_sub_le_and_den_le`, `Real.infinite_rat_abs_sub_lt_one_div_den_sq_of_irrational`, `Rat.finite_rat_abs_sub_lt_one_div_den_sq` | These are genuine kernel-checked Dirichlet/continued-fraction substrate. They neither quantify over an independent family of algebraic linear forms nor produce a finite cover by proper rational subspaces. | Rejected as root anchor: substantive statement mismatch |
| Number-field/projective height API | `Mathlib.NumberTheory.Height.NumberField` and `.Projectivization` at the pinned mathlib revision; `Projectivization.mulHeight`, `logHeight`, `one_le_mulHeight` | These can support a future alternate height model, but do not prove a product inequality or exceptional-subspace theorem. The canonical statement currently uses an elementary integer sup height, so a transport would also be required. | Object-model substrate only |
| `flt-regular` | `leanprover-community/flt-regular` at `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` | The recorded topic/name search found no Schmidt, Evertse, Schlickewei, Roth, or Subspace-Theorem terminal declaration. | Negative result |

The exact modules, declaration names, and proof sources were inspected in the
pinned mathlib tree. Fresh `lake env lean` checks could not resolve `Mathlib`
because the canonical shared `.lake` tree currently lacks the required compiled
Mathlib objects. The worker policy forbids repairing that cache with a build or
fetch. Consequently this audit credits source identity and immutable provenance,
not a fresh kernel replay or root proof.

## External search

Anonymous GitHub repository searches for `Schmidt subspace theorem Lean`,
`subspace theorem Lean4`, and `SubspaceTheorem lean` each returned
`total_count: 0`. GitHub code search returned HTTP 401 because this worker has
no authenticated GitHub session. grep.app returned a Vercel security-checkpoint
page instead of search data. Lean Reservoir displayed `No results found` for
`Schmidt`.

Thus no external repository, immutable revision, Lean module, declaration,
toolchain, proof body, axiom profile, license, or dependency graph exists to
credit or integrate from the accessible results. This is not an exhaustive
claim about all public Lean code. The retry condition is authenticated GitHub
code search or another accessible code index; any future exact hit must be
pinned, imported, and checked rather than left as anchor-only evidence.

## Human source boundary

Crossref verifies Wolfgang M. Schmidt, *Simultaneous approximation to algebraic
numbers by rationals*, Acta Mathematica 125 (1970), 189-201, DOI
`10.1007/BF02392334`. This identifies a primary published proof source and
supports `H1`, not `H0`. The exact internal theorem/page for the full
linear-forms formulation, premise-by-premise normalization, errata, and an
independent source review remain open.

## Result and validation

No exact terminal Lean 4 proof candidate was found. The canonical proposition
remains statement-only (`M3`), and the root debt is `formalization_debt`, not a
discovered `repo_local_integration_debt`. The bounded anchor-audit phase is
self-tested, while full audit completion and theorem completion are both false.

Commands run from the repository root unless a working directory is stated:

- `python3 Docs/tools/check_stage1_standard.py`: exit 0; all 1546 targets passed.
- `python3 scripts/stage1_target.py check`: exit 0; all 1546 unique targets passed.
- `python3 scripts/stage1_target.py show THM-M-0400`: exit 0; rank 13, L0,
  rework required, planned, theorem incomplete.
- From `Formalizations/Lean`, `lake env lean ../../Stage1_Instances/THM-M-0400/Statement.lean`:
  exit 1; `unknown module prefix 'Mathlib'`. The canonical shared `.lake` tree
  lists the Mathlib build path but lacks its compiled module objects. No build,
  update, clone, or fetch was attempted. The prior statement-phase elaboration
  remains recorded separately; this phase makes no fresh kernel claim.
- `python3 -m json.tool Stage1_Instances/THM-M-0400/anchor-audit.json`: exit 0.
- Scoped `rg` searches over the pinned mathlib and `flt-regular` Lean trees:
  exit 0 for the search pipeline; no arithmetic Subspace-Theorem terminal hit.
- Three GitHub repository-search API requests: exit 0; counts `0, 0, 0`.
- GitHub code-search API request: request exit 0, HTTP 401; access blocker recorded.
- grep.app API request: request exit 0, but returned security-checkpoint HTML.
- Crossref DOI request: exit 0; citation fields above returned.
- `git diff --check -- Stage1_Instances/THM-M-0400`: exit 0.

The existing untracked `Formalizations/Lean/.lake` link is outside the owned path
and was not intentionally modified. These results are worker evidence only;
master acceptance and every later rev-5.6 gate remain outstanding.
