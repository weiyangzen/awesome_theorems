# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:11637-11642` supplies exactly the title `信道容量`, Claude
Shannon, 1948, the gloss `信道的最大传输速率`, importance `high`, and status `已验证`. Git history
places all six uncited fields in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:42931-42956` repeats the metadata while explicitly leaving the formal
system and foundation, precise definitions and premises, proof route, dependencies, equivalent
forms, axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证`
only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

The repository record contains no channel class, capacity formula, information or error measure,
time or symbol normalization, logarithm base, binder, hypothesis, conclusion, bibliography,
incorporated definition, proof boundary, correction history, or reviewer. There is no legacy Lean
slot, repository declaration, or historical file for this target. Consequently the Lean module,
namespace, variables, ordered binders, imports, declaration, and elaborated expression are null.

## Inspected primary-source lead

Claude E. Shannon, *A Mathematical Theory of Communication*, *Bell System Technical Journal* 27
(1948), Part I, pages 379-423, DOI `10.1002/j.1538-7305.1948.tb01338.x`, and Part II, pages
623-656, DOI `10.1002/j.1538-7305.1948.tb00917.x`, is the exact author/year/result-family match.
The inspected 55-page consolidated copy identifies itself as reprinted with corrections and has
SHA-256 `6e4e3411984f3edf99dbfe8b941cb5e8a321379ff0cae6ae5c1f592ad8882ca8`.
Locators below use the consolidated copy's internal page numbers; admission of the correction and
errata history and independent source review remain open.

Part I, Section 1, consolidated page 3 defines the capacity `C` of a discrete noiseless channel by
`C = lim_(T -> infinity) log N(T) / T`, where the channel uses finitely many elementary symbols
with specified durations, only some symbol sequences may be allowed, and `N(T)` is the number of
allowed duration-`T` signals. The text says the limit exists finitely in “most cases of interest”;
that phrase is not an exact general theorem hypothesis.

Part I, Section 1, Theorem 1, consolidated pages 3-4, treats finite-state constraints. If
`b_ij^(s)` is the duration of the `s`-th symbol allowed in state `i` and leading to state `j`, it
states that `C = log W`, where `W` is the largest real root of the determinant equation formed from
the matrix entries `sum_s W^(-b_ij^(s)) - delta_ij`. This is an actual theorem, but it is much
narrower than the catalog gloss and depends on the preceding channel model and Appendix 1.

Part II, Sections 11-12, consolidated pages 19-22, considers finite-state noisy discrete channels.
It defines information rate as `R = H(x) - H_y(x)` and capacity as
`C = Max_(input sources) (H(x) - H_y(x))`, measured per second or per symbol. An independently
perturbed memoryless channel is only the one-state special case. The paper later allows an
approximating source if the maximum is not attained, so transcription must decide maximum versus
supremum and the required assumptions rather than copying notation mechanically.

Section 14, Theorem 12, consolidated pages 24-25, defines `N(T,q)` as the maximum size of an
equal-probability selected subset of duration-`T` signals, decoded by selecting the most probable
cause, with probability of incorrect interpretation at most `q`. It states
`lim_(T -> infinity) log N(T,q) / T = C` provided `q` is neither zero nor one. This gives the
catalog gloss an operational, truth-valued reading, but choosing it would be a substantive target
decision rather than a source-preserving transcription.

Part IV, Section 24, consolidated pages 41-42, treats continuous bandlimited channels and defines
capacity through a `T -> infinity` normalized maximum of a mutual-information integral over input
ensembles. Its domains and analytic obligations differ materially from all discrete candidates.

## Component crosswalk

