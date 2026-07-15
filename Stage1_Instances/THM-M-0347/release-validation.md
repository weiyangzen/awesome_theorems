# THM-M-0347 release decision

Item: `S56-M-0347-RELEASE`. Base revision:
`48fb6596b1844f4183c411142415d872ff21e842`.

## Exact verdict

The release verdict is `blocked`. Lifecycle remains `planned`, the accepted
root vector remains `H1/M3/R4`, and accepted receipt and obligation sets remain
empty. Both `audit_complete` and `theorem_complete` are false; neither
`AUDIT-Z` nor `THEOREM-Z` is accepted.

The first workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`.
`S56-M-0347-VALIDATION` is only a provisional `[_]` worker projection. Its
receipt has `accepted=false`, `release_grade=false`, and no dependency-ordered
master acceptance. A release worker cannot promote it or any predecessor.

## Evidence reconciliation

The exact frozen target elaborates. Existing validation evidence also replays
the premise-free exact root and a separately composed root under Lean trust
level zero with networking denied. The 13 selected declarations report exactly
`propext`, `Classical.choice`, and `Quot.sound`; Lean sorry checks and the
comment-aware source scan pass. The ATLAS source, upstream blob, source hash,
and retained license bytes agree with the proof and validation receipts.

These are provisional warm-cache facts, not accepted `M0-P` or `E1`. The proof
and validation receipts explicitly retain `accepted_root_closed=false`, no
accepted closed obligation, and no internal per-node composition credit. The
authoritative frozen graph remains open at `M3`, with the analytic, source,
foundation, provenance, readability, and workflow cut visible.

The first substantive acceptance blocker is the ATLAS source boundary. The
proof was discovered after the frozen anchor audit, and its CC BY-NC 4.0
license with a no-training/no-evaluation rider has no compatibility decision
for repository acceptance or this automation context. The proof route also has
not been mapped to independently checked composition certificates for the
frozen obligations.

`AUDIT-Z` independently fails: no pinpoint primary-source edition, theorem/page,
assumption, proof, and errata crosswalk has independent `H0` review; no
node-specific readable reconstruction has independent `R0` review; and the
post-audit proof source, source boundaries, evidence, and public projections
remain unreconciled.

## Commands and results

Commands ran from this worker clone on 2026-07-15 (`Asia/Shanghai`). The
automation-provided `.lake` link was reused without mutation. No `lake update`,
`lake build`, dependency clone/fetch/checkout, or `.lake` repair ran.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0347` | 0 | rank 840, lifecycle `planned`, `theorem_complete=false` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0347/Statement.lean)` | 0 | the exact `FejerTheoremTarget` elaborated and printed |
| `python3 Stage1_Instances/THM-M-0347/check_obligation_tree.py` | 0 | 15 obligations and 73 typed edges passed; root remains open M3 |
| `python3 -B Stage1_Instances/THM-M-0347/check_release.py` | 0 | authority, hashes, provisional narrow Lean evidence, and the blocked terminal decision agreed |
| JSON parsing, Python compilation to `/tmp`, and `git diff --check` | 0 | release artifacts parsed and compiled; no whitespace diagnostics |

The predecessor validation checker is intentionally bound to its earlier base
revision and phase worker packet. The release checker therefore hashes it as
historical input and invokes its existing network-isolated Lean runner directly
instead of misrepresenting that snapshot-bound checker as a current release
recipe.

## Release boundary

Release additionally lacks master-accepted immutable clean input, an empty-cache
cold build, offline restoration, complete transitive TCB/provenance/SBOM and
license closure, two distinct signed clean runners, an independently implemented
minimal verifier, protected mutation/adversarial CI, and a build-twice
deterministic content-addressed bundle.

This node is self-tested only as an exact negative reconciliation. It grants no
accepted proof state, `H0`, `M0-P/E1`, `R0`, `AUDIT-Z`, `THEOREM-Z`, release,
theorem completion, or master acceptance.
