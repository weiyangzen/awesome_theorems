# THM-M-0702 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "unification
algorithm". The source inventory supplies only the gloss "an algorithm for unifying terms",
attributes it to John Alan Robinson in 1965, and marks it `已验证`. It does not state a theorem.

An algorithm is not by itself a proposition. A faithful target must fix the term signature,
variables, substitutions and their composition/order, the input problem (two terms or a finite set
of equations), the occurs check, the success/failure result, and the exact correctness claim. At
least soundness, completeness/existence detection, most-generality, and termination are distinct
claims. Choosing one combination from the metadata would substitute invented mathematics.

The intake therefore freezes that ambiguity and the exclusion boundary, not a canonical theorem.
The root remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib exposes first-order terms,
variables, relabeling, and substitution needed to encode candidate formulations; it is not an
implementation or correctness proof. Exact commands and results are in `validation.md`.
