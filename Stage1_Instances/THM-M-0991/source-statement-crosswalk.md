# Source-statement crosswalk

## Source inventory

Repository metadata provides the name, the summary "rate of convergence in the central limit
theorem", attribution to Andrew Berry and Carl-Gustav Esseen, and the year 1941. It provides no
edition, theorem number, page, hypothesis list, constant, or errata. Accordingly `已验证` is treated
as untrusted screening metadata.

Two historical source candidates require page-level inspection: A. C. Berry, *The Accuracy of the
Gaussian Approximation to the Sum of Independent Variates*, Transactions of the American
Mathematical Society 49 (1941), 122-136; and C.-G. Esseen's early work on remainder terms in the
central limit theorem. This intake does not assert a pinpoint for Esseen or claim that either paper's
exact formulation already matches the candidate Lean encoding.

## Crosswalk

| Claim component | Repository/source anchor | Candidate Lean surface | Intake assessment |
|---|---|---|---|
| independent summands | theorem family and Berry title | `BerryEsseenIIDData.independent` | plausible; source scope not verified |
| identical distribution | common classical i.i.d. specialization | `BerryEsseenIIDData.identDistrib` | candidate restriction; may not match primary generality |
| mean and positive variance | central-limit normalization | `mean`, `sigma`, `mean_eq`, `variance_eq`, `sigma_pos` | encoding exists; exact conventions open |
| finite third absolute centered moment | classical rate hypothesis | `third_abs_integrable`, `third_abs_moment_le` | candidate bound uses `rho`; source mapping open |
| normalized sum | CLT sum scaled by `sigma * sqrt n` | `normalizedSum` | algebraic convention plausible but unaccepted |
| uniform CDF error | Berry-Esseen conclusion | `forall x`, `cdfError ... <= ...` | pointwise universal form models uniform bound |
| universal numerical constant | theorem asserts existence of an absolute constant | `D.constant` supplied in the data | material mismatch risk: current candidate does not quantify universality and must not be accepted unchanged |

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_271.lean` elaborates a useful candidate statement
and wrappers around local probability APIs. It explicitly reports no terminal CDF-rate proof. More
importantly, its `StatementShape` quantifies over data containing an arbitrary nonnegative
`constant`; it neither existentially chooses a universal constant nor prevents data with an
insufficient constant. Thus it is discovery input, not a source-faithful canonical theorem and not
machine closure. The next phase must repair or justify this quantifier boundary before credit.
