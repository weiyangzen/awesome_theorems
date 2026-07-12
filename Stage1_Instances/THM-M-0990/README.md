# THM-M-0990 rev-5.6 intake

This directory is the `planned` intake for the Lyapunov central limit theorem. It freezes the
intended human claim as the triangular-array, row-independent real-valued theorem with a positive
Lyapunov exponent offset and convergence to a standard normal law.

The legacy Lean module is discovery input only. Its `LyapunovData` includes a
`characteristicFunctionTaylorBridge : Prop`, and `StatementShape` assumes that bridge; it therefore
receives no statement or terminal-proof credit. The self-tested statement moves the provisional
root vector to `[H2, M3, R4]`, pending master acceptance.
`Statement.lean` now freezes and kernel-elaborates the exact target selected from that human scope,
with joint row independence, explicit moments, the textbook Lyapunov ratio, eventual positive row
variance, and convergence to `gaussianReal 0 1`. This provisional statement work awaits master
acceptance. Exact source anchoring, proof closure, and theorem completion remain open.
