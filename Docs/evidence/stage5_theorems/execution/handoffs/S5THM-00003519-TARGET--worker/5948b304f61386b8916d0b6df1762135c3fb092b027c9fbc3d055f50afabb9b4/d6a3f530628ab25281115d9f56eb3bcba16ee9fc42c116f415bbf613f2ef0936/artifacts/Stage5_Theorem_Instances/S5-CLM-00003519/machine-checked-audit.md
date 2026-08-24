# Machine-closure audit — S5-CLM-00003519

The proposed root is
`AwesomeTheorems.Stage5.S5_CLM_00003519.rank_2_2_machine`, at level `M0-L`:
its body is claim-owned and does not call the provider theorem. The proof uses a
diagonal transposition, a kernel-reducible exhaustive decision for permutations
of `Fin 2`, the exact provider kernel definitions, and subgroup closure rules.

Static review found no `sorry`, `admit`, custom axiom, opaque declaration,
unsafe declaration, native decision oracle, local semantic definition,
notation/syntax/macro substitution, namespace alias, or alternate import. The
provider theorem's `sorryAx` body is not in the root dependency graph.

`Audit.lean` contains both required terminal checks: an exact `type_of%` witness
from the provider declaration to the fully qualified claim root, and
`#print axioms` for that root. The previous Master compilation established that
the proof elaborates but rejected the checkpoint's empty terminal report. This
generation therefore records the printed standard logical dependencies
`propext`, `Classical.choice`, and `Quot.sound`. The worker does not invoke Lean;
Master must independently reproduce that exact ordered report, along with all
elaborated/type/body/dependency digests, in the provider-native environment.
