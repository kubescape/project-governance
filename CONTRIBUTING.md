# Contributing Guide

* [Contributor Guide](#contributing-guide)
   * [Ways to contribute](#ways-to-contribute)
  * [Find an issue](#find-an-issue)
  * [Working on issues](#working-on-issues)
  * [Ask for help](#ask-for-help)
  * [Build and test locally](#build-and-test-locally)
  * [Pull request process](#pull-request-process)
  * [Sign your commits](#sign-your-commits)


Welcome! It's awesome that you are considering contributing to Kubescape! Contributing is important and we welcome your efforts. 💖

As you get started, you are in the best position to give us feedback on areas of
our project that we need help with. 

If anything doesn't make sense, or doesn't work when you run it, please open a
bug report and let us know!

### Code of conduct

Please follow our [code of conduct](CODE_OF_CONDUCT.md) in all of your interactions within the project.

## Ways to contribute

We welcome many different types of contributions including:

* New features
* Builds, CI/CD
* Bug fixes
* Documentation
* Issue Triage
* Answering questions on Slack/Mailing List
* Web design
* Communications / Social Media / Blog Posts
* Release management

<!--Ben/Rotem/Matthias this language is from the CNCF suggested template, it incudes much more than we had in the original file, please indicate if something should be removed-->

Not everything happens through a GitHub pull request. You can find all the ways to become active in the Kubescape community [here](COMMUNITY.md)  

## Find an issue

We track Kubescape issues and bugs on the [project board](https://github.com/orgs/kubescape/projects/4)

Contributors should pay attention to three types of labels:
1. [good first issue](https://github.com/orgs/kubescape/projects/4/views/3?sliceBy%5Bvalue%5D=good+first+issue) - these are issues suitable for new contributors.
2. [open for contribution](https://github.com/orgs/kubescape/projects/4/views/4?sliceBy%5Bvalue%5D=open+for+contribution) - these are issues suitable for someone who isn't a core maintainer.
3. [help wanted](https://github.com/orgs/kubescape/projects/4/views/5?sliceBy%5Bvalue%5D=help+wanted) - these are issues that require knowledge beyond core Kubescape functionality.

Once you see an issue that you'd like to work on, please post a comment saying
that you want to work on it and assign yourself.

## Working on issues
We categorize contributions into two:
* Small code changes or fixes, whose scope is limited to documentation, minor fixes, development that involves no more than a file or two.
* Complex features and improvements, with potentially unlimited scope

If you are working on a small change, feel free to open a Pull Request.

If you want to work on a bigger change, please discuss the change you are plannning with the community and the maintainers. In this case, opening an issue in the  applicable repository and raising the improvement you want to add in the kubescape-dev slack or community meeting is a great start!

Getting sign-off before embarking on a big change is important so the maintainers can help guide you in the right direction. 

## Ask for help

The best way to reach us with a question when contributing is to ask on:

* The original github issue
* The kubescape-dev Slack channel

## Build and test locally

Please follow the [instructions here](https://github.com/kubescape/kubescape/wiki/Building).

## Pull Request process

1. Ensure any install or build dependencies are removed before the end of the layer when running a  build.
2. Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.
3. Open Pull Request to the `master`/`main` branch.
4. We will merge the Pull Request once you have the sign-off.

<!-- Ben/Rotem/Matthias the section below was in the CNCF template and seems important to me. WDYT?

## Development Environment Setup

[Instructions](https://contribute.cncf.io/maintainers/github/templates/required/contributing/#development-environment-setup)

⚠️ **Explain how to set up a development environment**-->

## Sign your commits

### Developer Certificate of Origin

All commits to the project must be "signed off", which states that you agree to the terms of the [Developer Certificate of Origin](https://developercertificate.org/).  This is done by adding a "Signed-off-by:" line in the commit message, with your name and email address.

Commits made through the GitHub web application are automatically signed off.

### Configuring Git to sign off commits

First, configure your name and email address in Git global settings:

```
$ git config --global user.name "John Doe"
$ git config --global user.email johndoe@example.com
```

You can now sign off per-commit, or configure Git to always sign off commits per repository.

### Sign off per-commit

Add [`-s`](https://git-scm.com/docs/git-commit#Documentation/git-commit.txt--s) to your Git command line. For example:

```git commit -s -m "Fix issue 64738"```

This is tedious, and if you forget, you'll have to [amend your commit](#fixing-a-commit-where-the-dco-failed).

### Configure a repository to always include sign off

There are many ways to achieve this with Git hooks, but the simplest is to do the following:

```
cd your-repo
curl -Ls https://gist.githubusercontent.com/dixudx/7d7edea35b4d91e1a2a8fbf41d0954fa/raw/prepare-commit-msg -o .git/hooks/prepare-commit-msg
chmod +x .git/hooks/prepare-commit-msg
```

### Use semantic commit messages (optional)

When contributing, you could consider using [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/), in order to improve logs readability and help us to automatically generate `CHANGELOG`s.

Format: `<type>(<scope>): <subject>`

`<scope>` is optional

#### Example

```
feat(cmd): add kubectl plugin
^--^ ^-^   ^----------------^
|    |     |
|    |     +-> subject: summary in present tense.
|    |
|    +-------> scope: point of interest
|
+-------> type: chore, docs, feat, fix, refactor, style, or test.
```

More Examples:
* `feat`: new feature for the user, not a new feature for build script
* `fix`: bug fix for the user, not a fix to a build script
* `docs`: changes to the documentation
* `style`: formatting, missing semi colons, etc; no production code change
* `refactor`: refactoring production code, eg. renaming a variable
* `test`: adding missing tests, refactoring tests; no production code change
* `chore`: updating grunt tasks etc; no production code change

### Fixing a commit where the DCO failed

Check out [this guide](https://github.com/src-d/guide/blob/master/developer-community/fix-DCO.md).