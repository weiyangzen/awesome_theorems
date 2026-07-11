# Source-statement crosswalk

The repository source record says `Dirichlet问题的上解-下解法` ("the
upper-solution/lower-solution method for the Dirichlet problem"). The crosswalk
below records the historical target while refusing to turn a method name into
an exact modern proposition.

| Claim component | Human source anchor | Lean target at intake | Assessment |
|---|---|---|---|
| Perron's treatment of the first boundary-value problem for harmonic functions | O. Perron, *Eine neue Behandlung der ersten Randwertaufgabe fur \(\Delta u=0\)*, Mathematische Zeitschrift 18 (1923), 42-54, DOI `10.1007/BF01192395` | None selected | Primary historical paper identified; exact theorem/page, edition image, premises, and errata still require direct audit |
| Upper and lower classes | Functions satisfying an interior super/subharmonic condition and a boundary inequality | Unselected definitions | The repository phrase does not specify semicontinuity, liminf/limsup, or sign/order conventions |
| Perron envelope | Infimum of the upper class or supremum of the lower class | Unselected expression | Finiteness and harmonicity require explicit assumptions and supporting lemmas |
| Interior harmonicity | Harmonic replacement and compact/local convergence yield a harmonic envelope | Future `PER-LIFT` and `PER-HARM` nodes | This is a central proof boundary, not a definitional consequence |
| Boundary values | Barriers give convergence to the datum at regular boundary points | Future `PER-BDY` node | A general domain can have irregular boundary points; full continuous boundary attainment cannot be inserted without regularity hypotheses |
| Complete Dirichlet solution | Envelope harmonicity plus boundary attainment and uniqueness | Future `PER-ROOT` and `PER-UNIQ` nodes | Whether this stronger result is the intended root remains unresolved |

The title's `Delta u = 0` supports the classical Laplace reading, but the
repository metadata alone does not fix dimension, boundedness, boundary-data
class, or regularity. Nor does it distinguish the historical harmonic Perron
method from later Perron variants for general elliptic equations or ODEs. The
statement phase must make that selection from an inspected source and must not
broaden the theorem by genealogy.

Discovery locator, not an immutable evidence receipt:

- Springer/DOI record: <https://doi.org/10.1007/BF01192395>

No `H0` claim is made. `H1` records a primary proof source locator while exact
statement/premise mapping, source hashing, translation checks, errata review,
and independent review remain outstanding.
