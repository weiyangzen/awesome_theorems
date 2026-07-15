# THM-M-0325 validation phase

Item: `S56-M-0325-VALIDATION`<br>
Intent: `validate`<br>
Base revision: `dafb8b51c4561eee5fcf162a8d5ee49555584bdb`<br>
Base tree: `cca569d6bbc491441652aae678232353fb385a74`

## Verdict

`blocked`. The validation implementation is self-tested, but its prerequisite
`S56-M-0325-PROOF` is only provisional and explicitly incomplete. The frozen
root remains `H2/M3/R4`, `root_closed=false`, with minimal cut
`M0325-T-PACKAGE`. The first missing substantive proof body is
`M0325-K-TRANSFORM`.

The scoped replay used the pinned Lean 4.29.0 toolchain and existing pinned
mathlib artifacts. Bubblewrap made the filesystem read-only except for fresh
temporary output, denied the network, fixed locale/timezone/thread settings,
and invoked `lake env lean --trust=0`. It re-elaborated the exact statement,
conditional composition, pinned tensor anchor, and eleven partial local proof
declarations. All direct axiom reports were subsets of `propext`,
`Classical.choice`, and `Quot.sound`; source scans found no prohibited proof
mechanism.

This is warm-cache, nonrelease evidence. The automation-provided `.lake`
symlink is untracked, the root has no proof body, the foundation and transitive
TCB/provenance profiles remain open, and no second independently provisioned
runner or independently implemented verifier exists. Repetition in this worker
is not independent validation.

## Commands

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0325` | 0 | rank 214, planned L0/rework-required target, legacy evidence unaccepted, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0325/check_obligation_tree.py` | 0 | 15 obligations and 33 typed edges passed; root open M3; cut `M0325-T-PACKAGE` |
| `python3 Stage1_Instances/THM-M-0325/check_anchor_audit.py` | 0 | structured anchor audit passed at mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -I -B Stage1_Instances/THM-M-0325/check_validation.py` | 0 | network-isolated trust-zero fresh-output replay passed for the declarations in `validation-spec.json`; every incomplete gate failed closed |
| `python3 -m json.tool Stage1_Instances/THM-M-0325/validation-spec.json` | 0 | validation recipe parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0325/validation-receipt.json` | 0 | validation receipt parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0325/validation-blocker.json` | 0 | validation blocker parsed |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | worker handoff parsed |
| `git diff --check --no-index /dev/null <each new validation artifact>` | 1 | expected content-difference exit for each new file; zero whitespace diagnostics |

## Boundary

No mathematical proof content was added. No frozen obligation or root was
promoted. The old obligation-tree recipes cover only structural checks and the
old proof checker is base/worktree-state bound to its proof worker; neither is
misrepresented as current validation-phase root evidence. Accepted receipt IDs
remain empty, `audit_complete=false`, and `theorem_complete=false`.
