# THM-M-0005 proof progress and blocker

Item: `S56-M-0005-PROOF`

Base revision: `195f312e0164390d672a8e6642dd1242dd7bbe8d`

Verdict: `blocked`, with genuine partial proof progress. The proof phase remains `[ ]`.

## Implemented bodies

`ProofProgress20260715Slot21.lean` adds seven placeholder-free declarations. It proves that every
degree of the singular chain complex is a free module on its singular simplices, pairs this with
the existing categorical projectivity proof, and proves identity and composition laws for both
the tensor and `Tor₁` maps already implemented in `Proof.lean`.

The degreewise freeness/projectivity package closes the mathematical content of
`M0005-CHAIN-FREE`, but the frozen registry remains authoritative: no obligation is claimed closed
until a node-specific receipt is reconciled and accepted by the master. The direct-sum map laws are
real helper evidence toward `M0005-COMPONENTS`; that node still depends on the open algebraic
naturality and grading-transport branches.

`kunnethFormula_of_fields` checks exact composition through the frozen `assemble_sequence` and
`root_compose` declarations to the unchanged `KunnethFormula`. Its six arguments explicitly expose
the unimplemented inclusion, projection, zero composite, short exactness, and two naturality
families. It is not an unconditional inhabitant of the root.

## Validation

The automation-provided pinned `.lake` symlink was reused read-only. No `lake update`, `lake build`,
dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0005` | 0 | Confirmed rank 100, planned hard-mathlib lane, and `theorem_complete: false`. |
| isolated resolved `lake env` Lean replay | 0 | The frozen statement, obligation tree, existing proof module, and new progress module elaborated with `--trust=0`; all seven new declarations reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0005/check_obligation_tree.py` | 0 | 18 obligations and 51 typed edges passed; denominator `563eac89...a762`; the root remains open at M3. |
| prohibited-token `rg` scan over owned `*.lean` | 1 | No match; exit 1 is ripgrep's expected no-match result. |
| `python3 -m json.tool Stage1_Instances/THM-M-0005/proof-progress-2026-07-15-head-195f312e-slot21.json` | 0 | The structured progress record parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0005` plus trailing-whitespace scan | 0 | No whitespace error. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent. |

The replay resolved the tool and search path with `lake env`, copied the four Lean modules to a
fresh directory under `/tmp`, and elaborated each with the resolved executable, `--trust=0`, `-t0`,
`-R`, `LEAN_NUM_THREADS=1`, isolated `.olean` outputs, and a timeout. The new source SHA-256 is
`b2fda08796e0feeb5ecc1fc5004c4162e76b6a9cb9d1ed2aaf31596b1a14cd21`; its temporary `.olean`
SHA-256 was `686162f75e24ab6645aa5bc914764a0d4e6e3ad90a09f1b57e2509bac0948f1`.

Pinned environment: Lean `4.29.0` at
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Remaining blocker

The first failed mathematical gate is `M0005-EZ-MAP`. The pinned closure contains no
placeholder-free Eilenberg-Zilber or Alexander-Whitney chain comparison. It also lacks the
algebraic Kunneth inclusion, boundary, exactness, and naturality needed by `M0005-ALG-MAPS`,
`M0005-ALG-EXACT`, and their downstream transports. The audited Atlas candidate at immutable
commit `34ffed396f376454c1a9b297f3fd74c5c801fb50` terminates in `sorry` throughout its root-critical
routes and does not match the frozen universe, component, and naturality surface.

The authoritative cut set therefore remains unchanged pending master reconciliation. The root
stays `[H1, M3, R3]`. No receipt is accepted, and no audit, theorem-completion, release, checklist,
or master-acceptance claim is made. Because the assigned positive proof phase is incomplete,
`.stage1-worker-selftest.json` is intentionally absent.
