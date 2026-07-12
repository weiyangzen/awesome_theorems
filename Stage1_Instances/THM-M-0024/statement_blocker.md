# Statement-phase blocker

Item: `S56-M-0024-STATEMENT`  
Theorem: `THM-M-0024`  
Base revision: `5ca8fc1410f15a749abdd685210ac788a730e45b`

## Verdict

The exact-statement phase is blocked and remains `M4`. No canonical Lean target was created.
The intake identifies the historical theorem family, but it deliberately leaves the prime,
character component, coefficient ring, Iwasawa module, involution, Euler factors, and exceptional
cases unfrozen. The available repository metadata says only "proof of the Iwasawa main conjecture."
That is not enough to choose a unique theorem from Mazur and Wiles without inventing mathematics.

The primary publication is B. Mazur and A. Wiles, *Class fields of abelian extensions of Q*,
*Inventiones Mathematicae* 76 (1984), 179-330, DOI `10.1007/BF01388599`. The repository contains
no immutable copy or theorem/page transcription. The publisher page exposes bibliographic data and
references but puts the article PDF behind access control; therefore this run could not inspect and
pinpoint the source theorem. Crossref confirms only the article title and page range. Those records
do not close the source-statement gate.

The legacy file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_296.lean` cannot supply the exact
target. Its `StatementShape` quantifies over a boundary structure whose decisive conclusion is an
uninterpreted `Prop` field named `pAdicLFunctionGeneratesCharacteristicIdeal`; several other
source-critical facts are likewise stored as proposition-valued boundary data. Reusing it would be
a placeholder or broadened/substituted theorem, forbidden by rev-5.6.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` has adjacent cyclotomic,
class-group, ideal, and p-adic infrastructure, but the scoped search found no cyclotomic Iwasawa
main-conjecture or p-adic-L-function declaration. The only `Iwasawa` hits concern the unrelated
group-action simplicity criterion. This observation is not an anchor audit and gives no machine
proof credit.

## Smallest real validation

Commands were run from the repository root on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0024` | 0 | rank 296; lifecycle `planned`; baseline L0; theorem incomplete |
| `jq '.targets[] \| select(.theorem_id=="THM-M-0024")' Docs/Stage1_Targets_rev-5.6.json` | 0 | manifest membership and execution rank 296 confirmed |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact pinned revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -i -n 'Iwasawa\|p-adic L-function\|padic L\|characteristic ideal' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | only unrelated Iwasawa group-action hits; no exact terminal target found |
| `curl -L --fail --silent --show-error https://api.crossref.org/works/10.1007/BF01388599` | 0 | bibliographic metadata and pages 179-330 only |
| `curl -L --fail --silent --show-error https://link.springer.com/content/pdf/10.1007/BF01388599.pdf` | 0 | returned a 291904-byte HTML purchase page, not a PDF |

No `lake env lean` command was run: without a source-faithful proposition there is no exact target
to elaborate, and elaborating the legacy boundary placeholder would be false evidence rather than
a narrow validation. The canonical pinned `.lake` symlink was inspected read-only and not mutated.

## Unblocking condition

Obtain a legally accessible immutable primary-source copy; record its content hash; identify the
precise theorem/page plus all referenced definitions; transcribe the ordered hypotheses and
normalizations; resolve character, parity, prime, and exceptional branches; then implement the
source-compatible Lean object model and elaborate it with minimal pinned imports. Until that work is
done, there is no truthful `statement.json`, expression hash, mutation suite, or statement receipt.

No `.stage1-worker-selftest.json` is written because the assigned phase is not self-tested and must
not be presented as `[_]` work.
