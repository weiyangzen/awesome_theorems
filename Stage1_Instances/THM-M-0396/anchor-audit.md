# THM-M-0396 Anchor Audit

## Verdict

The bounded rev-5.6 candidate audit found no exact kernel-checked Lean 4 theorem
for the frozen real multiplicative Matveev inequality. Pinned mathlib supplies
the number-field height, real/complex logarithm, exponential, and degree APIs,
but no terminal Baker, Baker-Wuestholz, or Matveev declaration. The legacy local
module is an abstract statement/interface and explicitly carries
formalization debt. Consequently the root remains `M3`; no `M0-W`, `M0-P`, or
theorem-completion credit is available.

## Immutable local audit

The dependency authority is `Formalizations/Lean/lake-manifest.json`. Its
mathlib entry pins commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, used through the canonical `.lake`
symlink without mutation. The full pinned mathlib source search used:

```text
rg -n -i "baker|baker.?w[üu]stholz|wustholz|wuestholz|matveev|linear.?forms?.?in.?logarithms?|linearformsinlogarithms" Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'
```

It exited `1` with no output, meaning no matching source line. The same query
over every other already-pinned package, excluding mathlib, also exited `1`
with no output. This is exact evidence about those immutable source trees. It
does not claim that an unnamed theorem with an unrelated spelling is absent.

`AnchorAudit.lean` elaborates the substrate declarations under Lean 4.29.0.
None has the frozen target type. In particular, `Height.logHeight₁` and
`Module.finrank` support parameters in the target; they do not prove its
explicit inequality.

## External discovery cutoff

On 2026-07-12, six unauthenticated GitHub repository-search queries covering
`Baker theorem`, `Baker Wuestholz`, `Matveev`, and `linear forms in logarithms`
with Lean/Lean4 terms returned zero repositories. Public Sourcegraph code
search returned zero Lean matches for `Matveev`, `Baker-Wuestholz`, and
`LinearFormsInLogarithms`. Sourcegraph excluded forks and archives and reported
shard limits. Grep.app returned HTTP 429. These mutable discovery services
therefore identify no candidate to pin, but cannot establish global absence.
No dependency was fetched or modified.

## Candidate disposition

| Candidate | Exact target match | Body provenance | Disposition |
|---|---|---|---|
| Pinned mathlib substrate at `8a178386...` | No | No terminal body | Keep as `M3` substrate; no wrapper target |
| Legacy `S1_M_009.lean` at repository base `63ffe6d...` | No | Explicitly no analytic body | Discovery only; zero proof credit |
| Public external Lean 4 search | No candidate located | None available to inspect or pin | Re-run at a later cutoff or when a concrete project is nominated |

An external integration task becomes actionable only when it has an immutable
repository revision, module, declaration, exact elaborated type or checked
transport, toolchain/dependency lock, terminal proof-body provenance, and
placeholder/axiom/unsafe audit. Until then, the proof phase must implement the
root or identify a new concrete candidate; it may not promote an anchor-only
record.

## Validation record

Commands were run from the worker clone unless a command says otherwise.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard, skill, 1546-target set, and legacy projections valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets valid |
| `python3 scripts/stage1_target.py show THM-M-0396` | 0 | Rank 9, planned, rework required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| pinned mathlib `rg` shown above | 1 | No matching terminal-name/phrase source lines |
| same `rg` over non-mathlib pinned packages | 1 | No matching source lines |
| `lake env lean ../../Stage1_Instances/THM-M-0396/Statement.lean` from `Formalizations/Lean` | 0 | Printed `Stage1Rev56.THMM0396.Statement.{u} : Prop` |
| `lake env lean ../../Stage1_Instances/THM-M-0396/AnchorAudit.lean` from `Formalizations/Lean` | 0 | Elaborated and printed the five audited substrate declaration types |
| `jq empty Stage1_Instances/THM-M-0396/anchor-audit.json` | 0 | Structured audit artifact is valid JSON |
| `rg -n "\\b(sorry|admit|axiom)\\b|sorryAx|placeholder|unsafe" Stage1_Instances/THM-M-0396/AnchorAudit.lean` | 1 | Expected no-match result: no forbidden proof mechanism in the Lean audit file |
| `git diff --check -- Stage1_Instances/THM-M-0396` | 0 | No whitespace errors in tracked diffs |

The phase audit is complete at its explicit cutoff, while `audit_complete` for
the whole theorem remains false. The next node is the obligation tree, not a
proof-completion or release claim.
