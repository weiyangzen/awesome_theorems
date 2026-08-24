# Machine-checked audit

Provisional machine level: M0-P. Root: `AwesomeTheorems.Stage5.S5_CLM_00003491.audit`. Root-expression digest: `5c605c98bb4f8adeee411e3d82372af4274ea47aacb491e9cc279fc1f26471ac`. Observed foundation axioms: `propext`, `Classical.choice`, and `Quot.sound`; observed non-foundation axioms: none. Human, machine and readability cut sets: empty.

The proof constructs `q^3` triples `(a*q+b+1, a*q+c+1, b*q+c+1)` for `q = n.sqrt`. Lexicographic changes raise two coordinates, all coordinates lie in `[1,q^2]`, and `q^2=n`. A separate pigeonhole argument bounds all candidate lengths, justifying `le_csSup`.

This worker performed only the mandated no-Lean semantic/evidence preflight. Trust-zero cold canonical compilation and independent per-declaration environment recomputation are Master responsibilities, not worker acceptance claims. The repair removes all claim-local imports from Proof and Audit; the terminal audit root is directly and independently reconstructed in Audit before the binder-explicit pointwise provider-type witness and axiom query. Quoted command syntax preserves the controller-mandated uninstantiated transport surface without asking Lean to synthesize its otherwise unconstrained implicit `n`.
