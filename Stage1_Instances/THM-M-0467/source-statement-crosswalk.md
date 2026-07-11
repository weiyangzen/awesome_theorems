# Source-statement crosswalk

## Primary source anchor

Michel Raynaud, "Courbes sur une variété abélienne et points de torsion," *Inventiones
mathematicae* **71** (1983), 207-233, is the historical primary-source candidate. Bibliographic
identity is recorded for discovery only: the exact theorem number/page, original formulation,
assumptions, and errata have not yet been inspected and therefore this is not `H0` evidence.

The repository's Stage0 record calls the item "Raynaud's theorem" and describes it as "proof of the
Manin-Mumford conjecture." That metadata disambiguates the theorem family but is an untrusted
secondary label, not a statement source.

## Crosswalk

| Repository/intake phrase | Mathematical object | Required Lean object | Intake status |
|---|---|---|---|
| abelian variety | proper smooth connected group variety `A` | concrete abelian-variety structure over `k` | included; API audit open |
| closed subvariety `X` | closed algebraic locus in `A` | closed subscheme/subvariety and inclusion | included; encoding open |
| torsion points on `X` | finite-order points of `A` lying in `X` | point group, finite-order predicate, membership | included; base points open |
| Zariski closure | smallest closed locus containing those points | concrete topological/schematic closure | included; convention open |
| finite union | finitely many irreducible/coset pieces | finite index type and equality of loci | included; exact equality open |
| torsion translates | `a + B`, with torsion `a` and abelian subvariety `B` | subgroup variety, translation, containment | included; formal interfaces open |

## Fidelity work still required

The statement phase must inspect a stable copy of the paper and crosswalk its theorem verbatim,
including the source's base field, curve/general-subvariety scope, density-versus-decomposition
form, and reduction steps. It must locate and assess errata and independently review every
assumption. If the paper's headline theorem is only the curve formulation, the dossier must not
attribute the later general finite-union wording directly to it without a separate primary source
and a checked mathematical transport.
