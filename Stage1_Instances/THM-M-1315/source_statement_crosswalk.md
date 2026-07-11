# Source-statement crosswalk

| Claim component | Primary source candidate | Lean target surface | Intake assessment |
|---|---|---|---|
| Inequality for a connected outermost minimal horizon | G. Huisken and T. Ilmanen, *The inverse mean curvature flow and the Riemannian Penrose inequality*, Journal of Differential Geometry 59 (2001), 353-437, Theorem 1.1 | asymptotically flat 3-manifold, weak inverse-mean-curvature-flow package, Hawking/ADM mass comparison | Primary theorem and pages located, but edition hash, errata, and premise-by-premise review remain open (`H1`) |
| General Riemannian Penrose inequality, including disconnected horizons | H. L. Bray, *Proof of the Riemannian Penrose inequality using the positive mass theorem*, Journal of Differential Geometry 59 (2001), 177-267, main theorem in the introduction | conformal-flow package; total boundary area; ADM mass inequality | Primary proof source located; exact theorem numbering, hypotheses, and corrections must be audited before `H0` |
| Constant and normalization | Both sources state the three-dimensional normalization equivalent to `m >= sqrt(A/(16*pi))` in geometrized units | real-valued area and ADM mass plus positivity needed for squared transports | Mathematical normalization frozen; no checked Lean transport exists |
| Equality/rigidity | Schwarzschild equality discussion/theorem in the primary papers | isometry of the exterior region to a spatial Schwarzschild exterior | Included in scope, but exact root packaging and source pinpoint remain open |
| Nonnegative scalar curvature and outermost minimal boundary | Hypotheses in the primary Riemannian statements | scalar-curvature predicate; mean-curvature/minimality; enclosure/outermost predicate | Essential hypotheses; removing any is not an allowed mutation |

Discovery identifiers (not immutable evidence receipts):

- Huisken-Ilmanen: DOI `10.4310/jdg/1090349447`.
- Bray: DOI `10.4310/jdg/1090349428`.

The generated legacy phrase "Huisken-Ilmanen/Bray's proof" identifies proof authors rather than an
exact proposition. This intake therefore freezes the standard three-dimensional, time-symmetric
Riemannian theorem and explicitly preserves the difference between the connected-horizon
Huisken-Ilmanen result and Bray's general result. The statement phase must inspect exact source
wording, decide the rigidity packaging, choose definitions for ends/decay/ADM mass/outermostness,
elaborate the complete expression, and mutation-test every indispensable hypothesis. No `H0` or
machine-closure claim is made.
