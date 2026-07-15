# THM-M-0822 proof-phase validation

Item: `S56-M-0822-PROOF`. Base revision:
`8cfd5229cfb37c4199bfe53eb119c41667c21dc1`.

## Implemented proof

`Proof.lean` realizes both halves of the unchanged exact maximum-value target.
`starAttainment` installs the target-owned construction of a star, its
intersection and uniformity properties, and its exact binomial cardinality.
`universalUpperBound` installs `Finset.erdos_ko_rado` from the manifest-pinned
mathlib revision. `erdosKoRadoMaximum` then consumes both packages through
`composeRoot` and the checked exact-assembly identity. It therefore proves an
attaining family exists and every admissible intersecting uniform family is
bounded; it does not substitute the upper bound alone for the maximum claim.

All eleven frozen required-machine obligations are provisionally realized.
Every one of the ten `proof_requires` edges has its reciprocal `composes` edge,
and all six nonleaf parents have checked abstract-child composition
certificates. The EKR body's eight source-level refinement overlays remain
expository provenance nodes rather than extra proof premises or duplicated
terminal bodies.

Lean reports `Finset.erdos_ko_rado` and all eleven exact target package/root
declarations sorry-free. Every axiom closure is contained in the allowed set
`propext`, `Classical.choice`, and `Quot.sound`; the elementary ground-element
package needs only `propext`. The proof and pinned terminal body contain no placeholder,
custom axiom, unsafe/opaque declaration, native oracle, external
implementation, or theorem substitution.

This supports an exact kernel-closed route but does not assign its eventual
`M0-*` class. The exact root and attainment/composition bodies are repo-local,
while the universal-bound terminal is pinned mathlib, so `M0-L` versus `M0-W`
requires master validation after release-grade E1. The proof phase claims
no accepted distinct-terminal-body closure: in particular, transitive
`Finset.kruskal_katona_lovasz_form` provenance and trust remain validation
work. The accepted dossier
remains `[H1, M3, R4]` with zero accepted obligations. This proof phase does
not claim theorem completion: master acceptance, `M0822-S-FOUNDATION`, source,
provenance, trust, readability, workflow, validation, and release gates remain
open.

## Commands and results

Commands ran in this isolated worker clone on 2026-07-15 (Asia/Shanghai). The
Lean runner writes only temporary `Statement.olean` and `ObligationTree.olean`
files under `/tmp`, prepends that directory to the pinned `LEAN_PATH`, and
removes it on exit. Existing canonical pinned `.lake` artifacts were reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
access, or `.lake` mutation ran. Network denial was not OS-enforced and the
ambient runner environment was inherited, so this is not hermetic evidence.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0822
  exit 0: rank 1380, planned, L0/rework_required,
  theorem_complete=false

bash Stage1_Instances/THM-M-0822/check_proof.sh
  exit 0: temporary statement and obligation modules elaborated; the pinned
  EKR terminal, target-owned star attainment, upper package, and exact root
  passed twelve sorry-free checks and twelve allowed axiom-profile checks; the shell
  passed the captured Lean log into the fail-closed structured checker

python3 -B Stage1_Instances/THM-M-0822/check_proof.py
  exit 0: independently reran scoped Lean elaboration and checked exact proof
  markers, frozen statement/registry/graph, all proof edges and composition
  certificates, immutable mathlib source/blob/olean/body, receipt hashes,
  worker packet, accepted-state boundary, placeholder policy, and dirty scope

python3 -B Stage1_Instances/THM-M-0822/check_obligation_tree.py
  exit 1 at its historical-base assertion: the predecessor checker is bound
  to obligation-tree worker base f023dbc3, while this proof worker starts from
  later integration commit 8cfd5229. The proof checker independently binds and
  checks the integrated statement, registry, graph, and obligation-tree bytes.

PYTHONOPTIMIZE=1 python3 -B \
  Stage1_Instances/THM-M-0822/check_proof.py
  exit 1 as expected: checker assertions cannot be disabled by optimized Python

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0822-proof-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0822/check_proof.py
  exit 0: checker syntax compiled outside the repository

python3 -m json.tool Stage1_Instances/THM-M-0822/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: both structured handoff artifacts parse

python3 <comment-aware prohibited-proof scan over Proof.lean and pinned
KruskalKatona.lean lines 343-390>
  exit 0: both the local proof and exact pinned terminal body passed after
  comments were removed; the same policy is enforced by check_proof.py

git diff --check -- Stage1_Instances/THM-M-0822 \
  .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

The receipt is provisional, warm-cache, nonrelease worker evidence only. The
integration lane must independently re-elaborate and accept it in dependency
order before changing authoritative state.
