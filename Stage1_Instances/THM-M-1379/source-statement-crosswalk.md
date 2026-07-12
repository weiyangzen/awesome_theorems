# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10048-10053` supplies exactly the title
`Hamilton-Jacobi方程`, attribution to William Hamilton and Carl Jacobi, the year 1837, the gloss
`经典力学的偏微分方程形式` ("the partial-differential-equation formulation of classical
mechanics"), importance "high," and status `已验证`. Git history places all six uncited lines in
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. There is no bibliography, source identifier,
formula, definition, theorem statement, proof, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:37506-37531` repeats the gloss while explicitly leaving the formal
system, foundation, precise definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. Its generated closed-result language is planning
metadata, not source or proof evidence. The rev-5.6 manifest carries `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required` and `planned`.

## Literal crosswalk

| Repository element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| `Hamilton-Jacobi方程` | a named equation/formalism family in mechanics | one exact truth-valued `Prop`, not merely a name or notation | no proposition selected |
| "PDE formulation" | partial derivatives in unspecified independent variables are broadly suggested | function domains, spatial/time split, derivative notions, equation, binders, hypotheses, and equality scope | all open |
| "classical mechanics" | a classical-mechanical setting is intended | configuration/phase spaces, Hamiltonian, action, units, regularity, and model assumptions | all open |
| Hamilton/Jacobi, 1837 | historical attribution and date | pinpoint source provenance | no edition, theorem/equation/page, proof, or errata |
| ODE manifest category | catalog classification | chosen mathematical domain and encoding | conflicts with the PDE gloss; unresolved |
| `已验证` | untrusted inventory metadata | accepted human proof and kernel receipt would be required | no H or M credit |

## Related physics record

`Docs/researches/physics_theorems.md:6443-6449` separately records
`THM-P-0755` through its Stage0 projection at `Docs/Stage0_Blueprint.md:66000-66027`. It displays
the schema `H(q, partial S/partial q, t) + partial S/partial t = 0` and says that it converts a
mechanics problem into a PDE. This is useful contextual notation only.

The physics record has a different UID, discipline, title spelling, date (`1834/1837`), and literal
statement, and Stage0 retains it as a separate record. More importantly, the schema still omits
domains, definitions, regularity, solution data, and a proposition saying whether it is derived,
solved, characterized, or merely defined. It cannot be promoted into the canonical statement of
`THM-M-1379`.

## Neighbor and source boundary

`THM-M-1380` separately says "a complete solution of the Hamilton-Jacobi equation." The catalog
therefore gives affirmative reason not to reinterpret this target as a complete-integral theorem.
The nearby action, Euler-Lagrange, Hamiltonian-system, and characteristics targets likewise require
separate source identities and cannot donate assumptions or proof credit.

V. I. Arnold, *Mathematical Methods of Classical Mechanics*, second edition, Chapters 8-9, is
recorded elsewhere in the repository as a broad Hamiltonian-mechanics discovery lead. No exact
Hamilton-Jacobi passage, edition/page-level proposition, incorporated definition chain, proof,
errata status, or independent review was admitted for this target. The citation is therefore not
claimed as primary `H0` evidence and selects no root.

## Source gate

Before leaving `H5`, an accountable reviewer must preserve and hash one immutable primary or
approved authoritative source edition, select one exact truth-valued claim, transcribe its complete
definitions, ordered binders, hypotheses, conclusion, conventions, boundary cases, and proof
boundary, audit corrections or errata, explain its relation to the distinct physics and neighboring
mathematics targets, and obtain independent review of the mapping.

The canonical module, expression, expression hash, environment fingerprint, checked transports,
and mutation tests remain null. The provisional `H5` classifies the received wording, not the
mathematical status of any source-corrected Hamilton-Jacobi theorem. No H0, M0, R0, audit
completion, or theorem completion is claimed.
