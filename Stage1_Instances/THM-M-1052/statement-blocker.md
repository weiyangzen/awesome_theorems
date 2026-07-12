# Exact-statement gate: blocked

Item: `S56-M-1052-STATEMENT`  
Base revision: `08764d477205bbae07c32197a9a83ac6c07866c9`

## Decision

The exact Lean 4 target cannot be truthfully frozen from the accepted inputs. The repository's
entire source claim is `不变测度的存在性` ("existence of an invariant measure"). The intake record
explicitly leaves open two materially different variants:

- the classical deterministic theorem for a continuous self-map of a nonempty compact space; and
- a Feller Markov-kernel theorem under tightness or relative compactness of Cesaro occupation
  measures.

Those variants have different objects, hypotheses, and conclusions. The available source record
does not determine whether the dynamics is a map, flow, semigroup, or Markov kernel; whether the
state space is compact, locally compact, Polish, or merely supports a tight orbit; whether the
measure is Borel/regular; or the required separation, compatibility, continuity, and nonemptiness
assumptions. It also provides no theorem/page pinpoint from the cited 1937 paper. Choosing any one
of these formulations would therefore broaden or substitute the target rather than elaborate an
exact source statement.

This is the hard blocker specified by section 5 of the rev-5.6 standard: statement ambiguity and a
missing expression fingerprint prevent tree construction. Minimal imports, an exact serialized
expression, credited alternate transports, and meaningful removed-hypothesis/domain/binder-scope/
boundary mutations cannot be established before the human claim is selected from an accountable
source.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_219.lean` was inspected and re-elaborated only as
unaccepted discovery material. Its `StatementShape` is not the claimed Krylov-Bogolyubov theorem:
it assumes a `CompactAveragingPackage` containing arbitrary propositions together with proofs, and
concludes `Nonempty (KrylovBogolyubovData kappa)`, whose data already includes the desired
`InvariantProbability`. Its `DeterministicStatementShape` assumes only measurability of the map,
not continuity, so on a compact space it is not a faithful encoding of the classical theorem.
Neither declaration can be adopted through a checked transport to the underspecified source claim.

The legacy module elaborates successfully with ten broad imports in the existing pinned
environment. That establishes syntax and type correctness of the legacy artifact only. It is not
evidence that an exact target has been identified or that its imports are minimal.

## Required unblock

An accountable source review must select one theorem variant and record an immutable edition,
theorem/page, exact wording, preceding definitions, and errata. It must freeze the dynamics object,
state-space and measurable/topological compatibility assumptions, compactness or tightness
hypothesis, Feller/continuity condition, initial-law requirements, and exact invariant Borel
probability conclusion. A later statement worker can then encode that claim, minimize imports,
serialize and hash the elaborated expression, check any alternate transports, and run the four
required mutation classes.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. The existing `.lake` artifacts were used without
running `lake update`, `lake build`, a dependency clone, or a dependency fetch.

| Command | Exit | Observed result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1052` | 0 | rank 219; planned; `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_219.lean)` | 0 | legacy module elaborated and printed declarations; discovery evidence only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |

First failed gate: canonical human-claim identity. Known failures are exact-target elaboration,
minimal-import determination, expression/environment fingerprinting, checked transports, and
mutation tests. The assigned phase is not self-tested or complete, so no
`.stage1-worker-selftest.json` is emitted. No proof, downstream-node, or theorem-completion credit
is claimed.
