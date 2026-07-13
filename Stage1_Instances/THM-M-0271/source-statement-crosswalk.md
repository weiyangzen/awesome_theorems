# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1950-1955` supplies exactly the title `富比尼定理`, Guido
Fubini, 1907, the gloss `重积分与累次积分的关系`, importance "high," and status `已验证`. Git
blame attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, formula,
domain, integral model, ordered binder, hypothesis, conclusion, proof boundary, correction history,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:7495-7520` repeats those fields and explicitly leaves the formal system,
logical foundation, precise definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. Its generic statement that a closed result is known
is planning metadata, not source or kernel evidence. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Historical source lead

The zbMATH Open API record for document `2643959`, JFM identifier `38.0343.02`, was inspected on
2026-07-13. It identifies:

> Guido Fubini, *Sugli integrali multipli*, Accademia dei Lincei, Rendiconti, fifth series, volume
> 16, number 1 (1907), pages 608-614.

The record preserves a contemporary German JFM review. It reports that for a Lebesgue-integrable
scalar function `f(x,y)` on a region `Gamma`, whose intersections with lines `x = constant` or
`y = constant` are linearly Lebesgue measurable, the integral over `Gamma` equals both iterated
integrals. It also says the paper indicates extensions to polar and other coordinates.

This is a strong historical identity and statement lead, but the API record is a secondary review,
not the primary paper. No lawful immutable copy of the 1907 paper, incorporated definitions, exact
Italian theorem text, complete proof, corrections or errata, or independent source review was
inspected. The review's compressed formula also leaves integration bounds and conventions implicit.
It therefore supports `H1`, not `H0`.

## Literal crosswalk

| Repository element | Candidate mathematical component | Prospective Lean component | Intake result |
|---|---|---|---|
| `富比尼定理` | scalar planar Fubini theorem or a modern product-measure generalization | one exact source-selected `Prop`, plus checked transports | family identified; exact root open |
| `重积分` | integral over a planar region or product measure | `Measure.prod`, set integral, or a source-defined planar encoding | region/product choice open |
| `累次积分` | one or both orders of section integration | nested `integral` expressions with explicit measures and binder order | both historical orders reported; canonical conclusion open |
| "relationship" | equality to each order, equality between orders, or a package including section integrability | `integral_prod`, `integral_prod_symm`, `integral_integral_swap`, and supporting obligations | relation and package boundary open |
| Fubini / 1907 | historical paper above | immutable source identity and node crosswalk | strong secondary locator only; primary audit open |
| `已验证` | untrusted inventory metadata | accepted source, kernel, trust, and receipt evidence would be required | no H0 or M0 credit |

## Pinned Lean candidate crosswalk

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.MeasureTheory.Integral.Prod`:

| Candidate declaration | Checked role | Unresolved source boundary |
|---|---|---|
| `MeasureTheory.integrable_prod_iff` | characterizes product integrability using a.e. section integrability and integrability of the section-norm integral | source may phrase measurability and absolute integrability differently |
| `MeasureTheory.Integrable.prod_left_ae` / `prod_right_ae` | gives almost-everywhere integrability of sections | historical review does not expose the exact exceptional-section convention |
| `MeasureTheory.Integrable.integral_prod_left` / `integral_prod_right` | proves integrability of the functions of inner integrals | may be a supporting conclusion rather than part of the source root |
| `MeasureTheory.integral_prod` | product Bochner integral equals the `x`-then-`y` iterated integral | abstract spaces, s-finite measures, normed-space codomain, and incomplete-space convention differ from the source lead |
| `MeasureTheory.integral_prod_symm` | product integral equals the reverse iterated order | whether both equalities belong to one root remains open |
| `MeasureTheory.integral_integral_swap` | the two iterated Bochner integrals are equal | consequence/alternate form, not automatically identical to a product-integral statement |

The checked candidate type quantifies measurable spaces `alpha` and `beta`, measures `mu` and
`nu`, s-finiteness of both measures, a normed additive commutative group `E` with a real normed-space
structure, a function `f : alpha x beta -> E`, and product-measure integrability. Representative
`#print axioms` output lists `propext`, `Classical.choice`, and `Quot.sound`. These facts authenticate
candidate interfaces only; exact statement identity, expression serialization, terminal-body and
transitive trust audit, source transport, and proof credit remain downstream.

The candidate module imports Tonelli infrastructure and names the Fubini-Tonelli family. That does
not merge target ownership: nonnegative `lintegral_prod` results remain outside this Fubini root and
inside the future audit boundary for `THM-M-0272`.

## Source and statement gates

Before `H0`, accountable reviewers must preserve an immutable primary or approved authoritative
edition, locate the exact theorem and incorporated definitions, map every region/measure, function
space, binder, measurability and integrability premise, conclusion, exceptional-section convention,
coordinate extension, and boundary case, inspect corrections and errata, and independently approve
fidelity to `THM-M-0271`.

The statement phase must then choose minimal imports, elaborate one exact Lean expression, preserve
its normalized expression and environment fingerprints, compile every credited planar/product,
scalar/Banach, product/iterated/order-swap, sigma-finite/s-finite, and curried/uncurried transport,
and mutation-test a removed hypothesis, changed domain, changed binder scope, and boundary case.
Until then the canonical statement, formal target, obligation registry, proof tree, and all proof
credit remain open.
