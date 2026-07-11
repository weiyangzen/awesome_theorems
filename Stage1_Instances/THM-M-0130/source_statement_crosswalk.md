# Source-statement crosswalk

The manifest name `志村簇` means "Shimura varieties." The legacy blueprint's content phrase is
`Hodge型志田簇的构造`; `志田` appears to be a typographical error for `志村`. More importantly,
"construction" does not specify which of several distinct theorems is intended.

| Claim component | Primary-source discovery anchor | Formal candidate | Intake assessment |
|---|---|---|---|
| Definition of a Shimura datum and analytic quotient | P. Deligne, *Travaux de Shimura*, Séminaire Bourbaki 1970/71, Exp. 389, Lecture Notes in Mathematics 244 (1971), pp. 123-165 | A future structure for `(G, X)` and `G(Q) \ (X × G(A_f)/K)` | Foundational source located, but a definition/quotient construction alone is not the requested theorem |
| Canonical models over the reflex field | P. Deligne, *Variétés de Shimura: interprétation modulaire, et techniques de construction de modèles canoniques*, Proc. Sympos. Pure Math. 33, Part 2 (1979), pp. 247-289 | Existence/descent proposition for a selected datum and level | Plausible intended theorem family; exact theorem, assumptions, and conclusion are not yet selected |
| Hodge-type integral canonical models | M. Kisin, *Integral models for Shimura varieties of abelian type*, Journal of the AMS 23 (2010), pp. 967-1012, especially the Hodge-type construction developed before the abelian-type extension | Existence/extension statement over a localization of the reflex field | Another plausible but strictly stronger and more conditional target; prime, level, and ramification restrictions cannot be omitted |

The candidates are not interchangeable. The complex double quotient, canonical model, and integral
canonical model differ in object, base, hypotheses, and universal property. Consequently there is
no truthful ordered-binder list or Lean expression to freeze from the repository phrase alone.

Statement-phase requirements:

1. Choose a pinpoint primary theorem (edition, theorem/section, and pages), not merely the subject.
2. Record all datum, embedding, level, reflex-field, prime, and ramification assumptions.
3. State the exact constructed object and its existence, uniqueness, descent, or extension property.
4. Check errata and map each source premise to the Lean binders before elaboration.

Discovery links (not immutable evidence receipts):

- Deligne 1971: <https://doi.org/10.1007/BFb0069270>
- Deligne 1979 bibliographic record: <https://www.ams.org/pspum/033.2>
- Kisin 2010: <https://doi.org/10.1090/S0894-0347-10-00667-3>

No `H0` claim is made. `H1` records that standard primary sources and established constructions
exist while the exact source statement and premise crosswalk remain unresolved.
