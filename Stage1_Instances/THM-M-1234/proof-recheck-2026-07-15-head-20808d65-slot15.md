# THM-M-1234 proof-phase recheck at `20808d65` (slot15)

Item: `S56-M-1234-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `20808d65f53d8801e78f061504b93bb7efd49489`

Base tree: `a5bf33a278a7a285878c89177838ae1a0dcc9990`

## Verdict

`blocked`. The exact universal declaration
`Stage1Rev56.THMM1234.Statement` still has no repo-local or pinned proof body.
This execution adds no proof body and closes no obligation. The proof phase
remains `[ ]`, lifecycle remains `planned`, and the root vector stays
`[H1, M3, R3] -> [H1, M3, R3]`. No proof receipt, provisional state,
audit-completion, theorem-completion, validation, release, or master-acceptance
claim is made.

The existing six owned Lean modules were re-elaborated from source at trust
level zero. They provide conditional root assembly, constant-in-time
structural candidate fields and their trace, the strict zero-data solution,
and a diagnostic for the malformed closure interface. None proves the
canonical statement for arbitrary `InitialData`.

There is no vacuity or constant-field shortcut. `zero_initial_data` witnesses
that the premise is inhabited. Reusing arbitrary initial fields at every time
closes the structural fields and trace but leaves the stationary nonlinear
`WeakMomentumEquation`; that identity does not follow from `InitialData`.
Zero fields close only the strict zero-data case.

The predecessor anchor audit records no exact compatible external Lean body.
A current read-only scan of all 9,676 pinned package Lean sources found no
Yudovich/Yudovitch, incompressible-Euler, bounded-vorticity, or Biot-Savart
terminal candidate. The legacy `S1_M_158.lean` module records interfaces and
formalization debt, not a root inhabitant. This proof recheck makes no
exhaustive external-nonexistence claim.

## Failed Gates

The immediate workflow dependency is unfinished:
`S56-M-1234-OBLIGATION_TREE` is worker-provisional `[_]`, not master-accepted
`[x]`. Its frozen artifacts are also not acceptance-ready:

- `typed-graphs.json` names `M1234-ROOT` as `root_node_id`, but the declared
  root node is `THM-M-1234-ROOT`.
- All 14 validation recipes are shell-string aliases for the same structural
  checker and omit the normative structured recipe fields and declaration
  coverage.
- `CandidateConstructionPackage` consumes none of its approximation, energy,
  or compactness children.
- `EquationAndTraceClosurePackage` quantifies over every unrelated candidate.
  Its checked zero-candidate diagnostic forces arbitrary admissible initial
  velocity and vorticity test pairings to vanish.

The direct frozen root cut remains `M1234-A-STRUCTURE` plus
`M1234-E-CLOSURE`. The first expanded mathematical gap is
`M1234-A-APPROX`; uniform estimates, nonlinear-compatible compactness,
structure preservation, linear and quadratic momentum passage, and the
one-sided trace also remain open.

Before this packet, 25 structured proof-attempt/blocker packets, including 22
rechecks, had already been integrated while the authoritative proof task still
records `attempts: 0` and `children: []`. Blueprint section 10.2 requires the
master/scheduler to reconcile that stale state and split the oversized item
instead of issuing another identical proof-only tick. This worker did not edit
the DAG, generated checklist, predecessor registry, or task state.

## Validation

The automation-provided `.lake` symlink to the canonical pinned artifacts was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
checkout, cache repair, or deliberate `.lake` mutation was run. Lean objects
and logs were created in a fresh `/tmp` directory and removed. The untracked
symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets at ranks 1 through 1,546, all `L0/rework_required`, passed. |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | Rank 158; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `cfa0a02c...34c5d`; root open at M3 and both analytic packages M4. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| Isolated trust-zero `lake env` replay below | 0 | All six owned modules elaborated; printed proof declarations reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Prohibited-device scan over owned `*.lean` | 1 | Expected no-match exit with empty output: no `sorry`, `admit`, declared axiom/constant, unsafe/opaque/extern escape, `sorryAx`, `implemented_by`, or `native_decide` was found. |
| Exact-topic scan over pinned package `*.lean` | 1 | Expected no-match exit with empty output: no exact-topic terminal candidate was found. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `jq empty Stage1_Instances/THM-M-1234/*.json` | 0 | Every pre-existing owned JSON artifact parsed. |
| Structured predecessor diagnostic | 0 | The root node reference is dangling; all 14 recipes are shell strings and miss the required structured field set. |

The narrow replay was:

```bash
set -u
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-1234-head-20808d65-slot15.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1234/{Statement,AnchorAudit,ObligationTree,ConstructionProof,Proof,ClosurePackageDiagnostic}.lean "$tmp"/
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd "$tmp"
for module in Statement AnchorAudit ObligationTree ConstructionProof Proof ClosurePackageDiagnostic; do
  if [ "$module" = Statement ]; then path="$lean_path"; else path=".:$lean_path"; fi
  LEAN_NUM_THREADS=1 LEAN_PATH="$path" timeout --foreground 600 \
    "$lean" --trust=0 -t0 -o "$module.olean" "$module.lean" \
    >"$module.stdout" 2>"$module.stderr" || exit $?
done
```

The pinned Lean binary SHA-256 was
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`.
The replay produced `Statement.olean` SHA-256
`1709e38a5b8cc96159b7042585666cb84536b4b3d9e26a63697992cd9820d308`
and `ObligationTree.olean` SHA-256
`2521d53bc0b3ea2c9d0b7e7bcae9854ebe5081fc0cecd39a8a5fdfdf4324fc50`.
The paired JSON packet binds all source, environment, object, and output
hashes.

## Retry Condition

The master must reopen the predecessor architecture, publish and accept an
append-only registry version with child-consuming construction targets and
closure tied to the specifically constructed candidate, correct the typed
root reference, replace the shell-string aliases with node-specific structured
validation recipes, reconcile the attempt history, and split the analytic
leaves. Then approximation, estimates, nonlinear compactness, momentum-limit,
and trace bodies can be implemented. An immutable compatible external terminal
theorem is an alternative only after exact-type, provenance, trust, and
composition checks.

## Status Boundary

This current-base target-scoped artifact is the required blocker handoff, not
a proof receipt. It does not satisfy `S56-M-1234-PROOF`, propose `[_]`, or
support audit or theorem completion. Because the assigned universal proof
phase is not genuinely self-tested as complete, `.stage1-worker-selftest.json`
is deliberately absent.
