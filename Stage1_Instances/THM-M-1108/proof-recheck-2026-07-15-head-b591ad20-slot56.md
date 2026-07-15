# THM-M-1108 proof-phase recheck at b591ad20 (slot56)

Item: `S56-M-1108-PROOF`

Recheck date: `2026-07-15T12:54:59+08:00` (`Asia/Shanghai`)

Base revision: `b591ad20d93005ec840e569f84d625ef246bd07d`

Base tree: `844da63e73e35787ef60899f9f194dc97006dc8c`

## Verdict

`blocked`; no proof body was added, no frozen obligation newly closed, and no
proof credit or state transition is claimed.

The exact target remains
`Stage1Instances.THM_M_1108.CanonicalStatement`.  The checked theorem
`canonicalStatement_of_poissonized_depoissonized` still consumes explicit
inhabitants of `PoissonizedAsymptotics` and `DePoissonizationTransfer`; it
constructs neither premise.  Consequently it remains a valid child-to-root
composition certificate rather than a proof of Baik--Deift--Johansson.

No proof input changed between the preceding `be2be0df` recheck and this base.
The only target-path additions were that preceding recheck's Markdown and JSON
blocker records.  The statement, obligation tree, registry, typed graphs,
anchor audit, and validation specifications have the same content hashes.

The first unavailable frozen mathematical package is `M1108-C-RSK`: neither
the repository nor pinned mathlib supplies a checked Robinson--Schensted
correspondence with the required LIS/first-row identity.  The downstream
Toeplitz determinant, Riemann--Hilbert steepest descent, Hastings--McLeod
identification, uniform edge estimates, Poissonized limit, monotonicity and
Poisson-tail estimates, and fixed-size de-Poissonization bodies are likewise
absent.  A logical-vacuity audit found no shortcut: the Airy and Tracy--Widom
predicates encode the standard mathematically satisfiable analytic objects, so
unfolding them does not yield a contradiction.

The immediate root cut therefore remains:

- `M1108-T-POISSONIZED`
- `M1108-T-DEPOISSONIZE`

Assuming either terminal package, declaring an axiom, or presenting the
conditional composer as the root theorem would be a placeholder or a
substituted theorem.  The root remains `[H2, M3, R3]`, with
`root_closed=false`, `proof_phase_complete=false`, and
`theorem_complete=false`.

## Narrow Validation Evidence

All checks ran inside this worker clone.  The automation-provided untracked
`Formalizations/Lean/.lake` symlink was treated as read-only.  No `lake
update`, `lake build`, dependency clone/fetch, network operation, or `.lake`
mutation was performed.  Temporary replay files and objects were created only
under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546, all L0/rework-required, passed. |
| `python3 scripts/stage1_target.py show THM-M-1108` | 0 | Rank 548; planned lifecycle; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1108/check_obligation_tree.py` | 0 | 18 obligations and 36 typed edges passed; denominator `2defff91...0322c8e`; root open at M3 and both terminal packages open at M4. |
| `cd Formalizations/Lean && timeout 20s lake env lean --version` | 1 | Lake rejected the shared `flt-regular` checkout because `HEAD` cannot be resolved; Lean was not invoked through this entry point. |
| Isolated temporary-copy direct replay of `Statement.lean`, `ObligationTree.lean`, and `AnchorCandidates.lean` using pinned Lean 4.29.0, existing Lake object paths, `--trust=0`, and `-t0` | 0 | Replay exits were `0/0/0`; all three modules elaborated.  The exact-statement transport and conditional composer reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom-like bodyless declaration, unsafe/oracle, or equivalent prohibited construct was found. |
| Pinned-mathlib topical source scan | 1 | Expected no-match exit; no BDJ, Tracy--Widom, Painleve, Hastings--McLeod, LIS, Riemann--Hilbert, Robinson--Schensted, or de-Poissonization terminal declaration was found. |
| Repository-local exact-interface scan outside this target and `.lake` | 1 | Expected no-match exit; no declaration of `normalizedLISCDF`, `IsTracyWidomCDF`, `poissonizedLISCDF`, `PoissonizedAsymptotics`, or `DePoissonizationTransfer` was found. |
| `git diff --name-status be2be0df...HEAD -- Stage1_Instances/THM-M-1108` | 0 | Only `proof-recheck-2026-07-15-head-be2be0df-slot56.{md,json}` was added; no proof input changed. |

The direct replay resolved the pinned Lean binary with `elan`, constructed an
explicit `LEAN_PATH` from the toolchain library and existing pinned Lake
object directories, compiled a temporary `Statement.olean`, and elaborated
the other two modules.  The exact replay command was:

```bash
set -uo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1108-slot56-replay.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1108/{Statement,ObligationTree,AnchorCandidates}.lean "$tmp"/
lean=$(cd Formalizations/Lean && elan which lean)
prefix=$("$lean" --print-prefix)
base=$(find -L Formalizations/Lean/.lake -type d \
  -path '*/.lake/build/lib/lean' -print0 | \
  xargs -0 -r realpath | sort -u | paste -sd:)
base="$prefix/lib/lean:$base"
status=0
LEAN_NUM_THREADS=1 LEAN_PATH="$base" timeout 300 "$lean" --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.out" 2>&1 || status=$?
statement_status=$status
if [ "$status" -eq 0 ]; then
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base" timeout 300 "$lean" --trust=0 -t0 \
    --root="$tmp" -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean" \
    >"$tmp/obligation.out" 2>&1 || status=$?
fi
obligation_status=$status
if [ "$status" -eq 0 ]; then
  LEAN_NUM_THREADS=1 LEAN_PATH="$base" timeout 300 "$lean" --trust=0 -t0 \
    --root="$tmp" "$tmp/AnchorCandidates.lean" \
    >"$tmp/anchor.out" 2>&1 || status=$?
fi
anchor_status=$status
sed -n '1,240p' "$tmp/statement.out"
sed -n '1,240p' "$tmp/obligation.out"
sed -n '1,240p' "$tmp/anchor.out"
printf 'STATEMENT_EXIT=%s\nOBLIGATION_EXIT=%s\nANCHOR_EXIT=%s\nREPLAY_EXIT=%s\n' \
  "$statement_status" "$obligation_status" "$anchor_status" "$status"
exit "$status"
```

It printed `STATEMENT_EXIT=0`, `OBLIGATION_EXIT=0`, `ANCHOR_EXIT=0`, and
`REPLAY_EXIT=0`.  The word `sorry` in the `Statement.lean` output is Lean's
diagnostic rendering inside four expected `#check_failure` probes; it is not
source syntax or an admitted proof.

## Reopen Condition

Implement both frozen terminal packages and their listed child obligations
without placeholders, or provide an immutable compatible Lean 4 BDJ proof for
pinned exact-type integration with complete terminal-body, dependency, trust,
license, and provenance validation.  Restore the canonical pinned
`flt-regular` checkout before requiring root-project `lake env` replay.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt.  It
does not satisfy `S56-M-1108-PROOF`, change task state, or claim audit
completion, theorem completion, validation, release, receipt acceptance, or
master acceptance.  `accepted_receipt_ids=[]`.  Because the assigned proof
phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.
