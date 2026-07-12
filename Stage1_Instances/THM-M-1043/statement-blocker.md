# Statement-phase blocker

Item: `S56-M-1043-STATEMENT`  
Base revision: `e1aeca70d414df009dea3559577ea90aa9834089`

## Gate result

The exact-statement gate is blocked. The intake deliberately leaves open the primary theorem,
diffusion regime, regularity assumptions, domain and exit behavior, and time/sign conventions.
The worker clone contains neither an inspected stable copy of Kac (1949) nor the cited Oksendal
edition. Consequently there is no exact source theorem from which to freeze the required ordered
binders, hypotheses, boundary cases, and conclusion. Selecting those details here would invent
missing mathematics or silently merge two materially different candidate theorems.

The only repo-local Lean candidate,
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_236.lean`, is not an exact substitute. Its own
module documentation says that it does not prove Feynman-Kac, and its
`FeynmanKacData.probabilisticRepresentation` is supplied as structure data rather than defined as
the exponential path-functional expectation of a selected diffusion. Its `StatementShape` also
quantifies over that abstract data and assumes `ParabolicPDE` and `PathFunctionalWellFormed`; it is
therefore a typed discovery boundary, not the exact source target required by rev-5.6 section 5.

Because an exact canonical target cannot truthfully be selected, no `Statement.lean`, normalized
expression hash, mutation certificate, or `.stage1-worker-selftest.json` is emitted. This phase is
not self-tested and remains open. The first failed gate is rev-5.6 section 5, target identification;
kernel elaboration of the legacy boundary does not change that result.

## Commands and results

All commands ran in this worker automation clone. No dependency fetch or `.lake` mutation was
performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1043` | 0 | rank 236; planned; legacy artifacts unaccepted; theorem incomplete |
| `find . -type f \( -iname '*oksendal*' -o -iname '*feynman*kac*' -o -iname '*kac*1949*' \) -not -path './Formalizations/Lean/.lake/*' -print` | 0 | no repo-local source scan or source text found |
| `lake env lean AwesomeTheorems/Stage1/S1_M_236.lean` (from `Formalizations/Lean`) | 0 | legacy discovery boundary elaborated with the existing pinned environment; output includes `StatementShape`-adjacent declarations but supplies no exact source target |
| `git diff --check -- Stage1_Instances/THM-M-1043` | 0 | no whitespace errors before this blocker record was added |

## Required unblock

Provide a stable, inspectable primary-source theorem coordinate (edition plus theorem/page or
formula anchor) and select one theorem family without combining it with the other candidate. A
later statement worker can then freeze its exact hypotheses and conventions, encode the concrete
diffusion/path expectation and PDE target, minimize pinned imports, elaborate it, serialize its
expression and environment fingerprints, and run the required structural mutations and boundary
checks.
