# Kubescape Threat Model

This document defines the security boundaries of the Kubescape project.
It applies to all repositories in the kubescape GitHub organization.
Maintainers use it to decide whether a report is a vulnerability.
If an attack only works for someone this model already trusts
(for example, an authenticated cluster user), it is not a vulnerability.

## Core assumption

Cluster access requires authenticated kubectl/API access.
Anyone with API access (users or workloads) is trusted at the level their RBAC grants, and no further.
Kubescape does not defend a cluster against actors doing what their RBAC already allows; that is the operator's responsibility.
Kubescape does enforce its own boundary: every trigger must come from an authenticated, RBAC-authorized source. A path that lets an actor exceed their RBAC is a vulnerability.

## Trust boundaries that DO matter

### 1. Untrusted scan inputs
The CLI scans files, Helm charts, repos, and images the user does not control.
A malicious manifest or chart must not gain code execution, network access, or filesystem writes.
This is the most important attack surface for the CLI.

Only `scan` inputs count. Kubescape's own outputs (reports) and loaded
artifacts (frameworks, policy bundles) are trusted by user choice.
Accepting a report or framework from an outsider is the user's decision, like running a script.

### 2. Supply chain of our own artifacts
Our binaries, images, and Helm charts run inside user clusters with high privileges.
A compromised dependency, GitHub Action, or build pipeline is a real vulnerability.
This includes CVEs in shipped images and reachable CVEs in Go dependencies.
It also includes workflow token permissions and release signing.

### 3. Privileges of in-cluster components
node-agent runs with eBPF and host-level access. The operator can patch workloads.
A bug letting a lower-privileged actor leverage these components is in scope.
Our components should follow least privilege even inside the trust boundary.

### 4. Scanner correctness (false negatives)
Kubescape is a security tool. A wrong "all clear" is a security-relevant defect.
False negatives in RBAC analysis, PSS, or controls deserve priority.
They are not vulnerabilities in us, but they weaken user security.

## What is NOT a vulnerability under this model

- "A cluster user can read CRD data" — yes, by design. Guard it with RBAC.
- "A pod can call a Kubescape API" — only with a service-account token that RBAC has bound to that action. If a route accepts calls without one, it IS in scope.
- "Scan results contain sensitive cluster info" — results go where the operator sends them.
- "Component X has permission Y" — only a finding if Y exceeds documented need.
- An actor suppresses an alert on an action their RBAC already allows, they gained nothing. Detection opt-outs living in the wrong place is hardening.
- A local user on the scan machine reading files — local security is the operator's job.
- Missing hardening (SBOM, signing, docs, scorecard checks) — improvement, not a vuln.

## In-cluster API authentication

Since chart `kubescape-operator` 1.42.0, every non-probe route of the in-cluster HTTP APIs (kubescape, kubevuln, synchronizer, operator trigger) requires a Kubernetes service-account token. Servers validate it with `TokenReview`
(audience `kubescape.io`) and authorize with `SubjectAccessReview` against RBAC virtual resources in the `kubescape.io` group. Auth is on by default and fails closed.

NetworkPolicies are also enabled by default. Design: kubescape/designs-and-proposals#32.

Consequences for triage:

- A route that accepts requests without a valid token, or lets a caller act
  beyond what its Role grants, is an **RBAC bypass → vulnerability**.
- Users should run the up to date versions, so reports against chart < 1.42.0, images pinned before the enforcing release, or deployments with `global.apiAuth.enabled=false` are not vulnerabilities. The user is running an outdated or opted-out configuration.

### Known limitations

- Metrics routes (`/v1/metrics`, `/metrics`) stay unauthenticated by design;
  exposure is metric values only. Reports about them are hardening at most.
- No TLS between components yet. Tokens travel in clear text inside the cluster.
  Audience binding and 1h expiry limit what a captured token is good for.
  Interception needs network position; this is a hardening follow-up.
- A compromised caller (operator, node-agent) keeps its Role's permissions.
  Narrowing those Roles is a hardening exercise.
- NetworkPolicy enforcement depends on the CNI; it is defense in depth, not the control.
- Probe ports (`/livez`, `/readyz`) are unauthenticated by design and must serve **only** probes. Any other handler reachable on them (debug, pprof, metrics) is a finding. Importing `net/http/pprof` registers on `DefaultServeMux`;  servers must use their own mux so this cannot leak onto a probe port.

