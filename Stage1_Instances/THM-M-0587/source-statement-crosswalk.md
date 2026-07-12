# Source-statement crosswalk

## Available repository source

The source record is `Docs/researches/math_theorems.md`, lines 4352-4357: title, attribution,
year, and the phrase "h-cobordism and diffeomorphism." It gives no bibliographic citation,
dimension convention, definition of h-cobordism, boundary hypotheses, or relative conclusion.
`Docs/Stage0_Blueprint.md` adds no mathematical specificity. These files identify the intended
family but do not establish source fidelity or human-proof status.

## Candidate primary sources

- Stephen Smale, "Generalized Poincare's Conjecture in Dimensions Greater Than Four,"
  *Annals of Mathematics*, second series, 74 (1961), 391-406.
- Stephen Smale, "On the Structure of Manifolds," *American Journal of Mathematics* 84 (1962),
  387-399.

These are bibliographic discovery candidates, not `H0` evidence. This intake did not inspect and
hash a stable scan, select an exact theorem and page, reconcile the two papers' conventions, or
check errata. The year in the repository does not by itself select the second paper or a unique
formulation.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "h-cobordism" | compact smooth cobordism with both boundary inclusions homotopy equivalences | manifold-with-boundary/corners data, boundary decomposition, inclusions, and homotopy-equivalence witnesses | family identified; definitions open |
| "Smale" / 1962 | high-dimensional simply connected smooth theorem | source-pinned dimension and simple-connectivity hypotheses | candidate sources only |
| "diffeomorphism" | trivial product cobordism, not merely diffeomorphic boundary components | diffeomorphism `W ~= M₀ x I` with explicit boundary compatibility | relative convention open |
| high-dimensional range | commonly `dim W >= 6`, or boundary dimension `>= 5` | one fixed natural-number dimension convention and inequality | not frozen |
| `已验证` | inventory metadata | no kernel or human-source evidence | no proof credit |

## Source and machine boundary

No theorem-specific Lean artifact for `THM-M-0587` exists in the repository. Intake does not claim
that pinned mathlib lacks all needed manifold, homotopy, Morse-theory, or handle-decomposition
infrastructure; that determination belongs to the dependency-ordered anchor audit after an exact
statement exists.

Before `H0`, an independent reviewer must approve a fixed source, theorem/page, every hypothesis,
the dimension translation, the exact relative conclusion, and an errata record. Before statement
credit, that approved row-level crosswalk must map to an elaborated Lean expression, with checked
transports for any alternative simple-connectivity, interval, boundary, or dimension encoding.
