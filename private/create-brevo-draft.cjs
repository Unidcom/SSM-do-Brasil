const fs = require("fs");
const https = require("https");

function readEnv(path) {
  return Object.fromEntries(
    fs
      .readFileSync(path, "utf8")
      .split(/\r?\n/)
      .filter((line) => /^\s*[^#=\s]+\s*=/.test(line))
      .map((line) => {
        const separator = line.indexOf("=");
        return [line.slice(0, separator).trim(), line.slice(separator + 1).trim()];
      }),
  );
}

async function main() {
  const env = readEnv("private/brevo-ssm.env");
  const name = "Radar Estrutural SSM — 2026-11-04";
  const headers = { "api-key": env.BREVO_API_KEY, accept: "application/json" };
  const request = (method, path, body) =>
    new Promise((resolve, reject) => {
      const requestHeaders = { ...headers };
      if (body) {
        requestHeaders["content-type"] = "application/json";
        requestHeaders["content-length"] = Buffer.byteLength(body);
      }
      const request = https.request(
        { hostname: "api.brevo.com", path, method, family: 4, headers: requestHeaders },
        (response) => {
          let result = "";
          response.setEncoding("utf8");
          response.on("data", (chunk) => (result += chunk));
          response.on("end", () => {
            if (response.statusCode < 200 || response.statusCode >= 300) {
              reject(new Error(`Brevo respondeu ${response.statusCode}: ${result}`));
              return;
            }
            resolve(result);
          });
        },
      );
      request.on("error", reject);
      if (body) request.write(body);
      request.end();
    });

  const campaigns = JSON.parse(
    await request("GET", "/v3/emailCampaigns?type=classic&status=draft&limit=50&offset=0"),
  );

  const existing = (campaigns.campaigns || []).find((campaign) => campaign.name === name);
  if (existing) {
    console.log(JSON.stringify({ action: "existing", id: existing.id, status: existing.status }));
    return;
  }

  const payload = {
    type: "classic",
    name,
    subject: "Baterias entram no leilão: contratos de 15 anos já têm regra",
    sender: {
      name: env.BREVO_SENDER_NAME,
      email: env.BREVO_SENDER_EMAIL,
    },
    htmlContent: fs.readFileSync("newsletter/2026-11-03/newsletter.html", "utf8"),
    recipients: { listIds: env.BREVO_LIST_IDS.split(",").map(Number) },
    mirrorActive: true,
    inlineImageActivation: false,
  };

  const body = await request("POST", "/v3/emailCampaigns", JSON.stringify(payload));
  console.log(JSON.stringify({ action: "created", response: JSON.parse(body) }));
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
