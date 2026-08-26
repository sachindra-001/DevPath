const { execSync } = require("child_process");

process.env.STITCH_API_KEY = "AQ.Ab8RN6KD5CGQe6vlb-X3cUSrjp87X8tjRUqfRJGPx_DoCc0MYw";

try {
  const result = execSync(
    'npx -y @_davideast/stitch-mcp tool get_project -d "{\\"name\\":\\"projects/1438700305025467898\\"}" -o json',
    {
      env: process.env,
      encoding: "utf-8",
    }
  );
  console.log("Project Details:\n", result);
} catch (error) {
  console.error("Error:", error.stdout || error.message);
}
