# Exact-statement gate: blocked

Item: `S56-M-1276-STATEMENT`  
Theorem: `THM-M-1276`  
Base revision: `ae31ccd191d463080f9c44bfdc48230fee30094a`

## Decision

The exact Lean 4 target cannot yet be truthfully frozen from the accepted repository evidence. The
catalog supplies only the name "Trudinger inequality" and the gloss "critical Sobolev embedding."
The planned intake selects a non-sharp zero-boundary exponential-integrability formulation, but it
explicitly leaves the source-required domain regularity, the definition of `W_0^{1,n}`, the weak
gradient and trace conventions, and the norm-versus-modular normalization unresolved. It also says
that the 1967 paper has not been pinned to an immutable scan, exact theorem/page, assumptions, or
errata.

Those omissions affect the proposition rather than only its proof. In particular, a bounded open
set, a bounded Lipschitz domain, a domain satisfying a cone condition, and a closure-of-compactly-
supported-functions formulation do not give definitionally identical Lean targets. Nor may a
statement about smooth compactly supported functions silently replace the intake's quantified
Sobolev functions without a checked density transport. Choosing one convenient version here would
invent missing mathematics or substitute a stronger or narrower theorem.

Consequently the rev-5.6 canonical source-statement identity gate fails before a canonical Lean
declaration can be created. Minimal pinned imports, an elaborated-expression fingerprint, checked
alternate-form transports, and meaningful removed-hypothesis/domain/binder/boundary mutations all
depend on that missing choice. Machine status remains `M4`; no statement acceptance, proof credit,
audit completion, or theorem completion is claimed.

## Repository and environment evidence

No target-specific Lean module or pinned primary-source asset for `THM-M-1276` was found. The only
repo-local mathematical text beyond the intake repeats the title, attribution, year, and one-line
gloss. The reused canonical Lake environment is present and pinned, so the blocker is statement
identity rather than an unavailable Lean executable.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

Commands ran from this worker clone on 2026-07-12. No Lake update, build, dependency clone/fetch, or
mutation of `.lake` was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1276` | 0 | rank 327, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `rg -n 'Trudinger|临界Sobolev|Orlicz|1276' Formalizations Docs` with generated target files excluded | 0 | only the catalog/research gloss and the planned dossier identify this target; no exact target-specific Lean declaration or pinned source was found |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes match the environment fingerprint above |

## Required unblock

An accountable source review must pin an immutable copy of Trudinger's 1967 paper, identify and
quote the exact result and referenced definitions, and freeze all domain regularity, Sobolev-space,
trace, weak-gradient, integral, exponent, constant-dependence, and normalization conventions. It
must also decide whether the intake's modern exponential integral form is the root statement or a
transport from the paper's Orlicz formulation.

After that review, a statement worker can encode the selected claim with the smallest pinned
imports, print and hash the elaborated expression, compile every credited transport, and perform
the four required structural mutations. Until then this assigned phase is not genuinely
self-tested, so no `.stage1-worker-selftest.json` is emitted.
