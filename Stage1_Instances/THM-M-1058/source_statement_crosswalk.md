# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| LDP as lower bound on open sets and upper bound on closed sets | A. Dembo and O. Zeitouni, *Large Deviations Techniques and Applications*, 2nd ed., Springer, 1998, Definition 1.2.1 | `LargeDeviationPrinciple E D` in legacy `S1_M_250.lean` | Standard primary monograph anchor located; edition/page text, assumptions, and errata are not yet accepted (`H1`) |
| Nonnegative lower-semicontinuous rate function | Dembo-Zeitouni, Definition 1.2.1 | `LargeDeviationData.rate_nonnegative`, `rate_lowerSemicontinuous` | Candidate field correspondence; exact codomain and topology remain unchecked |
| Speed/scaling convention | Dembo-Zeitouni uses a small-parameter family in the cited definition; sequence conventions are standard reparameterizations | `speed : Nat -> Real` and scaled log probability | Material encoding difference; a checked transport or a sequence-specific primary pinpoint is required |
| Good rate function | Dembo-Zeitouni, Definition 1.2.1 distinguishes compact level sets | no compact-sublevel field in the candidate | Correctly excluded from the base LDP; must not be inferred |
| Weak LDP | Standard variant replaces the closed-set upper bound by a compact-set bound | no credited candidate | Explicitly excluded; not interchangeable without exponential tightness hypotheses |

The repository's one-line source gloss, “decay rate of probabilities of rare events,” does not
identify a family, speed, or rate function and is insufficient as an exact theorem statement. The
candidate above interprets the title as the definition/property convention rather than inventing a
universal theorem. The statement phase must resolve the measurable/topological compatibility,
extended-real sign and empty-set conventions, sequence-versus-small-parameter encoding, and the
precise normalized Lean expression before machine evidence is inspected.

Discovery locator (not an immutable evidence receipt): DOI
<https://doi.org/10.1007/978-1-4612-5320-4>. A later source audit must record a scanned edition hash,
page-level quotation, corrections/errata, and premise-to-node mapping. No `H0` or proof claim is made.
