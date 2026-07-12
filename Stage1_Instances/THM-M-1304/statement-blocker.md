# Exact-statement gate: blocked

Item: `S56-M-1304-STATEMENT`  
Theorem: `THM-M-1304`  
Base revision: `d106a271df55889c00fab33c3ecbdcc7f1d21bd1`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative
repository record. The entire mathematical claim available for this target is
the phrase "paracomposition" / "复合函数的仿微分", together with the unverified
attribution "Jean-Michel Bony, 1981". The record supplies no bibliography,
primary-source edition, theorem number or page, quoted statement, definitions,
or errata disposition. The predecessor intake is provisional (`[_]`) and
correctly leaves the canonical human and Lean statements open.

The phrase names a topic or construction family rather than a unique
proposition. In particular, it does not fix:

- the definition of the paracomposition operator or its dyadic decomposition
  and quantization conventions;
- scalar or vector domain and codomain, dimension, local or global setting,
  and homogeneous or inhomogeneous function spaces;
- regularity, support, invertibility, or nondegeneracy assumptions on the
  composing map and the function being composed;
- whether the conclusion is a symbolic-calculus identity, a boundedness or
  continuity result, an intertwining formula, or a remainder estimate;
- the source and target regularity indices, derivative loss or gain, constant
  dependencies, and endpoint and low-frequency cases.

Changing any of those choices changes the domains, binders, hypotheses, or
conclusion. An ordinary chain rule, a Bony paraproduct theorem, an abstract
operator interface, or a convenient continuity estimate would therefore be a
substituted theorem. Introducing one would violate the exact-statement and
anti-shortcut rules in sections 5.1 and 10.8 of the rev-5.6 blueprint.

The gate fails before minimal imports can be determined. There is consequently
no canonical declaration, elaborated-expression fingerprint, alternate-form
transport, or meaningful removed-hypothesis, changed-domain, binder-scope, and
boundary-case mutation suite. No Lean source, axiom, placeholder, assumed
interface, weakened special case, or proof claim was added. Machine debt
remains `M4`; statement acceptance, audit completion, and theorem completion
remain false.

## Pinned environment and searches

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The existing
`.lake` dependency artifacts were only read; no update, build, clone, or fetch
was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1304` | 0 | Rank 472, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | SHA-256 `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, respectively |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository `rg` search for `paracomposition`, `复合函数的仿微分`, and `THM-M-1304` outside this dossier | 0 | Only the screened metadata, Stage0 open fields, generated target projections, and execution scheduling records were found; no exact proposition or target-specific Lean module exists |
| pinned-mathlib `rg` search for paracomposition, paradifferential, paraproduct, Littlewood-Paley, and Besov terms | 1 | No matching definitions or declarations (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` command: no exact target
expression exists. Elaborating a newly invented proxy would be false evidence
for the assigned deliverable, not a narrow validation of it.

## Retry condition

An accountable source review must first identify an immutable primary source
and pinpoint the exact theorem and definitions, verify or correct the stated
attribution and date, and freeze every operator, space, regularity, convention,
hypothesis, estimate, and boundary choice listed above. A later statement run
can then encode that proposition, minimize its pinned imports, preserve the
elaborated expression and environment fingerprint, compile any required
transports, and execute all four mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
