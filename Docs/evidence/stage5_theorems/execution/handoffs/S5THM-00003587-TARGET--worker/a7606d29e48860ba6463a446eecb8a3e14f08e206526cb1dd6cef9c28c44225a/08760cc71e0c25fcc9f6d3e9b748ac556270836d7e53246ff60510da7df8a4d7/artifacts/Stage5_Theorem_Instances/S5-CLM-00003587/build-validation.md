# Build validation

The target package is intended for offline, cold-from-source replay.  Each
claim-owned Lean file imports `FormalConjectures.ErdosProblems.1037` exactly,
and each root term references `Erdos1037.erdos_1037` directly.  The frozen
validator command is the authoritative worker gate; its result is recorded in
the worker result command outcome.
