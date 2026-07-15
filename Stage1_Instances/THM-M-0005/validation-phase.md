# THM-M-0005 validation-phase result

Item: `S56-M-0005-VALIDATION`. Base revision:
`63a9ed9c4aae594da31423142b0658129d5452a7` (tree
`7bee4fac4489bad36fd615a023df13bb294d1781`).

## Narrow validation

The structured recipe copies the exact statement, conditional composition
harness, all three proof-progress modules, and `Validation.lean` into a fresh
temporary tree. It invokes the pinned Lean 4.29.0 executable directly with
`--trust=0`, fixed locale, timezone, and thread count. Bubblewrap denies the
network and makes the host and shared dependency cache read-only; only fresh
temporary outputs are writable. The direct validator invokes no `.lake`-writing
command; the separate legacy recipe attempt is nonrelease failure evidence.

All 22 proof or composition declarations listed by the recipe elaborate and pass
`assert_no_sorry`. Their axiom reports are subsets of `propext`,
`Classical.choice`, and `Quot.sound`. The observed transitive closure contains
17,128 declarations across 645 modules with no bodyless nonaxiom or unsafe
declaration. Frozen local hashes, the tracked-clean pinned mathlib revision/tree,
license, and selected Singular Homology, Tor, and ShortExact source/olean
boundaries agree.

This is intentionally a blocked-root result. `S56-M-0005-PROOF` is only
provisional `[_]`, its strongest receipt is unaccepted and supports no frozen
obligation, and the authoritative graph records zero closed obligations and
an open `M3` root. `ObligationTree.root_compose` and
`ProofProgress20260715Slot21.kunnethFormula_of_fields` consume the missing
Kunneth construction, exactness, and naturality as premises; neither is an
unconditional root proof.

## Commands and results

Commands ran from the repository root on 2026-07-15 (Asia/Shanghai). The
automation-provided canonical `.lake` symlink was reused read-only. No `lake
update`, `lake build`, dependency clone/fetch, or dependency checkout ran.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0005` | 0 | rank 100, planned, L0/rework-required, theorem incomplete |
| exact DAG assertions | 0 | validation `[ ]` depends on unfinished proof `[_]`; positive acceptance is dependency-illegal |
| `python3 -B Stage1_Instances/THM-M-0005/check_obligation_tree.py` | 0 | 18 obligations, 51 typed edges, denominator `563eac89...a762`; root open M3 |
| exact graph and proof-receipt assertions | 0 | zero closed obligations; proof receipt unaccepted; root kernel closure false |
| historical `validation-specs.json` schema/scope audit | 0 | all 18 recipes relabel one conditional module and omit six normative keys |
| `cd Formalizations/Lean && timeout --foreground --kill-after=5s 20s lake env lean ../../Stage1_Instances/THM-M-0005/ObligationTree.lean` | 124 | legacy recipe timed out without output during Lake dependency resolution; Lean checked no declaration |
| `python3 -I -B Stage1_Instances/THM-M-0005/check_validation.py --probe` | 0 | network-isolated trust-zero fresh-output replay passed for all 22 extant declarations |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0005/check_validation.py --worker-packet .stage1-worker-selftest.json` | 0 | packet, receipt, pins, trust observations, selected provenance, and fail-closed decisions passed |
| JSON parse and external Python syntax checks | 0 | spec, receipt, worker packet, and checker syntax passed |
| `git diff --check -- Stage1_Instances/THM-M-0005 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | Exact statement plus all 22 existing partial/conditional declarations elaborate at trust zero. |
| Placeholder and unsafe boundary | provisional pass | All declarations are sorry-free; source scans and closure inspection find no prohibited construct, bodyless nonaxiom, or unsafe declaration. |
| Axiom observation | provisional pass | Only the selected classical/quotient trio is observed. There is no accepted theorem-specific foundation or full TCB closure. |
| Selected direct provenance | provisional pass | Current hashes, mathlib pin/origin/license, and three direct source/olean boundaries agree. Complete transitive provenance remains open. |
| Proof dependency and exact root | fail closed | Proof is unfinished and no premise-free `NaturalKunnethSequence` exists; zero frozen obligations close. |
| Human source and readability | fail closed | The splitting boundary and exact source identity remain H1; independent H0 and R0 reviews do not exist. |
| Hermetic release replay | fail closed | Shared warm artifacts are not a clean checkout, empty-cache cold build, or offline-restorable SBOM/TCB archive. |
| Independent verification | fail closed | This same-workspace replay is not a second signed independently provisioned runner or independent minimal verifier. |

The root remains `[H1, M3, R3]`, `audit_complete=false`, and
`theorem_complete=false`. This node is self-tested only as an honest blocked
validation packet. It grants no accepted obligation state, root closure,
`M0-*`, `E0/E1`, `H0`, `R0`, `AUDIT-Z`, `THEOREM-Z`, release, theorem
completion, or master acceptance.

Retry requires a master-accepted, placeholder-free proof predecessor that
unconditionally inhabits the unchanged, source-approved root and reconciles
every frozen obligation. After that, publish conforming declaration-scoped
recipes, complete foundation/provenance/TCB and H0/R0 evidence, run a clean
empty-cache offline-restorable replay, and obtain a second signed attestation
from an independently provisioned runner with an independent minimal verifier.
