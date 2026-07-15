# THM-M-1108 proof-phase recheck at 88a5a5c6 (slot48)

Item: `S56-M-1108-PROOF`

Recheck date: `2026-07-15T19:38:00+08:00` (`Asia/Shanghai`)

Base revision: `88a5a5c6fe6bac0d813a74ca20fa553eaf2a6d68`

Base tree: `a0a75048a918a3bf566c3dbcf6b4352c3b2ee8e4`

## Verdict

`blocked`; no proof body was added, no frozen obligation was newly closed, and no proof credit or
state transition is claimed.

The exact target remains `Stage1Instances.THM_M_1108.CanonicalStatement`, the full
Baik--Deift--Johansson pointwise limit for the normalized longest increasing subsequence of a
uniform permutation. The checked declaration
`canonicalStatement_of_poissonized_depoissonized` has body `hTransfer hPoissonized`. It consumes
inhabitants of `PoissonizedAsymptotics` and `DePoissonizationTransfer` and constructs neither, so it
is a conditional composition certificate rather than a proof of the root.

Relative to the latest target integration at `b1a5b03c`, no file under this dossier changed before
this attempt. `Statement.lean`, `ObligationTree.lean`, `AnchorCandidates.lean`, the obligation
registry, typed graphs, anchor audit, validation specifications, toolchain pin, and dependency
manifest retain their recorded hashes. The three Lean modules replay at trust level zero, but no
proof input changed.

Independent exact-interface, all-ref target-history, and locally available pinned-package source
searches found no inhabitant of either terminal package. Pinned mathlib supplies permutation,
Young-diagram, CDF, Poisson, derivative, integral, and filter infrastructure, but no checked
Robinson--Schensted/LIS first-row identity, Tracy--Widom/Painleve-II development, Toeplitz or
Fredholm asymptotics, Riemann--Hilbert steepest descent, uniform edge estimate, or
de-Poissonization theorem. The immutable prerequisite anchor audit likewise identifies no
compatible Lean 4 proof to pin or import.

Prior trust-zero semantic probes already exclude the evident accidental routes: zero functions do
not satisfy the Airy normalization, a represented Tracy--Widom CDF is positive by its exponential
formula, and the `N = 0` value is only a finite prefix of an `atTop` limit. Unfolding the antecedent
leaves the genuine normalized-LIS convergence claim. No definitional, contradiction, vacuity, or
finite-prefix proof was found.

The selected first unavailable package on the frozen route is `M1108-C-RSK`. The immediate root
cut remains:

- `M1108-T-POISSONIZED`
- `M1108-T-DEPOISSONIZE`

Assuming a terminal package, adding an axiom, weakening the proposition, or presenting the
conditional composer as BDJ would violate the assigned deliverable. The frozen registry and typed
graph project the root as `[H2, M3, R3]`; the intake-era instance and anchor audit still project
`[H2, M4, R4]`. That pre-existing projection conflict requires master reconciliation and receives
no debt transition here. Every projection has `root_closed=false`,
`proof_phase_complete=false`, and `theorem_complete=false`.

## Narrow Validation Evidence