| Repository element | Primary-source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `信道容量` | noiseless, noisy discrete, and continuous capacity definitions plus multiple capacity theorems | one exact canonical `Prop`, or a corrected definition target routed outside ordinary theorem proof | strong family match; artifact kind and exact root open |
| `信道的最大传输速率` | maximum allowed-signal growth, maximum information rate, or operational reliable-message growth | exact channel model, rate function, optimization and limit predicates | gloss collapses non-equivalent definitions and theorems |
| Claude Shannon / 1948 | two-part Bell System paper | immutable edition and source identity | bibliographic identity established; correction/errata admission and independent review open |
| `已验证` | untrusted inventory label | reviewed human source and kernel receipt would be required | no H or M credit |

## Candidate-root crosswalk

| Candidate root | Material content | Why not canonical at intake |
|---|---|---|
| Noiseless definition | asymptotic logarithmic growth of allowed signal count per unit time | a definition, not a theorem; general limit-existence assumptions are absent |
| Noiseless Theorem 1 | determinant/largest-root capacity formula for finite-state constraints | narrow channel class and incorporated graph/Appendix assumptions absent from the catalog |
| Noisy discrete definition | maximum information rate over all input sources | a definition whose maximum/supremum, source class, entropy-rate existence, and normalization need selection |
| Theorem 12 | operational limit of reliably distinguishable signal-set cardinality for nontrivial `q` | adds decoder, equiprobability, error, asymptotic, and finite-state noisy-channel semantics absent from the gloss |
| Continuous definition | normalized asymptotic maximum mutual-information integral | changes the domain to continuous bandlimited ensembles and imports substantial analytic structure |
| Modern finite-DMC formula/maximizer | capacity as a supremum or maximum of single-letter mutual information, possibly with an attaining prior | modern, narrower memoryless formulation absent from the catalog and historical statement |

## Repository boundary records

`Docs/researches/math_theorems.md:11623-11656` separately lists information theory, Shannon
entropy, channel capacity, the noisy-channel coding theorem, and the noiseless coding theorem. The
target must not absorb those roots merely because capacity is a definition used in coding proofs.

`Docs/researches/cs_theorems.md:599-608` separately lists channel coding, noisy-channel coding,
capacity converse, joint source-channel coding, and Gaussian channel capacity. These are Stage0
discovery records rather than this rev-5.6 target, but their separation confirms that coding,
converse, separation, Gaussian specialization, and general capacity must not be merged by default.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`PMF`, `ProbabilityTheory.Kernel`, `IsMarkovKernel`, `Real.binEntropy`,
`InformationTheory.klDiv`, its composition-product chain rule,
`InformationTheory.UniquelyDecodable`, and `hammingDist`. A bounded exact-topic search found no
channel-capacity or mutual-information declaration in pinned mathlib or repository-local Lean.
The sole repo-local topic hit is an audit metadata string naming the external project
`abenenson/channel-capacity` at commit `a212a605d3ec5a23034e0c40f51b2b92d594efa5`. The string is
not a declaration or proof artifact. Read-only inspection shows that the referenced project defines
capacity as a supremum of mutual information and contains capacity-achieving-prior existence
results, making it an unaudited candidate lead for the later anchor audit, not proof credit for an
unselected canonical root.

These are supporting interfaces and discovery leads only. The canonical module, namespace, declaration/expression,
ordered binders, imports, elaborated expression hash, checked transports, and statement mutations
remain null. The probe and search do not constitute the exhaustive downstream candidate audit or
proof of global absence.

## Source and statement gate

Before ordinary theorem-proof execution, accountable reviewers must decide whether this noun entry
is eligible as a theorem target or must be corrected, and then select one stable truth-valued
proposition. They must preserve an immutable primary or authoritative edition, transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, channel/rate/error convention,
proof boundary, correction, and erratum, reconcile neighboring records, and independently approve
the mapping. The statement phase must then freeze minimal imports, the elaborated expression and
environment fingerprint, checked alternate transports, and removed-hypothesis, changed-domain,
binder-scope, and boundary mutations.

Until then, `H5` records that the received catalog wording is not one stable proposition. It does
not refute Shannon's definitions or theorems. The canonical mathematical and Lean targets remain
null, and the downstream anchor audit remains open.
