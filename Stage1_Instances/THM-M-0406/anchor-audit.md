# THM-M-0406 anchor audit

Item: `S56-M-0406-ANCHOR_AUDIT`  
Audit date: 2026-07-12  
Canonical target: `Stage1Instances.THMM0406.CorvajaZannierTheoremOne`

## Verdict

No proof-bearing Lean 4 declaration for Corvaja--Zannier Theorem 1 was found
in the bounded immutable inventory. The exact proposition elaborates, but the
root remains `[H1, M3, R3]`: mathlib supplies useful foundations while the
surface intersection, Subspace-Theorem, and S-integral-point degeneracy
arguments remain formalization debt.

This self-tests the assigned anchor-audit node only. It does not establish H0,
prove the theorem, complete the overall audit, or support a release claim.

## Immutable candidates

| Candidate | Immutable revision | Finding | Classification |
|---|---|---|---|
| mathlib4 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`) | No Corvaja/Zannier, Evertse/Ferretti, Subspace-Theorem, or exact surface-degeneracy declaration | no terminal candidate |
| mathlib substrate | same revision | Schemes, proper/smooth/open morphisms, finite places, heights, Northcott interface, S-integers, and S-units elaborate in `AnchorAudit.lean` | support only |
| `flt-regular` | `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` (tree `32c9eace926573a9981787ae97643e520353c893`) | No relevant terminal or bridge declaration | no terminal candidate |
| Formal Conjectures | `b2e608fc52d765510915a244bb69b1a2741acc3c` | Complete 1204-entry recursive tree had no relevant path; the sole keyword path was the unrelated invariant-subspace problem | no candidate path |
| Public GitHub repositories | API responses dated 2026-07-12 | Five repository queries returned zero with `incomplete_results=false` | bounded negative result |
| Legacy `S1_M_019.lean` | repository base `4dabab14860067cbb1220d76c5a1bd9abd87d624` | Abstract planning interfaces and negative audit metadata; explicitly not repo-local closure | discovery only |

The external search is deliberately not called exhaustive. GitHub code search
returned HTTP 401 without authentication, and grep.app returned HTTP 429. No
candidate was found through the accessible routes, so there is currently
nothing concrete to pin, import, or vendor.

## Mathlib boundary

The checked substrate is useful for later decomposition, but none of it implies
the root. In particular, `Mathlib.RingTheory.DedekindDomain.SInteger` defines
`Set.integer`, `Set.unit`, and `Set.unitEquivUnitsInteger`, while its module
documentation explicitly leaves finite generation and Dirichlet's S-unit
theorem as TODOs. Searches also found no divisor intersection-number API tied
to smooth projective surfaces and no Schmidt Subspace Theorem. Generic
`Northcott` and scheme-morphism declarations are support, not bridge closure.

## Integration decision

`exact_external_closure_found = false`. Therefore adding a dependency or
vendoring a proof would be fabricated rather than integration. The honest next
step is an obligation tree separating scheme geometry, boundary-divisor
intersection theory, heights/S-integrality, the Subspace-Theorem input, and the
exceptional-subspace-to-curve descent. Until those obligations close, machine
status remains `M3` and theorem completion remains false.
