# THM-M-0602 rev-5.6 intake

This directory is the fail-closed `planned` intake for the h-cobordism theorem. The repository's
literal claim is only "simply connected h-cobordisms and diffeomorphism". The provisional scope is
the classical high-dimensional smooth theorem: a compact simply connected smooth h-cobordism is
trivial, subject to the dimension, boundary, and relative-diffeomorphism conventions fixed from an
inspected primary source.

Those conventions are not recoverable from the short repository gloss alone. In particular, the
dimension may refer to the cobordism or its boundary, and "trivial" is stronger than merely saying
that the two ends are diffeomorphic. The exact source theorem and Lean expression therefore remain
open. The provisional root vector is `[H3, M4, R4]`; no elaboration, source fidelity, proof, audit
completion, or theorem completion is claimed.

The scope map records the intended theorem family and its exclusions, the source crosswalk keeps
repository metadata separate from primary evidence, and the task DAG leaves every downstream
rev-5.6 phase open. Intake checks and their exact results are recorded in `validation.md`.
