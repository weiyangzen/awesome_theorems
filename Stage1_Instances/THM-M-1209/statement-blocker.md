# Statement-phase blocker

Item: `S56-M-1209-STATEMENT`  
Theorem: `THM-M-1209`  
Base revision: `446f3e80e7a93deeca70150fa80d9ee079ee0586`

## Verdict

The exact-statement gate remains blocked, so no canonical Lean declaration can truthfully be
frozen. The intake resolves the short repository label provisionally to Keel and Tao, *Endpoint
Strichartz Estimates*, American Journal of Mathematics 120(5) (1998), Theorem 1.2. However, the
owned source crosswalk expressly leaves the theorem's exact codomains, interpolation-space
notation, admissibility inequalities, infinity conventions, exceptional endpoint, mixed norms,
measurability conventions, and the three displayed conclusions open. Those are semantic parts of
the root rather than implementation details.

The available bibliographic record confirms the paper, authors, journal, pages 955-980, DOI
`10.1353/ajm.1998.0039`, and that the article proves an abstract Strichartz estimate. It does not
contain the text of Definition 1.1, hypotheses (1)-(2), or estimates (7)-(9). Attempts to retrieve
the publisher PDF in this environment returned an HTML error page, and the previously known UCLA
and WordPress PDF locations returned HTTP 404. Consequently, transcribing a declaration now would
require reconstructing source notation from memory. That could silently change an endpoint,
quantifier, interpolation space, norm, constant dependency, or retarded integration convention and
would violate the no-substitution rule.

There is a second encoding blocker even after source retrieval: the pinned mathlib tree has the
basic Bochner integral, `eLpNorm`, Hilbert adjoint, restricted-measure, and time-region interfaces,
but repository search found no ready abstract Keel-Tao compatible Banach-pair interpolation API.
An exact statement must therefore first choose and validate an explicit representation of the
paper's `B_theta` spaces and mixed `L_t^q B_theta^*` norms. An opaque proposition or a structure
field asserting the three desired estimates would only assume the theorem and receives no
statement credit.

## Lean boundary

`StatementInfrastructureProbe.lean` elaborates only the pinned interfaces named above. It is
deliberately not a canonical target, checked transport, or proof. Since the source statement is not
available exactly, removed-hypothesis, changed-domain, binder-scope, and boundary mutation tests
cannot be meaningfully specified.

## Validation record

Commands ran in this worker clone. Lean ran from `Formalizations/Lean` with the existing pinned Lake
environment; no dependency update, fetch, build, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard valid: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1209` | 0 | rank 402; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1209/StatementInfrastructureProbe.lean` | 0 | Hilbert adjoint, `eLpNorm`, Bochner integral, restricted measure, and `Set.Iio` interfaces elaborated |
| `git diff --check -- Stage1_Instances/THM-M-1209` | 0 | no output |

## Retry condition

Retry after an authoritative stable copy supplies Theorem 1.2 together with Definition 1.1 and the
definitions surrounding hypotheses (1)-(2) and conclusions (7)-(9). The next attempt must transcribe
each binder, restriction, constant dependency, and norm; implement the required interpolation and
mixed-norm encodings; minimize imports; elaborate and serialize the expression; provide checked
transports; and run all four mutation classes.

This artifact does not complete the statement node, accept a receipt, or claim theorem completion.
No `.stage1-worker-selftest.json` is emitted because the assigned deliverable is not genuinely
self-tested.
