# THM-M-0112 proof recheck at `6283de2` (slot 10)

Item: `S56-M-0112-PROOF`. Intent: `prove`. Base revision:
`6283de2dc03ba380a29fbfb2a045ad7e75ce8da4`; base tree:
`c369fd831f0133c0171276e7822862ee3e0d341b`.

## Verdict

`blocked`. No positive proof body, obligation closure, debt improvement, provisional item state, or
master acceptance is claimed. The assigned proof phase is not self-tested as complete, so
`.stage1-worker-selftest.json` is deliberately absent.

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY / M0112-S-INTERFACE`.
`Statement.lean` stores the four geometric conditions and `piMapIsInducedByInclusion` as
unconstrained propositions while allowing `piMap` to be an arbitrary function. The existing
placeholder-free declaration

```text
Stage1Instances.THMM0112.Proof.not_weakTopologicalLefschetzTarget :
  Not (Stage1Instances.THMM0112.WeakTopologicalLefschetzTarget.{0, 0})
```

kernel-checks a countermodel. It takes `X = PUnit`, discrete `Y = Bool`, complex dimension two,
constant inclusion, constant `piMap`, and makes all five opaque premises true. The target then
requires the degree-zero map to be injective because `0 < 2 - 1`, although the constant map
identifies the distinct `false` and `true` path components. Any positive universe-polymorphic proof
would specialize to universes `(0, 0)` and contradict this declaration.

This refutes only the frozen abstract encoding, not the mathematical Lefschetz hyperplane theorem.
Repairing the interface inside this proof-only item would change the accepted statement fingerprint
and invalidate the frozen registry. Assuming either substantive conclusion package would be
circular and is prohibited.

The accepted root vector remains `[H1, M3, R3]`; this packet proposes `[H5, M5, R3]` only as a
diagnosis for master review. `M0112-T-ASSEMBLE` remains a conditional composition certificate. The
frozen root cut set remains `M0112-B-BELOW` plus `M0112-B-EDGE`. The lifecycle remains `planned`,
and audit completion, theorem completion, validation, release, and master acceptance remain false.

At preflight, 32 matched unresolved JSON/Markdown proof-recheck pairs already existed while the
authoritative DAG still reported `attempts = 0` and no child nodes. Blueprint section 10.2 requires
the master or scheduler to reconcile the attempt count and split or redirect this repeatedly
blocked item. This worker did not edit the DAG or generated checklist.

## Retry Condition

Reopen `S56-M-0112-STATEMENT`; replace the opaque stand-ins with faithful complex-geometric
constructions and a noncircular law tying `piMap` to the actual inclusion-induced homotopy map;
accept a new exact-statement fingerprint and obligation-registry version; then rerun statement,
anchor-audit, obligation-tree, and proof phases. The pinned sources expose homotopy-group substrate
but no terminal weak Lefschetz theorem or the missing analytification, relative-homotopy,
Lefschetz-pencil, Morse, and cellular-attachment bridges.

## Validation

All Lean work reused the existing pinned Lake environment. No `lake update`, `lake build`, clone,
fetch, network access, or intentional `.lake` mutation was used. The worktree already contained the
automation-provided untracked `Formalizations/Lean/.lake` symlink, so this is nonrelease evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0112` | 0 | Rank 35, `planned`, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0112/check_statement.py` | 0 | Statement fingerprint `1daee7f6...e654`; all four required structural mutations killed. |
| `python3 Stage1_Instances/THM-M-0112/check_anchor_audit.py` | 0 | Three pinned substrate candidate families checked; terminal result open. |
| `python3 Stage1_Instances/THM-M-0112/check_obligation_tree.py` | 0 | 13 obligations and 31 typed edges passed; denominator `5d119562...7df7f4`; root open at M3. |
| Isolated trust-zero `lake env` replay of copied `Statement.lean` and `Proof.lean` | 0 | The statement and its negation elaborated; the negative declaration reports `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-token scan of `Proof.lean` | 1 | Expected no-match exit: no `sorry`, `admit`, `sorryAx`, `native_decide`, `axiom`, `unsafe`, `external`, or `implemented_by`. |
| Pinned-source terminal/API search | 1 | Expected no-match exit: no requested terminal theorem or named high-level bridge was found. |
| `python3 -m json.tool` on the adjacent JSON | 0 | The blocker packet is valid JSON. |
| Packet consistency check | 0 | Base/tree and source hashes match; all completion booleans are false; 33 record pairs exist; self-test is absent. |
| ASCII, line-ending, trailing-whitespace, and `git diff --check` checks | 0 | The two new artifacts passed. |

Exact narrow kernel recipe:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-0112-proof-head-6283de2-slot10.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0112/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0112/Proof.lean "$tmp/Proof.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground --kill-after=5s 600s \
  "$lean" --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH=.:"$lean_path" timeout --foreground --kill-after=5s 600s \
  "$lean" --trust=0 -t0 -o Proof.olean Proof.lean
```

Exact negative scans, where exit one is the expected no-match result:

```bash
rg -n --pcre2 '\b(?:sorry|admit|sorryAx|native_decide)\b|^[[:space:]]*(?:axiom|unsafe|external)\b|implemented_by' \
  Stage1_Instances/THM-M-0112/Proof.lean
rg -n -i 'weak[ _-]*lefschetz|lefschetz[ _-]*hyperplane|hyperplane[ _-]*section|analytification|relative[ _-]*homotopy' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib \
  Formalizations/Lean/.lake/packages/flt-regular --glob '*.lean'
```

The temporary object hashes were
`f869a1057c46e20107dd3464966d1b86c9d534d61224242ff1fc9576dffb2a77` for
`Statement.olean` and `5d11e1de5da347e936936bf2c5b4e965306a7639f98ee54404d58dfcd0173b82`
for `Proof.olean`. A before/after metadata digest of the dereferenced pinned dependency cache,
excluding its self-referential `.lake` symlink, was identical
(`79f59baa304b62145b389fd84a326033a9e2cb884dad6da47da1f1eaa3349f25`); this is a
mutation guard, not a content-addressed release receipt.

The adjacent JSON binds this result to the base/tree identities, source hashes, registry,
environment, exact commands, and status boundary. With this packet, the owned path contains 33
matched recheck pairs. It is a blocker packet, not a proof receipt.
