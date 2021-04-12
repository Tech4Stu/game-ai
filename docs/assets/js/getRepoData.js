import { createTokenAuth } from "https://cdn.skypack.dev/@octokit/auth-token";
import { Octokit } from "https://cdn.skypack.dev/@octokit/rest";

const TOKEN = "f6d70d34445424b440bb17ca322215b7db9f6a26";

async function getCommits() {
  const auth = createTokenAuth(TOKEN);
  const authentication = await auth();
  const octokit = new Octokit({auth: authentication});

  console.log("Async started");
  const commits = await octokit.rest.repos.listCommits({
    owner: "Tech4Stu",
    repo: "hillclimber",
  });
  console.log("Async finished");
  return commits
}

console.log(getCommits());
