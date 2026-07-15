# Proof-phase current-base recheck

Item: `S56-M-1067-PROOF`  
Theorem: `THM-M-1067`  
Attempt date: `2026-07-15T20:18:40+08:00`  
Base revision: `471e4458269351ee096972776c478d019941b679`

## Verdict

`blocked`. The proof phase is not self-tested as complete, and no
`.stage1-worker-selftest.json` is written. No proof body, obligation closure, receipt, scheduler
state, audit-completion state, or theorem-completion state is claimed.

The prerequisite `S56-M-1067-OBLIGATION_TREE` remains worker-provisional (`[_]`) rather than master
accepted. Independently, trust-zero Lean validation confirms that the frozen target fails the exact
statement gate, so a positive proof-phase handoff would be invalid.

## Checked statement defect

`Statement.lean` defines

```lean
nonnegativeLebesgue := Measure.map Real.toNNReal volume
```

`Real.toNNReal` maps the entire nonpositive half-line to zero. Therefore the preimage of `{0}` has
infinite real Lebesgue measure, and the pushforward gives the singleton zero infinite mass. At
`t = 0`, using the measurable indicator of the spatial singleton zero, the frozen time integral is
infinite while the spatial integral is zero for every `NNReal`-valued candidate field.

The placeholder-free bodies already in `Proof.lean` kernel-check the exact consequences:

- `nonnegativeLebesgue_singleton_zero`: the frozen time measure assigns `{0}` mass `infinity`;
- `occupation_at_zero_false`: every candidate occupation identity fails at time zero;
- `no_local_time_of_wiener`: no field satisfies the frozen predicate under a Wiener measure;
- `target_iff_no_wiener_measure`: the frozen target is equivalent to nonexistence of its own
  Wiener measures.

This is negative statement-fidelity evidence. It does not refute the mathematical Brownian
local-time theorem and earns no positive existence-proof credit. Proving the frozen target by
asserting that no Wiener measure exists would substitute a vacuous false premise and is prohibited
by rev-5.6.

## Open proof cut

All 15 machine-required obligations still have null terminal proof-body IDs. The pinned mathlib
tree has no Brownian-motion module and no stochastic local-time, occupation-density, or Tanaka
terminal theorem. The accepted predecessor audit likewise records no exact compatible,
placeholder-free external theorem. Even after repairing the statement, the Wiener construction,
moment/Cauchy estimates, limiting field, joint continuity, measurability, and simultaneous
occupation identity remain unimplemented.

The first failed gate is `M1067-S-BOUNDARY`: the frozen time measure is not Lebesgue time. The
required retry order is statement repair, statement mutations, anchor re-audit, versioned
obligation/graph refreeze and master acceptance, then proof implementation against that corrected
target.

## Validation

No dependency update, build, clone, fetch, or `.lake` mutation was run. The automation-provided
read-only `.lake` symlink was reused, and Lean outputs were written only to a fresh removed `/tmp`
directory.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1,546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546 |
| `python3 scripts/stage1_target.py show THM-M-1067` | 0 | rank 509; planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1067/check_obligation_tree.py` | 0 | 17 obligations, 71 typed edges, open M4 root |
| isolated `lake env lean` compilation of `Statement.lean`, `Proof.lean`, and `ObligationTree.lean` with `--trust=0 -t0` | 0 | all modules elaborated; each defect declaration reports only `propext`, `Classical.choice`, and `Quot.sound` |
| required-obligation terminal-body assertion | 0 | all 15 machine-required bodies are null |
| prohibited-construct scan over owned Lean files | 1 (expected) | no `sorry`, `admit`, axiom declaration, unsafe/external body, or related prohibited construct matched |
| pinned mathlib Brownian-module test and scoped source search | 0 | module absent; only unrelated Wiener-Ikehara prose matched |
| structured packet parsing, invariant assertions, and `git diff --check` | 0 | packet and owned patch valid |
| self-test/output absence check | 0 | no completion manifest or generated Lean output exists in the owned path |

Trust-zero object hashes are recorded in the adjacent JSON packet. This is current-base nonrelease
blocker evidence only; it does not satisfy `S56-M-1067-PROOF`.
