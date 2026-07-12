# Exact-statement gate: blocked

Item: `S56-M-1196-STATEMENT`  
Theorem: `THM-M-1196`  
Base revision: `ebd311cf50e67029e9794aa8f09ab3cee28a745f`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
complete mathematical wording is only "the wave equation and its generalizations," under the title
"hyperbolic equations." This identifies a subject area, not a truth-valued proposition. No primary
source, edition, theorem number, page, exact equation, or conclusion is attached.

At minimum, an exact statement would have to fix:

- the operator and definition of hyperbolicity, including order and coefficient regularity;
- the spatial dimension, spatial domain, time interval, scalar field, and boundary geometry;
- initial and boundary data, compatibility conditions, and the solution concept;
- whether the claim concerns existence, uniqueness, regularity, stability, an energy estimate,
  finite propagation speed, a representation formula, or another inequivalent conclusion;
- the function spaces, norms, constants and their dependencies, local/global scope, and endpoint or
  degenerate cases.

Changing any of these choices changes the theorem. Selecting the classical wave equation, an
energy estimate, d'Alembert's formula, a finite-propagation result, or a general well-posedness
theorem would substitute mathematics not present in the source. Nearby Stage0 entries separately
schedule energy estimates and the method of characteristics, so silently absorbing either result
would also collapse distinct repository targets.

The intake dependency reaches the same fail-closed result and assigns `[H4, M4, R4]`; it does not
authorize a canonical proposition. The Stage0 record explicitly leaves precise definitions,
premises, proof route, axioms, and machine artifacts `待补充` (to be supplied). The metadata label
`已验证` is untrusted and is neither a primary-source review nor kernel evidence.

Consequently this phase fails at canonical human-claim identity, before minimal imports, ordered
Lean binders, an elaborated expression fingerprint, checked transports, or meaningful removed-
hypothesis, changed-domain, binder-scope, and boundary-case mutations can be established. No Lean
declaration, abstract interface assuming the result, weakened example, axiom, placeholder, or
broadened target was introduced. Machine state remains `M4`.

## Pinned environment and search

Commands ran from this worker clone on 2026-07-12. The existing canonical `.lake` symlink and
artifacts were read only; no update, build, clone, fetch, or other dependency mutation was run.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1196` | 0 | rank 390, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| `rg -n -i 'hyperbolic equation\|wave equation\|finite speed of propagation\|d.alembert' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching declarations or source text in pinned mathlib |
| repository `rg` search for the Chinese and English title/claim | 0 | found only the underspecified metadata and unrelated references; no source-frozen proposition or target-local Lean module |

There is no applicable `lake env lean <target>.lean` command: no exact target expression exists.
Compiling a freely chosen proxy would be false evidence for this deliverable.

## Retry condition

An accountable source reviewer must select an immutable primary source by edition, theorem/page,
and exact wording, then freeze every operator, domain, coefficient, data, solution-space, boundary,
quantifier, conclusion, constant, and endpoint choice listed above. A later statement worker can
then encode that exact claim, determine minimal pinned imports, print and hash the elaborated
expression, check any alternate transports, and run all required structural mutations.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted. This artifact claims neither statement acceptance nor
audit/theorem completion, and all downstream nodes remain open.
