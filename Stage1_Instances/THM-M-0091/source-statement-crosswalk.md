# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:670-675` supplies exactly the title `外尔维数公式`, Hermann Weyl
attribution, year 1925, gloss `紧李群不可约表示的维数` ("dimensions of irreducible representations
of compact Lie groups"), importance high, and formalization status `已验证`. All six uncited fields
originate in repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:2605-2630` repeats the gloss while leaving exact definitions and premises,
proof route, dependencies, equivalent forms, axioms, formal system, machine status, and artifact
links open. The rev-5.6 manifest retains `已验证` only as untrusted metadata and resets this target
to `L0 / rework_required`.

Neither repository record provides a bibliography, edition, theorem or formula number, page,
formula, definition chain, ordered binders, proof boundary, translation or correction history, or
reviewer. The catalog is evidence of the requested family, not `H0` source evidence.

## Historical source lead

A bounded Crossref query on 2026-07-13 authenticated this bibliographic record:

- H. Weyl, *Theorie der Darstellung kontinuierlicher halb-einfacher Gruppen durch lineare
  Transformationen. I*, *Mathematische Zeitschrift* 23(1), 1925, pages 271-309,
  DOI `10.1007/BF01506234`.

The year, author, and subject match the catalog's historical lead. Crossref also identifies parts
II and III from 1926 and a corrigendum to part III, which makes article- and correction-level source
selection material. The part-I content link returned an access-page HTML document rather than a
lawful article transcription during intake. No exact formula passage, page within the paper,
definitions, assumptions, proof boundary, relationship to the modern compact-group statement,
translation, or applicable erratum was inspected or independently reviewed. The record therefore
remains a non-credited source lead and supports `H1`, not `H0`.

## Clause crosswalk

| Repository phrase | Material interpretations | Pinned Lean surface | Intake status |
|---|---|---|---|
| "compact Lie group" | compact connected semisimple, compact connected reductive, or possibly disconnected compact group | `LieGroup`, topological group APIs | connectedness and reduction to root data are absent |
| "irreducible representation" | finite-dimensional continuous complex group representation, unitary representation, or corresponding Lie-algebra highest-weight module | `Representation`, `FDRep`, irreducibility APIs | algebraic representation substrate exists; continuity and correspondence are not joined |
| "dimension" | natural vector-space dimension, `Module.finrank`, character value at the identity, or an integer/rational product | `FDRep.char_one`, `Representation.char_one` | character-at-one bridge exists only in generic algebraic representation theory |
| "Weyl dimension formula" | product over positive roots involving a dominant highest weight and Weyl vector | `RootPairing.Base.IsPos`, Lie weights, coroot and pairing APIs | no formula declaration or representation-to-root-data bridge found |
| roots and positivity | maximal-torus root system plus a positive system/base | `RootPairing`, `RootPairing.Base`, `RootPairing.Base.IsPos` | abstract and Lie-algebra root substrate only |
| highest weight and `rho` | dominant integral highest weight and half-sum of positive roots | `LieModule.Weight`; abstract sums and pairings | no direct highest-weight representation package or Weyl-vector formula found |
| `已验证` | untrusted inventory label | no expression or receipt | explicitly rejected as evidence |

## Pinned formal leads

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe authenticates
the following adjacent APIs:

1. `RootPairing`, `RootPairing.Base`, `RootPairing.Base.IsPos`, and
   `RootPairing.Base.isPos_of_mem_support` from the root-system library.
2. `LieModule.Weight`, `LieAlgebra.IsKilling.rootSystem`, and
   `LieAlgebra.IsKilling.apply_coroot_eq_cast` from the finite-dimensional semisimple Lie-algebra
   weight library.
3. `Representation`, `FDRep`, `FDRep.char_one`, and `Representation.char_one` from algebraic
   representation theory.
4. `LieGroup` from the manifold Lie-group interface.

These interfaces do not state the Weyl dimension formula. A bounded case-insensitive search for
`weyl` near `dimension` in repo-local Lean and pinned mathlib found no relevant declaration, and
source inspection found no single bridge combining compact connected Lie groups, continuous
irreducible representations, dominant highest weights, positive roots/coroots, and the product.
The probe elaborates only the named APIs and prints axiom reports for selected theorem interfaces.
This justifies the provisional `M3` interface-debt classification; it is not a downstream exhaustive
anchor/provenance audit, a statement fingerprint, or proof-body credit.

## Neighbor and non-substitution boundary

The adjacent catalog targets `THM-M-0090` (Weyl character formula) and `THM-M-0093` (highest-weight
theorem) do not share status or proof credit. Character-at-identity and root-system infrastructure
remain ingredients, not the requested product formula. No abstract root identity, special family,
or disconnected-group classification may silently replace the source-selected compact-group claim.

## First source/statement gate

An independent review must preserve a lawful authoritative source and select one exact proposition,
including the group and representation categories, torus/root choices, highest-weight and Weyl-
vector conventions, pairing and coroot normalization, product codomain, nonzero denominators,
boundary cases, and the route from the historical semisimple formulation to any modern compact-
group formulation. Only then may the statement phase freeze, elaborate, transport, fingerprint, and
mutation-test an exact Lean target.
