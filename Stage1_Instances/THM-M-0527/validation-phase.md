# THM-M-0527 validation-phase result

Item: `S56-M-0527-VALIDATION`. Base revision:
`874745ff39044c1e45ed30a04111d3d84aa0e348`.

## Narrow validation

The structured recipe rebuilds `Statement.olean` in a fresh temporary directory, then elaborates
all fourteen declarations in `Proof.lean` and the validation-only trust probes in
`Validation.lean` at Lean trust level zero. `Validation.lean` adds no theorem, definition, instance,
or other mathematical declaration; it applies `assert_no_sorry`, `#print sorries`, and
`#print axioms` to the proof-phase declarations.

Bubblewrap clears the environment, mounts the host read-only, provides a private writable `/tmp`,
and denies network access to the Python validator and every child Lean process. All declarations
report exactly `propext`, `Classical.choice`, and `Quot.sound`. The local files pass a
nested-comment-aware scan for placeholders, bodyless declarations, unsafe code, and oracle escape
hatches. Current hashes and the clean pinned mathlib revision, tree, origin, license, and selected
source/blob/olean boundaries agree.

This is an honest negative-root validation. The proof predecessor is only provisional and claims
zero complete frozen obligations because the ten fiber interfaces and their child-to-parent
composition receipts have not been reconciled. More importantly, `M0527-EX-COVER` and
`M0527-EX-RANGE` have no proof bodies: no checked construction realizes an arbitrary subgroup by a
connected cover. The root stays `[H1, M3, R3]`, `audit_complete=false`, and
`theorem_complete=false`.

## Commands and results

Commands ran from the repository root on 2026-07-15 (Asia/Shanghai). The automation-provided
canonical `.lake` symlink was reused without mutation. No `lake update`, `lake build`, dependency
clone, or dependency fetch was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0527` | 0 | Rank 584; planned; L0/rework-required; theorem incomplete. |
| `git status --short --untracked-files=all` | 0 | Before edits, only the pre-existing automation `.lake` symlink; dirty nonrelease checkout. |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | Revision `874745ff...e348`; tree `6e4fd01c...fc4`. |
| execute the `validation-spec.json` argv without shell interpolation and capture output | 0 | Network-isolated trust-zero narrow replay passed; exact root, complete trust/provenance, cold hermetic, and independent gates remained fail-closed. |

The structured runner's exact summary is:

```text
PASS THM-M-0527 network-isolated trust-zero fresh-output replay
PASS exact statement and all fourteen proof-phase declarations elaborated; Lean reports them sorry-free
PASS observed axioms are exactly propext, Classical.choice, and Quot.sound
PASS frozen inputs and selected pinned mathlib source, blob, olean, origin, license, and tool identities agree
OPEN proof master acceptance, arbitrary-subgroup cover construction, complete trust/provenance, cold hermetic replay, and distinct-runner verification
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | Fresh local outputs elaborate the exact statement and all fourteen genuine partial proof declarations at trust level zero. |
| Placeholder and unsafe boundary | provisional pass | Lean reports every declaration sorry-free, and the supplemental source scan finds no prohibited proof device. |
| Axiom observation | provisional pass | Every checked declaration uses exactly the observed classical trio; this is not an accepted complete foundation/TCB closure. |
| Selected direct provenance | provisional pass | Frozen inputs and selected mathlib source, blob, olean, revision, tree, origin, and license hashes agree. Full transitive provenance remains open. |
| Proof dependency | fail closed | `S56-M-0527-PROOF` is `[_]`, not master accepted, and its receipt grants zero complete frozen-obligation closure. |
| Exact root | fail closed | `M0527-EX-COVER` and `M0527-EX-RANGE` remain open; the exact root remains M3. |
| Human source and readability | fail closed | H1/R3, primary-source premise mapping, readable reconstruction, and independent H0/R0 reviews remain open. |
| Hermetic release replay | fail closed | The run reused a dirty checkout and shared warm artifacts rather than a clean empty-cache cold build with offline restoration and complete SBOM/TCB archive. |
| Independent verification | fail closed | The trust probe shares this worker, checkout, toolchain, and cache; no distinct signed verifier or independently implemented minimal release verifier exists. |

The validation node is self-tested only as a nonrelease blocked receipt. It grants no accepted
obligation state, exact root closure, `M0-*`, `E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release, theorem
completion, or master acceptance.
