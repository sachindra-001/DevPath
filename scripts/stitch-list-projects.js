const { execSync } = require("child_process");

process.env.STITCH_API_KEY = "AQ.Ab8RN6KD5CGQe6vlb-X3cUSrjp87X8tjRUqfRJGPx_DoCc0MYw";

try {
  const result = execSync("npx -y @_davideast/stitch-mcp tool list_projects -o json", {
    env: process.env,
    encoding: "utf-8",
  });
  const data = JSON.parse(result);
  const projects = data.projects || [];
  console.log(`Found ${projects.length} project(s):`);
  projects.forEach((p, idx) => {
    console.log(`[${idx + 1}] Title: "${p.title}" | ID/Name: "${p.name}"`);
  });
} catch (error) {
  console.error("Error:", error.stdout || error.message);
}
