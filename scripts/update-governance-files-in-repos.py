import os
import json
import sys
from github import Github
from github.GithubException import GithubException

def update_governance_files(org_name, token, governance_files, repos):
    g = Github(token)

    # Get authenticated user info from GitHub API
    github_user = g.get_user()
    git_name = github_user.name or github_user.login  # fallback to login if name is not set
    git_email = f"{github_user.id}+{github_user.login}@users.noreply.github.com"
    user = type('User', (), {'name': git_name, 'email': git_email})()
    print(f"User: {user.name} <{user.email}> ")
    org = g.get_organization(org_name)

    pr_urls = []
    failed_repos = []

    for repo_name in repos:
        repo = org.get_repo(repo_name)

        print(f"Processing {repo.name}")

        # Get default branch name
        default_branch = repo.default_branch

        print(f"Default branch: {default_branch}")

        try:
            # Create a new branch for updates
            base_branch = repo.get_branch(default_branch)
            branch_name = f"update-governance-files-{os.urandom(4).hex()}"
            repo.create_git_ref(f"refs/heads/{branch_name}", base_branch.commit.sha)

            for filename, local_path in governance_files.items():
                try:
                    with open(local_path, 'r') as f:
                        new_content = f.read()

                    commit_message = f"Update {filename}\n\nSigned-off-by: {git_name} <{git_email}>"
                    create_message = f"Add {filename}\n\nSigned-off-by: {git_name} <{git_email}>"

                    try:
                        file = repo.get_contents(filename, ref=branch_name)
                        repo.update_file(
                            filename,
                            commit_message,
                            new_content,
                            file.sha,
                            branch=branch_name
                        )
                    except Exception:
                        try:
                            repo.create_file(
                                filename,
                                create_message,
                                new_content,
                                branch=branch_name
                            )
                        except Exception as e:
                            print(f"Error creating {filename} in {repo.name} at line {sys.exc_info()[2].tb_lineno}: {str(e)}")
                            failed_repos.append(repo.name)

                except Exception as e:
                    print(f"Error processing {filename} in {repo.name} at line {sys.exc_info()[2].tb_lineno}: {str(e)}")
                    failed_repos.append(repo.name)
                    continue

            # Create pull request
            if repo.name not in failed_repos:
                pr = repo.create_pull(
                    title="Update governance files",
                body="Automated update of organization governance files",
                base=default_branch,
                head=branch_name
            )
            print(f"Created PR #{pr.number} in {repo.name}")
            pr_urls.append(pr.html_url)
        except GithubException as e:
            print(f"Error processing repo {repo.name} at line {sys.exc_info()[2].tb_lineno}: {str(e)}")

    return pr_urls, failed_repos

if __name__ == "__main__":
    ORG_NAME = "kubescape"
    TOKEN = os.getenv("GITHUB_TOKEN")
    if len(sys.argv) > 1:
        REPOS = json.load(open(sys.argv[1]))
    else:
        REPOS = json.load(open("repositories-under-governance.json"))

    GOVERNANCE_FILES = {
        "ADOPTERS.md": "repo-gov-templates/ADOPTERS.md",
        "CODE_OF_CONDUCT.md": "repo-gov-templates/CODE_OF_CONDUCT.md",
        "COMMUNITY.md": "repo-gov-templates/COMMUNITY.md",
        "CONTRIBUTING.md": "repo-gov-templates/CONTRIBUTING.md",
        "GOVERNANCE.md": "repo-gov-templates/GOVERNANCE.md",
        "MAINTAINERS.md": "repo-gov-templates/MAINTAINERS.md",
        "SECURITY.md": "repo-gov-templates/SECURITY.md"
    }

    pr_urls, failed_repos = update_governance_files(ORG_NAME, TOKEN, GOVERNANCE_FILES, REPOS)

    print(f"Created PRs:")
    for pr_url in pr_urls:
        print(f"  - {pr_url}")
    if len(failed_repos) > 0:
        print(f"Failed repos: {failed_repos}")
        # Save failed repos to a file
        with open("failed-repos.json", "w") as f:
            json.dump(failed_repos, f)





