# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `小波多分辨率分析`, attributes it to
Stéphane Mallat and Yves Meyer, dates it to 1986, and gives only `小波的多分辨率框架` ("the
multiresolution framework of wavelets"). Stage0 repeats this metadata. The rev-5.6 manifest keeps
`已验证` only as `source_status_untrusted`. There is no definition, theorem wording, source title,
edition, page, assumptions, conclusion, proof boundary, or formal artifact.

## Candidate source work

Stéphane G. Mallat's 1989 paper *A Theory for Multiresolution Signal Decomposition: The Wavelet
Representation* and Yves Meyer's wavelet work are plausible locators, but the repository's 1986
date and joint attribution do not uniquely select a passage. Neither candidate has been accepted
or independently reviewed here. The statement/source phases must identify an immutable source,
record exact theorem/page and errata, and distinguish definition, characterization, construction,
and basis consequences. These bibliographic leads provide no `H0` credit.

## Crosswalk

| Repository/source phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "multiresolution" | nested closed subspaces indexed by integers | `Int -> ClosedSubmodule` plus monotonicity | family identified; orientation open |
| "analysis" | dense union and trivial intersection | closure/supremum and infimum equations | candidate MRA axioms only |
| scale covariance | dyadic dilation maps one level to the next | measure-preserving/nonsingular domain action with normalization | convention and API open |
| translation covariance | integer translations preserve `V_0` | translation operator on `Lp` and invariant subspace | exact action open |
| scaling function | translates span or base `V_0` | an `OrthonormalBasis` or Riesz-basis interface | assumption versus conclusion open |
| wavelet conclusion | detail spaces and dyadic wavelet basis of `L^2` | orthogonal complements, direct sums, complete basis | not selected by metadata |
| `已验证` | untrusted inventory label | no proposition or proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe
checks `MeasureTheory.Lp`, composition by a measure-preserving map, `ClosedSubmodule`, orthogonal
complement, and `OrthonormalBasis`. A bounded name/path search found Fourier and general Hilbert/Lp
infrastructure but no wavelet- or MRA-named mathlib file. This is not the later immutable anchor
audit and says nothing about external Lean projects or exact closure.
