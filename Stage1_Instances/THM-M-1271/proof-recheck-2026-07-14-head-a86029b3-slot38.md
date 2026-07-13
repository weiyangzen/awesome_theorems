# THM-M-1271 proof-phase recheck at `a86029b3` (slot 38)

Item: `S56-M-1271-PROOF`

Recheck date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `a86029b30f12acc3537f70ab1c167cc25702c09b`

Base tree: `ab12055e811b574338987391b59b010338c120d2`

## Verdict

`blocked`. The tracked `Proof.lean` contains genuine, placeholder-free proof
bodies for sphere crossing, the exact geometric barrier package, and the
Palais-Smale compactness/limit-passage branch. It does not construct a
Palais-Smale sequence at the frozen minimax level.

The first failed gate is `M1271-C-PS-SEQUENCE`. The declaration
`mountainPassCriticalPackage_of_psSequence` still takes the exact missing
sequence producer as a premise, while
`root_of_barrier_and_critical_packages` still takes the entire analytic
package as a premise. Neither conditional declaration is a proof of
`MountainPassTarget`.

No repository-local or materialized pinned-dependency body supplies the
missing deformation/Ekeland argument. Fresh read-only discovery was also
negative but is not proof evidence: Sourcegraph searches including archived
and forked Lean repositories and GitHub repository searches found no candidate,
GitHub code search required authentication, and grep.app returned a service
checkpoint. No source or dependency was downloaded. These bounded queries do
not establish that no Lean formalization exists anywhere.

The item remains `[ ]`. No proof receipt, state transition, audit completion,
theorem completion, validation completion, release, or master acceptance is
claimed. `.stage1-worker-selftest.json` is deliberately absent because the
assigned proof phase is not genuinely self-tested as complete.

The frozen typed graph's root vector remains `[H3, M3, R4] -> [H3, M3, R4]`.
The older intake JSON's `[H2, M4, R4]` predates the statement, anchor, and
obligation-tree artifacts and is not rewritten by this proof-only worker.

## Validation

All credited validation checks ran in this worker clone using the existing
pinned Lake artifacts and no network access. No `lake update`, `lake build`,
dependency clone/fetch, or `.lake` mutation was performed. Temporary Lean
output was confined to `/tmp` and removed. The automation-provided untracked
`Formalizations/Lean/.lake` link makes this nonrelease blocker evidence. The
separate read-only discovery queries described above are not validation or
proof evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1271` | 0 | Rank 164; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1271/check_obligation_tree.py` | 0 | 13 obligations and 25 typed edges passed; denominator `2f6d1a3dc9064aff967ba0cf8443ff438e9cb99e0b2d34994252e6410d2d75bc`; root open at `M3`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | The exact statement, conditional root composition, and partial proof module elaborated. Six axiom reports named only `propext`, `Classical.choice`, and `Quot.sound`; `sorryAx` count was zero. Two nonfatal linter warnings reported unused automatically included section variables. |
| Owned Lean prohibited-token scan (exact command below) | 1 | Expected no-match: no prohibited proof placeholder or declaration form occurs in the owned Lean sources. |
| Pinned dependency term scan (exact command below) | 1 | Expected no-match: no matching dependency source file; match-file count zero. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `python3 -m json.tool` plus source-hash, base-identity, and blocked-state assertions on the adjacent JSON artifact | 0 | JSON syntax, all recorded input hashes, current base revision/tree, empty receipts, and false completion fields agree. |
| Scoped `git diff --check` and added-file whitespace checks | 0 | No whitespace diagnostics in either owned artifact. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
set -euo pipefail
TMP=$(mktemp -d /tmp/thm-m-1271-proof-recheck.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
BASE=$(timeout 120 lake env printenv LEAN_PATH)
timeout 180 lake env lean --trust=0 -t0 --root=../.. \
  -o "$TMP/Statement.olean" \
  ../../Stage1_Instances/THM-M-1271/Statement.lean
LEAN_PATH="$TMP:$BASE" timeout 180 lake env lean --trust=0 -t0 --root=../.. \
  -o "$TMP/ObligationTree.olean" \
  ../../Stage1_Instances/THM-M-1271/ObligationTree.lean
LEAN_PATH="$TMP:$BASE" timeout 180 lake env lean --trust=0 -t0 --root=../.. \
  ../../Stage1_Instances/THM-M-1271/Proof.lean
```

The combined Lean output SHA-256 was
`38a6ee8c1cb73a407a2c6d73f836a913184d42f38296b06f53a174315b20d794`.
Exact bound input hashes and environment pins are recorded in the adjacent
JSON artifact.

The exact no-match scans, run from the repository root, were:

```bash
rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe|opaque|constant)[[:space:]]' \
  Stage1_Instances/THM-M-1271 --glob '*.lean'
rg -l -i \
  'MountainPass|mountain[ -]?pass|PalaisSmale|Palais[ -]?Smale|Ekeland|Caristi|deformation lemma|minimax critical' \
  Formalizations/Lean/.lake/packages --glob '*.lean'
```

## Retry Condition

The remaining root cut set is `M1271-C-PS-SEQUENCE`,
`M1271-T-CRITICAL`, and `M1271-ROOT`. Resume after a placeholder-free local
construction of the exact minimax Palais-Smale sequence, or after an immutable
compatible Lean 4 deformation/Ekeland theorem can be pinned, transported to
the exact frozen type, and checked for terminal proof-body provenance.

This is durable blocker evidence, not a proof receipt, and it does not satisfy
`S56-M-1271-PROOF`.
