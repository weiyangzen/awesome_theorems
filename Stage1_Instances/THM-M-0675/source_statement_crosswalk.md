# Source-statement crosswalk

## Located repository source

The target manifest derives the item from
`Docs/researches/math_theorems.md`, whose complete mathematical payload is:

| Field | Source value |
|---|---|
| name | `齐性模型` (homogeneous models) |
| proposer | many mathematicians |
| time | 20th century |
| statement | `齐性模型的性质` (properties of homogeneous models) |
| importance | high |
| formalization status | `已验证` (verified) |

`Docs/Stage0_Blueprint.md` repeats that payload and explicitly leaves the
precise definition, assumptions, proof route, axioms, and artifact links to be
filled in. The rev-5.6 manifest marks the source status as untrusted and the
target as `L0 / rework_required`.

## Component crosswalk

| Required canonical component | Source anchor | Intake assessment |
|---|---|---|
| proposition | generic phrase "properties" | absent |
| notion of homogeneity | name only | ambiguous between materially different definitions |
| language and model | none | absent |
| cardinal and size bounds | none | absent |
| ordered quantifiers | none | absent |
| hypotheses | none | absent |
| conclusion | none | absent |
| primary proof source | "many mathematicians" | no bibliographic anchor |
| formal artifact | untrusted `已验证` label | no project, revision, module, or declaration |

## Fidelity decision

There is no source statement to crosswalk to an exact Lean proposition. A
theorem such as "saturated models are homogeneous," a Fraisse-limit
ultrahomogeneity theorem, or an existence/uniqueness result would add facts not
present in the source. Even encoding the definition of homogeneity as the root
would substitute a definition for the claimed unspecified "properties."

Accordingly, no primary-source, Lean-candidate, or `H0` claim is made. The
source-statement gate is blocked until a proposition-level source is supplied.
This is a statement-identity blocker, not evidence that the mathematical topic
is open or false.
