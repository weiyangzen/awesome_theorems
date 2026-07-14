# THM-M-1108 proof-phase recheck at c470319c

Item: `S56-M-1108-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `c470319c4a07f669317557ea705f6546605ac4da`

Base tree: `680bb215853ecfbfa26fe069d1282188ed3944aa`

## Verdict

`blocked`. No proof body inhabiting
`Stage1Instances.THM_M_1108.CanonicalStatement` exists in the owned source,
the repository-local Lean source outside this dossier, or the pinned mathlib
closure. This recheck adds no proof body and closes no obligation. The
lifecycle remains `planned`, and the root vector remains
`[H2, M3, R3] -> [H2, M3, R3]`.

`ObligationTree.lean` still contains one genuine placeholder-free composition
body, `canonicalStatement_of_poissonized_depoissonized`. Its exact premises are
`PoissonizedAsymptotics` and `DePoissonizationTransfer`; neither premise has an
inhabitant. The immediate open root cut is therefore
`M1108-T-POISSONIZED` plus `M1108-T-DEPOISSONIZE`.

The first unavailable package on the frozen route is `M1108-C-RSK`: the
current repository and pinned mathlib provide permutation and Young-diagram
infrastructure, but no checked Robinson-Schensted correspondence with the
required LIS/first-row identity. The later Toeplitz determinant,
Riemann-Hilbert steepest-descent, Hastings-McLeod/Painleve-II, uniform-error,
Poissonized-limit, monotonicity/tail, and de-Poissonization bodies are absent as
well. The prerequisite anchor audit has no compatible immutable Lean 4 proof
to pin or import.

The previous proof recheck was incorporated after base `a1a7e939`. Comparing
that base with this base changes only the previous recheck's Markdown and JSON
inside this dossier; `Statement.lean`, `ObligationTree.lean`, the frozen
registry, and all candidate inputs retain their recorded hashes. A current-base
source scan likewise found no exact reusable declaration.

Assuming either terminal package, introducing an analytic axiom, weakening the
target, or reporting the conditional composition as BDJ would be a prohibited
placeholder or substituted theorem. No such declaration was added.

## Failed Gate And Retry

The first failed implementation gate is `M1108-C-RSK`. Resume only after the
frozen combinatorial and analytic packages are implemented without
placeholders, or after an immutable compatible Lean 4 BDJ proof becomes
available for exact-type, terminal-body, dependency, trust, license, and
provenance validation in the pinned environment.

## Validation

All checks ran in this worker clone against the automation-provided pinned Lake
artifacts. The pre-existing untracked `Formalizations/Lean/.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation was performed. Live public-discovery HTTP queries were used;
they did not fetch a dependency or enter the proof closure. Temporary Lean
objects were removed after replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1108` | 0 | Rank 548; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1108/check_obligation_tree.py` | 0 | 18 obligations and 36 typed edges passed; denominator `2defff91...0322c8e`; root open at M3 and both terminal packages open at M4. |
| Isolated two-module `lake env lean` replay shown below, with `--trust=0` and `-t0` | 0 | `Statement.lean` and `ObligationTree.lean` elaborated. The exact statement transport and conditional composer reported only `[propext, Classical.choice, Quot.sound]`. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless axiom-like declaration, unsafe/oracle, or equivalent prohibited construct was found. |
| `rg -n -i --glob '*.lean' '\b(baik\|deift\|johansson\|tracy.?widom\|painlev[eé]\|hastings.?mcleod\|longest[ -]increasing[ -]subsequence\|riemann.?hilbert\|robinson.?schensted)\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | Expected no-match exit; no topical terminal declaration was found in pinned mathlib. |
| Exact-declaration `rg` scan over repo-local `*.lean` outside this owned target and `.lake` | 1 | Expected no-match exit; no declaration of `normalizedLISCDF`, `IsTracyWidomCDF`, `poissonizedLISCDF`, `PoissonizedAsymptotics`, or `DePoissonizationTransfer` was found. |
| GitHub repository-search API for `"Robinson-Schensted" language:Lean` and `Tracy-Widom Lean` | 0 | HTTP 200 for both; each response was valid JSON with `total_count=0`, `incomplete_results=false`, and no items. |
| Sourcegraph GraphQL search for `lang:Lean RobinsonSchensted count:20` | 0 | HTTP 200; valid JSON with no errors, `resultCount=0`, and no results. A separate TracyWidom retry timed out with curl exit 28/HTTP 000 and receives no negative-result credit. |
| `python3 -m json.tool Stage1_Instances/THM-M-1108/proof-recheck-2026-07-15-head-c470319c.json` | 0 | The current-base blocker record is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1108 .stage1-worker-selftest.json` | 0 | No tracked whitespace errors. |
| Per-file `git diff --no-index --check /dev/null <new-artifact>` for the Markdown and JSON blocker files | 1 each | Expected new-file diff exit with empty diagnostic output; both untracked artifacts have no whitespace errors. |

The isolated replay was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1108-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1108/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1108/ObligationTree.lean "$tmp/ObligationTree.lean"
cd Formalizations/Lean
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" timeout 300 lake env lean --trust=0 \
  -t0 -R "$tmp" "$tmp/ObligationTree.lean"
```

The word `sorry` printed during `Statement.lean` elaboration is Lean's
diagnostic rendering inside the four expected `#check_failure` mutation probes.
It is not source syntax or an admitted proof; the token-anchored source scan
confirms that distinction.

The public API queries are discovery evidence only and are not exhaustive. No
external revision was identified, so they supply no machine proof credit.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does
not satisfy `S56-M-1108-PROOF`, change the task state, or claim audit
completion, theorem completion, validation, release, receipt acceptance, or
master acceptance. `accepted_receipt_ids=[]`. Because the assigned proof phase
is incomplete, `.stage1-worker-selftest.json` is deliberately absent.
