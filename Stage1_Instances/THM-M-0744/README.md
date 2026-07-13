# THM-M-0744 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the recursion-theory catalog item
`s-m-n定理` (the s-m-n or parameter theorem). The repository attributes it to Stephen Kleene in
1943 and gives only `参数定理` ("parameter theorem") as the mathematical statement. A duplicate
computer-science catalog record adds that a computable function combines a program index with a
parameter. These records identify the theorem family, but not an exact proposition.

An inspected authoritative secondary source states the usual all-arities natural-index form: for
every `n,m`, a primitive-recursive transformer specializes the first `m` arguments of an indexed
`(n+m)`-ary partial computable function while leaving `n` inputs. The cited 1943 paper is only a
bibliographic lead here; its theorem passage and proof were not available for inspection.

Pinned mathlib contains a strong discovery candidate,
`Nat.Partrec.Code.smn`, in `Mathlib.Computability.PartrecCode`. It produces a computable
transformer from an inductive `Code` and one natural parameter to a new `Code`, and proves
pointwise equality after pairing the fixed parameter with one residual input. Its witness `curry`
is primitive recursive, but that stronger fact is not exposed by the candidate theorem's
conclusion.

The catalog does not choose the general natural-index form or mathlib's packed unary code form, nor
does it approve the required arity, encoding, pairing, primitive-recursiveness, and partial-value
transports. The canonical mathematical statement and Lean expression therefore remain null. The
provisional vector is `[H1, M4, R4]`: a standard theorem statement and primary bibliographic lead
are known, but exact source fidelity is not accepted; the Lean candidate receives no machine credit
before statement identity; and no reviewed reconstruction attaches to an unfrozen root. All six
downstream tasks remain open. Neither audit completion nor theorem completion is claimed.
