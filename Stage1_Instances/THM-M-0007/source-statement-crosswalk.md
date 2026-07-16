# Source-statement crosswalk

Statement-phase status: blocked. This crosswalk identifies a theorem family but does not admit an
exact source-selected proposition or a canonical Lean target.

## Primary source anchor

Charles A. Weibel, *An Introduction to Homological Algebra*, Cambridge Studies in Advanced
Mathematics 38, Cambridge University Press, 1994, section 5.8, especially Theorem 5.8.3
(Grothendieck spectral sequence). This identifies the intended theorem family and the standard
acyclicity hypothesis. The exact printed definitions, page numbering for the consulted impression,
and errata still require direct inspection before `H0`; this citation is an intake anchor only.

The cited pages are not present in this clone, and no owned artifact contains an accountable
page-level transcription. The repository source record says only "composition of derived
functors." Neither source is enough to select the exact convergence, naturality, indexing, or
filtration convention without adding mathematics not supplied by an authority.

## Crosswalk

| Source component | Repository/Lean candidate | Intake disposition |
|---|---|---|
| abelian categories and enough injectives | `Category`, `Abelian`, `HasInjectiveResolutions` | typed substrate available; exact source placement of enough-injective assumptions remains open |
| left-exact additive `F`, `G` | additive functors plus `PreservesFiniteLimits` in the legacy module | candidate only; the equivalence to the selected source convention is unchecked |
| `F` sends injectives to `G`-acyclic objects | legacy `GrothendieckAcyclicity` uses vanishing `G.rightDerived n` for `n > 0` | plausible discovery encoding; exact quantifiers and the source definition of acyclic remain unaudited |
| `E_2^{p,q} = R^pG(R^qF(X))` | `Statement.lean` checks `ExpectedE2Term` | object expression only; no page construction or natural isomorphism is asserted |
| convergence to `R^{p+q}(G F)(X)` | `Statement.lean` checks `ExpectedAbutment` | target object only; no filtration, abutment, or convergence relation is asserted |
| first-quadrant cohomological carrier | pinned `E₂CohomologicalSpectralSequenceNat` | typed carrier available; it does not by itself encode the required page identification or convergence |
| spectral-sequence naturality and convergence | legacy boundary uses an arbitrary `Type` and two bare `Prop` fields | excluded proxy; a typed, source-matched interface is required |

The legacy external anchor names in `S1_M_094.lean` point to Joel Riou's derived-categories work at
recorded revisions, but dependency compatibility and terminal proof provenance belong to the later
anchor-audit node. They receive no intake proof credit.

## Unresolved exact-statement decisions

- objectwise construction versus a natural spectral sequence of functors;
- weak, strong, or another source-defined convergence notion;
- the associated filtration, its exhaustiveness/separatedness, and boundedness conditions;
- homological/cohomological page orientation and differential bidegrees;
- the exact universes, category assumptions, left-exactness encoding, and placement of injective
  resolution instances;
- the source definition and quantifier order of the `G`-acyclicity hypothesis;
- the source treatment of zero objects, degree-zero edges, collapse, and other degenerate cases.

Because those choices can change the proposition, there is no truthful checked alternate transport
or source-directed mutation suite yet. `Statement.lean` is a negative boundary probe, not the
canonical declaration required by the statement acceptance contract.

Before source fidelity can reach `H0`, a reviewer must consult the stable primary text, transcribe
all hypotheses and the exact convergence conclusion, map its notation definition-by-definition,
check relevant errata, and independently approve the crosswalk.
