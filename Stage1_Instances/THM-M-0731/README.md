# THM-M-0731 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`去随机化` (derandomization). The only supplied claim is `随机算法的确定化` (turning randomized
algorithms into deterministic ones). That phrase names a research area, not a unique theorem.

It is compatible with materially different claims: fixing a finite random seed non-uniformly,
simulation with advice such as `BPP subseteq P/poly`, conditional hardness-versus-randomness
theorems, or the general `BPP = P` conjecture. These differ in uniformity, complexity overhead,
error model, assumptions, and even whether the claim is known. Choosing one would substitute a
new theorem for the repository record.

The intake therefore freezes this ambiguity and the exclusion boundary. The root is
`[H5, M4, R4]`: the current wording is not a stable proposition, no exact formal artifact is
identified, and there is no proof reconstruction. A pinned Lean probe checks only that finite
probability distributions and polynomial-time Turing-machine interfaces are available as possible
encoding ingredients. It is not a target statement or proof. Validation is recorded in
`validation.md`.
