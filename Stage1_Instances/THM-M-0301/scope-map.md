# Scope map

## Included source claim

- The theorem is the classical real-variable duality on Euclidean space, not holomorphic Hardy
  space duality and not an abstract Banach-space naming convention.
- `BMO(R^n)` consists of locally integrable functions whose average absolute oscillation is
  uniformly bounded over cubes. Functions differing by a constant represent the same BMO element.
- `H^1(R^n)` is the real Hardy space described in the inspected announcement as the `L^1`
  functions whose Riesz transforms are all in `L^1`.
- The source's phrase "BMO is the dual" includes both directions: a BMO class supplies a bounded
  functional on `H^1`, and every continuous functional on `H^1` is represented by a BMO class.
- The pairing is integration over `R^n`, first on the stated dense subspace of smooth rapidly
  decreasing `H^1` functions and then, in a complete formulation, by continuous extension.
- Uniqueness is modulo constants. An isometric identification is not asserted at intake; the exact
  norm comparison must follow the selected complete source and normalization.

## Binder and definition decisions still open

The statement phase must bind, in source-faithful order:

1. The dimension parameter and whether the theorem explicitly assumes `n >= 1`.
2. Real or complex scalar-valued functions and the corresponding bilinear or sesquilinear pairing.
3. Lebesgue measure and the representation of `R^n` (for example, `Fin n -> Real`).
4. Locally integrable and `L^1` functions modulo almost-everywhere equality.
5. Cubes, their admissibility, average convention, and the BMO seminorm and quotient norm.
6. The kernel of the seminorm and the proof that it is exactly the almost-everywhere constants.
7. The normalized Euclidean Riesz transforms and the precise `H^1` norm/completion model.
8. The dense smooth rapidly decreasing subspace on which the integral pairing is initially defined.
9. The integrability, boundedness, and unique extension of that pairing.
10. The representation, uniqueness-modulo-constants, and two-sided norm estimates encoded by
    "is the dual."

No ordered Lean binder list is frozen at intake because these choices change the proposition.

## Boundary and degenerate cases

- Dimension zero versus the source's implicit positive-dimensional Euclidean setting.
- The zero functional and constant BMO representatives.
- Equality of functions versus almost-everywhere equality.
- Pairings that are not initially integrable for arbitrary representatives.
- Cube conventions, null or degenerate cubes, and normalization of averages.
- Real versus complex duals and conjugation order.
- Functions with undefined or non-`L^1` Riesz transforms.
- Seminormed BMO before quotienting versus the resulting normed quotient.

No case is silently excluded. Each must be incorporated or rejected by the exact source-mapped
statement and later mutation tests.

## Prohibited substitutions

- Abstract types named `H1` and `BMO` together with an assumed equivalence or duality field.
- The tautology that a type is the dual of a type defined to be its continuous dual.
- Only the BMO-to-functional direction, or only the functional-representation direction.
- Equality of raw BMO functions instead of uniqueness modulo almost-everywhere constants.
- The John-Nirenberg inequality, atomic decomposition, Fefferman-Stein `H^p` characterizations,
  martingale BMO, a bounded-domain variant, or holomorphic Hardy/BMO duality.
- A one-dimensional or finite-dimensional toy model offered as the Euclidean theorem.
- Generic quotient, integration, Hahn-Banach, Schwartz-space, or continuous-dual APIs by themselves.
- The `THM-M-0363` dossier, receipt, or future proof imported without an accepted duplicate-identity
  and exact-statement transport decision.
- The catalog's `verified` label, a source citation, or the API probe as proof credit.

## Neighbor and duplicate boundary

`THM-M-0363` is separately scheduled at rank 681 under harmonic analysis with the gloss "BMO is
the dual space of H^1." Its attribution, year, intended mathematical content, and current planned
scope match this target. It is therefore a probable catalog duplicate, not a dependency or an
alternate proof obligation. Until the integration lane resolves identity and ownership, both IDs
remain independent L0 instances and no evidence or acceptance crosses between them.
