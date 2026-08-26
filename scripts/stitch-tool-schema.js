const { execSync } = require("child_process");

process.env.STITCH_API_KEY = "AQ.Ab8RN6KD5CGQe6vlb-X3cUSrjp87X8tjRUqfRJGPx_DoCc0MYw";

try {
  const schema = JSON.parse(
    execSync("npx -y @_davideast/stitch-mcp tool --schema", {
      env: process.env,
      encoding: "utf-8",
    })
  );
  
  const relevant = schema.filter(t => ["list_screens", "get_project", "get_screen_code", "get_screen"].includes(t.name));
  console.log(JSON.stringify(relevant, null, 2));
} catch (error) {
  console.error("Error:", error.message);
}
