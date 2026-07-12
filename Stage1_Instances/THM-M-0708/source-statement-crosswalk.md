# Source-statement crosswalk

| Claim component | Source anchor | Formal candidate | Intake assessment |
|---|---|---|---|
| Repository claim | `Docs/researches/math_theorems.md`, Rice entry: "程序性质的非平凡性不可判定"; duplicated under logic/proof theory and recursion theory | none | Metadata-level theorem family only; "program behavior" and "nontrivial" require formal scope |
| More explicit repository wording | `Docs/researches/cs_theorems.md`, table 1.1.4: every nontrivial property of program behavior is undecidable | induced predicate on program indices | Useful source-record gloss, but not a primary proof and not machine evidence |
| Classical primary theorem | H. G. Rice, *Classes of recursively enumerable sets and their decision problems*, Transactions of the AMS 74(2), 1953, pp. 358-366, DOI `10.1090/S0002-9947-1953-0053041-6` | an extensional nontrivial index class in an acceptable enumeration | Primary publication and bibliographic extent identified; exact theorem number/page wording, assumptions, and errata remain to be inspected, so the root stays `H1` |
| Program enumeration | Rice's formulation uses classes/indexes of recursively enumerable sets | `Nat.Partrec.Code`, `Nat.Partrec.Code.eval`, and `Nat.Partrec.Code.exists_code` in pinned mathlib | Repo-local definitions were located, but no exact Rice theorem or checked transport was established |
| Extensionality | membership depends on the recursively enumerable set / computed partial function rather than the chosen index | equality invariance of `S : (Nat ->. Nat) -> Prop` | Frozen as an explicit hypothesis; exact Lean expression deferred |
| Nontriviality | the index class is neither empty nor universal | represented witnesses `f_in`, `f_out` | Frozen explicitly; prevents the constant-property counterexamples |
| Undecidability conclusion | the induced index set is not recursive/decidable | negation of mathlib `ComputablePred` for the code predicate, or an equivalent selected notion | Candidate only; exact type and equivalence to source terminology require statement elaboration |

The canonical functional formulation is intended to match the familiar modern form of Rice's
theorem, but the map from Rice's recursively enumerable-set presentation to partial-function
semantics is not credited at intake. In particular, an equality of ranges would lose output-graph
information unless the selected encoding is designed for it. The statement phase must choose one
representation and make every other representation an explicit checked transport.

Discovery links, not immutable evidence receipts:

- Primary-paper DOI: <https://doi.org/10.1090/S0002-9947-1953-0053041-6>
- Publisher metadata gives volume 74, issue 2, year 1953, pages 358-366.

Required source follow-up: obtain and hash an immutable edition, locate the exact theorem and
definition pages, audit corrections/errata, map acceptable-numbering premises to the Lean model,
and obtain independent review. Until then no `H0` claim is made.
