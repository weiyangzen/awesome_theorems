# Source-statement crosswalk

## Repository record and candidate sources

The repository inventory supplies the title "SLE and percolation", the year 2001, the names
Smirnov/Lawler/Schramm/Werner, and the gloss "the connection between SLE and critical percolation".
Its `\u5df2\u9a8c\u8bc1` field is explicitly untrusted under rev-5.6. It gives no theorem number,
percolation model, domain, boundary conditions, curve topology, or convergence mode, and therefore
does not identify one proposition.

A primary candidate for the percolation side is Stanislav Smirnov, *Critical percolation in the
plane: conformal invariance, Cardy's formula, scaling limits*, **Comptes Rendus de l'Academie des
Sciences - Series I Mathematics** 333 (2001), 239-244, DOI
`10.1016/S0764-4442(01)01991-7`. The title and date fit the inventory, but this intake has not
inspected an immutable edition theorem by theorem, and no exact locator, hypotheses, or errata have
been approved.

Oded Schramm's *Scaling limits of loop-erased random walks and uniform spanning trees*,
**Israel Journal of Mathematics** 118 (2000), 221-288, introduced SLE and predicted SLE6 for
percolation interfaces, but it is not by itself a proof of the selected percolation convergence
statement. Lawler, Schramm, and Werner's early SLE papers establish SLE properties and derive
critical exponents; they are likely part of the repository's broad attribution, not automatically
the primary source for the root proposition. These entries are discovery anchors only, not `H0`.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "critical percolation" | lattice, site/bond model, critical parameter, and product measure | embedded discrete graph, configuration probability space, open-site predicate | family identified; exact model open |
| "SLE" | chordal SLE normalization and parameter `kappa = 6` | Brownian driving process, Loewner chain/trace, and induced curve law | intended limit identified; encoding open |
| "connection" | convergence of an exploration-interface law, not mere analogy | weak convergence in a specified probability-measure/curve topology | intended family identified; exact theorem open |
| planar domain | simply connected domain and two marked boundary points | domain/prime-end representation and discrete approximations | regularity and approximation open |
| exploration path | boundary conditions, orientation, interpolation, and endpoint | random unparametrized curve in the selected curve space | conventions open |
| 2001 / named authors | source genealogy and disambiguation | bibliographic provenance only | Smirnov candidate found; four-author intent unresolved |

## Human and machine boundary

The repository-wide search found no Lean artifact for `THM-M-1123`; historical slot files
`S1_M_138.lean` and `S1_M_139.lean` belong to neighboring manifest entries rather than this target.
This intake does not perform the later exhaustive formal-anchor audit and makes no claim about
external Lean projects or pinned mathlib support for SLE or planar percolation scaling limits.

Before `H0`, an independent reviewer must inspect an immutable primary edition, select the exact
theorem or displayed result and pinpoint locator, map every definition and assumption, check
errata/corrections and attribution, and approve the row-by-row mapping. Before statement credit,
that selected claim must map to an elaborated Lean target without replacing interface convergence
by Cardy's formula, changing the lattice, omitting boundary/domain hypotheses, or strengthening a
stopped/local convergence result to unrestricted global convergence.
