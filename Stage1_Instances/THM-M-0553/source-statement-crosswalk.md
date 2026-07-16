# Source-statement crosswalk

## Candidate primary source

J. F. Adams, "On the structure and applications of the Steenrod algebra", *Commentarii
Mathematici Helvetici* **32** (1958), 180-214, DOI `10.1007/BF02564578`. This is the primary
historical source for the mod-2 Adams spectral-sequence method and its applications to stable
homotopy. The exact theorem label, pages, hypotheses, notation, and any corrections must be checked
against a stable scan before the canonical claim or `H0` can be frozen.

This citation is a discovery anchor, not an evidence receipt. Later generalized or modern
formulations cannot silently supply hypotheses absent from the selected source statement.

## Crosswalk

| Metadata component | Source-level possibilities | Lean-side consequence | Intake disposition |
|---|---|---|---|
| "Adams spectral sequence" | classical mod-2, mod-`p`, or generalized construction | coefficient theory and resolution machinery must be selected | unresolved |
| "stable homotopy groups" | stable maps generally or stable stems of spheres | source/target spectra and grading must be bound explicitly | unresolved |
| "calculation" | convergence theorem, computational method, or particular stem values | a mathematical conclusion and convergence target must replace the gloss | blocking |
| no hypotheses | connectivity, finite type, completeness, and convergence conditions omitted | no exact ordered Lean binders are justified | blocking |

## Existing-source boundary

The generated Stage1 queue mentions topology, homotopy-adjacent, and (co)homology APIs only. That is
an infrastructure search hint, not evidence that mathlib contains the exact spectral sequence,
Steenrod-algebra `Ext` identification, or convergence theorem. Candidate Lean declarations and
external projects belong to the later anchor-audit phase and receive no intake proof credit.

Before `H0`, an independent reviewer must inspect the primary edition, record exact theorem/page
anchors and definitions, audit errata, and map every assumption and conclusion to the selected
canonical claim.

## Statement-phase disposition

The statement run at base `1cc6aa61bb055a5c032297ee457905c849af7608` did not admit any of the
candidate interpretations above. The mod-2 sphere form, an arbitrary-prime stable-maps form, and a
generalized Adams form remain materially different targets. Accordingly `statement.json` keeps
the canonical mathematical and Lean expressions null, and `Statement.lean` checks only adjacent
pinned interfaces. Its successful elaboration is not an Adams proposition or proof. The semantic
validator reports `phase_accepted=false`; the source-fidelity debt in this crosswalk remains
blocking.
