# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names `图基引理`, attributes it to John Tukey, dates it to 1940,
and gives only the phrase `有限特征族的极大元` ("a maximal element of a family of finite
character"). Stage0 repeats these fields and explicitly leaves exact definitions, assumptions,
proof path, axioms, and existing machine artifacts open. The rev-5.6 manifest preserves `已验证`
only as `source_status_untrusted`.

No publication title, edition, theorem or page, quotation, definition of finite character,
nonemptiness premise, proof, assumptions, or errata is present. Therefore the repository metadata
does not establish `H0`. In particular, `John Tukey / 1940` must not silently settle the common
`Teichmuller-Tukey` naming or the historical source boundary.

## Frozen interpretation and source gaps

The standard mathematical reading of the gloss is: a nonempty family `F` of subsets of a set has a
maximal member when membership in `F` is determined by membership of all finite subsets. A pointed
form says every `x in F` is contained in a maximal member. This reading is frozen as the intake
scope because it makes every noun in the gloss precise and exposes the necessary nonempty premise.

The source audit must inspect an immutable primary publication or authoritative edition, record the
exact theorem and page, compare its set/universe conventions and finite-character definition,
check whether it states the pointed strengthening, record corrections, and obtain independent
review. If the source differs, this intake must be revised rather than broadening the theorem.

## Crosswalk

| Repository phrase | Frozen mathematical component | Candidate Lean component | Intake status |
|---|---|---|---|
| family | `F`, a set of subsets of an arbitrary carrier | `F : Set (Set alpha)` | type checked |
| finite character | `X in F` iff every finite `Y subseteq X` is in `F` | `Order.IsOfFiniteCharacter F` | definition type checked; source wording open |
| nonempty (omitted) | required boundary premise or a seed `x in F` | `{x : Set alpha} -> x in F -> ...` | necessity checked; source omission explicit |
| maximal element | a member of `F` maximal under subset inclusion | `Maximal (fun y => y in F) m` | candidate conclusion type checked |
| extension form | selected `x` is contained in maximal `m` | `x subseteq m` | candidate strengthening type checked |
| `已验证` | untrusted inventory label | no Lean proposition or proof credit | explicitly rejected as evidence |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Order.TeichmullerTukey` exposes `Order.IsOfFiniteCharacter` and
`Order.IsOfFiniteCharacter.exists_maximal`. Its module documentation calls the latter the
Teichmuller-Tukey lemma and gives the nonempty-family reading. `IntakeProbe.lean` checks the exact
types through the pinned Lean environment and proves only the small boundary fact that the empty
family has finite character. It does not re-prove or accept the maximality theorem.

The module is a strong formal candidate, but terminal proof-body provenance, exact expression
identity, axioms, trust closure, wrappers/transports, and external candidates belong to later gates.
The module's documentation links a tertiary web reference, not the pinpoint primary human source
required for `H0`.
