# THM-M-0372 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Carleson
measure theorem". The source inventory supplies only "characterization of Carleson measures",
attributes it to Lennart Carleson, and gives 1962. It does not state a proposition or cite a work.

The label covers materially different formulations. A disk or upper-half-plane box condition can
be characterized by a bounded embedding of a Hardy space into an interior `L^p` space; other
versions use reproducing kernels, Poisson extensions, different exponents, or other domains. These
are not definitionally interchangeable, and constants and boundary conventions are part of an
exact claim. Selecting one from the title alone would substitute invented mathematics.

The intake therefore freezes that ambiguity and the exclusion boundary, not a proposition. The
root remains `[H1, M4, R4]`: the named classical theorem is treated as published but its exact
source statement has not been audited. A pinned Lean probe confirms only that basic measure,
restriction, integration, integrability, metric-ball, and interval APIs elaborate. Exact commands
and results are recorded in `validation.md`; no theorem or proof is claimed.
