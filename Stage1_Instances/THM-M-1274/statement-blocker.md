# Exact-statement gate: blocked

Item: `S56-M-1274-STATEMENT`  
Theorem: `THM-M-1274`  
Base revision: `aae45673b30d1b10288a632168bbf9df19b441b9`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record supplies only the theory name "Ljusternik-Schnirelmann theory", the attribution and year,
and the gloss "topological index and critical points". It supplies no primary-source edition,
theorem/page, exact statement, or definitions. The accepted intake therefore correctly leaves the
canonical statement and formal target unset.

The label denotes a family of inequivalent results. It does not fix:

- normalized versus unnormalized Lusternik-Schnirelmann category;
- the class of spaces (for example, closed smooth manifolds, topological spaces, or an
  infinite-dimensional variational setting);
- the regularity and domain of the function or functional;
- compactness, Palais-Smale, boundary, or nondegeneracy assumptions;
- the definition of critical point and whether distinct points or distinct critical values are
  counted;
- whether the conclusion is a bound by `cat(X)`, `cat(X) + 1`, cup-length, or another index.

These choices change the domains, ordered binders, hypotheses, boundary cases, and numerical
conclusion. Selecting the familiar closed-manifold slogan, an abstract category axiom, or a PDE
specialization would substitute mathematics rather than elaborate the repository claim. Thus the
canonical human statement fails before minimal imports, expression serialization, checked
transports, or meaningful removed-hypothesis, changed-domain, binder-scope, and boundary mutation
tests can exist. No Lean declaration, placeholder, assumed interface, weakened special case, or
broadened theorem was introduced. Machine state remains `M4`; statement acceptance and theorem
completion are false.

## Pinned environment and searches

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. The canonical `.lake` artifacts were read through the
existing worker symlink; no update, build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1274` | 0 | Rank 447, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for both spellings, both author names, and the source gloss | 0 | Found only the same underspecified metadata and target projections; no source-frozen proposition |
| pinned-mathlib `rg` search for both spellings, LS category, category/critical-point combinations, and cup-length | 0 | The only name hit was unrelated additive-combinatorics `Schnirelmann` density; no Lusternik-Schnirelmann category or critical-point target was found |

There is no applicable `lake env lean <target>.lean` command: the exact expression required by the
statement gate is precisely what the source record does not identify. Elaborating an invented
abstract proxy would be fake evidence rather than the assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary or authoritative edition and exact
theorem/page, resolve errata, and freeze the category normalization, space and function classes,
regularity and compactness hypotheses, critical-point notion, quantifier order, and exact lower
bound. A later statement run can then crosswalk every source premise, encode the exact expression,
minimize its pinned imports, fingerprint the elaboration and environment, compile any alternate
transports, and execute all four mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
