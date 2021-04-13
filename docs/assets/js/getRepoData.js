import { createTokenAuth } from "https://cdn.skypack.dev/@octokit/auth-token";
import { Octokit } from "https://cdn.skypack.dev/@octokit/rest";

async function authenticate(){
  const TOKEN = "f6d70d34445424b440bb17ca322215b7db9f6a26";
  const auth = createTokenAuth(TOKEN);
  const authentication = await auth();
  return authentication
}

async function getCommits(var_authentication) {
  const octokit = new Octokit({auth: var_authentication});

  console.log("Async started");
  const commits = await octokit.rest.repos.listCommits({
    owner: "Tech4Stu",
    repo: "hillclimber",
  });
  console.log("Async finished");
  return commits
}

authenticated = authenticate();
console.log(getCommits(authenticated));
