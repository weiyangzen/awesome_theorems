# Source-statement crosswalk

## Candidate primary source

J. Q. Zhong and H. C. Yang, "On the estimate of the first eigenvalue of a compact Riemannian
manifold", *Scientia Sinica, Series A* 27 (1984), commonly cited at pages 1265-1273. This
bibliographic record is a discovery anchor only: a stable scan, the exact theorem/page, hypotheses,
normalizations, and errata have not been independently inspected, so it is not `H0` evidence.

The repo-local source `Docs/researches/math_theorems.md` supplies only the Chinese phrase "lower
bound for the first eigenvalue of a convex domain", authors, year, and an untrusted "verified"
label. It supplies neither a proof nor a formal artifact and earns no proof credit.

## Crosswalk

| Repository/source phrase | Candidate mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Zhong-Yang estimate" | sharp spectral-gap estimate | exact theorem declaration | identity plausible; source inspection open |
| "compact Riemannian manifold" | compact connected boundaryless `M` | Riemannian manifold and compactness instances | candidate only |
| nonnegative Ricci curvature | pointwise tensor lower bound | concrete Ricci API and order encoding | absent from repository phrase |
| first eigenvalue | first positive Laplace-Beltrami eigenvalue | operator, spectrum, indexing and sign convention | normalization open |
| diameter | metric diameter `d` | concrete finite diameter term | degeneracies open |
| lower bound | `lambda1 >= pi^2 / d^2` | typed real-valued inequality | constant/source wording open |
| "convex domain" | possibly a different Neumann spectral theorem | Euclidean domain, convexity, boundary conditions | attribution conflict; excluded pending resolution |

Before `H0`, an independent reviewer must inspect the primary paper and any errata, verify the exact
theorem and page, and approve every hypothesis and normalization. Before statement acceptance, the
chosen source claim must be mapped binder-by-binder to Lean without conflating it with the convex
domain theorem.
