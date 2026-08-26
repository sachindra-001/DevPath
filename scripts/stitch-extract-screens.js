const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

process.env.STITCH_API_KEY = "AQ.Ab8RN6KD5CGQe6vlb-X3cUSrjp87X8tjRUqfRJGPx_DoCc0MYw";

try {
  const result = execSync(
    'npx -y @_davideast/stitch-mcp tool get_project -d "{\\"name\\":\\"projects/1438700305025467898\\"}" -o json',
    {
      env: process.env,
      encoding: "utf-8",
      maxBuffer: 10 * 1024 * 1024,
    }
  );
  
  const project = JSON.parse(result);
  console.log("Project Title:", project.title);
  console.log("Design System Tokens:", JSON.stringify(project.designSystem, null, 2));

  // Save full project JSON to docs/stitch_project.json
  fs.writeFileSync(
    path.join(__dirname, "../docs/stitch_project.json"),
    JSON.stringify(project, null, 2),
    "utf-8"
  );
  console.log("Saved project metadata to docs/stitch_project.json");

  // List screens
  const instances = project.screenInstances || [];
  console.log(`Found ${instances.length} screen instance(s):`);
  instances.forEach((inst, i) => {
    console.log(`[${i + 1}] ID: ${inst.id}, Source: ${inst.sourceScreen}, Type: ${inst.type || "SCREEN"}`);
  });
} catch (error) {
  console.error("Error:", error.stdout || error.message);
}
