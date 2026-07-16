# Source-statement crosswalk

## Candidate primary source

Henri Cartan and Samuel Eilenberg, *Homological Algebra*, Princeton University Press, 1956, is the
bibliographic work suggested by the repository attribution and date. No immutable copy, chapter,
section, theorem or definition number, page range, assumption list, or errata record is admitted by
the current dossier. The book is therefore a discovery lead, not an `H0` source receipt and not a
source-authorized statement.

## Crosswalk

| Claim component | Repository source | Lean discovery candidate | Statement assessment |
|---|---|---|---|
| Attribution | `Docs/researches/math_theorems.md`: Henri Cartan/Samuel Eilenberg, 1956 | none | Bibliographic hint only; no edition, theorem/page, invoked definitions, translation, or errata |
| Root wording | `左/右导出函子的存在性` (existence of left/right derived functors) | `AbelianDerivedCanonicalStatement` in the legacy module and `AbelianResolutionCandidate` in the target-owned discovery file | The word "existence" does not select a construction, universal property, degree convention, or package of consequences |
| Left derived | no domains or hypotheses | `F.leftDerived n` under abelian categories, `HasProjectiveResolutions C`, and `F.Additive` | Plausible degreewise branch, but every domain and hypothesis is supplied by the candidate rather than the source record |
| Right derived | no domains or hypotheses | `F.rightDerived n` under abelian categories, `HasInjectiveResolutions C`, and `F.Additive` | Plausible degreewise branch, but every domain and hypothesis is supplied by the candidate rather than the source record |
| Total derived | not distinguished | total Kan-extension APIs wrapped in `S1_M_095` | Materially different branch with localization and Kan-extension existence assumptions; it cannot silently replace the degreewise interpretation |
| Variance and exactness | not stated | candidates use covariant additive functors; comparison wrappers add finite-(co)limit preservation | Scope is unresolved; contravariant functors and left/right exact hypotheses cannot be invented or omitted by fiat |
| Consequences | not stated | acyclic-object, degree-zero, naturality, and long-exact wrappers | Discovery inventory only; none belongs to the root without a source-authorized scope decision |
| Boundary cases | not stated | zero categories/functors, degree zero, one-sided resolution availability | Unfrozen; meaningful mutation and boundary tests require an exact canonical root first |

## Existing Lean discovery boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_095.lean` contains real checked wrappers for both
degreewise and total-derived APIs. `Stage1_Instances/THM-M-0006/StatementCandidate.lean` isolates the
narrow degreewise interpretation. Both are discovery inputs only: the manifest says legacy
artifacts are unaccepted, and neither artifact can determine what the sparse human record intended.
The statement boundary probe in `Statement.lean` checks only that the pinned degreewise interfaces
are available. It deliberately declares no canonical proposition.

Before the positive statement gate can close, an independent source process must admit a stable
edition, exact theorem or definition-plus-existence result, pages, all assumptions and conventions,
errata, and a premise-by-premise source map. The selected target must then receive explicit ordered
Lean binders, a normalized expression fingerprint, checked alternate transports, and the four
required statement mutations. Until then `H4` and `M4` remain the truthful source and machine
statement classifications.
