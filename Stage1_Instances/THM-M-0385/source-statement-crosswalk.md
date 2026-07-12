# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `Bourgain\u548c\u79ef\u5b9a\u7406`, attributes it to
Jean Bourgain, dates it to 2003, and gives only `\u548c\u96c6\u4e0e\u79ef\u96c6\u7684\u5927\u5c0f\u5173\u7cfb` ("a relationship between
the sizes of sumsets and product sets"). Stage0 repeats that metadata and leaves exact definitions
and assumptions open. The manifest deliberately preserves `\u5df2\u9a8c\u8bc1` as
`source_status_untrusted`; it supplies no proof credit.

## Primary-source candidates

- Jean Bourgain, "On the Erd\u0151s-Volkmann and Katz-Tao ring conjectures", *Geometric and
  Functional Analysis* **13** (2003), 334-365, DOI `10.1007/s00039-003-0411-7`. The title, author,
  and year fit the metadata, but an exact theorem/page and its discretized or Hausdorff-dimension
  formulation have not yet been inspected and accepted.
- Jean Bourgain, Nets Hawk Katz, and Terence Tao, "A sum-product estimate in finite fields, and
  applications", *Geometric and Functional Analysis* **14** (2004), 27-57, DOI
  `10.1007/s00039-004-0451-1`. This is a distinct primary candidate for the finite-field reading;
  its year and coauthorship do not exactly match the repository row.

These are discovery anchors, not immutable evidence receipts and not an `H0` crosswalk. The source
audit must inspect stable copies, record file hashes, theorem labels/pages, invoked definitions,
all assumptions, proof boundaries, and errata, and obtain independent review.

## Crosswalk

| Repository phrase | Candidate mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "sumset" | `A + A` in reals or a prime field | pointwise addition on a finite set, or a scale/fractal analogue | subject only |
| "product set" | `A * A` in the same ambient domain | pointwise multiplication with the selected domain instances | subject only |
| "size" | finite cardinality, covering number, or Hausdorff dimension | `Finset.card`, a covering-number definition, or dimension theory | unresolved and blocking |
| "relationship" | a max/lower bound with constants and parameter ranges | exact inequalities and ordered quantifiers | absent |
| "Bourgain", 2003 | likely the ring-conjecture paper | source theorem must be pinpointed | plausible, not frozen |
| `\u5df2\u9a8c\u8bc1` | untrusted inventory label | no Lean proposition or proof evidence | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded
`IntakeProbe.lean` imports the pointwise finite-set API and checks that `A + A`, `A * A`, and their
cardinalities elaborate for finite subsets of the reals and a prime field. Those are encoding
ingredients only. They do not choose the domain, size notion, constants, hypotheses, or conclusion
of THM-M-0385, and no formal candidate receives machine credit at intake.
