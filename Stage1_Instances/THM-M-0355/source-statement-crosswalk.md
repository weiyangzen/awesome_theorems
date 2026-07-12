# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names `Meyer小波`, attributes it to Yves Meyer, dates it to
1985, and states only `光滑小波的构造` ("construction of smooth wavelets").
`Docs/Stage0_Blueprint.md` repeats this gloss while leaving exact definitions, assumptions, proof
route, axioms, equivalent statements, and formal artifacts open. The manifest preserves `已验证`
only in the explicitly untrusted `source_status_untrusted` field.

The gloss is not a complete proposition: it supplies no quantified witness, function class,
frequency window, support bounds, normalization, or conclusion. The attribution and year are
locators, not an inspected proof source.

## Candidate source work

An original Meyer publication or an authoritative wavelet text containing the explicit smooth
frequency-window construction is a source-audit lead. Intake did not select or independently
inspect an immutable edition, theorem/definition number, page range, assumptions, proof boundary,
or errata. No lead therefore receives `H0` credit. The statement phase must crosswalk the exact
source formulas rather than reconstruct a standard-looking variant from memory.

## Crosswalk

| Repository phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "construction" | explicit cutoff/window followed by a mother-wavelet definition | source-faithful definitions and an existential or named witness theorem | formulas and theorem boundary absent |
| "smooth" | `C^infinity`, Schwartz, or another stated regularity class | `ContDiff`, `SchwartzMap`, or a checked equivalent | exact strength open; Schwartz API probed |
| "wavelet" | dyadic dilates and integer translates of a mother function | explicit `Z x Z` indexed family in the selected `L^2(R)` model | indexing and normalization open |
| Meyer | source-specific frequency-window and partition identities | predicates for support, symmetry, overlap, and partition formulas | exact variant and constants open |
| frequency construction | compactly supported smooth Fourier-side window and inverse transform | Schwartz Fourier transform plus support statements and transports | Fourier convention and bounds open |
| basis, if asserted | orthonormality and completeness of the generated family | `OrthonormalBasis`/`HilbertBasis` or orthonormality plus dense span | conclusion not present in repository gloss |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks Schwartz maps and their Fourier transform, the `L^2` Fourier isometry interface, and
orthonormal/Hilbert basis interfaces. A bounded name/content search over the repository and pinned
mathlib found no Meyer-wavelet-specific declaration. This is an intake observation only, not the
later immutable anchor audit and not a proof of global absence.

Before statement credit, each selected source component must map to an elaborated expression and
each alternate convention must have a kernel-checked transport. Before `H0`, an independent
reviewer must approve the source edition, exact passage, definitions, assumptions, proof boundary,
and errata record.
