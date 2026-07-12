# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the title `冯·诺依曼双换位子定理`, attributes it to John
von Neumann, dates it to 1929, and states only `算子代数的双换位子` ("the double commutant of
operator algebras"). Stage0 repeats this wording while leaving exact definitions, assumptions,
equivalent formulations, axioms, proof route, and artifact links open. The rev-5.6 manifest keeps
`已验证` only in the explicitly untrusted source-status field.

This identifies a classical theorem family but is not an exact statement or an `H0` source. It
provides no edition, paper title, theorem/page locator, errata, or premise mapping. The later source
audit must inspect an immutable primary edition or a justified authoritative formulation, record
every assumption and conclusion, and obtain independent mathematical review.

## Source-statement crosswalk

| Repository phrase | Conventional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "operator algebra" | a unital self-adjoint subalgebra of bounded operators on a complex Hilbert space | `StarSubalgebra ℂ (H →L[ℂ] H)` plus any extra source hypotheses | carrier API present; exact input open |
| "commutant" | all bounded operators commuting with every member of the carrier | `Set.centralizer` / `StarSubalgebra.centralizer` | pinned API present |
| "double commutant" | commutant of that commutant | iterated centralizer | expression ingredient present |
| theorem conclusion | weak/strong closure equals bicommutant, or equivalently closedness iff bicommutant equality | operator-topology coercion, `closure`, set/subalgebra equality, checked transports | exact topology and direction open |
| `已验证` | untrusted inventory label | no Lean proposition or proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.VonNeumannAlgebra.Basic` defines a concrete `VonNeumannAlgebra` as a star
subalgebra whose carrier is equal to its double centralizer. It consequently proves
`VonNeumannAlgebra.commutant_commutant` for an object already carrying that equality. The module
documentation explicitly says that proving the von Neumann double commutant theorem, namely the
equivalence with weak closedness, is still needed. Therefore this declaration is an interface
anchor and exclusion guard, not closure of the target theorem.

The bounded `IntakeProbe.lean` also confirms that the weak operator topology wrapper and its
defining convergence theorem elaborate. No exact closure characterization was selected or proved.
A complete immutable mathlib/external search belongs to `S56-M-0333-ANCHOR_AUDIT`, after the exact
statement gate, and is not claimed here.
