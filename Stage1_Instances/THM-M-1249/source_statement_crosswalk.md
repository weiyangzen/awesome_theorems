# Source-statement crosswalk

| Metadata or candidate component | Human source anchor | Lean target | Intake assessment |
|---|---|---|---|
| `分布理论` / "distribution theory" | Laurent Schwartz, *Théorie des distributions*, Tome I (Hermann, Paris, 1950) and Tome II (1951) | none frozen | The source is a monograph developing a theory, not a single theorem matching the metadata |
| "the theory of generalized functions" | The same work supplies the historical subject and definitions | none frozen | Subject description only; it has no ordered binders, hypotheses, or conclusion |
| Distribution as a continuous linear functional on test functions | Candidate definitional core in Schwartz's framework | candidate continuous-linear-map encoding | Test-function space, topology, scalars, and ambient open set must be fixed before exact correspondence can be assessed |
| Distributional derivative | Candidate theorem family defined by transposition against derivatives of test functions | none frozen | A possible exact target, but selecting it now would broaden or substitute the metadata claim |
| Locally integrable functions induce regular distributions | Candidate representation theorem family | none frozen | A possible bounded statement after source pinpointing; no Lean closure is claimed |

The Stage0 fields give only a date (`1950`), author (`Laurent Schwartz`), and umbrella description.
They do not distinguish a definition, an existence/embedding result, differentiation closure, or a
structure theorem. Consequently there is no truthful source-to-formal proposition crosswalk yet.

The statement phase must first choose a literal proposition attested by an edition, chapter/section,
page, assumptions, and errata check. It must then record why that proposition represents the target
rather than neighboring `THM-M-1250`, freeze the exact Lean expression, and test changes to topology,
scalar field, domain, binder scope, and boundary cases. Independent source review is also required
before `H0`.

Discovery bibliographic identifiers, not immutable evidence receipts:

- Tome I: Laurent Schwartz, *Théorie des distributions*, Publications de l'Institut de
  Mathématique de l'Université de Strasbourg, no. 9, Hermann, 1950.
- Tome II: Laurent Schwartz, *Théorie des distributions*, Publications de l'Institut de
  Mathématique de l'Université de Strasbourg, no. 10, Hermann, 1951.

No `H0`, exact-statement, machine-proof, or theorem-completion claim is made.
