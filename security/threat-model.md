# Kubescape Threat Model

This document defines the security boundaries of the Kubescape project.
It applies to all repositories in the kubescape GitHub organization.
Maintainers use it to decide whether a report is a vulnerability.
If a report assumes a weaker attacker than this model, it is not a vulnerability.

## Core assumption

Cluster access requires authenticated kubectl/API access.
Anyone with API access is trusted at the level their RBAC grants.
Workloads inside the cluster are not treated as hostile by default.
Protecting the cluster from its own workloads is the operator's responsibility.

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
- "A pod can query the storage APIService" — in-cluster workloads are not our attackers.
- "Scan results contain sensitive cluster info" — results go where the operator sends them.
- "Component X has permission Y" — only a finding if Y exceeds documented need.
- A local user on the scan machine reading files — local security is the operator's job.
- Missing hardening (SBOM, signing, docs, scorecard checks) — improvement, not a vuln.

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
