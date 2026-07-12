# Anchor-audit validation record

Item: `S56-M-0657-ANCHOR_AUDIT`  
Base revision: `9dd26b41d0fd448cfe71600d74accc729bff401b`

## Verdict

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
the usable anchors are the definition `Cardinal.Categorical`, its
Los-Vaught completeness consequence, and the ACF and DLO categoricity examples.
None has the canonical root type: ACF and DLO concern particular theories, and
`Categorical.isComplete` derives completeness rather than categoricity transfer.

Five relevant external repositories were inspected at the immutable commits in
`anchor-audit.json`. The one Lean 4 project with a categoricity API supplies
only a many-sorted definition and Los-Vaught result. The Lean 3 project supplies
ACF special cases. The remaining three Lean 4 archives contain no Morley or
categoricity candidate. Thus no external exact proof is waiting to be imported,
and no `repo_local_integration_debt` is created. The root remains `M3` with
`formalization_debt`; this phase gives no theorem proof credit.

## Commands and results

All local Lean commands used the existing pinned Lake environment. No dependency
update, fetch, clone, or build command was run.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0657/AnchorAudit.lean` | 0 | Four anchors resolved; `#print axioms` reported `propext`, `Classical.choice`, and `Quot.sound` for each theorem anchor. |
| `python3 Stage1_Instances/THM-M-0657/check_anchor_audit.py` | 0 | Checked item identity, fail-closed candidate classifications, manifest digest, and exact mathlib pin. |
| `rg -n -i 'Morley|uncountabl.*categor|categor.*uncountabl|categoricity|Categorical' Formalizations/Lean/.lake/packages/mathlib/Mathlib/ModelTheory` | 0 | Only the recorded foundation, ACF, and DLO hits; no Morley transfer declaration. |
| GitHub repository search for `model theory language:Lean`, `categoricity language:Lean`, and `Morley language:Lean`, followed by commit-addressed GitHub source archives and `rg -n -i 'morley|uncountabl.*categor|categor.*uncountabl|categoricity|categorical' --glob '*.lean'` | 0 | Audited the five repositories and revisions recorded in JSON; only the two non-exact families described above matched. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard and 1546-target coverage valid. |
| `python3 scripts/stage1_target.py check` | 0 | Ordered manifest valid. |
| `python3 scripts/stage1_target.py show THM-M-0657` | 0 | Rank 702, planned, L0/rework-required, theorem incomplete. |
| `git diff --check -- Stage1_Instances/THM-M-0657 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

External archives were downloaded only under `/tmp` for read-only inspection;
they were not added to `.lake` or treated as dependencies. GitHub API/grep.app
discovery calls that returned HTTP 429/403 were not used as positive or
negative evidence; the successful commit-addressed archives are the audit
surface.
