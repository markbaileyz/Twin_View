#!/usr/bin/env node
import { execSync } from 'node:child_process';

const log = (m) => console.log(m);
const fail = (m) => { console.error(m); process.exit(1); };

const [maj] = process.versions.node.split('.').map(Number);
if (maj < 18) fail('Node.js >=18 required.');

function pyVer(bin) {
  try {
    const out = execSync(`${bin} --version`, { encoding: 'utf8' }).trim();
    const m = out.match(/(\d+)\.(\d+)\.(\d+)/);
    if (!m) return null;
    return { major: +m[1], minor: +m[2], text: out };
  } catch { return null; }
}
const py = pyVer('python') || pyVer('python3');
if (!py || py.major < 3 || py.minor < 11) fail('Python >=3.11 required.');
log(`✅ Node ${process.versions.node}`);
log(`✅ ${py.text}`);
log('ℹ️ Ollama is optional.');
