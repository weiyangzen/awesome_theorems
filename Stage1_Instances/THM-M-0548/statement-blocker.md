# Exact-statement gate: blocked

Item: `S56-M-0548-STATEMENT`
Theorem: `THM-M-0548`
Base revision: `1cc6aa61bb055a5c032297ee457905c849af7608`

## Decision

The exact Lean 4 target cannot yet be frozen truthfully. The repository source record says only
"duality for subspaces in a sphere." The intake selected a conservative classical variant for a
compact locally contractible subset `A` of `S^n`, but deliberately deferred the choices required
to turn that prose into one proposition:

- the coefficient ring or coefficient object and whether coefficients are constant or local;
- the concrete reduced singular homology and reduced singular cohomology constructions;
- homological versus cohomological orientation of the displayed isomorphism;
- integer grading and the treatment of `n - i - 1`, rather than truncated `Nat` subtraction;
- whether naturality is part of the root conclusion and, if so, its category of admissible maps;
- the empty/full subset, `n = 0`, and out-of-range degree policies.

These are semantic choices, not Lean syntax. Different choices produce non-equivalent targets. In
particular, the pinned mathlib snapshot exposes ordinary singular chains and homology, but the
repository contains no selected reduced singular cohomology construction for this topological
claim. Inventing an opaque cohomology object, or accepting an isomorphism as an input field, would
substitute a statement shape for Alexander duality.

The legacy `AwesomeTheorems.Stage1.S1_M_120.StatementShape` does exactly that: its
`AlexanderDualityData` asks the caller to supply `subsetReducedCohomology`, the degree shift, and
`dualityIso`; it also uses ordinary complement singular homology and only assumes that the carrier
is closed. It neither expresses the intake-selected compact/local-contractibility hypotheses nor
constructs the theorem's reduced theories. It is therefore discovery input only and cannot supply
canonical-statement identity, a checked transport, or proof credit.

Consequently section 5.1's exact-statement gate fails before expression serialization and mutation
testing. No canonical declaration, expression hash, alternate-encoding credit, statement
acceptance, or theorem completion is claimed. The negative boundary itself is self-tested and is
handed off as `[_]`; that state records checked blocker evidence, not positive phase closure.

## Dependency and claim order

The exact v2 claim key is `(v2_execution_rank=336, phase_layer=1,
phase_item_id=S56-M-0548-STATEMENT)`. The authoritative `parent_inspection_order` is `[]`: there is
no admitted direct hard parent, transitive hard ancestor, reuse hint, or shared lemma group. The
schema-1.1 dependency ledger records that empty traversal. No provider declaration, body, receipt,
checkbox state, or acceptance was consumed or transferred. An empty admitted closure is not a
claim that Alexander duality is mathematically independent of other results.

## Checked Lean boundary

`Statement.lean` uses the smallest pinned imports found for the unambiguous substrate:

```lean
import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Topology.Category.TopCat.Sphere
import Mathlib.Topology.Homotopy.LocallyContractible
```

It elaborates the sphere subset and complement, the conjunction `IsCompact A ∧
LocallyContractibleSpace A`, and the available ordinary complement singular-homology object. It
deliberately declares no canonical Alexander-duality proposition, proof, axiom, or proxy predicate.

## Environment and validation evidence

Commands ran from this worker clone on 2026-07-17. Lean commands ran from `Formalizations/Lean`
against the existing canonical `.lake` symlink. No update, build, fetch, or clone was performed.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- v2 theorem DAG SHA-256:
  `e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b`.
- Dependency context SHA-256:
  `068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
- `Statement.lean` SHA-256:
  `c70ec17e76aa2dff0ad5aac5597df7220478c96f6fcdc90b1dada916721f4895`.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean --trust=0 ../../Stage1_Instances/THM-M-0548/Statement.lean` | 0 | subset hypotheses and ordinary complement singular-homology types elaborated and printed; no canonical target declared |
| three direct-import deletion replays | 1 each | deleting singular homology, sphere, or local-contractibility respectively makes its credited boundary symbol unknown, so all three boundary-probe imports are necessary |
| `lake env lean --version` | 0 | Lean version and commit match the fingerprint above |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | mathlib revision matches the Lake pin above |
| `python3 Docs/tools/check_stage1_standard.py` | 1 | Expected worker-local evidence-inventory drift: the fresh deterministic theorem DAG sees the new target-owned statement artifacts, while only the master may regenerate the read-only DAG projection |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | Expected worker-local evidence-inventory drift for the same target-owned additions; no authority file was edited |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0548` | 0 | rank 120, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0548/check_statement.py` | 0 | one typed JSON object reports `status=blocked`, `phase_accepted=false`, and the exact first failed gate |

Known failure: without an authoritative coefficient, reduced-theory, grading, naturality, and
boundary-case decision, the canonical expression and meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutations cannot be produced.

## Retry condition

An accountable source reviewer must select and pinpoint a stable formulation and freeze every
choice listed above. The statement phase can then implement the actual reduced (co)homology types,
minimize imports, serialize the elaborated expression, and run all four mutation classes.

Until then, statement acceptance and theorem completion are false. A zero validator exit means only
that this negative packet is internally consistent; it does not turn the blocker into a positive
statement result or master acceptance.
