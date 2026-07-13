# THM-M-1138 validation blocker

Item: `S56-M-1138-VALIDATION`

Base revision: `ffea62ba1a7c0b0f84d70fd07f87d3eef57fe330`

Base tree: `4662e08d189bd534919775f750c6909591aeafcb`

Validation time: `2026-07-14T02:27:49+08:00`

## Verdict

`blocked`. The assigned validation phase is not self-tested, so no validation receipt or root
worker self-test manifest is emitted. The exact public declaration has provisional proof-phase
kernel evidence, but that evidence cannot pass the rev-5.6 validation gates against the currently
frozen architecture.

The first failed gate is frozen-route reconciliation. Registry version 1 decomposes a
strong-maximum/local-constancy route. `Proof.lean` instead proves the same terminal package by a
strict-subharmonic perturbation. The proof receipt therefore withholds closure credit for
`M1138-C-CLOSURE-MAXIMIZER`, `M1138-B-MAXIMIZER-LOCATION`,
`M1138-L-INTERIOR-LOCAL`, `M1138-L-CONNECTED-PROPAGATION`, and
`M1138-L-CONTINUITY-EXTENSION`. It also withholds foundation credit. The authoritative typed graph
consequently remains `root_closed=false`, `M3`, with no accepted closed obligations.

The frozen `validation-specs.json` cannot resolve this mismatch. It belongs to
`S56-M-1138-OBLIGATION_TREE`; all fifteen recipes invoke only `check_obligation_tree.py`, and its
declared boundary is structural freeze and conditional composition, not the proof-phase analytic
declarations. Treating those recipes as validation of the perturbation proof would be false-scoped
evidence. Correcting the registry, graphs, and recipes requires a versioned append-only architecture
reconciliation rather than a silent validation-phase rewrite.

## Observed evidence

The committed proof receipt reports that
`Stage1Instances.THM_M_1138.Proof.boundaryMaximumPackage` and
`Stage1Instances.THM_M_1138.Proof.harmonicWeakMaximumPrinciple` elaborate without placeholders and
use exactly `propext`, `Classical.choice`, and `Quot.sound`. That receipt is provisional,
`accepted=false`, and `content_addressed=false`; its accepted obligation list is empty. This run did
not promote that observation to an accepted foundation or complete transitive trust certificate.

The current structural checker passed the immutable version-1 registry and explicitly reported an
open `M3` root and an `M4` terminal analytic package. Input hashes agree with the proof receipt:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `a6a2c5d7cc38249b3d96a3f8037a68175db5d62eecec2790865086dce2747c5a` |
| `ObligationTree.lean` | `433c6beaaa9d7c5a74c8afe1f5337b38d4015ec3964988a2dea9b7dae938640d` |
| `Proof.lean` | `52105d067464dff747110a6fc147da9392adeddce2ca6fe61ddf70f37feef8f2` |
| `obligation-registry.json` | `a3fc025b941f6cfc039562e443bd41f5548bf1233e4f2181b3396b015f9a657e` |
| `typed-graphs.json` | `b66bd5f13ebfcc7b47c853872c615f235ca2cb5235fc641fa0ad778beb65dcdc` |
| `validation-specs.json` | `9d3a523540af6474d4c176d4b926bec893cd4d771c15f53dbb6caae2c2d90c25` |
| `proof-receipt.json` | `88d6e0626a192c417c62f6970d31afa75a821b9786517672785bca233af1c3ff` |

## Additional failed gates

- The proof prerequisite is only provisional `[_]`; master acceptance is pending.
- No accepted theorem-specific foundation profile or complete transitive declaration, import,
  executable, compiler/bootstrap, plugin, evaluator, and TCB closure exists.
- `M1138-X-SOURCE`, `M1138-X-PROVENANCE`, `H0`, and independently reviewed `R0` remain open.
- The worker clone reuses the canonical shared warm `.lake` symlink. Under section 10.6 this is
  performance evidence, not a clean empty-cache cold build or network-disconnected restoration.
- There is no content-addressed TCB/SBOM/license archive or deterministic release bundle.
- There are no two signed attestations from distinct identities and independently provisioned clean
  runners, no independent writable cache, and no independently implemented minimal verifier.
  Repeating Lean in this clone would not satisfy section 10.7.

The accepted vector therefore remains `[H1, M3, R3]`; `audit_complete=false` and
`theorem_complete=false`.

## Commands and exact results

No command ran `lake update`, `lake build`, dependency clone/fetch, or modified `.lake`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1138` | 0 | rank 343, planned, L0/rework-required, theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-1138/check_obligation_tree.py` | 0 | 15 obligations and 36 typed edges passed; registry denominator `a2093825...ca49`; root open `M3`; terminal package `M4` |
| `python3 -m json.tool Stage1_Instances/THM-M-1138/proof-receipt.json` | 0 | proof receipt parses |
| `python3 -m json.tool Stage1_Instances/THM-M-1138/validation-specs.json` | 0 | frozen obligation-tree recipes parse |
| `git diff --check -- Stage1_Instances/THM-M-1138` | 0 | no tracked-diff whitespace errors before this blocker was added |
| `git status --short --untracked-files=all` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked before this blocker was added |

## Retry condition

An architecture-owning lane must publish an append-only registry/typed-graph/recipe delta that
models the perturbation route, preserves the old IDs and eligibility history, and checks every new
child-to-parent composition. After dependency-ordered master acceptance, validation must replay the
exact declarations with an accepted foundation and complete provenance packet. Release assurance
then additionally requires a clean cold offline restoration and distinct signed independent
verification.

Because the assigned validation gate failed, `.stage1-worker-selftest.json` is intentionally absent.
