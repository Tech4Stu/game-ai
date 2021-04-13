import { Octokit } from "https://cdn.skypack.dev/@octokit/rest";

async function getCommits(var_authentication) {
  const octokit = new Octokit({auth: "f6d70d34445424b440bb17ca322215b7db9f6a26"});

  console.log("Async started");
  const commits = await octokit.rest.repos.listCommits({
    owner: "Tech4Stu",
    repo: "hillclimber",
  });
  console.log("Async finished");
  return commits;
}

console.log(getCommits());
