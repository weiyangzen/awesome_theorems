# THM-M-1148 release decision

Item: `S56-M-1148-RELEASE`. Base revision:
`99cd22cccebeb1f25106f5bdb86b82a536ae1a68`.

## Exact verdict

The release verdict is `blocked`. The lifecycle remains `planned`, accepted
receipt IDs remain empty, and both `audit_complete` and `theorem_complete` are
false. Neither `AUDIT-Z` nor `THEOREM-Z` is accepted.

The first workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`.
`S56-M-1148-VALIDATION` is only a provisional `[_]` worker projection. Its
receipt has `accepted=false`, `release_grade=false`, and no dependency-ordered
master acceptance. This release worker cannot promote it or any predecessor.

The structured records also disagree about the machine debt: the intake
instance records `[H2, M3, R4]`, while the frozen graph and validation receipt
record `[H2, M4, R4]`. The weaker `[H2, M4, R4]` boundary therefore controls
this fail-closed decision. Both projections remain unchanged, and their
unreconciled conflict independently blocks `AUDIT-Z`.

## Evidence reconciliation

A fresh narrow replay copies `Statement.lean`, `PoissonUnitDisk.lean`,
`Proof.lean`, and `Validation.lean` into a temporary directory and runs pinned
Lean at `--trust=0`. Bubblewrap denies networking and makes the host tree
read-only. The exact root and the separately composed validation root elaborate;
all 29 selected declarations report exactly `propext`, `Classical.choice`, and
`Quot.sound`. A comment-aware scan finds no proof placeholder, local axiom,
bodyless constant, unsafe declaration, native oracle shortcut, external
implementation, or `sorryAx` in the four replayed modules.

That is provisional kernel evidence, not accepted `M0-L` or `E0`. The frozen
graph still has no closed obligation and retains the cut
`{M1148-C, M1148-L1, M1148-B, M1148-N3}`. The implemented Mobius-transform
route has not been reconciled with the frozen near/far-arc architecture, so it
has no accepted per-node composition credit.

The adapted source boundary also remains open. The upstream ATLAS source is not
vendored for offline comparison, and its CC BY-NC 4.0 license with the
no-training/no-evaluation rider has no compatibility decision. There is no
complete accepted transitive foundation, provenance, computation, executable,
TCB, SBOM, or license closure. Pinpoint primary-source `H0`, independently
reviewed node-specific `R0`, and `AUDIT-Z` are absent.

## Commands and results

Commands ran from the repository root on 2026-07-15 (`Asia/Shanghai`). The
automation-provided `.lake` link was reused read-only. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` repair was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-1148` | 0 | rank 353, lifecycle `planned`, `theorem_complete=false` |
| `python3 Stage1_Instances/THM-M-1148/check_statement.py` | 0 | exact expression hash and all five statement mutations passed |
| `python3 Stage1_Instances/THM-M-1148/check_anchor_audit.py` | 0 | four anchors and pinned mathlib revision passed |
| `python3 Stage1_Instances/THM-M-1148/check_obligation_tree.py` | 0 | 26 obligations and 51 typed edges passed; root remains open M4 |
| `python3 -I -B Stage1_Instances/THM-M-1148/check_release.py` | 0 | current hashes, authority reconciliation, network-isolated trust-zero warm-cache replay, and blocked terminal decision passed |
| JSON parsing, Python compilation to `/tmp`, and `git diff --check` | 0 | release artifacts parsed and compiled; no whitespace error was found |

The predecessor validation checker is intentionally bound to its earlier base
revision and root worker packet, so it is hash-bound as historical evidence
rather than reused as the current recipe.

## Release boundary

Release additionally lacks immutable clean input, an empty-cache cold build,
offline restoration, complete SBOM/licenses, two distinct signed clean runners,
an independently implemented minimal verifier, protected adversarial CI, and a
build-twice deterministic content-addressed bundle.

This node is self-tested only as an exact negative reconciliation. It grants no
accepted proof state, `H0`, `M0/E0/E1`, `R0`, `AUDIT-Z`, `THEOREM-Z`, release,
theorem completion, or master acceptance.
