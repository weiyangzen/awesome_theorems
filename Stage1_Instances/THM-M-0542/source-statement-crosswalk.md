# Source-statement crosswalk

## Repository record and source candidate

The repository inventory gives the title "de Rham cohomology", attributes it to Georges de Rham
in 1931, and supplies only "cohomology of differential forms" as its statement. Its `已验证` field
is untrusted metadata under rev-5.6. In particular, the record does not distinguish a definition
of a cohomology group from a proposition about that group.

A historical primary-source lead is Georges de Rham, *Sur l'analysis situs des varietes a n
dimensions*, Journal de Mathematiques Pures et Appliquees (9) 10 (1931), 115-200. This intake has
not inspected an immutable facsimile, selected a numbered result/page within it, reconciled modern
notation with the original conventions, or checked corrections. It is therefore a discovery lead,
not `H0` evidence. A modern primary-quality definition/theorem source may be selected later, but it
must be pinned by edition, theorem/definition, and page.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "differential forms" | smooth real `k`-forms on a specified manifold | concrete bundled manifold differential forms | intended; model and regularity open |
| "cohomology" | closed forms modulo exact forms | kernel/image or submodule quotient of an explicit cochain complex | intended construction; exact type open |
| exterior derivative | degree-raising differential | concrete `d_k` with domain/codomain and smoothness proof | required; API selection open |
| exact implies closed | `im d_(k-1)` lies in `ker d_k` | checked `d^2 = 0` theorem | required well-definedness bridge; not credited |
| degree `k` | natural grading, including degree zero | ordered `k : Nat` binder and predecessor convention | open |
| 1931 / de Rham | historical locator | no machine-proof credit | candidate paper identified only |

## Existing Lean boundary

The repository file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_109.lean`, owned by the
separate Hodge-theory target, is discovery input only. Its `ClosedFormsQuotientModel` receives
`closedForm`, `exactDifference`, and proof that the relation is an equivalence as structure fields.
Its resulting quotient is an abstract shape, not de Rham cohomology of a concrete smooth manifold,
and gives this target no statement or proof credit.

A narrow intake search of pinned mathlib found only an explanatory de Rham-cohomology mention in
`Mathlib/Data/Fin/Parity.lean` and unrelated p-adic `BDeRham` period-ring definitions. This is not
an exhaustive anchor audit, which remains a later task. Before `H0`, an independent reviewer must
approve an immutable source locator, all assumptions and definitions, errata, and a row-by-row map
to the eventual elaborated Lean expression.
