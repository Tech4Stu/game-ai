import { Octokit } from "https://cdn.skypack.dev/@octokit/rest";

// Create a personal access token at https://github.com/settings/tokens/new?scopes=repo
const octokit = new Octokit({auth: "0459c1c341c8b7b6a9f7a79a05ab266e629cbaad"});

const auth = await octokit.request("/user");

(async () => {
  const commits = await octokit.rest.commits.get({
  owner: "Tech4Stu",
  repo: "hillclimber"",
  mediaType: {
    format: "patch",
  },
});
  console.log("Async is working");
  console.log(commits);
});
