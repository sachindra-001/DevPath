const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

process.env.STITCH_API_KEY = "AQ.Ab8RN6KD5CGQe6vlb-X3cUSrjp87X8tjRUqfRJGPx_DoCc0MYw";

const projectData = JSON.parse(
  fs.readFileSync(path.join(__dirname, "../docs/stitch_project.json"), "utf-8")
);

const screens = [];

for (const inst of projectData.screenInstances || []) {
  if (!inst.sourceScreen) continue;
  try {
    const res = execSync(
      `npx -y @_davideast/stitch-mcp tool get_screen -d "{\\"name\\":\\"${inst.sourceScreen}\\",\\"projectId\\":\\"1438700305025467898\\",\\"screenId\\":\\"${inst.id}\\"}" -o json`,
      { env: process.env, encoding: "utf-8", maxBuffer: 10 * 1024 * 1024 }
    );
    const screen = JSON.parse(res);
    screens.push({
      id: inst.id,
      title: screen.title,
      deviceType: screen.deviceType,
      hasHtml: !!screen.htmlCode,
      downloadUrl: screen.htmlCode?.downloadUrl,
    });
    console.log(`[Screen] ${inst.id}: "${screen.title}" (${screen.deviceType})`);
  } catch (err) {
    console.error(`Failed to get screen ${inst.id}:`, err.message);
  }
}

fs.writeFileSync(
  path.join(__dirname, "../docs/stitch_screens_summary.json"),
  JSON.stringify(screens, null, 2),
  "utf-8"
);
console.log("Saved screens summary to docs/stitch_screens_summary.json");
