# THM-M-1078 rev-5.6 intake

This directory is the `planned` intake for the discrete-time martingale-transform inequality. The
intended claim is the qualitative `L^p` boundedness, for `1 < p < infinity`, of transforms of a
real-valued martingale by predictable scalar multipliers bounded in absolute value by one. The
exact source normalization, constant, indexing convention, and Lean encoding remain statement-
phase work.

The manifest's historical `已验证`, `1972`, and `Burkholder/Davis/Gundy` fields are untrusted
discovery metadata. They supply neither a precise theorem nor proof credit. In particular, this
intake does not silently substitute the BDG maximal/square-function inequality or a continuous
stochastic-integral theorem for the martingale-transform claim.

No canonical Lean expression or kernel proof is claimed. The provisional root vector is
`[H1, M4, R4]`; audit and theorem completion are false. `scope-map.md`,
`source-statement-crosswalk.md`, and `task-dag.json` delimit the downstream work. Exact intake
checks and results appear in `validation.md`.
