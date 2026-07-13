# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10686` through `:10691` supplies exactly the title
`间断Galerkin方法`, attribution to W. H. Reed and T. R. Hill, year 1973, gloss
`允许间断的有限元`, importance `high`, and status `已验证`. All six uncited lines originate at
repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no PDE,
domain, mesh, function space, trace, numerical flux, ordered binder, hypothesis, conclusion, proof,
correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:39811` through `:39837` repeats the gloss while explicitly leaving exact
definitions and premises, proof route, dependencies, alternate forms, axioms, machine status, and
artifact links open. Its generic closed-result and leaf-audit language is planning metadata, not
source evidence. Rev-5.6 retains `已验证` only as untrusted metadata and resets this target to
`L0 / rework_required`.

## Inspected primary source

The attribution and year identify Wm. H. Reed and T. R. Hill, *Triangular Mesh Methods for the
Neutron Transport Equation*, University of California, Los Alamos Scientific Laboratory,
LA-UR-73-479 / CONF-730414--2 (October 1973), OSTI 4491151. The OSTI API records it as a conference
work published 1973-10-31 under contract W-7405-ENG-36. Stable locators are
`https://www.osti.gov/biblio/4491151` and `https://www.osti.gov/servlets/purl/4491151`.

The complete 23-leaf PDF was retrieved and inspected on 2026-07-13. It is 591,992 bytes at SHA-256
`ec04436524f01ad10647398d8d8c81cd21f2b15a69cbcb5d3e9f1f70c22c2d89`.
The OSTI JSON response was 902 bytes at SHA-256
`841f59fe6c37395b5faa228492ab364c72ee9a1925374a75eaf5d65596099319`.
These hashes authenticate the observed external bytes; the files are not vendored, an independent
source review has not occurred, and the integration lane must reacquire or archive them before
admitting source evidence.

## Pinpoint source crosswalk

| PDF locus | Source content | Intake mapping |
|---|---|---|
| leaf 2, abstract | Piecewise-polynomial angular flux on a triangular x-y grid; first class continuous, second discontinuous; accuracy and stability illustrated numerically | method family and empirical-evidence boundary, not one theorem |
| leaves 3-5, introduction | Finite-dimensional transport schemes; only explicit methods and, in the paper's analysis, regular triangular meshes with characteristic-directed sweeps | excludes generic implicit Galerkin and generic PDE substitutions |
| leaf 5, Eq. (1) | One-velocity neutron transport in x-y geometry, with scattering, fission, and inhomogeneous terms bundled into the source | continuous model and omitted source-generation dependencies |
| leaf 6, Eq. (2) | Standard discrete-ordinates equations `mu_m * d_x psi_m + eta_m * d_y psi_m + sigma * psi_m = S_m`; incoming single-cell boundary flux is assumed known | angular model, direction binders, coefficients, and upwind boundary data |
| leaf 6, Eq. (3) | Each cell flux is a total-degree polynomial of degree at most `N` | broken trial-space premise |
| leaf 7, continuity paragraph | The second method imposes no interface continuity; the boundary value is the limit in the streaming direction and the jump is on the other side | precise discontinuity/upwind-trace rule |
| leaves 7-8, Eq. (4) | `K = (N+1)(N+2)/2` properly placed points define a Lagrange basis; `N+1` points lie on each face | local degrees of freedom and an explicit unisolvence premise |
| leaves 8-10, Eq. (5) | Continuous comparator uses incoming-face data and weighted residual equations; proper weights give a stated nonsingular local system | comparator only; nonsingularity is qualified, not a general DG theorem |
| leaf 10, stability disclaimer | Weights can make the method unstable; the authors state they have no theoretical result and only report no observed instability for two continuous choices | hard boundary against a source-proved stability claim |
| leaves 10-11, discontinuous method | Boundary points split by cell; the jump creates an incoming-face Dirac term; `K` polynomial tests yield a `K` by `K` cell system; any basis spanning the polynomial test space gives the same result | construction-level Reed-Hill candidate, still missing an exact theorem conclusion |
| leaf 11, disclaimer and Section III | Non-polynomial weights were not investigated; stability with polynomial weights is found experimentally; tests use one-group isotropic scattering and S2 angular quadrature | stability is empirical and parameter-limited |
| leaves 11-12, Table II | Pure absorber square with uniform isotropic source and vacuum boundary; 200/800 triangles and degrees 1-4 compared to the exact S2 equations | reproducible benchmark candidate only after data/code/numerical semantics are frozen |
| leaf 13, accuracy observation | Halving mesh spacing in the table suggests second-order integral quantities and first-order point values | observation for one refinement test, not a quantified convergence theorem |
| leaves 13-23 | Further test problems motivate relative stability and rebalance claims with language such as "we believe", "we find", and "designed to test this hypothesis" | numerical comparison, not theorem/proof evidence |

The inspected primary source is strong historical and scope evidence, but not `H0` for a canonical
root because the catalog has not selected one proposition and the source itself presents multiple
construction and experimental claims. No theorem/formula has been independently crosswalked and
reviewed as the root.

## Literal statement crosswalk

| Repository phrase | Source-family component | Prospective Lean component | Result |
|---|---|---|---|
| discontinuous Galerkin method | explicit cellwise weighted-residual family in the 1973 source, or a much broader modern DG family | PDE model, mesh, broken trial/test spaces, traces, jumps, numerical flux, local/global scheme | family identified; variant absent |
| finite elements allowing discontinuities | independent cell polynomials and streaming-direction trace in Reed-Hill | cell-indexed functions and face data without global continuity | too broad to fix a proposition |
| Reed/Hill, 1973 | historical locator | provenance only | primary source inspected, but no canonical root selected |
| verified | catalog screening label | accepted source and kernel receipts | no H or M credit |

The literal record cannot populate a canonical domain, ordered quantifiers, hypotheses, conclusion,
alternate encodings, excluded cases, or formal expression fingerprint.

## Pinned Lean crosswalk

| Candidate | What is checked | Why it is not the target |
|---|---|---|
| `Affine.Simplex`, `Affine.Triangle`, `Affine.Simplex.faceOpposite` | finite affine-simplex geometry and faces | no mesh complex, broken polynomial space, trace, or transport sweep |
| `MeasureTheory.integral_piecewise` | integral of a measurable piecewise function splits across a set and its complement | generic measure identity, not element/face integration or jump residual |
| `IsCoercive.continuousLinearEquivOfBilin` and application/uniqueness theorems | abstract well-posedness for coercive real bilinear forms | no DG form, coercivity proof, transport operator, discretization, or error estimate |

`IntakeProbe.lean` checks these declarations at the pinned revision. A bounded search found no
source-selected terminal DG theorem. The probe is discovery evidence only, not a formal target,
proof body, exhaustive anchor audit, or absence proof.

## Source gate

The first downstream gate requires an accountable correction that selects a preserved source
edition and one truth-valued result; maps every PDE, coefficient, domain, mesh, discrete-space,
trace, jump, flux, boundary, stability/regularity, norm, rate, constant, computation, and degenerate
case; distinguishes analytic proof from experiment; audits corrections; and receives independent
numerical-analysis and source review. Only then may the statement phase freeze the Lean expression,
minimal imports, checked transports, and required mutations.

Until then, `H5` describes the catalog target's ill-posed proposition status, `M4` records the lack
of a source-identical usable formal artifact, and `R4` records the lack of an anchorable proof
reconstruction. These classifications do not say that established DG results are false or open.
