# Intake validation

Base revision: `0f70149d61a952d44f907f4662a143372bcb4c44`; base tree:
`35328e4f56f47446a4e1dfdbe361a1b70a4b18a7`.

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
| `python3 scripts/stage1_target.py show THM-M-0479` | 0 | rank 1360; planned; L0/rework_required; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 3518,3523 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '3518,3523p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog excerpt SHA-256 `1e67501d...eaaa6` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0 at `98dc76e3...` on `x86_64-unknown-linux-gnu` |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0479/IntakeProbe.lean)` | 0 | eleven predicates and direct Dirichlet-theorem interfaces elaborated; both set-infinitude candidates reported `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `f8ebef27...e7537` |
| direct stdin elaboration of the standard `ZMod` candidate with `lake env lean /dev/stdin` | 0 | an `example` with nonzero modulus and unit residue elaborated to set infinitude; discovery check only, no owned target declaration added |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0479-pycache python3 -m py_compile Stage1_Instances/THM-M-0479/check_intake.py` | 0 | scoped checker compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0479/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, base and source pins, planned H1/M3/R4 boundary, null canonical target, exact inventory, packet/receipt agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0479/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| `rg -n --glob '*.lean' '(^\|[^[:alnum:]_])(sorry\|admit\|sorryAx)([^[:alnum:]_]\|$)\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0479` | 1 (expected no match) | no prohibited proof escape or declaration in the discovery-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0479 .stage1-worker-selftest.json` plus per-file no-index checks | 0 for the aggregate; no per-file diagnostics | no whitespace diagnostics in any new artifact |

The exact discovery-only stdin elaboration was:

```bash
cd Formalizations/Lean
lake env lean /dev/stdin <<'EOF'
import Mathlib.NumberTheory.LSeries.PrimesInAP

example (q : Nat) [NeZero q] (a : ZMod q) (ha : IsUnit a) :
    Set.Infinite {p : Nat | p.Prime ∧ (p : ZMod q) = a} :=
  Nat.infinite_setOf_prime_and_eq_mod ha
EOF
```

It exited `0` with no output. This candidate elaboration is not the canonical statement gate and
does not add a declaration or proof artifact to the dossier.

## Known open gates

An approved immutable primary or authoritative source, exact theorem and definition locators,
complete premise/conclusion/proof-boundary/translation/errata crosswalk, and independent source
review remain open. So do universal versus fixed-progression scope, natural versus integer modulus
and residue domains, nonzero/positivity and coprimality hypotheses, congruence and infinitude
encodings, ordered binders, boundary decisions, the canonical Lean expression and environment
fingerprint, checked alternate transports, and statement mutations.

The scheduled exhaustive anchor and provenance audit, discovery protocol, obligation registry,
typed graphs, terminal proof-body and dependency audit, proof and composition acceptance, readable
reconstruction, hermetic replay, deterministic evidence bundle, independent verification, master
acceptance, audit completion, and theorem completion also remain open. These failures do not
invalidate a truthful self-tested `planned` intake.
