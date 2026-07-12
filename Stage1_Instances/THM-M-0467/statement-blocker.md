# Exact-statement gate: blocked

Item: `S56-M-0467-STATEMENT`  
Theorem: `THM-M-0467`  
Base revision: `acc50c1ea63521fb2703cee1859ad05751924480`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record identifies Michel Raynaud and gives only the gloss "proof of the Manin-Mumford conjecture."
The intake deliberately treats Raynaud's 1983 paper *Courbes sur une variete abelienne et points
de torsion* as an uninspected discovery candidate, not as an accepted source statement. It records
the intended theorem family but leaves the exact historical formulation open.

The missing source decision is material. The available wording does not fix:

- whether the root is Raynaud's curve theorem or a general closed-subvariety formulation;
- whether the base is a number field, an algebraic closure of one, or an arbitrary algebraically
  closed characteristic-zero field;
- whether `X` is an integral subvariety, a reduced closed subscheme, or another closed locus;
- whether the conclusion is finiteness for a curve, a density criterion, or a finite-union
  decomposition by torsion translates;
- the geometric-point, torsion, translate, containment, and Zariski-closure conventions;
- the binder order and behavior for the empty locus, zero-dimensional variety, and `X = A`.

These alternatives have different domains, hypotheses, and conclusions. Choosing the intake's
provisional general finite-union wording, or replacing it by a curve corollary, would invent or
substitute mathematics. Therefore the canonical human claim fails before import minimization,
elaboration fingerprinting, checked transports, or meaningful hypothesis/domain/binder/boundary
mutations can begin. No Lean declaration, abstract interface that assumes the conclusion, axiom,
placeholder, weakened special case, or broadened target was introduced. Machine state remains
`M4`; statement acceptance and theorem completion are false.

## Pinned environment and search

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. The existing `.lake` symlink and pinned packages were read
only; no update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0467` | 0 | Rank 313, lifecycle `planned`, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for Raynaud, Manin-Mumford, the Chinese labels, and the candidate-paper title | 0 | Found only underspecified metadata, this uninspected intake citation, and unrelated SGA citations; no source-frozen proposition for this target |
| pinned-mathlib `rg` search for `Manin-Mumford` | 1 | No match (`rg` exit 1 means no match) |
| inspection of `Mathlib.AlgebraicGeometry.Group.Abelian` | 0 | The module proves commutativity of proper geometrically integral group schemes; it does not define or state the torsion-point theorem required here |

There is no applicable `lake env lean <target>.lean` validation because the exact proposition is
not fixed. Compiling a proxy proposition or a structure carrying the desired conclusion would be
fake statement evidence rather than the assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, dispose of errata, and freeze all curve/subvariety, base-field, locus, point, torsion,
translate, closure, quantifier, and degenerate-case conventions above. If the selected primary
theorem is narrower than the general finite-union formulation, a separately sourced statement and
checked mathematical transport are required rather than silent attribution. A later statement run
can then produce and minimize the exact Lean expression, fingerprint its elaboration, crosswalk it
row by row, and execute structural mutation tests.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
