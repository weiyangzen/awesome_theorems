# THM-M-0689 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "proof
complexity". The repository gives only the gloss "lower bounds on proof length", attributes it to
Stephen Cook, and dates it to 1971. That describes a research area, not a unique theorem.

A proof-length lower bound is meaningful only after fixing at least a proof system, the represented
formula or formula family, the size encoding, and the asymptotic lower-bound rate. Resolution,
bounded-depth Frege, Frege, extended Frege, cutting planes, and algebraic proof systems have
materially different known bounds. The adjacent Haken entry is specifically about the pigeonhole
principle and therefore cannot silently supply this target's missing scope.

The intake freezes this ambiguity and exclusion boundary rather than inventing a theorem. The root
remains `[H3, M4, R4]`. A pinned Lean probe confirms only that mathlib supplies generic encodings,
encoded-string length, and asymptotic comparison APIs that could be ingredients of a future target;
it is not a statement or proof. Exact commands and results are recorded in `validation.md`.
