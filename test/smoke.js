const assert = require("assert").strict;
const { analyze, samplePacket } = require("../src/index.js");

const sample = analyze(samplePacket);
assert.ok(["ready", "needs-review", "blocked"].includes(sample.status));
assert.ok(Number.isFinite(sample.score));
assert.ok(Array.isArray(sample.findings));
assert.ok(sample.summary.includes("issue"));

const broken = analyze({});
assert.equal(broken.status, "blocked");
assert.ok(broken.findings.some((finding) => finding.id === "missing-required-field"));
assert.ok(broken.score < 70);

console.log("smoke tests passed");
