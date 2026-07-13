# THM-M-0958 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry `Elkin
construction`. The repository supplies only the gloss `improvement of the Behrend construction`,
attributes it to Michael Elkin in 2011, and labels it verified. Under rev-5.6 that label is
untrusted inventory metadata, not an exact source statement or proof evidence.

An inspected primary-source lead identifies the intended family much more closely: Michael
Elkin's *An Improved Construction of Progression-Free Sets*, arXiv `0801.4310v1` (2008), later
published in *Israel Journal of Mathematics* 184 (2011), pages 93-128, DOI
`10.1007/s11856-011-0061-1`. The preprint defines progression-free subsets of
`{1, ..., n}` and reports an asymptotic lower bound improving Behrend by a factor of order
`sqrt(log n)`. The inspected arXiv version is a strong source lead, but the catalog does not cite an
edition, the final journal text was not admitted and cross-checked, and exact formula transcription,
source-version differences, assumptions, corrections, errata, and independent review remain open.
No `H0` claim is made.

Pinned mathlib supplies `ThreeAPFree`, `rothNumberNat`, interval translation infrastructure, and a
machine-checked Behrend lower bound. `IntakeProbe.lean` authenticates those interfaces. The pinned
Behrend result has a different, weaker quantitative bound; it is not Elkin's improvement and is not
credited as a target proof.

The catalog gloss still does not freeze the domain encoding, ordered asymptotic binders, exact
base-2 formula, constant and threshold semantics, progression predicate, one-based to zero-based
transport, or boundary cases. Intake does not silently choose those proposition-changing details.
The provisional vector is `[H1, M4, R4]`: a matching published proof source is known but not fully
audited, no usable exact formal artifact is credited, and no source-faithful readable
proof reconstruction is available.

`instance.json` is the structured scope authority and `task-dag.json` keeps all six downstream
phases open. No canonical proposition, exact Lean target, accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
