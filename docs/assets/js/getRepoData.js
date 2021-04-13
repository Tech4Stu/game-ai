import { Octokit } from "https://cdn.skypack.dev/@octokit/rest";

async function getCommits(var_authentication) {
  const octokit = new Octokit({auth: "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"});

  console.log("Async started");
  const commits = await octokit.rest.repos.listCommits({
    owner: "Tech4Stu",
    repo: "hillclimber",
  });
  console.log("Async finished");
  return commits;
}

console.log(getCommits());