All commands ran inside this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was treated as read-only. No
`lake update`, `lake build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. Temporary replay files and objects lived only under `/tmp` and were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1108` | 0 | Rank 548; planned lifecycle; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1108/check_obligation_tree.py` | 0 | 18 obligations and 36 typed edges passed; denominator `2defff91...0322c8e`; root open at M3 and both terminal packages open at M4. |
| Isolated temporary-copy replay below | 0 | `Statement.lean`, `ObligationTree.lean`, and `AnchorCandidates.lean` exited `0/0/0` under `lake env lean --trust=0 -t0`; the checked transport and conditional composer reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Token-anchored prohibited-device scan below | 1 | Expected no-match exit; no prohibited construct occurs in an owned Lean file. |
| Locally available pinned-package topical scan below | 1 | Expected no-match exit; no named or topically matching theorem-level terminal candidate was found. |
| Repository-local exact-interface scan below | 1 | Expected no-match exit; no reusable exact declaration was found outside this dossier. |
| All-ref target `Proof*.lean` history scan below | 1 | Expected no-match exit; repository history contains no target proof module to recover. |
| `git diff --name-status b1a5b03c9eb85b0777b34f58df31029086acf260..HEAD -- Stage1_Instances/THM-M-1108` | 0 | No output; no target file changed after the latest target evidence integration. |
| `sha256sum Stage1_Instances/THM-M-1108/{Statement.lean,ObligationTree.lean,AnchorCandidates.lean,obligation-registry.json,typed-graphs.json,anchor-audit.json,validation-specs.json} Formalizations/Lean/{lean-toolchain,lake-manifest.json}` | 0 | All source, registry, graph, audit, toolchain-pin, and manifest hashes matched the structured record. |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean `4.29.0` at commit `98dc76e3...6740`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Revision `8a178386...ea95`; tree `bdc39a31...c2b`. |
| `jq empty Stage1_Instances/THM-M-1108/proof-recheck-2026-07-15-head-88a5a5c6-slot48.json` | 0 | The structured blocker artifact is valid JSON. |
| Two `git diff --no-index --check /dev/null <artifact>` checks | 1/1 | Expected new-file diff exits with zero diagnostic bytes; no whitespace errors were found in either artifact. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The self-test manifest is absent because the assigned proof phase is incomplete. |

The exact trust-zero replay command was:

```bash
set -uo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1108-slot48-head88a5a5c6-replay.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1108/{Statement,ObligationTree,AnchorCandidates}.lean "$tmp"/
cd Formalizations/Lean
base=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base" timeout 300 lake env lean \
  --trust=0 -t0 --root="$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean"
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 \
  --root="$tmp" "$tmp/AnchorCandidates.lean"
cd "$repo"
```

The exact source and candidate scan was:

```bash
set +e
pattern='(^|[^[:alnum:]_])(sorry|admit|sorryAx|implemented_by|native_decide|unsafe|extern|run_tac)([^[:alnum:]_]|$)|^[[:space:]]*(axiom|constant|opaque)[[:space:]]'
rg -n --glob '*.lean' "$pattern" Stage1_Instances/THM-M-1108
s1=$?
rg -n -i --glob '*.lean' '\b(baik|deift|johansson|tracy[-_ ]?widom|painlev[eé]|hastings[-_ ]?mcleod|robinson[-_ ]?schensted|schensted|longest[-_ ]?increasing[-_ ]?subsequence|riemann[-_ ]?hilbert|toeplitz determinant|fredholm determinant|airy kernel|de[-_ ]?poissonization)\b' Formalizations/Lean/.lake/packages
s2=$?
rg -n --glob '*.lean' '\b(normalizedLISCDF|IsTracyWidomCDF|PoissonizedAsymptotics|DePoissonizationTransfer|poissonizedLISCDF|lisLength)\b' . --glob '!Stage1_Instances/THM-M-1108/**' --glob '!Formalizations/Lean/.lake/**' --glob '!.git/**'
s3=$?
git rev-list --all --objects | rg -i 'Stage1_Instances/THM-M-1108/(proof[^/]*\.lean|.+/proof[^/]*\.lean)$'
s4=$?
printf 'SCAN_EXITS prohibited=%s topical=%s exact_interface=%s history_proof=%s\n' \
  "$s1" "$s2" "$s3" "$s4"
test "$s1" -eq 1 && test "$s2" -eq 1 && test "$s3" -eq 1 && test "$s4" -eq 1
```

The word `sorry` printed while replaying `Statement.lean` is Lean's diagnostic rendering inside
four expected `#check_failure` mutation probes. It is not source syntax or an admitted proof, as
the token-anchored source scan confirms.

## Reopen And Scheduling Condition

Implement both frozen terminal packages and their child obligations without placeholders, or
provide an immutable compatible Lean 4 BDJ proof for pinned exact-type integration with complete
provenance, dependency, trust, and license validation.

Thirty-two blocker recheck pairs predated this attempt. Blueprint section 10.2 mandates splitting
after five unresolved execution ticks rather than dispatching the same oversized item again. The
master/scheduler must reconcile retry accounting and create dependency-legal child tasks beginning
with `M1108-C-RSK`; this worker may not edit the authoritative DAG, whose assigned row still records
`attempts=0` and `children=[]`.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-1108-PROOF`, change task state, or claim audit completion, theorem completion, validation,
release, receipt acceptance, or master acceptance. `accepted_receipt_ids=[]`. Because the assigned
proof phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.
