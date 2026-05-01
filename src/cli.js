#!/usr/bin/env node
const { readFile } = require("fs").promises;
const process = require("process");
const { analyze, samplePacket, project } = require("./index.js");

async function readStdin() {
  if (process.stdin.isTTY) return "";
  let data = "";
  for await (const chunk of process.stdin) data += chunk;
  return data.trim();
}

async function main() {
  const arg = process.argv[2];
  if (arg === "--help" || arg === "-h") {
    console.log(`${project.title} v${project.version}

Usage:
  red-team-replay sample
  red-team-replay packet.json
  cat packet.json | red-team-replay
`);
    return;
  }

  let packet = samplePacket;
  if (arg && arg !== "sample") {
    packet = JSON.parse(await readFile(arg, "utf8"));
  } else {
    const stdin = await readStdin();
    if (stdin) packet = JSON.parse(stdin);
  }

  console.log(JSON.stringify(analyze(packet), null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
