# THM-M-0984 validation-phase result

Item `S56-M-0984-VALIDATION` was run against the integrated proof-phase
snapshot. The narrow kernel, trust-observation, provenance, dependency-pin,
and placeholder gates pass for the exact frozen modern strong-law target.
`Validation.lean` separately restates that exact target and applies the pinned
terminal declaration without importing `Proof.lean`.

## Exact result

The structured recipe in `validation-spec.json` was run from repository root
on 2026-07-12:

```text
python3 Stage1_Instances/THM-M-0984/check_validation.py
  exit 0
  PASS narrow kernel replay: exact proof, frozen composition, and separately written exact-target probe elaborated
  PASS trust observation: three root-relevant declarations report only propext, Classical.choice, and Quot.sound
  PASS local provenance: frozen input hashes, registry denominator, clean pinned mathlib, toolchain, and manifest agree
  STALE authoritative graph: terminal/root remain open pending master reconciliation with proof evidence
  BLOCKED release gates: shared warm .lake, incomplete TCB/SBOM archive, unresolved H1/R3, and no distinct runner
```

The validator copies the four Lean sources into a fresh temporary directory
under `Formalizations/Lean`, invokes only `lake env lean`, and removes all
temporary output. It verifies mathlib is clean at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. No update, build, clone, fetch,
network access, or dependency mutation is performed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Statement, obligation composition, proof, and separate exact-target probe elaborate with pinned Lean 4.29.0/mathlib. |
| Placeholder/unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in the four checked modules. |
| Trust observation | provisional pass | `terminalStrongLaw`, `strongLawRoot`, and `independentStrongLawTarget` report exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Provenance and pins | pass | Input hashes, statement/registry link, denominator, toolchain manifest, clean mathlib worktree, and immutable revision agree. |
| Structured state | stale, fail closed | The frozen graph predates `Proof.lean`; it still reports `root_closed=false` and `M0984-L-TERMINAL` open. Master reconciliation is required. |
| Hermetic release replay | fail closed | This worker reused shared writable warm `.lake`; no clean checkout, empty-cache cold build, offline restore, complete TCB inventory, or SBOM/license closure exists. |
| Independent verification | fail closed | The separate source probe ran in this same clone/cache. There is no distinct identity and runner, second signed attestation, or independently implemented evidence verifier. |
| Source/readability | fail closed | The Borel-versus-modern-source identity remains H1 and readable reconstruction remains R3. |

This validation node is self-tested but not release evidence. It grants no
`AUDIT-Z`, `THEOREM-Z`, theorem completion, release, or master-acceptance
credit. The first release failure is the hermetic cold-build gate; source,
readability, independent-runner, and stale-state gates also remain open.
