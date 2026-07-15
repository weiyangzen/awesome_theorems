# THM-M-1146 proof recheck at `32d90d6a`

Item: `S56-M-1146-PROOF`

Date: `2026-07-15`

Base revision: `32d90d6afe5c1ba9d60738ca106ee0ee0f29409f`

## Verdict

`blocked`. The exact frozen Schwarz-reflection root remains open at the real-axis harmonic-gluing
obligation `M1146-L-GLUING`. The current source genuinely proves Laplacian preservation under
complex conjugation, both strict off-axis harmonic branches, continuity of the odd reflection on
the symmetric domain, and conditional composition of an axis proof into
`ReflectedHarmonicPackage`. It does not contain the axis proof itself.

This attempt rechecked the current base and searched the pinned source tree, target history,
canonical checkout, and the available worker-clone copies. No newer or hidden unconditional proof
was found. Every available `Proof.lean` and `ProofNext.lean` has the same content hash as this
clone. Pinned mathlib still has forward harmonic mean-value and Poisson formulas, Morera
interfaces, local full-ball harmonic representatives, and reflection calculus, but no converse
mean-value theorem, harmonic gluing theorem, or Schwarz-reflection theorem that closes the axis.

No `.stage1-worker-selftest.json` was written. The assigned proof phase is incomplete, the root
remains `M3`, and theorem completion is false.

## Remaining Blocker

At an axis point, `HarmonicAt` requires a `ContDiffAt Real 2` germ and an eventually zero classical
Laplacian. The frozen assumptions provide continuity through the axis and harmonicity only on the
strict upper side. The checked conjugate lower branch does not definitionally supply the missing
axis regularity.

A Morera proof would still need a holomorphic representative on an upper half-ball with controlled
boundary trace and a manual rectangle split/cancellation across the uncountable real-axis segment.
The pinned off-countable Cauchy-Goursat theorem cannot discard that segment. A disk Dirichlet and
maximum-principle proof would need a license-clean Poisson construction plus substantial semidisk
frontier and uniqueness infrastructure. The nearby target-local Poisson development is
ATLAS-derived under a restrictive license/provenance boundary and cannot be silently credited here.

## Validation

All Lean commands reused the automation-provided pinned `.lake` link read-only. No Lake update,
Lake build, dependency clone/fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed |
| `python3 scripts/stage1_target.py show THM-M-1146` | 0 | Rank 351; planned; L0/rework-required; theorem incomplete |
| `timeout 900 env LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-1146/check_statement.py` | 0 | Exact expression hash `14336b88...deef53d`; all five mutations killed |
| `python3 Stage1_Instances/THM-M-1146/check_obligation_tree.py` | 0 | 18 obligations and 40 typed edges passed; root open M3 and reflected package open M4 |
| isolated `lake env lean --trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `ProofNext.lean` | 0 | All four modules elaborated from fresh temporary outputs; every printed body used only `propext`, `Classical.choice`, and `Quot.sound` |
| prohibited-construct scan over owned Lean files | 1 | Expected no-match exit; no placeholder, bodyless axiom, unsafe/oracle, or native shortcut found |
| comparison with the canonical checkout and all available worker copies | 0 | No later or distinct proof source found; current Lean hashes are identical |
| `git diff --check -- Stage1_Instances/THM-M-1146` | 0 | No whitespace errors before this record was added |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest correctly absent |

Environment: Lean `4.29.0` commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`;
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

Source hashes: `Statement.lean` `1eed1535...1bdf5dd`; `ObligationTree.lean`
`1c8ddbb8...01812e8`; `Proof.lean` `31c325c8...759d0c4`; `ProofNext.lean`
`019fc699...110f37`.

## Reopen Condition

Resume after a placeholder-free implementation of axis harmonic gluing and its boundary/locality
prerequisites, or an immutable compatible terminal proof whose exact type, provenance, license,
trust closure, and composition can be checked without dependency mutation. This packet is current
base blocker evidence, not a proof receipt or a request for scheduler promotion.
