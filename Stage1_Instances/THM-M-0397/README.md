# THM-M-0397: Baker method

## Intake verdict

This is a rev-5.6 `planned` instance at `L0 / rework_required`. The repository's
source wording, "effective solution methods for Diophantine equations", names a
method and a family of applications rather than one exact theorem. Consequently
the canonical claim, binders, hypotheses, conclusion, and boundary cases are not
yet frozen. No theorem completion, Lean closure, H0, M0, or R0 is claimed.

The neighboring target THM-M-0396 owns lower bounds for nonzero linear forms in
logarithms. This target owns an application pipeline: a specified Diophantine
problem is reduced to such a lower bound, an explicit height/coefficient bound is
derived, and the remaining finite search is certified. A later statement phase
must select one precise application or rigorously quantify an admissible class;
it may not turn the current broad label into a theorem by fiat.

## Scope map

| Surface | Included in this target | Excluded or not yet fixed |
|---|---|---|
| Mathematical role | Effective Diophantine application of a Baker-type logarithmic lower bound | The lower-bound theorem itself (THM-M-0396) |
| Input | A future, explicitly specified equation/problem, solution type, height, and reduction certificate | "All Diophantine equations" and unspecified decidability claims |
| Output | A future explicit bound plus kernel-checked finite-search closure | An algorithm, complexity bound, or numerical answer without a selected problem |
| Formal surface | Lean 4 with pinned mathlib; legacy `S1_M_010.lean` is discovery input only | Any inherited proof/status credit from the legacy artifact |
| Current phase | Dossier, ambiguity record, source crosswalk, and open task DAG | Statement elaboration, anchor acceptance, proof, validation, or release |

## Source-statement crosswalk

| ID | Record | Mapping and boundary | Status |
|---|---|---|---|
| SRC-REPO-1 | `Docs/researches/math_theorems.md`, entry "贝克方法", lines 2884-2889 in this revision | Supplies only the name, 1966 date, and broad Chinese sentence. Its `已验证` label is explicitly untrusted by the rev-5.6 manifest. | located; insufficient for H0 |
| SRC-STAGE0-1 | `Docs/Stage0_Blueprint.md`, THM-M-0397 | Repeats the broad sentence and marks definitions, assumptions, proof, and dependencies as pending. | located; confirms underspecification |
| SRC-LEGACY-1 | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_010.lean` | Models an abstract Baker-method pipeline and explicitly says it does not supply a Baker lower-bound theorem. It is a discovery hint, not the exact source statement or accepted evidence. | legacy; zero proof credit |
| SRC-PRI-1 | Alan Baker, "Linear forms in the logarithms of algebraic numbers. I", *Mathematika* 13 (1966), 204-216, DOI `10.1112/S0025579300003971` | Primary historical anchor for the logarithmic lower-bound engine. It does not by itself state the repository's broad method claim or select a Diophantine application. | candidate for later source audit; not H0 |

No primary source presently crosswalks the repository sentence to a unique theorem
with exact assumptions and conclusion. The first statement-phase gate is therefore
to select and document a primary-source application theorem (edition, theorem/page,
assumptions, and errata) or to reject the label as non-unique. Until then the exact
statement remains M3 and human-source fidelity remains H3.

## Open task DAG

`STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
All six tasks are open. `STATEMENT` must resolve `SRC-GAP-1`, the missing unique
source theorem, before Lean elaboration can receive exact-statement credit.

## Validation record

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

The intake was checked with the repository standard validator, target-manifest
validator, target query, JSON parser, and whitespace checker. Exact commands and
results are recorded in `validation.md`. These checks validate intake structure
only; they are not kernel evidence for THM-M-0397.
