# THM-M-1037 statement-phase blocker

Item: `S56-M-1037-STATEMENT`  
Base revision: `d8e739d08e6a4c17f08c309bafac6637d21620bb`  
Verdict: `blocked`

## First failed gate

The rev-5.6 exact-source/statement gate fails before Lean elaboration. The authoritative target
metadata provides the name `强解与弱解` and only the description `SDE解的不同概念` (different
concepts of SDE solutions). This is a topic, not a truth-valued proposition. It does not determine
whether the target is a definition, an implication, an existence claim, an equivalence, or a
uniqueness result, and it fixes none of the coefficient, stochastic-basis, Brownian-driver,
initial-condition, filtration-completion, stochastic-integral, or equality conventions needed to
state one of those claims.

The intake's proposed strong-to-weak forgetful map cannot be promoted to the canonical statement:
it is explicitly marked as a candidate, and the historical `S1_M_230.lean` packages the stochastic
integral and SDE equation as arbitrary proposition fields. Elaborating that wrapper again would
show only that the substituted abstraction type-checks, not that it is the exact manifest target.
The adjacent `THM-M-1038` separately owns the Yamada-Watanabe theorem, so that result cannot be used
to resolve the ambiguity either.

Consequently there is no honest Lean declaration or expression to place in an owned `Statement.lean`,
no elaborated-expression hash to record, and no meaningful minimal-import or mutation-test result.
Creating any of them would invent missing mathematics and violate the statement identity gate.

## Retry condition

An authoritative source decision must identify one exact definition or proposition and pin a
primary-source edition plus page/theorem locator. It must freeze the full SDE model and all ordered
binders, hypotheses, conventions, and conclusion. Only then can this phase introduce the canonical
Lean expression, minimize its imports, serialize its elaborated form and environment fingerprint,
and run the required removed-hypothesis, changed-domain, binder-scope, and boundary mutations.

## Validation record

Commands were run from the worker clone root on 2026-07-12.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1037` | 0 | rank 230; `planned`; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `rg -n '定理内容: SDE解的不同概念\|THM-M-1037 强解与弱解' Docs/Stage0_Blueprint.md Docs/Stage1_Blueprint.md` | 0 | confirms the only repository-level description is the topic phrase quoted above |
| `git rev-parse HEAD` | 0 | `d8e739d08e6a4c17f08c309bafac6637d21620bb` |

No `lake env lean` command was represented as target validation: the exact target does not yet
exist, and checking the legacy candidate would be evidence for a broadened or substituted theorem.
This blocker does not complete the statement phase, change lifecycle or debt, or establish any
machine proof credit.
