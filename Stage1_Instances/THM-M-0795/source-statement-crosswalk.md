# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `力迫公理`, attributes it to "many
mathematicians", dates it only to the twentieth century, and states `各种力迫公理及其应用`
("various forcing axioms and their applications"). Stage0 repeats this metadata while leaving the
exact definitions, assumptions, equivalences, required axioms, and artifact links open. The
rev-5.6 manifest preserves `已验证` solely as `source_status_untrusted`.

No formula, forcing class, cardinal bound, named application, base theory, primary source edition,
theorem/page, errata record, proof, or formal artifact is supplied. Nearby repository entries for
Martin's Axiom and PFA confirm that the inventory itself treats named family members separately;
they do not select a meaning for this umbrella entry.

## Candidate source work

The standard literature for each named forcing axiom is a future locator, not accepted evidence for
this unspecific record. Source audit must first determine whether the intended root is a particular
axiom, a relative-consistency theorem, or one named application. It must then inspect an immutable
primary or authoritative edition and record definition/theorem/page, base theory, all assumptions,
proof boundary, errata, and an independent review. Assigning one family member now would not be an
`H0` crosswalk; it would be a substituted theorem.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "forcing axioms" | quantification over a selected class of forcing notions | internal forcing notion and class predicate | family not selected |
| dense sets | a bounded family of dense subsets of the order | fixed order orientation and density predicate | generic relation API probed; semantics open |
| generic object | a filter or directed set meeting each dense subset | `Filter` or checked alternate encoding | generic API probed; encoding open |
| family strength | a cardinal bound such as `< continuum` or `aleph_1` | explicit `Cardinal` inequality/indexing | cardinal API probed; bound open |
| "applications" | one or many conditional consequences | exact axiom hypothesis and named conclusion | no application selected |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports generic order/filter and cardinal modules and checks partial orders, filters, the
generic densely-ordered class, cardinality, `aleph`, and `aleph_1`. These are encoding ingredients only;
they do not define a forcing notion, forcing-class predicate, forcing axiom, or application. A
bounded content search found no forcing-axiom development in pinned mathlib, but that negative
intake observation is not a substitute for the later immutable anchor audit.
