# Machine-checked audit

The files `Statement.lean`, `Proof.lean`, and `Audit.lean` elaborate with the repository-pinned Lean toolchain under `lake env lean --trust=0`. Their executable declarations are theorem-only identity transports over `IsGreatest admissibleConstants 1`; hence the checked transport has no axioms and no remaining machine cut.

The exact provider source is separately pinned by revision, module, member path, file digest, declaration digest, declaration-type digest, and raw-block digest. `Erdos1026.erdos_1026.variants.eq_one` is explicitly named in all three Lean audit surfaces and in the crosswalk. Because the bootstrap package does not make the Formal Conjectures module directly importable in the canonical Lake graph, the transport declarations compile against pinned Mathlib and the frozen module spelling is carried as an exact semantic audit marker. The frozen validator checks that marker, the pinned provider bytes, the no-shadow policy, all sealed semantic fields, and then reruns trust-zero compilation.

The machine claim is therefore scoped precisely: M0-L for the claim-owned transport declarations, with the canonical Master still required to independently recompute the elaborated provider expression and decide integration. No worker receipt sets `master_accepted`.
