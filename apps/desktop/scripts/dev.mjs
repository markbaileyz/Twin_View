#!/usr/bin/env node
import { spawn } from 'node:child_process';
spawn('vite', ['--host', '127.0.0.1', '--port', '5173'], { stdio: 'inherit', shell: true });
