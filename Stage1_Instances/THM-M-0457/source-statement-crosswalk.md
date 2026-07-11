# Source-statement crosswalk

## Candidate primary source

S. J. Arakelov, "Intersection theory of divisors on an arithmetic surface", *Mathematics of the
USSR-Izvestiya* 8 (1974), 1167-1180, is the historical primary-source candidate matching the
repository's author, date, and description. This bibliographic identification is a discovery
anchor only. The article text, original/translated edition correspondence, numbered theorem,
page, definitions, and errata have not yet been inspected, so it is not `H0` evidence.

## Crosswalk

| Repository input | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "Arakelov theory" | historical theory introduced by Arakelov | one concrete declaration, not a theory package | ambiguous; theorem selection open |
| "intersection theory" | pairing/product and its asserted properties | definitions plus a proposition about the concrete pairing | included subject; exact result open |
| "arithmetic surfaces" | source category of surfaces over arithmetic bases | schemes, divisors, places, analytic data | included; hypotheses open |
| year 1974 / Suren Arakelov | historical attribution | no proof credit | consistent with candidate citation |
| source status "verified" | untrusted legacy metadata | kernel and provenance receipts | no credit |

## Source-to-statement gate

Before canonical Lean elaboration, an independent source inspection must record a stable scan or
edition identifier, exact numbered result and page, verbatim mathematical claim, all locally
referenced definitions, assumptions and normalizations, and any errata. Each binder and conclusion
in the proposed Lean expression must map to that record. Until then, `M4` remains appropriate: no
formal statement has been chosen and no existing formal candidate has been credited.
