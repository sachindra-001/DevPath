const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

process.env.STITCH_API_KEY = "AQ.Ab8RN6KD5CGQe6vlb-X3cUSrjp87X8tjRUqfRJGPx_DoCc0MYw";

const targetScreens = [
  { id: "85d94abfbf5c45dca9d255d7a98e52ef", name: "landing" },
  { id: "8d117f11af4849ba97d3e715f2824c74", name: "catalog" },
  { id: "be4a1565da03416aa6da708af10a67a1", name: "roadmap_detail" },
  { id: "65494c55dc374a7385e08d36974b0bf9", name: "topic_detail" },
  { id: "23f639591faa47cdb8bb4099ec8fcad8", name: "login" },
  { id: "d0044c6bdc804226b4b5504e402e9794", name: "register" },
  { id: "cfdded434c734b80a6245999d3f9a601", name: "dashboard" },
];

const outDir = path.join(__dirname, "../docs/stitch_screens");
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

for (const s of targetScreens) {
  try {
    console.log(`Downloading screen code for: ${s.name} (${s.id})...`);
    const res = execSync(
      `npx -y @_davideast/stitch-mcp tool get_screen_code -d "{\\"name\\":\\"projects/1438700305025467898/screens/${s.id}\\",\\"projectId\\":\\"1438700305025467898\\",\\"screenId\\":\\"${s.id}\\"}" -o json`,
      { env: process.env, encoding: "utf-8", maxBuffer: 10 * 1024 * 1024 }
    );
    const data = JSON.parse(res);
    const html = data.htmlCode || data.html || data.code || JSON.stringify(data, null, 2);
    fs.writeFileSync(path.join(outDir, `${s.name}.html`), html, "utf-8");
    console.log(`Saved ${s.name}.html`);
  } catch (err) {
    console.error(`Error for ${s.name}:`, err.message);
  }
}
