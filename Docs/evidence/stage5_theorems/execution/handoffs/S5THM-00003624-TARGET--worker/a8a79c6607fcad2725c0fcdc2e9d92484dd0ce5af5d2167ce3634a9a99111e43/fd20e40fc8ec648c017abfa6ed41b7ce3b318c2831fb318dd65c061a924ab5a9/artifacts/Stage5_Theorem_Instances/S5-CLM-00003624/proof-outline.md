# Proof outline

1. Import the pinned source module `FormalConjectures.ErdosProblems.1057`.
2. State the target with fully qualified provider symbols.
3. Apply the exact frozen declaration `Erdos1057.erdos_1057.variants.agp_infinite`.
4. Check identity transports in both directions; no conversion or semantic substitution is needed.
5. Replay each claim-owned Lean file at trust zero and leave final semantic acceptance to the Master.

There are no mathematical side conditions or exceptional input cases because the theorem is an unconditional convergence statement. The material exception is evidentiary: the pinned source file contains a placeholder in the provider theorem body, so the worker must never infer historical proof provenance merely from source prose or bytes. The release candidate instead records the exact explicit provider dependency and requires independent Master recomputation.
