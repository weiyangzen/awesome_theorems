# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:663-668`, introduced by repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`, contains the entire source record:

- title: `外尔特征标公式`;
- proposer: Hermann Weyl;
- date: 1925;
- statement: `李群表示的特征标公式`;
- importance: high;
- source status: `已验证`.

`Docs/Stage0_Blueprint.md:2578-2603` projects the same metadata and explicitly leaves the exact
definitions, hypotheses, proof route, dependencies, equivalent forms, logical foundation, axioms,
machine state, and artifact links unresolved. The rev-5.6 manifest carries `已验证` only as
`source_status_untrusted`. These records are secondary inventory evidence, not an `H0` source
crosswalk.

## Inspected modern source lead

Pavel Etingof, *18.755 S24 Full Lecture Notes: Lie Groups and Lie Algebras I & II*, MIT
OpenCourseWare, 2024, Section 26 (PDF pages 138-142), was inspected at
`https://ocw.mit.edu/courses/18-755-lie-groups-and-lie-algebras-ii-spring-2024/mit18_755_s24_lec_full.pdf`
on 2026-07-13. The observed PDF SHA-256 was
`9604129911b24dc6602a263e066992df378bded27a5b30a93467ad4f2ef5b8d4`.

Section 26.1 starts with a finite-dimensional representation of a semisimple complex Lie algebra,
relates it to the corresponding simply connected complex Lie group, and defines its character from
weight-space dimensions as an element of the integral group algebra of the weight lattice. Section
26.2 defines the Weyl denominator. Theorem 26.4 states, for every dominant integral weight
`lambda`, the Weyl character formula for the irreducible finite-dimensional representation
`L_lambda`. Section 26.4 supplies a proof; Corollary 26.5 separately derives the Weyl denominator
formula.

This is an authoritative modern proof lead and supports provisional `H1`. It does not establish
`H0`: the repository does not cite it, the exact definition chain and premise mapping have not been
preserved and independently reviewed, corrections have not been audited, and its semisimple
Lie-algebra/formal-character statement has not been shown to be the catalog's intended Lie-group
statement.

## Source-to-target gaps

| Source/catalog component | Mathematical information | Required Lean consequence | Intake result |
|---|---|---|---|
| catalog title and gloss | names a classical formula family | exact proposition identity | recognizable but not binder-complete |
| Etingof Section 26.1 | semisimple complex Lie algebra, simply connected group, weights and formal character | coefficient field, Lie algebra, module, Cartan/weight decomposition, group-algebra encoding | source lead; no checked transport |
| Etingof Section 26.2 | positive roots, Weyl group action, sign, `rho`, Weyl denominator | root datum/base, finite alternating sums, exponential/group-ring notation and denominator | definitions not frozen in this instance |
| Etingof Theorem 26.4 | dominant integral `lambda`, irreducible finite-dimensional `L_lambda`, character quotient identity | ordered binders, existence/uniqueness of `L_lambda`, exact equality/divisibility type | candidate proposition only |
| catalog year 1925 | historical attribution | exact primary publication, edition, page and translation | not supplied or audited |
| catalog `已验证` | inventory classification | accepted source review or kernel receipt | explicitly untrusted; no credit |

## Lean boundary

The pinned discovery probe checks `FDRep.character`, `Representation.character`,
`LieModule.weightSpace`, `LieModule.Weight`, `LieAlgebra.IsKilling.rootSystem`, and root-pairing
Weyl-group interfaces. These show that some substrate exists. The `FDRep` interfaces are generic
representation characters, while the root and weight interfaces do not provide the highest-weight
module or numerator-denominator character identity. A bounded exact-topic search found no target
declaration. None of these declarations is credited as a proof or checked alternate encoding.

Before source acceptance, an independent reviewer must pin a lawful immutable source copy, record
the exact statement and all incorporated definitions, audit corrections and historical identity,
and map every domain, ordered binder, hypothesis, normalization, boundary case, and conclusion to
the chosen Lean expression. The source crosswalk intentionally remains open until then.
