# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Symmetric events of an iid sequence have probability zero or one | E. Hewitt and L. J. Savage, "Symmetric Measures on Cartesian Products," *Transactions of the American Mathematical Society* 80 (1955), 470-501 | `AwesomeTheorems.Stage1.S1_M_288.StatementShape` | Primary historical paper identified; exact theorem/page, edition hash, assumptions, and errata review remain open, so only `H1` is claimed |
| Countable iid coordinate family | Same paper's product-measure setting; a modern source must be selected to cross-check the random-variable formulation | `HewittSavageData.independent` and `.identicallyDistributed` | Candidate interfaces only; their exact types and measurability consequences are statement-phase work |
| Measurable path event | Product measurable space on the countable Cartesian product | `HewittSavageData.eventMeasurable` | Candidate presently says `MeasurableSet event`; compatibility with the intended product structure is unverified |
| Invariance under finite coordinate permutations | Classical symmetric-event hypothesis | `ExchangeableEvent` plus `FiniteSupportPermutation` | Intended symmetry is recorded, but equivalence to the source convention has not been checked |
| Probability zero or one | Zero-one conclusion for the inverse image of the path event | `ZeroOneConclusion` | Candidate conclusion located; no elaboration or proof credit is assigned |

The repository metadata phrase `可交换事件的零一性质` is too compressed to distinguish a symmetric
event of an iid sequence from an exchangeable law. This dossier adopts the standard symmetric-event
iid theorem and explicitly keeps independence; it does not assert that exchangeability alone gives
the conclusion.

Discovery links, not immutable evidence receipts:

- Historical paper: bibliographic discovery is limited to the journal citation above; DOI/resolver
  metadata remains deliberately unasserted pending verification
- Repository source record: `Docs/researches/math_theorems.md`, entry `THM-M-1008`
- Historical Lean candidate: `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_288.lean`

No `H0` or machine-closure claim is made. The source audit must obtain a stable scan, verify its
bibliographic identifier and exact theorem/page, map every premise, search corrections/errata, and
receive independent review. The statement phase must then inspect and normalize the candidate Lean
type and test domain, binder, measurability, independence, identical-law, symmetry, and boundary
mutations.
