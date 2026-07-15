# THM-M-0468 proof phase: current-base blocker

Item: `S56-M-0468-PROOF`

Base revision: `50db6284742415b7da294d323c820bf4b224711d`

Base tree: `bb477aa021efaf69c84ee3a98f486f4ba407bae2`

Validated: `2026-07-15T16:32:57+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`: no consistent positive proof body can inhabit the exact frozen Lean
target. The proof item remains `[ ]`; no proof, provisional state, validation,
release, theorem completion, receipt acceptance, or master acceptance is
claimed. A root `.stage1-worker-selftest.json` is deliberately absent.

`Statement.lean` quantifies over every `BogomolovData`, but the record has no
laws connecting its operations or predicates to abelian geometry. The
placeholder-free `ProofBlocker.lean` constructs singleton carriers for which
all ambient hypotheses and density claims hold while `isTorsionPoint` is false
everywhere. Trust-zero Lean checks

```text
Stage1Instances.THM_M_0468.not_bogomolovTarget :
  Not Stage1Instances.THM_M_0468.BogomolovTarget
```

The declaration is sorry-free and depends only on `propext`,
`Classical.choice`, and `Quot.sound`. A positive inhabitant of the frozen root
would contradict this declaration. This refutes only the overbroad abstract
Lean encoding, not the mathematical Ullmo--Zhang theorem. The checked
`root_of_direction_packages` declaration assumes both missing implications
and supplies no positive proof-body credit.

The first substantive proof failure is exact-target consistency at
`M0468-S-DOMAINS`. Separately, the predecessor
`S56-M-0468-OBLIGATION_TREE` is worker-provisional `[_]`, not master-accepted
`[x]`. Rev-5.6 permits provisional later-node preparation under concurrency,
but proof-node master closure remains dependency-illegal.

## Retry Condition

Reopen `S56-M-0468-STATEMENT`. Replace the unconstrained record with concrete
pinned definitions, or add source-justified noncircular laws connecting
height, torsion, translation, subvariety membership, and Zariski density. The
repair must rule out the countermodel without assuming either direction of the
desired equivalence. It must also add the rev-5.6 changed-domain,
binder-scope, and boundary-case mutations absent from the current four
predicate-removal mutations. Then freeze and accept a new statement
fingerprint, obligation registry, typed graph, and node-scoped validation
specifications before rerunning proof work.

This directory contained 29 earlier target-scoped blocker/recheck JSON packets,
including 25 head-bound proof blockers, before this packet. The authoritative
proof item still records `attempts: 0` and no children. Rev-5.6 section 10.2
requires splitting after five unresolved execution ticks. The master should
reconcile scheduler accounting and redirect work to statement repair rather
than scheduling another unchanged positive-proof attempt. This worker did not
edit the authoritative DAG.

## Scoped Validation

All commands ran in this worker clone. The automation-provided untracked
`.lake` symlink to canonical pinned artifacts was reused read-only. No `lake
update`, `lake build`, dependency clone/fetch, checkout repair, network
command, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0468` | 0 | Rank 314; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0468/check_statement.py` | 0 | Fingerprint `def6574...fa0e`; the four recorded predicate-removal mutations passed. This does not cover the three missing mutation classes. |
| `python3 Stage1_Instances/THM-M-0468/check_anchor_audit.py` | 0 | Target fingerprint, exact pin, module hash, and four candidate classifications passed. |
| `python3 Stage1_Instances/THM-M-0468/check_obligation_tree.py` | 0 | 20 obligations and 44 typed edges passed; denominator `0b324115...6c4`; root remains open at `M4`. |
| Pinned `lake env lean --trust=0` replay below | 0 | Exact target, conditional composition, and exact negation elaborated; both proof declarations were sorry-free and had axioms `[propext, Classical.choice, Quot.sound]`. |
| `rg -n '\b(sorry\|admit\|sorryAx\|native_decide)\b\|^[[:space:]]*(axiom\|unsafe\|external)[[:space:]]'` over the three checked Lean sources | 1 | No matches; exit 1 is ripgrep's expected no-match result. |
| Pinned dependency-source alias search | 1 | No relevant Bogomolov/canonical-height/small-point/special-subvariety declaration matched; exit 1 is ripgrep's expected no-match result. |

The replay used collision-free copies in a fresh `/tmp` directory, removed by
a trap. It ran from `Formalizations/Lean` so `lake env lean` used the canonical
pinned environment directly. The JSON companion records each Lean invocation
as a structured `argv` array with its repository-relative working directory,
environment, timeout, network policy, exit, covered obligations, and covered
declarations.

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-0468-head-50db6284-slot42-canonical.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
sed 's/^import Statement$/import M0468Statement/' \
  "$root/Stage1_Instances/THM-M-0468/ObligationTree.lean" \
  > "$tmp/M0468ObligationTree.lean"
sed 's/^import Statement$/import M0468Statement/' \
  "$root/Stage1_Instances/THM-M-0468/ProofBlocker.lean" \
  > "$tmp/M0468ProofBlocker.lean"
cp "$root/Stage1_Instances/THM-M-0468/Statement.lean" \
  "$tmp/M0468Statement.lean"
cd "$root/Formalizations/Lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" timeout --foreground --kill-after=10s 300 \
  lake env lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/M0468Statement.olean" "$tmp/M0468Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" timeout --foreground --kill-after=10s 300 \
  lake env lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/M0468ObligationTree.olean" "$tmp/M0468ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" timeout --foreground --kill-after=10s 300 \
  lake env lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/M0468ProofBlocker.olean" "$tmp/M0468ProofBlocker.lean"
printf '%s\n' \
  'import M0468ObligationTree' \
  'import M0468ProofBlocker' \
  'import Mathlib.Util.AssertNoSorry' \
  '' \
  'open Stage1Instances.THM_M_0468' \
  '' \
  '#check BogomolovTarget' \
  '#check root_of_direction_packages' \
  '#check not_bogomolovTarget' \
  'assert_no_sorry root_of_direction_packages' \
  'assert_no_sorry not_bogomolovTarget' \
  '#print sorries root_of_direction_packages' \
  '#print sorries not_bogomolovTarget' \
  '#print axioms root_of_direction_packages' \
  '#print axioms not_bogomolovTarget' > "$tmp/Probe.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" timeout --foreground --kill-after=10s 300 \
  lake env lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Probe.olean" "$tmp/Probe.lean"
sha256sum "$tmp/M0468Statement.olean" \
  "$tmp/M0468ObligationTree.olean" "$tmp/M0468ProofBlocker.olean" \
  "$tmp/Probe.olean"
```

The four temporary olean hashes were, respectively,
`ceaf7430cba2e39a950d7684b0ba6278f2d95b6df695ad3ae0c3fbcd87e6c689`,
`5d46f876330d38723ff860d92dd85c4ff230ef3cca8ec2157e320fed2ff47841`,
`a4afb48af34b95c7b20e22f352cac526a32084532083bace11358507c5fa8c17`,
and `6c60263d9c8044afed458d2b63b7f0c478cb41062516e5643d5006e211eead13`.

Pinned identities are Lean `4.29.0` at
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib commit/tree
`8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

The frozen `validation-specs.json` routes every obligation through the graph
checker and does not bind the relevant Lean declarations. Passing that checker
therefore establishes graph consistency, not semantic closure. The structured
packet is explicitly non-content-addressed and current only for this base; it
is actionable negative kernel evidence, not a proof receipt or item-state
transition.
