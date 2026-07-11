# Scope map

## Included claim family

- A concrete second-order uniformly elliptic linear operator on a domain in finite-dimensional
  Euclidean space, with coefficient regularity fixed by the selected source.
- A weak or strong solution of the corresponding equation with source in `L^p`.
- Membership of the solution in `W^{2,p}` and an a priori estimate controlling its second weak
  derivatives (and any lower-order term required by the source).
- The exact range of `p`, locality/globality, and homogeneous or nonhomogeneous boundary data from
  the chosen primary theorem.

## Decisions required in the statement phase

Select one primary theorem before choosing binders. Freeze divergence versus nondivergence form,
scalar versus systems, coefficient symmetry and regularity, ellipticity constants, domain geometry,
interior versus boundary estimate, solution notion, boundary/trace data, measure and norm
conventions, `p` range, dimension, lower-order coefficients, and uniqueness assumptions. Record
degenerate cases such as empty domains and zero source rather than silently excluding them.

## Explicit exclusions

- Replacing the result by first-order Sobolev embedding or a Gagliardo-Nirenberg inequality.
- An `H^2 = W^{2,2}` estimate when the selected claim requires arbitrary `p`.
- Schauder, De Giorgi-Nash-Moser, or parabolic regularity as a substitute.
- Classical `fderiv` membership without a checked bridge to weak derivatives and Sobolev space.
- A structure that contains the desired `W^{2,p}` conclusion or estimate as an input field.

The later target must use concrete operator, weak-solution, Sobolev, domain, and boundary APIs, or
record an exact elaboration blocker. The legacy abstract propositions are not eligible hypotheses.
