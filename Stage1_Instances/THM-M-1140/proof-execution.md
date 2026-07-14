# Proof-phase execution record

Item: `S56-M-1140-PROOF`
Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`
Execution date: 2026-07-15

## Result

`Proof.lean` now supplies a placeholder-free proof of the exact frozen
`HarmonicStrongMaximumPrinciple`. It implements the missing
`InteriorLocalRigidity` package with an explicit Gaussian barrier on a tangent
annulus, retains the connected clopen propagation proof, and composes both through
the checked theorem in `ObligationTree.lean`.

The analytic argument does not assume or import a strong maximum principle. It
proves that a local maximum has nonpositive Laplacian, constructs a strictly
subharmonic Gaussian perturbation, applies compact maximum comparison on an
annulus, and derives a contradiction from its positive inward derivative at the
tangent point. This rules out a strict drop near the maximizer. The argument also
preserves the `n = 0` case: a nontrivial-space instance is derived only under an
assumed strict drop, which already supplies distinct points.

Fresh isolated compilation of `Statement.lean`, `ObligationTree.lean`, and
`Proof.lean` passed under Lean `--trust=0`. The conditional composition, local
rigidity, connected propagation, and exact root each reported only `propext`,
`Classical.choice`, and `Quot.sound`; all three new public proof declarations
also reported that their dependency closures are sorry-free. The proof source
SHA-256 is
`998609dc7186a333fbf3ae6220e6b7f63bd1b5c22995af1bd752a9d2d7de98ae`.

This is provisional worker proof evidence, not master acceptance or theorem
completion. The frozen registry and graphs retain their pre-proof M3 snapshot.
The planned `M1140-L-MEAN-VALUE` bridge is realized by a barrier route rather
than a literal mean-value identity, so the integration lane must accept the
formal-output mapping or issue a registry-v2 method supersession before promoting
authoritative closure. Validation, source H0, readability R0, complete trust and
provenance, cold offline replay, distinct-runner verification, release,
`AUDIT-Z`, and `THEOREM-Z` remain open.

## Commands and exact results

All commands ran in this worker clone and reused the existing pinned Lake
artifacts read-only.

| Command | Exit | Result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-1140/check_proof.sh` | 0 | Fresh temporary compilation via `lake env lean --trust=0` passed; four axiom reports were exactly the three allowed standard axioms and three root-relevant declarations were sorry-free |
| `python3 -B Stage1_Instances/THM-M-1140/check_proof.py` | 0 | Exact target, frozen inputs, receipt, source hygiene, and pinned mathlib identities passed |
| `python3 Stage1_Instances/THM-M-1140/check_obligation_tree.py` | 0 | Frozen 16-obligation, 36-edge pre-proof architecture passed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1140` | 0 | Rank 345; planned; L0/rework-required; theorem incomplete |
| scoped prohibited-construct scan over `Proof.lean` | 1 | Expected no-match: no prohibited declaration or proof term |
| `git diff --check -- Stage1_Instances/THM-M-1140 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors |

No `lake update`, `lake build`, dependency clone/fetch, network operation, or
`.lake` mutation was performed.
