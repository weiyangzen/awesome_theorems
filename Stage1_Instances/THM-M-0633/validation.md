# Intake validation

Base revision: `0e5ae82e6d507ee607c3f011900571ffd8096800`; base tree:
`400e6edf1f69b971b60a367e3ea29be359b07907`.

This validation covers manifest and execution-item identity, the planned dossier and six-node open
task DAG, exact repository-source provenance, the source-statement and non-substitution boundaries,
JSON and scoped invariants, a narrow pinned Lean declaration and axiom probe, prohibited-construct
hygiene, and whitespace. It does not validate a canonical source statement, a canonical Lean
target, a proof body, audit completion, or theorem completion.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The structured recipes require a denied-network replay, but this
worker run does not attest operating-system network isolation; it records only that no command used
the network. The owned intake files and root worker packet make the final tree dirty and
nonrelease.

The packet-aware checker mode binds this exact worker handoff. Packet-free replay permits the
integration lane to rerun structural checks after moving the authoritative intake cursor from
`[ ]` to `[_]`; mutable blueprint and execution-DAG inputs are compared with their recorded base
blobs where appropriate. The provisional receipt remains unsigned and non-content-addressed, and
master acceptance must recapture its own evidence.

## Commands and results

All commands ran on 2026-07-13 in Asia/Shanghai. Commands without an explicit working directory ran
at the repository root.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0633` | 0 | rank 1326; planned; L0/rework_required; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 4692,4697 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '4692,4697p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog excerpt SHA-256 `92f408cf...512dfd` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 at `98dc76e3...`; Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0633/IntakeProbe.lean)` | 0 | nine adjacent predicates and Heine-Cantor interfaces elaborated; both candidate axiom reports were `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `4a9a065b...2ae36` |
| direct stdin elaboration of the compact-subset candidate with `lake env lean /dev/stdin` | 0 | an `example` with uniform spaces, `IsCompact s`, and `ContinuousOn f s` elaborated to `UniformContinuousOn f s`; discovery check only, no owned target declaration added |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0633-pycache python3 -m py_compile Stage1_Instances/THM-M-0633/check_intake.py` | 0 | scoped checker compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0633/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, base and source pins, planned H1/M3/R4 boundary, null canonical target, exact inventory, packet/receipt agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0633/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| `rg -n --glob '*.lean' '(^\|[^[:alnum:]_])(sorry\|admit\|sorryAx)([^[:alnum:]_]\|$)\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0633` | 1 (expected no match) | no prohibited proof escape or declaration in the discovery-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0633 .stage1-worker-selftest.json` plus a per-file `git diff --no-index --check /dev/null PATH` loop | 0 for the aggregate; 1 with empty diagnostics for each new-file comparison | no whitespace diagnostics in any new artifact |

The exact discovery-only stdin elaboration was:

```bash
cd Formalizations/Lean
lake env lean /dev/stdin <<'EOF'
import Mathlib.Topology.UniformSpace.HeineCantor

open Set

universe u v

example {α : Type u} {β : Type v} [UniformSpace α] [UniformSpace β]
    {s : Set α} {f : α → β} (hs : IsCompact s) (hf : ContinuousOn f s) :
    UniformContinuousOn f s :=
  hs.uniformContinuousOn_of_continuous hf
EOF
```

It exited `0` with no output. This candidate elaboration is not the canonical statement gate and
does not add a declaration or proof artifact to the dossier.

## Known open gates

An approved immutable primary or authoritative source, exact theorem and definition locators,
complete premise/conclusion/proof-boundary/translation/errata crosswalk, and independent source
review remain open. So do metric versus uniform-space scope, separation assumptions, compact-subset
versus compact-domain carrier, relative versus global continuity and uniform continuity, ordered
binders, boundary decisions, the canonical Lean expression and environment fingerprint, checked
alternate transports, and statement mutations.

The scheduled exhaustive anchor and provenance audit, discovery protocol, obligation registry,
typed graphs, terminal proof-body and dependency audit, proof and composition acceptance, readable
reconstruction, hermetic replay, deterministic evidence bundle, independent verification, master
acceptance, audit completion, and theorem completion also remain open. These failures do not
invalidate a truthful self-tested `planned` intake.
