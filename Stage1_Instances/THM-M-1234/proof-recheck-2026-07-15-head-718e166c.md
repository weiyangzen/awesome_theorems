# THM-M-1234 proof-phase recheck at `718e166c`

Item: `S56-M-1234-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `718e166c56e53c552ebb861ee01427f9a606fc72`

Base tree: `f2e15921b967c6f80b9e964361b684b5f9a011d9`

## Verdict

`blocked`. The exact target `Stage1Rev56.THMM1234.Statement` has no proof body
in the owned source or pinned dependency closure. No eligible proof body is
added and no obligation closes in this recheck. The lifecycle remains
`planned`, and the root vector remains `[H1, M3, R3] -> [H1, M3, R3]`.

The direct frozen root cut is `M1234-A-STRUCTURE` plus
`M1234-E-CLOSURE`. The first expanded failed gate is `M1234-A-APPROX`:
there is no checked construction of smooth global Euler approximants for every
`InitialData` witness. Uniform energy and bounded-vorticity estimates,
nonlinear-compatible compactness, structure preservation, passage of the
linear and quadratic momentum terms, and the one-sided initial trace also
remain open.

The current checked local bodies are strictly narrower than the root.
`root_of_construction_and_closure` consumes two explicit package premises.
`candidateConstructionPackage_from_initialData` supplies constant-in-time
fields, but its under-specified formal interface consumes none of the frozen
approximation, energy, or compactness children, so it cannot close the semantic
`M1234-A-STRUCTURE` obligation. `initialCandidateFields_trace` proves the trace
only for that constant candidate. The identically zero construction in
`Proof.lean` proves only the zero-data boundary case. Neither route establishes
the arbitrary-data nonlinear weak momentum equation required by the universal
root.

There is no definitional or vacuity shortcut: `InitialData` is inhabited by
zero data. The legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_158.lean`
contains interfaces and an explicit noncompletion audit, not an exact terminal
body. The pinned mathlib source search found no Yudovich, incompressible-Euler,
or bounded-vorticity existence theorem. The immutable predecessor anchor audit
likewise found no compatible external Lean body eligible for pinned import.

## Failed Gate And Retry

The first failed gate is `M1234-A-APPROX`. Resume only after an accepted repair
of the child-consuming obligation interfaces and placeholder-free bodies for
smooth approximation, uniform estimates, nonlinear-compatible compactness,
momentum limit passage, and initial trace. An immutable exact Lean 4 terminal
body could instead be pinned and checked for exact type, trust, and provenance.
Assuming either missing package, adding an axiom, or substituting the zero-data
case is not eligible.

The predecessor `S56-M-1234-OBLIGATION_TREE` is also only worker-provisional
`[_]`, not master-accepted, so dependency-legal master closure of this proof
item is independently unavailable at this base.

## Validation

All checks ran in this worker clone against the existing pinned Lake artifacts.
The pre-existing untracked `Formalizations/Lean/.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed. All generated Lean objects and
captured output were kept in a temporary directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | Rank 158; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `cfa0a02c...34c5d`; root open at M3. |
| Isolated trust-zero five-module Lean replay below | 0 | All modules elaborated; printed proof declarations reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no prohibited construct was found. |
| Exact-topic search in pinned mathlib Lean sources | 1 | Expected no-match exit for Yudovich, Yudovitch, incompressible Euler, and bounded vorticity. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1234/proof-recheck-2026-07-15-head-718e166c.json >/dev/null` | 0 | This structured blocker packet is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1234 .stage1-worker-selftest.json` | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Required self-test manifest remains absent because the proof phase is incomplete. |

Bounded GitHub repository API discovery was also performed without cloning or
fetching dependencies. Queries for `Yudovich Lean` and `Euler PDE Lean4`
returned zero repositories. The quoted `incompressible Euler` plus `Lean`
query returned one three-dimensional critical-inequality project, and
`vorticity Lean4` returned the already audited three-dimensional Navier-Stokes
and SQG projects. None states or proves the exact two-dimensional Yudovich
root. Each `curl -LfsS <GitHub repository-search API URL> | jq ...`
pipeline exited 0; because `pipefail` was not set, that is formally the `jq`
status, although each response was parseable JSON. Unauthenticated GitHub code
search was unavailable and is not credited as negative evidence.

The successful narrow Lean replay was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1234-proof-head-718e166c.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1234/{Statement,AnchorAudit,ObligationTree,ConstructionProof,Proof}.lean "$tmp"/
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
export LEAN_NUM_THREADS=1
cd "$tmp"
LEAN_PATH="$lean_path" timeout 600 "$lean" --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_PATH=".:$lean_path" timeout 600 "$lean" --trust=0 -t0 AnchorAudit.lean
LEAN_PATH=".:$lean_path" timeout 600 "$lean" --trust=0 -t0 -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$lean_path" timeout 600 "$lean" --trust=0 -t0 ConstructionProof.lean
LEAN_PATH=".:$lean_path" timeout 600 "$lean" --trust=0 -t0 Proof.lean
```

The replay produced `Statement.olean` SHA-256
`1709e38a5b8cc96159b7042585666cb84536b4b3d9e26a63697992cd9820d308`.
The paired JSON packet records source and output hashes.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does
not satisfy `S56-M-1234-PROOF`, change task state, or claim audit completion,
theorem completion, validation, release, or master acceptance.
`accepted_receipt_ids=[]`. Because the assigned universal proof phase is not
self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.
