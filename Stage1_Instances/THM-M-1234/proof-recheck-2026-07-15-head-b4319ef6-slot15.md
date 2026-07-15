# THM-M-1234 proof-phase recheck at `b4319ef6` (slot15)

Item: `S56-M-1234-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `b4319ef6d039de12cec559f173287d541c238d70`

Base tree: `0b0762ebd01405d33218c3bcbcb24d4544b0fad0`

## Verdict

`blocked`. The exact universal declaration
`Stage1Rev56.THMM1234.Statement` still has no repo-local or pinned proof body.
This execution adds no proof body and closes no obligation. The proof phase
remains `[ ]`, lifecycle remains `planned`, and the root vector stays
`[H1, M3, R3] -> [H1, M3, R3]`. No proof receipt, audit-completion,
theorem-completion, validation, release, or master-acceptance claim is made.

The existing checked source provides conditional root assembly, a
constant-in-time structural candidate and its trace, and the strict zero-data
solution. None proves the canonical statement for arbitrary `InitialData`.
The legacy `S1_M_158.lean` artifact likewise defines an existence package and
projects its fields only after a solution is supplied; it explicitly records
the construction and nonlinear limit as formalization debt. It is not an
alternate root proof.

This proof-phase recheck made no fresh network-wide external search. Its
external boundary is the predecessor audit, which records no exact compatible
terminal Lean body eligible to pin or import; no claim of exhaustive external
nonexistence is made here.

The checked target diagnostic also confirms a defect in frozen registry
version 1: `EquationAndTraceClosurePackage` quantifies over every structurally
admissible candidate. Applying it to unrelated zero fields forces every
admissible initial velocity and vorticity test pairing to vanish. Meanwhile,
`CandidateConstructionPackage` consumes none of its approximation, energy, or
compactness children. These interfaces cannot certify the intended analytic
composition.

The tempting constant-candidate route does not conceal a short proof. For
arbitrary data it closes the structural fields and trace but leaves
`WeakMomentumEquation u0 (fun _ => u0)`, a stationary Euler identity not
implied by `InitialData`. A sound replacement would construct a particular
candidate together with its momentum and trace proofs; inhabiting that
dependent package is precisely the missing Yudovich formalization.

## Failed Gates

The immediate dependency gate is unfinished:
`S56-M-1234-OBLIGATION_TREE` is worker-provisional `[_]`, not master-accepted
`[x]`. Its structured artifacts also need predecessor repair before acceptance:

- `typed-graphs.json` names `M1234-ROOT` as `root_node_id`, but the declared
  root `node_id` is `THM-M-1234-ROOT`.
- Each of the 14 validation recipes is a shell-string alias for the structural
  checker, rather than a node-specific structured `cwd`/`argv` recipe with
  fixed environment, timeout, expected outputs, covered obligation IDs, and
  covered declarations.
- The construction target ignores its analytic children, while the closure
  target is overquantified and not tied to the candidate built by construction.

Independently, the first expanded mathematical gap is `M1234-A-APPROX`: no
child-consuming, placeholder-free construction of global smooth Euler
approximants for every frozen `InitialData` witness exists in the repository or
pinned dependency closure. Uniform energy and bounded-vorticity estimates,
nonlinear-compatible compactness, structure preservation, passage of the
linear and quadratic momentum terms, and the initial trace also remain open.
The direct frozen root cut is `M1234-A-STRUCTURE` plus `M1234-E-CLOSURE`.

Twenty-three structured proof packets (20 rechecks, one attempt, and two
blocker packets) predate this attempt, but the authoritative proof item still
records `attempts: 0` and `children: []`. Blueprint section 10.2 requires the
master/scheduler to
reconcile this stale state and split the oversized item after five unresolved
ticks. This worker did not edit the DAG, generated blueprint, predecessor
registry, graphs, or validation specifications.

## Validation

All checks reused the existing pinned artifacts read-only. No `lake update`,
`lake build`, dependency clone/fetch, network access, checkout repair, or other
`.lake` mutation was performed. Generated Lean objects and logs stayed in a
fresh `/tmp` directory and were removed. The automation-provided untracked
`.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | Rank 158; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `cfa0a02c68993c8b3eefc0edfe7d3d7bd20e2b58d140f47a1f5444a8ba734c5d`; root open at M3 and both analytic packages M4. This checker does not detect the defects above. |
| Isolated trust-zero Lean replay below | 0 | All six owned modules elaborated with Lean 4.29.0. Printed proof declarations reported only `propext`, `Classical.choice`, and `Quot.sound`; two nonfatal `unnecessarySimpa` warnings appeared. |
| Prohibited-device scan over owned `*.lean` | 1 | Expected no-match exit: no `sorry`, `admit`, declared axiom/constant, unsafe/opaque/extern escape, `sorryAx`, `implemented_by`, or `native_decide` was found. |
| Exact-topic scan over all 9,676 pinned package `*.lean` sources | 1 | Expected no-match exit: no Yudovich/Yudovitch, incompressible-Euler, bounded-vorticity, or Biot-Savart terminal candidate was found. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `jq empty Stage1_Instances/THM-M-1234/*.json` | 0 | Every pre-existing owned structured JSON artifact parsed before this packet was written. |
| Structured predecessor conformance diagnostic | 0 | Confirmed `root_node_id=M1234-ROOT` is absent from `nodes[].node_id`; all 14 recipes use shell-string commands and lack the required structured fields. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The self-test manifest was absent and remains deliberately absent because the proof phase is incomplete. |

The narrow replay used only the exact binary and `LEAN_PATH` selected by the
existing Lake environment:

```bash
set -u
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-1234-b4319ef6-slot15.XXXXXX)
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
    >"$module.stdout" 2>"$module.stderr" || exit $?
done
```

Lean was version `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; its binary SHA-256 was
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`.
The Lake-produced `LEAN_PATH`, including its trailing newline, hashed
`a1f241207d1001c61dacf122668dd950a44dc8b08db04f212a81bd16627e38f7`.
The paired JSON packet binds the source, environment, object, and output
hashes.

## Retry Condition

The master must reopen the predecessor architecture, publish and accept an
append-only registry version with child-consuming construction targets and
closure tied to the specifically constructed candidate, correct the typed root
reference, replace the shell-string recipe aliases with node-specific
structured validation, reconcile the attempt history, and split the analytic
leaves. Then the approximation, estimates, nonlinear compactness,
momentum-limit, and trace bodies can be implemented. An immutable compatible
external terminal theorem is an alternative only after exact-type,
provenance, trust, and composition checks.

## Status Boundary

This current-base nonrelease packet is a blocker handoff, not a proof receipt.
It does not satisfy `S56-M-1234-PROOF`, propose `[_]`, or support audit or
theorem completion. Because the assigned universal proof phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` is
deliberately absent.
