# THM-M-0750 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:5528-5533` contains the complete source record:

- title: `图灵度` (Turing degrees);
- catalog attribution: Emil Post;
- time: 1944;
- statement gloss: `不可解度的结构` (the structure of degrees of unsolvability);
- importance: high; and
- formalization status: `已验证` (verified).

All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no citation, definition, formula,
theorem locator, quantifiers, hypotheses, conclusion, proof, formal declaration, or validation
link. `Docs/Stage0_Blueprint.md:20488-20513` repeats the gloss while explicitly leaving exact
definitions and premises, proof route, dependencies, equivalent forms, axioms, machine status, and
artifact links open. Rev-5.6 therefore preserves `已验证` only as untrusted metadata.

## Literal crosswalk

| Repository phrase | What it establishes | Missing exact-statement component | Intake result |
|---|---|---|---|
| `图灵度` | a standard recursion-theory object/family | one named truth-valued proposition | open |
| `不可解度` | intended comparison of computational unsolvability | oracle objects, computation model, reducibility relation | open |
| `结构` | some property of the resulting degrees | exact order, least element, join, density, incomparability, or other conclusion | open |
| Emil Post / 1944 | a historical and bibliographic lead | inspected passage, attribution audit, definitions, proof and errata | open |
| `已验证` | catalog inventory status only | source fidelity, exact Lean identity, kernel and trust evidence | explicitly untrusted |

There is no repository-source clause to map to an ordered binder, hypothesis, or conclusion. The canonical
human claim and Lean expression therefore remain null rather than silently choosing a convenient
structural fact.

## Inspected primary-source boundary

The author and year match Emil L. Post, "Recursively enumerable sets of positive integers and their
decision problems", *Bulletin of the American Mathematical Society* 50(5) (1944), 284-316, DOI
`10.1090/S0002-9904-1944-08111-1`. Crossref confirmed the bibliographic fields. An AMS publisher
version-of-record PDF was retrieved from the stable but non-content-addressed URL
`https://www.ams.org/journals/bull/1944-50-05/S0002-9904-1944-08111-1/S0002-9904-1944-08111-1.pdf`.
The observed 33-page, 3,959,828-byte PDF has SHA-256
`b2f200e8035696dd82903a2dabc6a179641ae3fe4ad97155508a2777523d0c1d`; extracted text has SHA-256
`3e782de4473b362fb296fb386aaff0f40b8abdcbecd7a3497f4243c877ebbad0`. These hashes bind this
inspection but do not make the mutable publisher URL an immutable dependency.

The paper gives several relevant but nonidentical statement surfaces:

- Printed pages 289-290 define degree terminology through mutual, one-way, and absent reducibility,
  then make determining degrees for unsolvable decision problems of recursively enumerable sets a
  primary problem. Post says Turing's formulation makes the lower-degree problem precise and that
  it remains a problem at the end of the paper.
- Printed page 297 proves that every recursively enumerable set's decision problem is one-one
  reducible to the complete set `K`, yielding a highest degree for that reduction. The subsequent
  general-reducibility extension is explicitly described as still informal.
- Section 11, printed pages 311-312, describes general or Turing reducibility by a terminating
  yes/no decision process whose later oracle questions may depend on earlier answers. It explicitly
  calls the discussion informal and says "We shall talk as if our intuitive discussion has already
  been formalized."
- Printed page 314 leaves open whether a recursively enumerable set has absolutely lower degree
  than `K` or all unsolvable such decision problems have the same degree.

This primary inspection supports the `H5` target decision: the catalog's generic structure gloss
does not choose the definition, highest-degree theorem, open lower-degree question, or another
special theorem in the paper. It supplies useful source components, but not a single proposition,
complete premise/proof crosswalk, errata review, or independent target approval sufficient for
`H0`. Ordinary proof phases remain blocked until the integration lane authorizes a corrected
truth-valued target or redirection.

## Neighbor crosswalk

| Neighbor | Separate repository scope | Boundary for THM-M-0750 |
|---|---|---|
| `THM-M-0748` | Post's problem | no transfer of an intermediate-degree question or solution |
| `THM-M-0749` | Friedberg-Muchnik theorem | no transfer of incomparable c.e.-degree existence |
| `THM-M-0751` | supremum / lattice structure of Turing degrees | join or upper-bound result requires an explicit ownership decision |
| `THM-M-0752` | jump operator | jump definitions and theorems are not this unspecified root |
| `THM-M-0758` | computably enumerable degrees | restriction to c.e. degrees is not implicit |
| `THM-C-0011` | Turing reducibility, outside Stage1 | definition overlap is ambiguity evidence, not proof credit |

## Pinned Lean candidates

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Computability.TuringDegree` contains:

| Declaration | Pinned meaning | Intake status |
|---|---|---|
| `RecursiveIn` | oracle partial-recursiveness for a set of partial-function oracles | supporting interface only |
| `TuringReducible` | `RecursiveIn {g} f` for partial functions `f g : Nat ->. Nat` | candidate encoding; requires a checked bridge from Post's set/decision-problem yes/no model |
| `TuringEquivalent` | mutual `TuringReducible` via `AntisymmRel` | candidate equivalence encoding |
| `TuringEquivalent.equivalence` | equivalence relation for that encoding | candidate structural theorem |
| `TuringDegree` | `Antisymmetrization _ TuringReducible` | candidate degree carrier |
| `TuringDegree.instPartialOrder` | induced partial order on that carrier | candidate structural result |

The module cites Piergiorgio Odifreddi, *Classical Recursion Theory*, Vol. I (1989), a useful
secondary-source lead but not a source crosswalk for the catalog's Post/1944 claim. The probe
elaborates the exact names under the pinned toolchain. It does not establish which declaration or
bundle is the source statement, a checked transport from set-based degrees, a terminal proof-body
audit, or an exhaustive anchor search.

## Gate result

Human status is provisionally `H5` because the received catalog wording is not one stable
proposition. Machine status is `M4` because no formal artifact can match an exact root that has not
been selected. Readability status is `R4` because this boundary record is not a proof
reconstruction. Retry requires independent source and target review, an integration-authorized
truth-valued correction or redirection, and explicit resolution of every proposition-changing row
before Lean statement freeze.
