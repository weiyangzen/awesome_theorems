# THM-M-0525 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the fundamental group. The terse source phrase
"the group of path-homotopy classes of a topological space" is read in its standard based sense:
loops at a chosen point, modulo homotopies that keep both endpoints fixed. Arbitrary paths form the
fundamental groupoid, while free-loop classes do not generally form the claimed group.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | For `X` with basepoint `x`, endpoint-fixed homotopy classes of loops `x` to `x` form a group | Exact Lean declaration/expression, normalized hash, and binder audit belong to the statement phase |
| Carrier | Quotient of based paths by endpoint-preserving path homotopy | Equality convention and quotient implementation must be inspected, not inferred from the name |
| Multiplication | Concatenation of representatives, descending to homotopy classes | Well-definedness and the direction convention for composition remain proof obligations |
| Unit | Class of the constant path at `x` | Identity laws require checked quotient-level composition |
| Inverse | Class of the reversed path | Both inverse laws require checked endpoint and homotopy handling |
| Laws | Associativity, left/right identity, and left/right inverse | No existing instance is credited as proof closure during intake |
| Functorial context | Fundamental groupoid and induced maps are relevant architecture | They are not substitutes for the based vertex group root |
| Related theories | first homotopy group, basepoint-change isomorphisms, van Kampen, and coverings | Candidate downstream relationships only; excluded from this root |

The provisional scope nodes `FG-ROOT`, `FG-PATH`, `FG-QUOT`, `FG-MUL`, `FG-ONE`, `FG-INV`, and
`FG-LAWS` are navigation labels, not a frozen obligation registry. A later phase must expand and
type them without treating aliases, quotient wrappers, or inherited category instances as distinct
proof bodies.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. `IntakeProbe.lean` confirms that
the pinned local mathlib exposes the intended construction and candidate carrier/group APIs. That
probe is discovery evidence only. It does not freeze an exact formal proposition, inspect terminal
proof bodies, or establish the trust and provenance closure required for machine credit.

The first open gate is the exact-statement gate. The dependent statement task must decide whether
the canonical formal target is a declaration audit of `FundamentalGroup` plus its `Group` instance
or an explicit proposition packaging the carrier identification and operations, then elaborate and
mutation-test that exact target.

## Statement-phase handoff

`Statement.lean` now freezes the latter choice: for every topological space `X` and basepoint `x`,
the endpoint-fixed path-homotopy quotient is equipped with a `Group` whose multiplication, identity,
and inverse are respectively quotient path concatenation, the constant path, and path reversal.
The `Group` laws therefore express exactly the claimed construction laws, while operation equations
rule out satisfying the target with an unrelated structure. `statement.json` records the signature,
environment hashes, carrier equality, and four required mutation/boundary checks. This is
self-tested statement evidence pending master acceptance, not proof or theorem-completion credit.

## Validation

Exact commands and results are recorded in `validation.md`. They establish manifest consistency,
JSON validity, dossier-local hygiene, and narrow candidate-API elaboration only. Master acceptance
and every dependent phase remain outstanding.
