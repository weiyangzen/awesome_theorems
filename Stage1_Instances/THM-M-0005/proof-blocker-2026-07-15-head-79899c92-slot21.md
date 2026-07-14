# THM-M-0005 proof execution blocker

Item: `S56-M-0005-PROOF`

Base revision: `79899c925fb9bacf9126eb11f7f24954b0516a3d`

Execution date: 2026-07-15 (Asia/Shanghai)

## Verdict

The proof phase remains blocked at `[ ]`. The exact root is not inhabited, no obligation receives
closure credit, and no worker self-test manifest is written. This execution adds a current-head
blocker receipt rather than relabeling the existing partial proof bodies as theorem closure.

## Checked progress and first failed gate

The existing owned sources genuinely prove degreewise freeness and projectivity of singular chains,
the tensor and `Tor₁` direct-sum maps, their component formulas and functor laws, and conditional
composition to `KunnethFormula`. The conditional theorem takes the Kunneth inclusion, projection,
zero composite, short exactness, and two naturality families as explicit premises; it does not
construct them.

The first failed root-critical gate is `M0005-EZ-MAP`. Pinned mathlib has singular homology,
tensor-complex, `Tor`, coproduct, and `ShortExact` infrastructure, but no placeholder-free
Eilenberg-Zilber or Alexander-Whitney chain comparison. Algebraic Kunneth maps, exactness, and
naturality are also absent. The sole audited external candidate,
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`, terminates in `sorry` on
every root-critical route and does not exactly match the frozen universe and naturality/component
surface. It therefore receives no proof credit.

## Narrow validation

The automation-provided canonical `.lake` symlink was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0005` | 0 | Rank 100, lifecycle `planned`, lane `hard_mathlib_anchor_and_wrapper`, `theorem_complete: false`. |
| Isolated `lake env` Lean replay of `KunnethStatement.lean`, `ObligationTree.lean`, `Proof.lean`, and `ProofProgress20260715Slot21.lean` | 0 | All modules elaborated with `--trust=0`; every printed declaration used exactly `propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx`. |
| `python3 Stage1_Instances/THM-M-0005/check_obligation_tree.py` | 0 | Passed 18 obligations and 51 typed edges with denominator `563eac891739af1e2468c4fd23e7465013f9e5791e069a03e22ccdf67119a762`; root remains open at M3. |
| `rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe' Stage1_Instances/THM-M-0005 --glob '*.lean'` | 1 | No prohibited construct; exit 1 is ripgrep's no-match result. |

The exact replay recipe was:

```bash
lean=$(cd Formalizations/Lean && lake env which lean)
base_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
tmp=$(mktemp -d /tmp/thm-m-0005-slot21-recheck.XXXXXX)
cp Stage1_Instances/THM-M-0005/{KunnethStatement,ObligationTree,Proof,ProofProgress20260715Slot21}.lean "$tmp/"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout 600 "$lean" --trust=0 -t0 \
  -R "$tmp" -o "$tmp/${src%.lean}.olean" "$tmp/$src"
```

The last command was run for each module in dependency order. `KunnethStatement`, `ObligationTree`,
and `Proof` exited 0. `ProofProgress20260715Slot21` first exited 124 at the 600-second process timeout
without a diagnostic; the identical command with `timeout 1800` then exited 0. The progress `.olean`
SHA-256 is
`686162f75e24ab6645aa5bc914764a0d4e6e3ad90a09f1b57e2509bac0948f1b`; its axiom output SHA-256 is
`3290b52c414f29c959ee82ecb1f0e7a2de6d58bce83e21905581a58b87157f18`.

## Required unblock condition

Provide placeholder-free Eilenberg-Zilber and algebraic Kunneth implementations at the frozen
types, or an immutable compatible proof already present in the pinned dependency closure. Then
implement the grading/direct-sum transports, construct the topological inclusion and projection,
prove exactness and two-variable naturality, and compose them unconditionally to the unchanged
`KunnethFormula` root. Until then the vector remains `[H1, M3, R3]`, and this proof item cannot
truthfully receive `[_]` or theorem-completion credit.
