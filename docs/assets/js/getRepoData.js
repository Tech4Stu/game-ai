import { Octokit } from "https://cdn.skypack.dev/@octokit/rest";

// Create a personal access token at https://github.com/settings/tokens/new?scopes=repo
const octokit = new Octokit({auth: "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"});

async function getCommits() {
  console.log("Async started");
  const commits = await octokit.rest.repos.listCommits({
    owner: "Tech4Stu",
    repo: "hillclimber",
  });
  console.log("Async finished");
  return commits
}

console.log(getCommits());