### Open ports inventory

Snapshot of in-cluster listeners, from the Helm chart and component source.
**This inventory is correct only for today.** The project plans to move all
inter-component communication to CRDs; direct pod-to-pod ports will be removed.
External callers should already use the `OperatorCommand` CRD, not the HTTP APIs.

Sensitivity levels:

- **L1 — operational**: health, readiness, metrics. No cluster content.
- **L2 — service**: accepts work or serves component data. Abuse wastes resources or leaks component-level info.
- **L3 — sensitive**: can read cluster-wide security data or change cluster state.

| Component | Port | Purpose | Auth | Necessary? | Level |
|---|---|---|---|---|---|
| kubescape (ksserver) | 8080 | HTTP scan API (`/v1/scan`, `/v1/results`) | SA token + RBAC | Only with in-cluster scanning | L3 |
| kubescape (ksserver) | 8080 | `/v1/metrics` | None (by design) | Only with monitoring | L1 |
| operator | 4002 | `/v1/triggerAction` (legacy; CLI now uses `OperatorCommand`) | SA token + RBAC | No known caller | L3 |
| operator | 8000 | Health/readiness | None (probe) | Yes | L1 |
| operator | 8443 | Admission webhook (TLS, called by apiserver) | TLS | Only with admission enabled | L2 |
| operator | 6060 | pprof debug, binds all interfaces | None | No — disable in prod | L2 |
| storage | 443 | Aggregated API server | kube-apiserver authn/RBAC | Yes | L3 |
| storage | 6060 | pprof debug, binds all interfaces | None | No — disable in prod | L2 |
| kubevuln | 8080 | Scan API (`/v1/*`, `/v1/diagnostics`) | SA token + RBAC | Yes | L2 |
| kubevuln | 8080 | `/metrics` | None (by design) | Only with monitoring | L1 |
| node-agent | 8080 | Prometheus metrics | None | Only with monitoring | L1 |
| node-agent | 7888 | Health/liveness (`/livez`, `/readyz`) | None (probe) | Yes | L1 |
| node-agent | 6060 | pprof, localhost-only (`ENABLE_PROFILER`) | None | Debug only | L1 |
| synchronizer | 8089→8080 | Ingest endpoint (runtime alerts, profiles → backend) | SA token + RBAC | Only with backend | L3 |
| synchronizer | 7888 | Health/liveness | None (probe) | Yes | L1 |
| synchronizer | config | Prometheus metrics (optional) | None | Only with monitoring | L1 |
| grype-offline-db | 8080 | Serves vulnerability DB files | None | Only air-gapped | L1 |
| prometheus-exporter | 8080 | Metrics incl. vulnerability counts | None | Only with monitoring | L2 |

Action items from this inventory: the all-interface pprof listeners (operator,storage) should bind localhost like node-agent's; the operator trigger route can be removed once no caller remains; TLS between components is the next step.

## Data stored in CRDs

We store vulnerability data, profiles, and configs in CRDs / aggregated APIs.
Reading them requires RBAC permission, like any Kubernetes object.
Reports that CRD data is "exposed" must show a bypass of RBAC.
Without a bypass, it is a feature request for finer-grained access, at most.

## Per-component notes

| Component | Main risk to check |
|---|---|
| kubescape CLI | Untrusted input handling (charts, manifests, repos) |
| node-agent | Host privileges, eBPF, data it writes cluster-wide |
| operator | Workload patching power, command handling |
| storage | API server surface, data integrity |
| kubevuln | Image parsing of untrusted images |
| helm-charts | Default RBAC, image versions, CVEs in shipped images |
| CI (all repos) | Token permissions, pinned actions, release integrity |

## Severity anchors

- Critical: RCE or privilege escalation from untrusted scan input or network.
- High: supply-chain compromise path; RBAC bypass; our component escalates an attacker.
- Medium: reachable dependency CVE; excessive default permissions; false negatives.
- Low: hardening gaps, hygiene, docs, non-reachable CVEs.

## Reporting

See [SECURITY.md](../SECURITY.md) for how to report a vulnerability.
Triage decisions follow the [triage guide](triage-guide.md).
