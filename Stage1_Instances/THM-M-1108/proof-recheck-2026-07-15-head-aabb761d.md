# THM-M-1108 proof-phase recheck at aabb761d

Item: `S56-M-1108-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `aabb761d975829b09920d981edc8220edb90e8c3`

Base tree: `a988020866eb03a08cd23d18d5e7711cb5d03742`

## Verdict

`blocked`. No proof body inhabiting the exact target
`Stage1Instances.THM_M_1108.CanonicalStatement` exists in the owned source,
repository-local Lean source outside this dossier, or the pinned mathlib
closure. This recheck adds no Lean proof body and closes no obligation. The
lifecycle remains `planned`, and the root vector remains
`[H2, M3, R3] -> [H2, M3, R3]`.

The only checked child-to-root theorem is
`canonicalStatement_of_poissonized_depoissonized`. It consumes
`PoissonizedAsymptotics` and `DePoissonizationTransfer`, but neither proposition
has an inhabitant. Consequently the immediate root cut remains
`M1108-T-POISSONIZED` plus `M1108-T-DEPOISSONIZE`.

The first unavailable frozen package is `M1108-C-RSK`: neither the repository
nor pinned mathlib supplies a checked Robinson-Schensted correspondence with
the required LIS/first-row identity. The later Toeplitz determinant,
Riemann-Hilbert steepest-descent, Hastings-McLeod/Painleve-II, uniform-error,
Poissonized-limit, monotonicity/tail, and de-Poissonization bodies are absent as
well. The immutable prerequisite anchor audit identifies no compatible Lean 4
proof to pin or import.

Since base `c470319c`, the only changes under this target are the preceding
proof-recheck Markdown and JSON. The statement, obligation interfaces, frozen
registry, typed graphs, anchor audit, and validation specifications retain
their recorded hashes. Fresh repo-local and pinned-mathlib scans found no new
candidate.

Assuming either terminal package, introducing an analytic axiom, weakening the
target, or presenting the conditional composer as the BDJ proof would be a
prohibited placeholder or substituted theorem. No such declaration was added.

## Failed Gate And Retry

The first failed implementation gate is `M1108-C-RSK`. Resume only after the
frozen combinatorial and analytic packages are implemented without
placeholders, or after an immutable compatible Lean 4 BDJ proof is available
for exact-type, terminal-body, dependency, trust, license, and provenance
validation in the pinned environment.

## Validation

All commands ran in this worker clone using the automation-provided pinned Lake
artifacts. The pre-existing untracked `Formalizations/Lean/.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
network discovery, or `.lake` mutation was performed. Temporary Lean objects
were removed after replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1108` | 0 | Rank 548; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1108/check_obligation_tree.py` | 0 | 18 obligations and 36 typed edges passed; denominator `2defff91...0322c8e`; root open at M3 and both terminal packages open at M4. |
| Isolated two-module `lake env lean` replay shown below, using `--trust=0` and `-t0` | 0 | `Statement.lean` and `ObligationTree.lean` elaborated. The exact statement transport and conditional composer reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless axiom-like declaration, unsafe/oracle, or equivalent prohibited construct was found. |
| `rg -n -i --glob '*.lean' '\\b(baik\|deift\|johansson\|tracy.?widom\|painlev[eé]\|hastings.?mcleod\|longest[ -]increasing[ -]subsequence\|riemann.?hilbert\|robinson.?schensted)\\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | Expected no-match exit; no topical terminal declaration was found in pinned mathlib. |
| Exact-interface `rg` scan over repo-local `*.lean` outside this target and `.lake` | 1 | Expected no-match exit; no declaration of `normalizedLISCDF`, `IsTracyWidomCDF`, `poissonizedLISCDF`, `PoissonizedAsymptotics`, or `DePoissonizationTransfer` was found. |
| `git diff --name-status c470319c4a07f669317557ea705f6546605ac4da..HEAD -- Stage1_Instances/THM-M-1108` | 0 | Only `proof-recheck-2026-07-15-head-c470319c.{md,json}` were added; proof inputs did not change. |
| `python3 -m json.tool Stage1_Instances/THM-M-1108/proof-recheck-2026-07-15-head-aabb761d.json` | 0 | The current-base blocker record is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1108 .stage1-worker-selftest.json` | 0 | No tracked whitespace errors. |
| Per-file `git diff --no-index --check /dev/null <new-artifact>` for this Markdown and JSON | 1 each | Expected new-file diff exit with empty diagnostic output; neither artifact has a whitespace error. |

The isolated replay command was:

```bash
set -u
tmp=$(mktemp -d /tmp/thm-m-1108-proof-recheck.XXXXXX)
cp Stage1_Instances/THM-M-1108/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1108/ObligationTree.lean "$tmp/ObligationTree.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
base=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$base" timeout 300 "$lean" --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base" timeout 300 "$lean" --trust=0 \
  -t0 --root="$tmp" "$tmp/ObligationTree.lean"
```

The word `sorry` printed during `Statement.lean` elaboration is Lean's
diagnostic rendering inside four expected `#check_failure` mutation probes. It
is not source syntax or an admitted proof; the token-anchored source scan
confirms the distinction.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does
not satisfy `S56-M-1108-PROOF`, change task state, or claim audit completion,
theorem completion, validation, release, receipt acceptance, or master
acceptance. `accepted_receipt_ids=[]`. Because the assigned proof phase is not
complete, `.stage1-worker-selftest.json` is deliberately absent.
