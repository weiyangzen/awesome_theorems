# THM-M-0502 rev-5.6 intake

This directory is the `planned` rev-5.6 intake for Page's theorem (also called the
Landau-Page theorem) on exceptional real zeros of primitive Dirichlet L-functions. The repository
source phrase, "existence of real zeros of L-functions", is too weak and too ambiguous to serve as
the theorem statement: the usual theorem is a uniform *at-most-one exceptional zero* result over a
bounded family of conductors.

The intake therefore freezes the intended theorem family and its exclusions, but leaves the exact
absolute constant, zero region, lower bound on the conductor cutoff, and any simplicity/character
properties to the source-pinned statement phase. The provisional root vector is `[H2, M4, R4]`.
There is no accepted proof state, exact Lean target, audit completion, or theorem completion.

The scope map and source-statement crosswalk record the ambiguity without silently choosing a
stronger or weaker variant. `IntakeProbe.lean` only checks that the pinned environment exposes the
basic complex Dirichlet-character L-function and a neighboring nonvanishing theorem; it is not a
formalization of Page's theorem. Exact commands and results are in `validation.md`.
