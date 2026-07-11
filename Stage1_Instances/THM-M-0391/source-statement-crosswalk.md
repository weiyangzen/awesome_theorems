# Source-statement crosswalk

## Source anchors

- Preda Mihailescu, "Primary Cyclotomic Units and a Proof of Catalan's Conjecture", *Journal fur die
  reine und angewandte Mathematik* 572 (2004), 167-195, DOI `10.1515/crll.2004.048`.
- Eugène Catalan, 1844 conjecture, used only for historical naming; it is not proof evidence.

The journal article is the primary proof-source candidate. Its bibliographic identity is recorded
for discovery, but a stable copy, exact theorem/page wording, invoked definitions, assumptions,
and errata have not yet been inspected. Therefore this dossier makes no H0 claim.

| Source component | Frozen repository meaning | Lean consequence | State |
|---|---|---|---|
| consecutive perfect powers | values differ by exactly one | orient as `x ^ a = y ^ b + 1` | included |
| nontrivial powers | base and exponent exceed one | four strict `Nat` inequalities | included |
| unique exception | `9` and `8` | tuple `(3,2,2,3)` in the chosen orientation | included |
| integer wording | positive bases are intended | use naturals provisionally; integer transport later | pending transport |
| proof hypotheses | cyclotomic proof infrastructure | must be mapped node-by-node during source audit | unresolved |

The Stage0 gloss `卡塔兰猜想的证明` and its `已验证` metadata are untrusted intake metadata, not a
statement or machine-proof receipt. Before H0, an independent reviewer must inspect the primary
article, record exact page/theorem anchors and errata results, and approve every row of the mapping.
