# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Strong `L^p` boundedness underlying the estimate | A. P. Calderon and A. Zygmund, "On the existence of certain singular integrals," *Acta Mathematica* 88 (1952), 85-139, DOI `10.1007/BF02392130` | No declaration selected | Primary paper and bibliographic span located, but theorem/page-level premise mapping and errata review remain open |
| Second derivatives controlled by the Laplacian on `R^n` | Standard PDE corollary obtained by representing second derivatives through singular-integral operators applied to `Delta u` | No exact expression selected | This is the Stage0 phrase "second derivative L-p estimate" made narrow enough for review; the Stage0 record itself does not fix the formulation |
| `1 < p < infinity` | Strong-type Calderon-Zygmund range | Exponent likely encoded by `ENNReal`/`Real` plus an `Lp` API | Endpoints are deliberately excluded; exact library representation is open |
| `u` smooth and compactly supported | Dense test-function formulation avoiding boundary and completion choices | Candidate `ContDiff` plus compact support predicate | Formal domain, measurability, integrability, and derivative encoding remain open |
| Hessian norm versus componentwise derivatives | Equivalent in finite dimension after choosing norms and constants | Fréchet derivative/Hessian or iterated partial derivatives | Choice changes the literal proposition and constant, so a checked transport is required before credit |

## Provenance boundary

The 1952 paper is a primary source for the singular-integral theorem family, but this intake does
not claim that the dossier's modern PDE inequality occurs there verbatim. A later source with an
explicit theorem statement must be pinned, or the corollary from the primary singular-integral
result must receive a premise-by-premise derivation. Edition/file hashes, exact theorem and page,
assumptions, errata/corrections, and independent review are all still required. Therefore no `H0`
claim is made.

Discovery locator (not an immutable evidence receipt):

- <https://doi.org/10.1007/BF02392130>

## Statement-phase decisions

1. Select the exact Hessian and `L^p` norm encodings and freeze the order of quantifiers for `C`.
2. Decide whether `n = 1` is retained as a degenerate but valid case or the analytic theorem begins
   at `n >= 2`; mutation-test that boundary.
3. Inspect pinned mathlib for the minimal imports and elaborate the literal target.
4. Check, rather than narrate, componentwise/Hessian and test-function/Sobolev transports.
5. Reject bounded-domain, endpoint, weighted, and variable-coefficient variants unless separately
   represented; none may silently substitute for this root.
