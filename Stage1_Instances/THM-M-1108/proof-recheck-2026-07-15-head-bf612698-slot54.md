# THM-M-1108 proof-phase recheck at bf612698 (slot54)

Item: `S56-M-1108-PROOF`

Recheck date: `2026-07-15T17:17:03+08:00` (`Asia/Shanghai`)

Base revision: `bf6126986da025eabca097776ede0ba9484bbf71`

Base tree: `98c8e9b005d8d255ee3e05a1c34a449daf02a5a5`

## Verdict

`blocked`; no proof body was added, no frozen obligation was newly closed, and no proof credit or
state transition is claimed.

The exact target remains `Stage1Instances.THM_M_1108.CanonicalStatement`, the full
Baik--Deift--Johansson pointwise limit for the normalized longest increasing subsequence of a
uniform permutation. The checked declaration
`canonicalStatement_of_poissonized_depoissonized` has body `hTransfer hPoissonized`. It consumes
inhabitants of `PoissonizedAsymptotics` and `DePoissonizationTransfer` and constructs neither, so it
is a conditional composition certificate rather than a proof of the root.

Relative to the preceding proof recheck at base `4d389eb4`, only that recheck's Markdown and JSON
records were added under this target. `Statement.lean`, `ObligationTree.lean`,
`AnchorCandidates.lean`, the obligation registry, typed graphs, anchor audit, validation
specifications, and pinned dependency closure retain their recorded hashes. The three target
modules replay at trust level zero, but no proof input changed.

Fresh repository, history, and all-pinned-package searches found no inhabitant of either terminal
package. Pinned mathlib supplies permutations, Young diagrams and semistandard tableaux, CDFs,
Poisson limits, derivatives, integrals, and filters, but no checked RSK/LIS first-row identity,
Tracy--Widom/Painleve development, Toeplitz/Fredholm asymptotics, Riemann--Hilbert steepest descent,
uniform edge estimate, or de-Poissonization theorem. The closest local tableau and
Riemann--Hilbert artifacts are explicitly nonterminal scaffolds. The prerequisite immutable
external audit also identifies no compatible Lean 4 BDJ proof to pin.

An exact logical-shortcut probe unfolded `IsTracyWidomCDF` and rewrote its CDF equation. The
remaining goal was still convergence of `normalizedLISCDF N t` to the explicit exponential of the
restricted-set integral defining `F t`, so the source predicate is not a vacuous route to closure.
No definitional, contradiction, or finite-prefix proof was found.

The first unavailable dependency-legal package is `M1108-C-RSK`. The immediate root cut remains:

- `M1108-T-POISSONIZED`
- `M1108-T-DEPOISSONIZE`

Assuming a terminal package, adding an axiom, weakening the proposition, or presenting the
conditional composer as BDJ would violate the assigned deliverable. The root remains
`[H2, M3, R3]`, with `root_closed=false`, `proof_phase_complete=false`, and
`theorem_complete=false`.

## Narrow Validation Evidence

All commands ran inside this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts was treated as read-only. No
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
| All-pinned-package topical scan below | 1 | Expected no-match exit; no relevant theorem-level terminal declaration was found. |
| Repository-local exact-interface scan below | 1 | Expected no-match exit; no reusable exact declaration was found outside this dossier. |
| All-ref target `Proof*.lean` history scan below | 1 | Expected no-match exit; repository history contains no target proof module to recover. |
| `git diff --name-status 4d389eb47e043f6f44925a418baee0d034f764ba..HEAD -- Stage1_Instances/THM-M-1108` | 0 | Only `proof-recheck-2026-07-15-head-4d389eb4-slot46.{json,md}` was added; no proof input changed. |
| `sha256sum Stage1_Instances/THM-M-1108/{Statement.lean,ObligationTree.lean,AnchorCandidates.lean,obligation-registry.json,typed-graphs.json,anchor-audit.json,validation-specs.json} Formalizations/Lean/{lean-toolchain,lake-manifest.json}` | 0 | All hashes matched the structured record. |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean `4.29.0` at commit `98dc76e3...6740`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Revision `8a178386...ea95`; tree `bdc39a31...c2b`. |

The exact trust-zero replay command was:

```bash
set -uo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1108-slot54-headbf612698-replay.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1108/{Statement,ObligationTree,AnchorCandidates}.lean "$tmp"/
cd Formalizations/Lean
base=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
s1=$?
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base" timeout 300 lake env lean \
  --trust=0 -t0 --root="$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean"
s2=$?
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 \
  --root="$tmp" "$tmp/AnchorCandidates.lean"
s3=$?
cd "$repo"
printf 'REPLAY_EXITS Statement=%s ObligationTree=%s AnchorCandidates=%s\n' \
  "$s1" "$s2" "$s3"
test "$s1" -eq 0 && test "$s2" -eq 0 && test "$s3" -eq 0
```

The exact source and candidate scan was:

```bash
set +e
pattern='(^|[^[:alnum:]_])(sorry|admit|sorryAx|implemented_by|native_decide|unsafe|extern|run_tac)([^[:alnum:]_]|$)|^[[:space:]]*(axiom|constant|opaque)[[:space:]]'
rg -n --glob '*.lean' "$pattern" Stage1_Instances/THM-M-1108
s1=$?
rg -n -i --glob '*.lean' '\b(baik|deift|johansson|tracy[-_ ]?widom|painleve|hastings[-_ ]?mcleod|robinson[-_ ]?schensted|schensted|longest[-_ ]?increasing[-_ ]?subsequence|riemann[-_ ]?hilbert|toeplitz determinant|fredholm determinant|airy kernel|de[-_ ]?poissonization)\b' Formalizations/Lean/.lake/packages
s2=$?
rg -n --glob '*.lean' '\b(normalizedLISCDF|IsTracyWidomCDF|PoissonizedAsymptotics|DePoissonizationTransfer|poissonizedLISCDF|lisLength)\b' . --glob '!Stage1_Instances/THM-M-1108/**' --glob '!Formalizations/Lean/.lake/**' --glob '!.git/**'
s3=$?
git rev-list --all --objects | rg 'Stage1_Instances/THM-M-1108/(Proof[^/]*\.lean|.+/Proof[^/]*\.lean)$'
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

Twenty-six blocker recheck pairs predated this attempt. Blueprint section 10.2 mandates splitting
after five unresolved execution ticks instead of dispatching the same oversized item again. The
master/scheduler must reconcile retry accounting and create dependency-legal child tasks beginning
with `M1108-C-RSK`; this worker may not edit the authoritative DAG, whose assigned row still records
`attempts=0` and `children=[]`.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-1108-PROOF`, change task state, or claim audit completion, theorem completion, validation,
release, receipt acceptance, or master acceptance. `accepted_receipt_ids=[]`. Because the assigned
proof phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.
