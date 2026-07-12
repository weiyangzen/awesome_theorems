# Source-statement crosswalk

## Repository record

| Catalog component | Repository evidence | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Target identity | `Docs/researches/math_theorems.md`: `LDPC码` | Future canonical namespace and declaration | Stable UID and subject only |
| Attribution and date | Robert Gallager, 1963 | Provenance metadata | Consistent with Gallager's 1963 monograph, but not a theorem locator |
| Literal claim | `低密度奇偶校验码` | No expression | A noun phrase naming a code family, not a proposition |
| Source status | `已验证` | No receipt | Explicitly untrusted metadata; no H or M credit |
| Exact premises and result | Marked `待补充` in Stage0 | Ordered binders, hypotheses, conclusion | Absent; canonical statement remains null |
| Proof and formal artifact | Marked `待补充` in Stage0 | Proof body, wrapper, or pinned dependency | Absent |

The computer-science catalog separately lists `THM-C-0385`, attributes the topic to Gallager and
MacKay over 1963-99, and uses the same noun-phrase gloss. That entry is not in the Stage1 Lean target
set. It is a neighbor/duplicate subject record, not authority to broaden or select `THM-M-1593`.

## Primary-source lead

Robert G. Gallager, *Low-Density Parity-Check Codes*, MIT Press, 1963, DOI
`10.7551/mitpress/4347.001.0001`, is an authoritative source-family lead. An externally hosted
90-page scan was inspected for intake discrimination (observed SHA-256
`3ce9a28ba5abfbcd453a75e4d1f61ffc9d2e7ce7c6b3a22f309496320b80c7e0`). Crossref independently
identifies the monograph, author, publisher, date, DOI, and ISBN. Gallager's journal article,
"Low-density parity-check codes," *IRE Transactions on Information Theory* 8(1), 1962, pages 21-28,
DOI `10.1109/TIT.1962.1057683`, is a second primary bibliographic lead.

Neither source is admitted as H0. The repository cites no edition or exact result; no accepted local
source copy, full theorem/premise/errata crosswalk, proof-boundary audit, or independent source review
exists. The scan and bibliographic metadata are discovery inputs only.

## Source-family alternatives

| Gallager source component | Prospective Lean target surface | Intake assessment |
|---|---|---|
| Regular low-density parity-check construction: a binary parity-check matrix with fixed small column weight `j` and row weight `k` | Finite index types, matrix over `ZMod 2`, row/column support counts, kernel code | Definition and ensemble setup, not by itself the catalog's theorem |
| Typical minimum distance grows linearly with block length for fixed degrees, with exceptional low-degree behavior | Ensemble probability, Hamming weight, nonzero kernel vectors, asymptotic lower bound | Plausible root family; exact theorem, constants, parameter restrictions, and probability convention not selected |
| Maximum-likelihood decoding error bounds on sufficiently quiet binary-input symmetric channels | Channel kernel, likelihood decoder, block-error probability, asymptotic exponent | Distinct root family; channel and decoding semantics absent from the repository |
| Comparison with random codes at a related rate | Two ensembles, rate relation, matched error criterion | Cannot be merged with the distance or decoder theorem without source authority |
| Iterative probabilistic decoding bound on a binary symmetric channel | Tanner graph/messages, iterations, local-tree analysis, error event and finite/asymptotic bound | Distinct algorithmic theorem with materially different binders and hypotheses |
| Linear decoder equipment/data-handling scaling | Explicit machine and cost model | Complexity result, not automatically a mathematical distance/error theorem |
| Stronger observed or hypothesized decoding behavior | Formal conjecture or experiment boundary | Must not be presented as a proved theorem |

The 1962 article abstract likewise combines the definition, typical distance growth, ML error decay,
an iterative decoder, complexity claims, a weaker proved decoding bound, and experimental results.
That confirms family ambiguity rather than selecting a root.

## Pinned Lean discovery surface

| Pinned module/declaration | Possible role | Credited status |
|---|---|---|
| `Mathlib.InformationTheory.Hamming`: `hammingDist`, `hammingNorm`, `Hamming` | Word distance and weight substrate | API availability only |
| `Mathlib.LinearAlgebra.Matrix.ToLin`: `Matrix.mulVec`, `Matrix.mulVecLin` | Parity-check linear map substrate | API availability only |
| finite functions, matrices, and `ZMod 2` transitively available under those imports | Candidate binary word/check representation | No canonical encoding selected |

A bounded case-insensitive search of pinned mathlib and repo-local Lean found no `LDPC`,
`low-density parity-check`, or exact `parity-check code` declaration. A negative lexical search is
not an exhaustive formal-candidate audit and cannot prove nonexistence under another encoding.
`IntakeProbe.lean` merely authenticates the generic APIs above at the pinned revisions.

## Required source acceptance

Before the statement phase can pass, an accountable source decision must select one proposition and
record an immutable edition, stable source identifier, theorem/equation/section/page locator, exact
ordered premises and conclusion, incorporated definitions, proof dependencies, errata/correction
status, translation decisions where relevant, and independent review. The crosswalk must then map
every ensemble, algebra, channel, decoder, probability, rate, asymptotic, and boundary convention to
the Lean target. Until then the exact statement and expression fingerprint remain null, human status
is at most `H1`, and no machine or theorem-completion claim is legal.
