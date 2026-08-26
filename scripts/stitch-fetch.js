const { execSync } = require("child_process");

process.env.STITCH_API_KEY = "AQ.Ab8RN6KD5CGQe6vlb-X3cUSrjp87X8tjRUqfRJGPx_DoCc0MYw";

try {
  const result = execSync("npx -y @_davideast/stitch-mcp tool list_projects", {
    env: process.env,
    encoding: "utf-8",
  });
  console.log("Projects Result:\n", result);
} catch (error) {
  console.error("Error listing projects:", error.stdout || error.message);
}
