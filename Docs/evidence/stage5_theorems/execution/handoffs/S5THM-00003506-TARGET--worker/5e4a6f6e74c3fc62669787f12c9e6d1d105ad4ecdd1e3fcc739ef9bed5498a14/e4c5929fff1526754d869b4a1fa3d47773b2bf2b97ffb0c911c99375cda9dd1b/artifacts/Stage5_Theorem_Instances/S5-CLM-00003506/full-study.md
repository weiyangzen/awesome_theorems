# Full study — Furstenberg times-p, times-q answer normalization

## Frozen statement

The record names `Arxiv.id2303_01089.conjecture_1_4`. Its right-hand side
universally quantifies natural numbers `p,q ≥ 2`, their multiplicative
independence, and atomless `T_p`-invariant probability measures on the
additive circle, and asserts convergence of the `T_(q^n)` pushforwards to
the Haar probability measure. The source prefixes that proposition with
`answer(False) ↔` to record the published negative resolution.

## Trust boundary

The pinned source file authenticates only the statement bytes. Its open proof
body is outside the accepted foundation profile and is not a proof dependency.
The claim-owned files therefore preserve the exact source import and qualified
name only inside comments and elaborate against `Mathlib` alone.

## A-forward — eliminating the answer surface

Hypotheses: a proposition `P`, an equivalence `False ↔ P`, and an assumed
proof of `P`. Inference: apply the `P → False` projection of the equivalence.
Output: `False`, discharging the assumed proof and yielding `¬ P`. Formal
anchor: `answer_false_to_negation` / `source_to_target_theorem`. Downstream
use: the left-to-right branch of the exact root. Exceptional case: none;
false elimination is not used in this direction. Trust boundary: Lean's
primitive implication and biconditional eliminators only.

## A-reverse — rebuilding the answer surface

Hypotheses: a proposition `P` and `h : ¬ P`. Inference: build the two arrows
of `False ↔ P`; the first follows by false elimination and the second is `h`.
Output: `False ↔ P`. Formal anchor: `negation_to_answer_false` /
`target_to_source_theorem`. Downstream use: the right-to-left branch of the
exact root. Exceptional case: the impossible `False` input is handled by
`False.elim`. Trust boundary: Lean's primitive false eliminator only.

## A-composition — closing the root

Hypotheses: the universally quantified proposition parameter `P`. Inference:
combine the forward and reverse fragments using biconditional introduction.
Output: `(False ↔ P) ↔ ¬ P`. Formal anchors:
`conjecture_1_4_claim_owned_root` and `audit_exact_root`. Downstream use: the
statement crosswalk and provisional release candidate. Exceptional case:
none. Trust boundary: the two preceding kernel-checkable fragments; no source
theorem body, external oracle, or claim-specific assumption enters the term.

## Semantic substitution checks

The three Lean files contain no declarations that can capture provider surface
symbols, no namespace alias, no notation/parser extension, and no provider
module import. Replacing the frozen provider revision, declaration digest,
source path, answer polarity, either implication, or the active `Mathlib`
import changes an authenticated field or breaks a required proof edge. These
mutations are therefore rejected by the evidence preflight or Master replay.
