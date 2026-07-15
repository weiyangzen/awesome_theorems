# THM-M-1108 proof-phase recheck at 8400eb33

Item: `S56-M-1108-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `8400eb33dbc4ffb9ebd94456e4de9bfb8d28e005`

Base tree: `02fcb6bc0f0786ce18871dc9c2c0d2d3db071200`

## Verdict

`blocked`. No proof body inhabiting
`Stage1Instances.THM_M_1108.CanonicalStatement` exists in the owned source,
the repository-local Lean source outside this dossier, or the pinned mathlib
closure. This recheck adds no proof body and closes no obligation. The
lifecycle remains `planned`, and the root vector remains
`[H2, M3, R3] -> [H2, M3, R3]`.

`ObligationTree.lean` contains one genuine placeholder-free composition body,
`canonicalStatement_of_poissonized_depoissonized`. Its exact premises are
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

The previous recheck was incorporated at this base. Relative to parent
`c45766a10a075c90791ad416bdb458018dabecd3`, the only target changes are that
recheck's Markdown and JSON. `Statement.lean`, `ObligationTree.lean`, the
frozen registry, typed graphs, anchor audit, and validation specifications
retain their recorded hashes. Current source and history scans found no exact
reusable declaration or historical target proof module.

Assuming either terminal package, introducing an analytic axiom, weakening the
target, or reporting the conditional composition as BDJ would be a prohibited
placeholder or substituted theorem. No such declaration was added.

## Failed Gate And Retry

The first failed implementation gate is `M1108-C-RSK`. Resume only after the
frozen combinatorial and analytic packages are implemented without
placeholders, or after an immutable compatible Lean 4 BDJ proof becomes
available for exact-type, terminal-body, dependency, trust, license, and
provenance validation in the pinned environment.

This dossier contains 28 earlier proof-recheck pairs at this base. Blueprint
section 10.2 and the execution skill require splitting an obligation after
five unresolved execution ticks. The authoritative assigned row nevertheless
still has `attempts=0` and `children=[]`. The master must reconcile retry
accounting and split dependency-legal work beginning at `M1108-C-RSK`; this
worker is forbidden to edit the authoritative DAG.

## Validation

All checks ran in this worker clone against the automation-provided pinned Lake
artifacts. The pre-existing untracked `Formalizations/Lean/.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
network operation, or `.lake` mutation was performed. Temporary Lean objects
were removed after replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1108` | 0 | Rank 548; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1108/check_obligation_tree.py` | 0 | 18 obligations and 36 typed edges passed; denominator `2defff91...0322c8e`; root open at M3 and both terminal packages open at M4. |
| Isolated three-module `lake env lean` replay shown below, with `--trust=0` and `-t0` | 0 | `Statement.lean`, `ObligationTree.lean`, and `AnchorCandidates.lean` elaborated. The exact statement transport and conditional composer reported only `[propext, Classical.choice, Quot.sound]`. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom declaration, or unsafe declaration was found. |
| Topical `rg` scan over pinned mathlib source | 1 | Expected no-match exit; no BDJ, Tracy-Widom, Painleve, Hastings-McLeod, LIS, Riemann-Hilbert, or Robinson-Schensted terminal declaration was found. |
| Exact-interface `rg` scan over repo-local `*.lean` outside this dossier and `.lake` | 1 | Expected no-match exit; no declaration using the target-specific interfaces was found. |
| `git rev-list --all --objects` target-proof-module scan | 1 | Expected no-match exit; repository history contains no `Proof*.lean` module for this target. |
| `sha256sum` over the seven frozen target inputs and two environment pins | 0 | Every digest matched the values in the accompanying JSON record. |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 commit `98dc76e3...ab16740`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Mathlib revision `8a178386...eea95`; tree `bdc39a31...242c19e5c2b`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1108/proof-recheck-2026-07-15-head-8400eb33-slot37.json` | 0 | The current-base blocker record parsed successfully. |
| `git diff --check -- Stage1_Instances/THM-M-1108 .stage1-worker-selftest.json` | 0 | No tracked whitespace errors. |
| Per-file `git diff --no-index --check /dev/null <new-artifact>` for this Markdown and JSON | 1 each | Expected new-file diff exit with empty diagnostic output; neither untracked artifact has a whitespace error. |

The isolated replay was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1108-slot37.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1108/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1108/ObligationTree.lean "$tmp/ObligationTree.lean"
cp Stage1_Instances/THM-M-1108/AnchorCandidates.lean "$tmp/AnchorCandidates.lean"
cd Formalizations/Lean
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" timeout 300 lake env lean --trust=0 \
  -t0 -R "$tmp" "$tmp/ObligationTree.lean"
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 -R "$tmp" \
  "$tmp/AnchorCandidates.lean"
```

The word `sorry` printed during `Statement.lean` elaboration is Lean's
diagnostic rendering inside the four expected `#check_failure` mutation probes.
It is not source syntax or an admitted proof; the token-anchored source scan
confirms that distinction.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does
not satisfy `S56-M-1108-PROOF`, change the task state, or claim audit
completion, theorem completion, validation, release, receipt acceptance, or
master acceptance. `accepted_receipt_ids=[]`. Because the assigned proof phase
is incomplete, `.stage1-worker-selftest.json` is deliberately absent.
