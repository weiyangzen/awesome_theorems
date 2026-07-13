# Intake validation

Base revision: `1c0c5fc6f43e6ae5ecc3b50589b45c3628e0ead4` (tree
`61214aa2a03c032134ddc4958b1df63df3430a85`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers target membership, planned lifecycle, the source and scope crosswalk, the open
six-task DAG, immutable repository and dependency identities, a narrow pinned Lean API probe, the
read-only external-candidate object, JSON and dossier invariants, prohibited-construct hygiene, and
whitespace. It does not validate an exact Ore statement or proof.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was reused read-only. No
`lake update`, `lake build`, dependency clone or fetch, branch checkout, or other `.lake` mutation
was performed. This is nonrelease worker evidence.

## Environment

- Platform: Linux 7.0.0-27-generic, x86_64; timezone Asia/Shanghai.
- Lean: 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- External source lead: existing Git object `c83689ab8f1abfba1f646e65dc8b131fd256b73f`;
  not checked out, built, imported, or credited.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0854` | 0 | rank 1408, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the pre-existing `.lake` symlink; base revision and tree recorded above |
| `git blame -L 6264,6269 -- Docs/researches/math_theorems.md` | 0 | all six catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error https://api.crossref.org/works/10.2307/2308928`, selecting the recorded fields with `jq -S` | 0 | exact Ore, 1960, title, venue, volume, issue, and page match; selected canonical JSON SHA-256 `34a78ad13eec2845595bff9157d71c153fa3b6498594f2a268083b93d2af5bf0`; metadata only |
| `curl -L --silent --show-error https://www.jstor.org/stable/pdf/2308928.pdf` | 0 | 5816-byte access-check HTML, not article content; no primary statement admission |
| `curl -L --fail --silent --show-error https://export.arxiv.org/pdf/1805.05149v1 -o /tmp/1805.05149v1.pdf`; `pdftotext -layout` | 0 | PDF SHA-256 `60e37541a790f905531f8fd9ff5f31deab3d6a6bc0ba7a97a56836683a66555b`; Theorem 1 on PDF p. 2 states the simple-graph, order-at-least-three, degree-sum implication; secondary corroboration only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision/tree agree and package source is clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0854/IntakeProbe.lean)` | 0 | ten adjacent graph, degree, Hamiltonicity, and boundary APIs elaborated; output SHA-256 `20de440dc41f5b86d6b82713d3174a775c49089e230af80187d228266de1fbce` |
| bounded `rg` for Ore and Bondy-Chvatal declarations in repo-local and pinned `Mathlib` Lean | 1 expected | no exact target declaration in the pinned closure; intake discovery only |
| `git -C Formalizations/Lean/.lake/packages/mathlib show-ref --verify refs/remotes/origin/meow-sister/BondyChvatal_PR` | 0 | ref resolves to `c83689ab8f1abfba1f646e65dc8b131fd256b73f` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse` for the candidate tree, Bondy-Chvatal file, and toolchain | 0 | tree `1f6492...`, source blob `fe5f07...`, toolchain blob `98556b...` |
| `git -C Formalizations/Lean/.lake/packages/mathlib merge-base 8a178386... c83689ab...` | 0 | merge base `3bebc671e9c9c1b535ad7ce3a6f96a2263835424` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-list --left-right --count 8a178386...c83689ab...` | 0 | `16380 79`; divergent revisions |
| `git show` each of `BondyChvatal.lean` and its three direct imports at `c83689ab...`, piped to the recorded prohibited-construct `rg` expression | 1 expected | no `sorry`, `admit`, `sorryAx`, bodyless axiom/constant/opaque, unsafe, or extern marker matched; source scan only |
| `python3 -m json.tool` on the three owned JSON files and root packet | 0 | valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0854-pycache python3 -m py_compile Stage1_Instances/THM-M-0854/check_intake.py` | 0 | checker compiles without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0854/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source pins, H1/M4/R4 null target, external boundary, inventory, packet, and six open tasks agree |
| prohibited Lean construct scan of `IntakeProbe.lean` | 1 expected | no proof escape or assumed declaration matched |
| per-file no-index whitespace checks and scoped `git diff --check` | 0 | no whitespace diagnostics |

## Status boundary

This is a self-tested `planned` intake proposal. The exact primary statement, pair distinctness,
three-vertex bound, graph and Hamiltonicity conventions, canonical Lean expression, checked
transports and mutations, and every later assurance gate remain open. The source-visible external
branch body has no reproduced kernel evidence and is outside the pinned closure; it receives no
M1 or M0 credit. No accepted state, audit completion, theorem completion, or master acceptance is
claimed.
