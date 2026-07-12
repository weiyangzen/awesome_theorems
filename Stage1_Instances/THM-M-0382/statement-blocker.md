# Statement-phase blocker

Item: `S56-M-0382-STATEMENT`  
Theorem: `THM-M-0382`  
Base revision: `562c428c3d520ab42bba305174b7cad9409d7c0b`

## Verdict

The exact-statement gate is blocked. The repository source says only "endpoint Strichartz
estimate" and identifies Keel and Tao (1998). The accepted intake consequently does not select a
unique claim: it leaves open whether the root is the whole abstract package commonly cited as
Theorem 1.2 or one of its homogeneous, dual, or retarded estimates. It also leaves the operator
domains, interpolation spaces, admissibility relation, exceptional endpoint, mixed-norm order,
measurability conventions, time domain, and constant dependence unresolved. These are semantic
parts of the theorem, not Lean implementation choices.

The bibliographic locator is Markus Keel and Terence Tao, *Endpoint Strichartz Estimates*, American
Journal of Mathematics 120(5) (1998), 955-980, DOI `10.1353/ajm.1998.0039`. Source retrieval probes
in this run did not yield an authoritative PDF: the UCLA URL returned HTTP 404, the Project Euclid
PDF URL returned a short HTML response rather than a PDF, and Project MUSE returned HTTP 503.
Therefore Definition 1.1, hypotheses (1)-(2), and conclusions (7)-(9) could not be transcribed and
checked from an immutable primary-source copy. Reconstructing them from memory would risk changing
an endpoint, quantifier, norm, space, or integration region and is forbidden by the no-substitution
rule.

Even after retrieval, an exact Lean representation must be chosen for the paper's interpolation
spaces and mixed time-space norms. Repository-local and pinned-library inspection found the basic
Hilbert adjoint, Bochner integral, `eLpNorm`, restricted-measure, and time-region interfaces, but no
already selected Keel-Tao statement in this dossier. An opaque proposition, or a structure that
assumes the desired estimates as fields, would merely assume the theorem and receives no statement
credit.

## Lean boundary

`StatementInfrastructureProbe.lean` elaborates only those pinned interfaces. It is deliberately not
a canonical target, equivalence transport, or proof. With no source-exact proposition, the required
removed-hypothesis, changed-domain, binder-scope, and boundary mutation tests cannot truthfully be
specified or run.

## Validation record

Commands ran from this worker clone. Lean used the existing pinned Lake environment; no update,
fetch, dependency build, or deliberate `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets validated |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0382` | 0 | rank 870; planned; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0382/StatementInfrastructureProbe.lean` | 0 | Hilbert adjoint, `eLpNorm`, Bochner integral, restricted measure, and `Set.Iio` elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0382` | 0 | no output |

## Retry condition

Retry after an authoritative stable copy supplies Theorem 1.2 together with Definition 1.1 and the
definitions surrounding hypotheses (1)-(2) and estimates (7)-(9). The next attempt must select the
exact source clause or package, transcribe every binder and boundary convention, implement the
interpolation and mixed-norm representations, minimize imports, elaborate and fingerprint the
expression, compile all credited transports, and run all four mutation classes.

This artifact does not complete the statement node, accept a receipt, or claim theorem completion.
No `.stage1-worker-selftest.json` is emitted because the assigned deliverable is not genuinely
self-tested.
