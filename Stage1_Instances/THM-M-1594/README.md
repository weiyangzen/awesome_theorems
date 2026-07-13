# THM-M-1594: Turbo codes

## Intake verdict

This directory is the rev-5.6 `planned` intake for `S56-M-1594-INTAKE`. The repository supplies the
name `Turbo码`, an attribution to Claude Berrou and Alain Glavieux in 1993, and the gloss
`接近香农限的码` (a code near the Shannon limit). It does not supply one stable truth-valued
proposition. The canonical mathematical statement and Lean expression therefore remain null.

The received catalog target is provisionally `[H5, M4, R4]`. Here `H5` classifies the catalog gloss
as ill-posed for theorem execution; it does not refute established results about turbo codes.
`M4` records that no usable exact formal artifact has been located, and `R4` records that no
source-selected proof route can yet be reconstructed.

## Blocker

The statement phase must first select an immutable primary-source proposition and freeze its turbo
construction, constituent convolutional encoders, interleaver and termination or puncturing rules,
channel, decoder, rate and block-length regime, error metric, probability and asymptotic
quantifiers, numerical constants, and proved-versus-empirical boundary. Construction, decoder
correctness, finite simulation, analytic error bounds, distance-spectrum claims, and asymptotic
capacity or threshold claims are inequivalent and cannot be substituted for one another.

## Artifacts

- `instance.json` is the structured scope authority for this planned intake.
- `scope-map.md` records unresolved decisions, boundaries, and degenerate cases.
- `source-statement-crosswalk.md` separates the catalog wording from bibliographic leads.
- `task-dag.json` keeps all six downstream nodes open.
- `IntakeProbe.lean` authenticates adjacent pinned APIs only.
- `check_intake.py`, `validation.md`, and `intake-receipt.json` record the scoped self-test.

No accepted proof state, exact-statement fingerprint, obligation registry, proof, audit completion,
theorem completion, or master acceptance is claimed.
