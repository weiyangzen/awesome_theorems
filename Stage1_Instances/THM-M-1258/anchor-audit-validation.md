# Anchor-audit validation record

Base revision: `128665c876bc80ee014065205b64f2dc6700cf5c`.

| Command | Exit | Exact result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1258/AnchorAudit.lean` | 0 | Printed the types of the five pinned supporting declarations; no diagnostics |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1258/Statement.lean` | 0 | Printed the frozen declaration and explicit type; no diagnostics |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | Empty output; the pinned package worktree is clean |
| pinned-package negative search (below) | 0 | No matching Lean source in pinned mathlib |
| `python3 -m json.tool Stage1_Instances/THM-M-1258/anchor-audit.json` | 0 | Parsed successfully |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1258` | 0 | Rank 436, planned, L0/rework_required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1258 .stage1-worker-selftest.json` | 0 | No whitespace errors |

Pinned-package negative search:

```bash
test -z "$(rg -l -i 'h[oö]rmander|hormander|hypoellipt|subellipt|bracket[-_ ]generat' \
  Formalizations/Lean/.lake/packages/mathlib --glob '*.lean')"
```

The GitHub searches and response hash are recorded in `anchor-audit.json`; secondary search
failures are recorded rather than hidden. The successful Lean probes validate supporting names and
the already-frozen target, not a proof of the predicate. No `.lake` artifact was mutated.
