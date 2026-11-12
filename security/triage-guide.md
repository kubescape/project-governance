# Security Issue Triage Guide

Maintainer guide for triaging issues and advisories framed as "security".
Applies to all repositories in the kubescape organization.
Goal: decide in under 5 minutes if a report is a vulnerability, hardening, or a feature.
The baseline is the [threat model](threat-model.md).

## Step 1: Identify the attacker

Ask: who is the attacker, and what access do they already have?

- No attacker named → not a vulnerability. Reclassify.
- Attacker is a cluster user or workload acting within their RBAC → trusted. Reclassify.
- Attacker is a cluster user or workload gaining access **beyond** their RBAC through a Kubescape component → **in scope**. Continue to Step 2.
  - In-cluster HTTP APIs require a service-account token checked against RBAC (chart ≥ 1.42.0). A route that skips the check is an RBAC bypass.
  - Reports against older charts/images or `global.apiAuth.enabled=false` are outdated or opted-out configurations, not vulnerabilities.
  - Metrics routes are unauthenticated by design; see "Known limitations" in the [threat model](threat-model.md).
- Attacker is a local user/process on the scan machine → out of scope. Reclassify.
- Attacker controls input to `scan` (chart, manifest, repo, image) → **in scope**.
- Attacker is on the network / supply chain → **in scope**.

Remember: reports and policy artifacts fed back into Kubescape are not scan input.
Loading them is a user trust decision, like running a script.

## Step 2: Identify the gain

Ask: what does the attacker gain that they did not already have?

- Code execution, file writes, or network calls from scan input → vulnerability.
- Privilege escalation via our component's RBAC or host access → vulnerability.
- Reading data their RBAC already allows → nothing gained. Close as by-design.
- "Could be safer / best practice" → hardening, not a vulnerability.

## Step 3: Classify

| Verdict | Criteria | Action |
|---|---|---|
| Vulnerability | Steps 1+2 both pass | Private report, fix, advisory |
| Hardening | Real risk reduction, no concrete attack | Public issue, label `security-hardening` |
| Quality | Detection content gaps (boundary 4), wrong results, evidence integrity without an attacker | Label `bug`; welcome a PR |
| Feature | New control, new capability, docs | Label `feature`, normal backlog |

## Step 4: Route

- Vulnerabilities: ask the reporter to use GitHub private vulnerability reporting
  per [SECURITY.md](../SECURITY.md). Do not discuss exploit details in public issues.
- Declined advisories: use the canned response below, fix valid hardening publicly,
  and credit the reporter in the public issue/PR.
- Everything else stays public with the right label.

## Red flags that it is NOT a security issue

- The "attack" starts with "a user with cluster-admin...".
- The report is a scanner/scorecard output with no attack scenario.
- The fix is "add a doc" or "add a badge".
- The report proposes a new Kubescape control. That is a feature for regolibrary.
- The report is about what a control, policy, or rule does or does not catch. That is detection content (threat model, boundary 4), not a vulnerability.
- The CVE is in a dependency but the vulnerable function is unreachable.
- The prerequisite is the user loading an attacker-supplied artifact by choice.

## Red flags that it IS serious

- Scanning a file/chart does something besides reading it.
- An in-cluster API route accepts a request without a valid service-account token.
- A caller can act beyond the verbs/resources its Role grants.
- A probe or metrics port serves anything besides probes or metrics.
- A default install grants our components more RBAC than the docs claim.
- Release artifacts can be altered without detection.

## Canned responses

**By-design (authenticated access):**
> Kubescape assumes cluster access requires authentication.
> Users with API access are trusted per their RBAC.
> This report does not cross that boundary, so we're treating it as a feature request.

**Hardening:**
> Thanks — this is a valid hardening improvement, not an exploitable vulnerability.
> Relabeling as security-hardening and keeping it open.

**Outdated or opted-out configuration:**
> Thanks for the report. In-cluster API authentication enforcement is fixed since chart
> kubescape-operator 1.42.0 (service-account tokens + RBAC, on by default).
> The behavior you describe applies to older versions or to deployments that set
> `global.apiAuth.enabled=false`. Please upgrade; we are not issuing an advisory.

**Detection content (control, policy, or rule gap):**
> Thanks — this is a gap in Kubescape's detection content, not a vulnerability in
> Kubescape itself (see the threat model, boundary 4). We don't issue advisories
> for these. Please open a public issue or, better, a pull request with the fix
> and a test; improving detection coverage is one of the most valuable
> contributions to the project, and we'll credit you there.

**Declining an advisory:**
> Thanks for the report. Kubescape's threat model treats access already granted
> by RBAC as trusted, and local machine security as the operator's responsibility.
> Your report does not show an actor gaining access beyond what they already hold,
> so we are not treating this as an exploitable vulnerability.
> It is a valid hardening improvement — we will fix it in a public issue/PR
> and credit you there. Closing this advisory without a CVE.

## Multi-repo note

Issues land on many repos (node-agent, operator, storage, helm-charts, regolibrary...).
Triage with the same model everywhere.

Private vulnerability reporting is enabled only on kubescape/kubescape.
Reporters file there regardless of the affected component; this is expected.
Once triaged as a vulnerability in another component, a maintainer opens a draft advisory on the owning repo (copying the report and crediting the reporter), then closes the kubescape/kubescape one with a pointer.
The advisory is published from the owning repo so the affected Go module and version range are correct.
