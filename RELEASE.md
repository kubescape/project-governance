# Release Process for Kubescape

## Overview

This document outlines the release process for Kubescape.

## Release Schedule

Kubescape follows a regular release schedule:
- **Minor Releases**: Every 6-8 weeks.
- **Patch Releases**: As needed for critical fixes.
- **Major Releases**: Planned for significant architectural changes or new features.

## Release Steps

1. **Preparation**
    - Ensure all tests pass.
    - Update documentation.
    - Review and merge all pending PRs.

2. **Versioning**
    - Follow [Semantic Versioning](https://semver.org/).

3. **Changelog**
    - Update release notes in "https://github.com/kubescape/helm-charts/releases/tag/" with the new release details.
    - Include new features, bug fixes, and any breaking changes.

4. **Tagging**
    - According to workflow : https://github.com/kubescape/helm-charts/actions/workflows/03-helm-release.yaml  
    
5. **Build and Test**
    - Build the release artifacts.
    - Run system tests.

   kubescpe helm chart release is build in github actions and can be found here: 
   https://github.com/kubescape/helm-charts/actions/workflows/03-helm-release.yaml  
   
   kubescape cli release is build in github actions and can be found here:
   https://github.com/kubescape/kubescape/actions/workflows/02-release.yaml 

6. **Release Artifacts**
    - Publish the release artifacts to the appropriate repositories (e.g. kubescape, helm-charts as github releases).

7. **Announcement**
    - Announce the release on the project's communication channels (e.g. CNCF kubescape Slack).

## Post-Release

- Re-run helm on different environments 
- Monitor for any critical issues.
- Plan for the next release cycle.

## Contact

For any questions or issues, please contact the maintainers at [maintainers@kubescape.io](mailto:maintainers@kubescape.io).
