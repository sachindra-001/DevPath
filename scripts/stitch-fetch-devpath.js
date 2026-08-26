const { execSync } = require("child_process");

process.env.STITCH_API_KEY = "AQ.Ab8RN6KD5CGQe6vlb-X3cUSrjp87X8tjRUqfRJGPx_DoCc0MYw";
const projectId = "1438700305025467898";

try {
  const result = execSync(
    `npx -y @_davideast/stitch-mcp tool list_screens -d "{\\"projectId\\":\\"${projectId}\\"}"`,
    {
      env: process.env,
      encoding: "utf-8",
    }
  );
  console.log("Screens list:\n", result);
} catch (error) {
  console.error("Error:", error.stdout || error.message);
}
