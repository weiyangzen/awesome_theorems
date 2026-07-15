# THM-M-1234 proof-phase recheck at `fd995645` (slot15)

Item: `S56-M-1234-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `fd995645725ec3633e4da7e6d759deb14f530861`

Base tree: `5846121ab94ff0502b98217f643539881bc9c045`

## Verdict

`blocked`. The exact universal declaration
`Stage1Rev56.THMM1234.Statement` still has no repo-local or pinned proof body.
This execution adds no proof body and closes no obligation. The proof phase
remains `[ ]`, lifecycle remains `planned`, and the root vector stays
`[H1, M3, R3] -> [H1, M3, R3]`. No proof receipt, provisional state,
audit-completion, theorem-completion, validation, release, or master-acceptance
claim is made.

The six existing owned Lean modules were re-elaborated from source at trust
level zero. They provide only conditional root assembly, constant-in-time
structural candidate fields and their trace, the strict zero-data solution, and
a diagnostic for the malformed closure interface. None proves the canonical
statement for arbitrary `InitialData`.

There is no vacuity or constant-field shortcut. `zero_initial_data` witnesses
that the premise is inhabited. Reusing arbitrary initial fields at every time
discharges the structural fields and trace but leaves
`WeakMomentumEquation u0 (fun _ => u0)`, the stationary Euler identity, which
does not follow from `InitialData`. Zero fields solve only the zero-data case.

No fresh network-wide discovery was performed. The accepted search boundary
for this proof tick is the predecessor anchor audit, which records no exact
compatible external Lean body. The current read-only scan of all 9,676 pinned
package Lean sources likewise found no Yudovich/Yudovitch,
incompressible-Euler, bounded-vorticity, or Biot-Savart terminal candidate. The
legacy `S1_M_158.lean` file records interfaces and formalization debt, not a
root inhabitant.

## Failed Gates

The immediate workflow dependency is unfinished:
`S56-M-1234-OBLIGATION_TREE` is worker-provisional `[_]`, not master-accepted
`[x]`. Its artifacts are also not acceptance-ready:

- `typed-graphs.json` names `M1234-ROOT` as `root_node_id`, but no declared
  `nodes[].node_id` has that value; the root node is `THM-M-1234-ROOT`.
- All 14 validation recipes are shell-string aliases for the structural
  checker. All 14 lack the complete structured `cwd`, `argv`, environment,
  timeout, expected-output, covered-obligation, and covered-declaration fields.
- `CandidateConstructionPackage` consumes none of its approximation, energy,
  or compactness children. `EquationAndTraceClosurePackage` instead quantifies
  over every unrelated candidate, and the checked zero-candidate diagnostic
  shows that it would erase arbitrary admissible initial pairings.

Independently, the first expanded mathematical gap is `M1234-A-APPROX`: no
placeholder-free construction of global smooth Euler approximants for every
frozen `InitialData` witness exists in the repository or pinned closure. The
uniform energy and vorticity estimates, nonlinear-compatible compactness,
structure preservation, momentum limit, and initial trace also remain open.
The direct frozen cut is `M1234-A-STRUCTURE` plus `M1234-E-CLOSURE`.

Twenty-four structured proof packets (21 rechecks, one attempt, and two blocker
packets) predate this attempt, yet the authoritative proof item still records
`attempts: 0` and `children: []`. Blueprint section 10.2 requires the
master/scheduler to reconcile the stale state and split an unresolved item
after five ticks. This worker did not edit the DAG, generated blueprint,
predecessor registry, graphs, validation specifications, or prior artifacts.

## Validation

Checks reused the automation-provided pinned Lake artifacts read-only. No
`lake update`, `lake build`, dependency clone/fetch, network access, checkout
repair, or `.lake` mutation was performed. Generated objects and logs were
confined to a fresh `/tmp` directory and removed. The untracked `.lake` symlink
makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | Rank 158; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `cfa0a02c68993c8b3eefc0edfe7d3d7bd20e2b58d140f47a1f5444a8ba734c5d`; root open at M3 and both analytic packages M4. The checker does not detect the defects above. |
| Isolated trust-zero replay below | 0 | All six modules elaborated with Lean 4.29.0. Printed declarations reported only `propext`, `Classical.choice`, and `Quot.sound`; two nonfatal `unnecessarySimpa` warnings appeared. |
| Prohibited-device scan over owned `*.lean` | 1 | Expected no-match exit: no axiom/constant/opaque/unsafe/extern declaration, `sorry`, `admit`, `sorryAx`, `implemented_by`, or `native_decide` was found. |
| Exact-topic scan over 9,676 pinned package `*.lean` sources | 1 | Expected no-match exit: no exact-topic terminal candidate was found. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `jq empty Stage1_Instances/THM-M-1234/*.json` | 0 | Every pre-existing owned structured JSON artifact parsed before this packet was written. |
| Structured predecessor diagnostic | 0 | The typed root reference is dangling; all 14 recipes are shell-string recipes and all 14 miss the complete required structured field set. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The manifest was absent and remains deliberately absent because the proof phase is incomplete. |

The narrow replay used the exact Lean binary and `LEAN_PATH` selected by the
existing Lake environment:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1234-fd995645-slot15.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1234/{Statement,AnchorAudit,ObligationTree,ConstructionProof,Proof,ClosurePackageDiagnostic}.lean "$tmp"/
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd "$tmp"
for module in Statement AnchorAudit ObligationTree ConstructionProof Proof ClosurePackageDiagnostic; do
  if [ "$module" = Statement ] || [ "$module" = AnchorAudit ]; then
    path="$lean_path"
  else
    path=".:$lean_path"
  fi
  LEAN_NUM_THREADS=1 LEAN_PATH="$path" timeout --foreground 600 \
    "$lean" --trust=0 -t0 -o "$module.olean" "$module.lean" \
    >"$module.stdout" 2>"$module.stderr"
done
```

Lean was version `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; its binary SHA-256 was
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`.
The Lake-produced `LEAN_PATH`, including its trailing newline, hashed
`a1f241207d1001c61dacf122668dd950a44dc8b08db04f212a81bd16627e38f7`.
The paired JSON packet binds all source, environment, object, and output
hashes.

## Retry Condition

The master must reopen the predecessor architecture, publish and accept a
registry-v2 append-only delta with child-consuming construction targets and
closure tied to the specifically constructed candidate, correct the typed root
reference, replace the shell-string aliases with node-specific structured
validation recipes, reconcile the attempt history, and split the analytic
leaves. Then the approximation, estimates, nonlinear compactness,
momentum-limit, and trace bodies can be implemented. An immutable compatible
external root theorem is an alternative only after exact-type, provenance,
trust, and composition checks.

## Status Boundary

This current-base nonrelease packet is a blocker handoff, not a proof receipt.
It does not satisfy `S56-M-1234-PROOF`, propose `[_]`, or support audit or
theorem completion. Because the assigned universal proof phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` is
deliberately absent.
