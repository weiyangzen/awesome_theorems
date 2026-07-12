# Anchor-audit validation record

Base revision: `937d8467b6060fe4128f6ddd0b930b16ba7bd6e6`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1027` | 0 | rank 218, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1027/AnchorAudit.lean` | 0 | all eight pinned-mathlib `#check` anchors elaborated and the candidate-contract expansion was kernel checked |
| `printf 'import BrownianMotion.Gaussian.BrownianMotion\n#check ProbabilityTheory.IsBrownian\n' \| (cd Formalizations/Lean && lake env lean --stdin)` | 1 | expected integration blocker reproduced: `unknown module prefix 'BrownianMotion'` |
| `rg -n -i 'brownian\|wiener' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | sole match is the unrelated Wiener-Ikehara reference in `NumberTheory/LSeries/PrimesInAP.lean`; no Brownian/Wiener-process construction is present |
| `git ls-remote --tags https://github.com/RemyDegenne/brownian-motion.git 'refs/tags/v4.29.0*'` | 0 | tag object `6c93424...`; peeled immutable commit `fdcef67f...`; also reported distinct `v4.29.0-rc6` |
| `curl -L --fail --silent --show-error 'https://api.github.com/repos/RemyDegenne/brownian-motion/git/trees/fdcef67f41b51b7635b3c2d08eb61768604f8f74?recursive=1' \| python3 -c 'import json,sys; d=json.load(sys.stdin); print(next(x for x in d["tree"] if x["path"]=="BrownianMotion/Gaussian/BrownianMotion.lean"))'` | 0 | exact path is blob `4ebeae388f3ed11876b0307ed4b74e99516cd81d`, size 50114 |
| `python3 -m json.tool Stage1_Instances/THM-M-1027/anchor-audit.json >/dev/null` | 0 | structured audit is valid JSON |
| `rg -n '(^\|[^[:alnum:]_])(sorry\|admit\|sorryAx)([^[:alnum:]_]\|$)\|^[[:space:]]*axiom[[:space:]]\|theorem_complete[[:space:]]*:[[:space:]]*true' Stage1_Instances/THM-M-1027/{AnchorAudit.lean,anchor-audit.json,anchor-audit.md}` | 1 | no proof placeholder, axiom declaration, or completion claim found; exit 1 means no match |
| `git diff --check -- Stage1_Instances/THM-M-1027 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The successful Lean run checks only locally available infrastructure and the
typed component contract. The failed import is recorded evidence of the
repo-local integration blocker, not a kernel check of the external project.
Network discovery resolved immutable Git objects but did not clone, fetch, or
modify `.lake`. Root state remains `M3`; theorem completion remains false.
