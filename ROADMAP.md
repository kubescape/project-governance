# Kubescape Project Roadmap

This document outlines the development roadmap for Kubescape, an open-source Kubernetes security platform.

This roadmap is a high-level list of things we plan to do in the future. It is meant to give you a first impression of where the project is going. For a more in-depth roadmap containing tickets and specific features, please refer to the project roadmap table on GitHub.

## Planning principles

Kubescape roadmap items are labeled based on where the feature is used and by their maturity.

The features serve different stages of the workflow of the users and labeled as such:

* Development phase (writing Kubernetes manifests) - example: The VS Code extension is used while editing YAMLs.
* CI phase (integrating manifests to GIT repo) - example: GitHub action validating HELM charts on PRs.
* CD phase (deploying applications in Kubernetes) - example: running a cluster scan after a new deployment.
* Monitoring phase (scanning application in Kubernetes) - example: Prometheus scraping the cluster security risk.

The items in the Kubescape roadmap are split into three major groups based on the feature planning maturity:

* [Planning](#planning-) - we have tickets open for these issues with a more or less clear vision of design.
* [Backlog](#backlog-)  -  features that were discussed at a high level but are not ready for development.
* [Wishlist](#wishlist-) -  features that we are dreaming of in 😀 and want to push them gradually forward.


## Planning 👷

### Core Platform Enhancements
- [x] Storage and Node-agent memory and CPU consumption
- [x] Improve image scanning performance and resource utilization
- [ ] Deprecation of Kollektor and Gateway components (as Synchronizer takes over them)
- [ ] Scanning container image on the host filesystem

### Security Features
- [x] Layer 7 (HTTP) parsing in eBPF to create visibility over which workload uses which APIs
- [ ] Scanning for misplaced secrets in container images (Monitoring phase)

### User Experience
- [ ] Integration with more image registries for vulnerability scanning
- [ ] Kubescape CLI control over cluster operations
- [ ] Creating more user guides

## Backlog 📅

### Core Platform Enhancements
- [ ] Reimplement the data backend of the Storage component so it can become scalable horizontally
- [ ] Moving to image based Gadgets with Inspektor Gadget
- [ ] Moving the Host scanner functionality to the Node-agent

### Security Features
- [ ] Scanning the Kubernetes host and kernel for vulnerabilities (Monitoring phase)
- [ ] Produce fixed paths for HELM charts (CI/CD phase)
- [ ] Implement a rule based alerting system in Kubescape to send notifications (Monitoring phase)
- [ ] Implement a CEL based rule engine for Kubescape controls (as an alternative to Rego)

### User Experience
- [ ] Create Kubescape HELM plugin for Kubescape


## Wishlist 💭

- Integrate with other Kubernetes CLI tools
- Add visualization in K9s
- Kubernetes audit log integration
- Scanning Dockerfile-s for security best practices
- Custom controls and rules

## Completed features 🎓

* Runtime detection based on eBPF
* Kubelet configuration validation
* API server configuration validation
* Image vulnerability scanning based controls
* Assisted remediation (telling where/what to fix)
* Integration with Prometheus
* Configuration of controls (customizing rules for a given environment)
* Installation in the cluster for continuous monitoring
* Host scanner
* Cloud vendor API integration
* Custom exceptions
* Custom frameworks


## Contributing

We welcome contributions from the community! Please check our [Contributing Guidelines](CONTRIBUTING.md) for more information on how to get involved.

## Note

This roadmap is a living document and will be updated quaterly based on community feedback and evolving security needs. Priorities and timelines may shift as we progress.
