# THM-M-1271 proof-phase recheck at `fb0fd5be` (slot 28)

Item: `S56-M-1271-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `fb0fd5be494d0813177dbdc959ec911d69a72015`

Base tree: `f6d39faae5fb024a71ee786e7a6b017d335841cd`

## Verdict

`blocked`. The tracked `Proof.lean` has genuine placeholder-free bodies for
sphere crossing, the exact geometric barrier package, and the compactness and
limit-passage part of the analytic package. It does not construct a
Palais-Smale sequence at the frozen minimax level.

The first failed gate is `M1271-C-PS-SEQUENCE`. The declaration
`mountainPassCriticalPackage_of_psSequence` still takes that exact missing
sequence producer as a premise. The frozen composer
`root_of_barrier_and_critical_packages` still takes the whole critical package
as a premise. Neither conditional declaration proves `MountainPassTarget`.

A fresh repository and materialized pinned-dependency scan found no eligible
deformation, Ekeland, Caristi, mountain-pass, Palais-Smale, or minimax-critical
proof body. The legacy `S1_M_164` module, adjacent `THM-M-1270` dossier, and
Struwe package expose their hard variational constructions as premises rather
than implement them. Fresh read-only Sourcegraph global Lean searches and
GitHub repository searches also returned no candidate. These bounded external
searches neither establish nonexistence nor receive kernel proof credit. No
source or dependency was downloaded.

The item remains `[ ]`. No proof receipt, state transition, audit completion,
validation completion, release, theorem completion, or master acceptance is
claimed. `.stage1-worker-selftest.json` is deliberately absent because the
assigned proof phase is not genuinely self-tested complete.

The frozen typed graph's root vector remains `[H3, M3, R4] -> [H3, M3, R4]`.
The older intake JSON predates the statement, anchor, and obligation-tree
artifacts and is not rewritten by this proof-only worker.

## Validation

All credited validation ran in this worker clone with the existing pinned Lake
artifacts and no network access. No `lake update`, `lake build`, dependency
clone/fetch, or `.lake` mutation was performed. Temporary Lean output was
confined to `/tmp` and removed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink makes this nonrelease blocker evidence. The
separate read-only discovery queries above are not validation evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1271` | 0 | Rank 164; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1271/check_obligation_tree.py` | 0 | 13 obligations and 25 typed edges passed; denominator `2f6d1a3dc9064aff967ba0cf8443ff438e9cb99e0b2d34994252e6410d2d75bc`; root open at `M3`. |
| Isolated pinned Lean `--trust=0 -t0` recipe below | 0 | Exact statement, conditional root composition, and partial proof elaborated. Six axiom reports named only `propext`, `Classical.choice`, and `Quot.sound`; `sorryAx` count was zero. Two nonfatal unused-section-variable linter warnings occurred. |
| Owned Lean prohibited-construct scan below | 0 | Comment-stripped check passed: no `sorry`, `admit`, `sorryAx`, bodyless `axiom`/`constant`, `unsafe`, or `opaque` declaration. |
| Pinned dependency term scan below | 1 | Expected no-match: zero materialized dependency source files matched the missing theorem family. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `python3 -m json.tool` plus source-hash, base-identity, and blocked-state assertions on the adjacent JSON | 0 | JSON syntax, recorded hashes, base identity, empty receipts, and false completion fields agree. |
| Scoped `git diff --check` plus added-file whitespace checks | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Exact Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1271
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-1271-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
{
  LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
    "$lean" --trust=0 -t0 -R "$target" \
    -o "$tmp/Statement.olean" "$target/Statement.lean"
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
    "$lean" --trust=0 -t0 -R "$target" \
    -o "$tmp/ObligationTree.olean" "$target/ObligationTree.lean"
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
    "$lean" --trust=0 -t0 -R "$target" "$target/Proof.lean"
} >"$tmp/lean-output.log" 2>&1
cat "$tmp/lean-output.log"
sha256sum "$tmp/lean-output.log"
```

The combined Lean output SHA-256 was
`1bdb7a03aadbca8e3b817c6f0e71aa0d3b7b62018414510e541e9f1720292d7b`.
It is identical to the prior recheck digest because all three Lean inputs,
the pinned environment, and the emitted diagnostics are byte-identical.

The exact no-match scans, run from the repository root, were:

```bash
python3 - <<'PY'
import re
from pathlib import Path
pattern = re.compile(
    r'\b(sorry|admit|sorryAx)\b|^\s*(axiom|constant|unsafe|opaque)\b', re.M
)
for path in Path('Stage1_Instances/THM-M-1271').glob('*.lean'):
    text = path.read_text()
    text = re.sub(r'/-.*?-/', '', text, flags=re.S)
    text = re.sub(r'--.*', '', text)
    assert not pattern.search(text), path
PY
rg -l -i \
  'MountainPass|mountain[ -]?pass|PalaisSmale|Palais[ -]?Smale|Ekeland|Caristi|deformation lemma|minimax critical' \
  Formalizations/Lean/.lake/packages --glob '*.lean'
```

## Retry Condition

The remaining root cut set is `M1271-C-PS-SEQUENCE`,
`M1271-T-CRITICAL`, and `M1271-ROOT`. Resume after a placeholder-free local
construction of the exact minimax Palais-Smale sequence, or after an immutable
compatible Lean 4 deformation/Ekeland theorem can be pinned, transported to
the exact frozen type, and checked for terminal proof-body provenance.

This is current-base blocker evidence, not a proof receipt, and it does not
satisfy `S56-M-1271-PROOF`.
