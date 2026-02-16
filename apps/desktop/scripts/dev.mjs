#!/usr/bin/env node
import { spawn } from 'node:child_process';

function run(cmd, args, opts = {}) {
  const child = spawn(cmd, args, { stdio: 'inherit', shell: true, ...opts });
  child.on('exit', (code) => {
    if (code && code !== 0) process.exit(code);
  });
  return child;
}

run('tsc', ['-p', 'tsconfig.json'], { cwd: process.cwd() });
const vite = run('vite', ['--host', '127.0.0.1', '--port', '5173'], { cwd: process.cwd() });

const waiter = run('wait-on', ['http://127.0.0.1:5173'], { cwd: process.cwd() });
waiter.on('exit', (code) => {
  if (code === 0) {
    run('electron', ['dist/main/index.js'], {
      cwd: process.cwd(),
      env: { ...process.env, VITE_DEV_SERVER_URL: 'http://127.0.0.1:5173' },
    });
  } else {
    vite.kill('SIGTERM');
    process.exit(code ?? 1);
  }
});
