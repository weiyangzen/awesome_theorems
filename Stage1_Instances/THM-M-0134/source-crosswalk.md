# Source-statement crosswalk

## Available source record

The only located repository source record is
`Docs/researches/math_theorems.md`, lines 977-982. It gives the Chinese label,
attributes the item to W. Burnside/A. Young, dates it to the 1900s, describes it
as "representation theory of symmetric groups", and supplies an untrusted
`已验证` status. It gives no title, edition, theorem number, page, hypotheses,
conclusion, bibliography, or errata trail.

No primary mathematical source is therefore claimed by this intake. In
particular, the generic attribution is insufficient for H0 or H1 and does not
establish that "Burnside-Young theorem" is a stable historical theorem name.

## Provisional crosswalk

| Intake component | Repository evidence | Disposition |
|---|---|---|
| finite symmetric group `S_n` | topic says symmetric-group representation theory | candidate inclusion; exact convention unresolved |
| complex representations | not specified | candidate inclusion; requires primary-source confirmation |
| finite dimensionality | not specified | candidate inclusion; requires confirmation |
| irreducible isomorphism classes | suggested by legacy Lean discovery artifact only | no source credit |
| partitions of `n` | suggested by legacy Lean discovery artifact only | no source credit |
| classification by bijection | suggested by legacy Lean discovery artifact only | no source credit |
| all `n`, including `0` and `1` | not specified | boundary convention unresolved |

## Required H-gate resolution

Before the statement node may certify an exact target, locate a stable scan of
a primary work by Burnside or Young, or a historically authoritative edition
that explicitly identifies the result and its original source. Record exact
edition, theorem/page, assumptions, field, range of `n`, equivalence notion,
construction, and published errata. Then either confirm the candidate root or
revise it through master review; do not choose a nearby named theorem merely to
make the metadata definite. Independent review is required before H0.

## Provenance boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_050.lean` is useful discovery
input because it states the partition-classification interpretation. Under the
uniform L0 rework rule it supplies no accepted source, statement, proof, build,
or status evidence. The repository's `已验证` label likewise supplies none.
