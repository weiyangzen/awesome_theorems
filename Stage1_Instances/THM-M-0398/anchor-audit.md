# Lean 4 anchor audit

Audit date: 2026-07-12. This audit concerns the exact declaration
`Stage1Instances.THMM0398.ThueSiegelRoth` frozen in `Statement.lean`. It does
not credit the broader legacy integer-pair lower-bound formulation.

## Immutable environment

- Lean toolchain: `leanprover/lean4:v4.29.0`.
- Pinned mathlib repository: `https://github.com/leanprover-community/mathlib4.git`.
- Pinned and locally inspected mathlib commit:
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- The dependency commit was confirmed with `git -C
  Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD`; its worktree was
  clean. No dependency was fetched, updated, or modified.

## Pinned mathlib candidates

| Module and declaration | Audited role | Exact-root disposition |
|---|---|---|
| `Mathlib.NumberTheory.DiophantineApproximation.Basic`; `Real.infinite_rat_abs_sub_lt_one_div_den_sq_of_irrational` | Infinitely many exponent-2 approximations to an irrational real | Supporting interface only; opposite finiteness direction and exponent exactly 2 |
| same module; `Rat.finite_rat_abs_sub_lt_one_div_den_sq` | Exponent-2 finiteness for a rational target | Supporting interface only; target is rational, not irrational algebraic |
| same module; `Real.infinite_rat_abs_sub_lt_one_div_den_sq_iff_irrational` | Characterizes exponent-2 infinitude | Supporting interface only; it does not address exponent `2 + epsilon` |
| `Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleWith`; `LiouvilleWith`, `LiouvilleWith.exists_pos` | Encodes infinitely frequent approximation with a real exponent and a positive constant | Object-model candidate only; the module documentation says the `p > 2` algebraic result is Roth's theorem, but supplies no such declaration |
| `Mathlib.NumberTheory.Height.Basic`; `Height.mulHeight₁`, `Height.logHeight₁` | Height infrastructure for fields with admissible absolute values | Substrate only; no checked bridge to the canonical rational-denominator finite set |
| `Mathlib.NumberTheory.SiegelsLemma` | Auxiliary integer-matrix Siegel lemma infrastructure | Substrate only; no Roth auxiliary-polynomial or terminal theorem was found |
| `Mathlib.Combinatorics.Additive.Corner.Roth`; `roth_3ap_theorem`, `roth_3ap_theorem_nat` | Roth-name search hits | Rejected false positives: these concern three-term arithmetic progressions |

Repository-local searches over the entire pinned `Mathlib` source used the
case-insensitive terms `thue.?siegel`, `siegel.?roth`, `roth.?theorem`,
`rational approximations to algebraic`, `irrationality measure`,
`irrationality exponent`, and `diophantine approximation`. They found the
infrastructure above and the combinatorial name collision, but no declaration
whose conclusion implies the canonical finite set for every irrational
algebraic real and every positive `epsilon`. `AnchorAudit.lean` checks the
principal discovered declaration names against the pinned environment.

## External Lean 4 search

The following GitHub repository-search queries were executed against
`https://api.github.com/search/repositories` on 2026-07-12:

- `"Thue-Siegel-Roth" Lean`
- `"Roth theorem" Lean theorem prover`
- `DiophantineApproximation Roth Lean`
- `LiouvilleWith IsAlgebraic Lean`

Each response reported `total_count: 0` and `incomplete_results: false`, so
there was no candidate repository, revision, module, declaration, toolchain,
license, proof body, or dependency closure to inspect or integrate. GitHub CLI
reported that no host was authenticated. Attempts to use the GitHub code-search
API for `"Thue-Siegel-Roth" language:Lean`, `"Roth theorem" language:Lean`,
and `LiouvilleWith IsAlgebraic language:Lean` returned HTTP 401. Thus this is a
truthful bounded search, not proof that no external formalization exists.

## Classification and gate result

No exact mathlib theorem or credible external Lean 4 terminal candidate was
identified. Consequently there is no external proof-body provenance, axiom
profile, unsafe/oracle boundary, or dependency feasibility claim to credit.
The mathlib rows are checked supporting anchors or false positives, not
`local_wrapper_upstream_mathlib`; the external search produced no
`external_upstream_pinned` candidate. Root debt remains `[H1, M3, R4]` and
the theorem remains `planned`, with `audit_complete: false` and
`theorem_complete: false`. This anchor-audit phase is complete as a candidate
inventory, while proof, source-fidelity, readability, trust, hermetic, and
release gates remain open.

## Validation receipt

Base revision: `c6c42c0e2299434c893a99fb40cc6f586e261523`.

| Command | Result |
|---|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; printed the pinned commit above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; no output |
| repository-local `rg` searches described above | exit 0; only supporting infrastructure, documentation mention, and false-positive Roth hits |
| GitHub REST repository searches described above | exit 0; four complete zero-result responses |
| GitHub REST code searches described above | HTTP 401; recorded search-coverage limitation, not a candidate-validation failure |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0398/AnchorAudit.lean)` | exit 0; all principal anchor declaration names and types checked |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0398/Statement.lean)` | exit 0; canonical statement still elaborates |
| `git diff --check -- Stage1_Instances/THM-M-0398` | exit 0; no whitespace errors |

Known limitation: unauthenticated GitHub code search could not provide global
source-file coverage. Since no external candidate is being credited, this
does not invalidate completion of the bounded anchor inventory, but any future
candidate must be audited at an immutable commit and pinned/imported/checked
before receiving machine-closure credit.
