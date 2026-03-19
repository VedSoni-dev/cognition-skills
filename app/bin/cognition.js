#!/usr/bin/env node

const { execSync, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');
const crypto = require('crypto');

const SKILLS_DIR = path.join(__dirname, '..', '..');
const COG_DIR = path.join(os.homedir(), '.cognition');
const TOKEN_PATH = path.join(COG_DIR, 'token');
const IDENTITY_PATH = path.join(COG_DIR, 'identity.json');

// ── Custom Banner ──
const banner = `
\x1b[38;5;99m  ██████╗ ██████╗  ██████╗ ███╗   ██╗██╗████████╗██╗ ██████╗ ███╗   ██╗
\x1b[38;5;135m ██╔════╝██╔═══██╗██╔════╝ ████╗  ██║██║╚══██╔══╝██║██╔═══██╗████╗  ██║
\x1b[38;5;141m ██║     ██║   ██║██║  ███╗██╔██╗ ██║██║   ██║   ██║██║   ██║██╔██╗ ██║
\x1b[38;5;177m ██║     ██║   ██║██║   ██║██║╚██╗██║██║   ██║   ██║██║   ██║██║╚██╗██║
\x1b[38;5;213m ╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║██║   ██║   ██║╚██████╔╝██║ ╚████║
\x1b[38;5;213m  ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝\x1b[0m

\x1b[38;5;245m  AI that watches what you learn and helps you remember it.\x1b[0m
`;

console.log(banner);

// ── 1. Identity (auto-generated on first run) ──
fs.mkdirSync(COG_DIR, { recursive: true });

let identity;
if (fs.existsSync(IDENTITY_PATH)) {
  identity = JSON.parse(fs.readFileSync(IDENTITY_PATH, 'utf8'));
  console.log(`  \x1b[32m✓\x1b[0m User: ${identity.username} (${identity.user_id})`);
} else {
  // First run — grab OS username, generate unique ID
  const username = os.userInfo().username;
  const user_id = `${username}-${crypto.randomBytes(4).toString('hex')}`;
  identity = {
    username,
    user_id,
    created_at: new Date().toISOString(),
    machine: os.hostname(),
  };
  fs.writeFileSync(IDENTITY_PATH, JSON.stringify(identity, null, 2));
  console.log(`  \x1b[32m✓\x1b[0m Identity created: ${username} (${user_id})`);
}

// ── 2. API Token ──
if (!fs.existsSync(TOKEN_PATH)) {
  // Use the shared API key for now — in production this would call a signup endpoint
  fs.writeFileSync(TOKEN_PATH, 'dev-secret');
  console.log('  \x1b[32m✓\x1b[0m API token created');
} else {
  console.log('  \x1b[32m✓\x1b[0m API token found');
}

// ── 3. Screenpipe ──
try {
  execSync('curl -s http://localhost:3030/health', { timeout: 3000, stdio: 'pipe' });
  console.log('  \x1b[32m✓\x1b[0m Screenpipe running');
} catch {
  console.log('  \x1b[33m→\x1b[0m Starting Screenpipe...');
  try {
    spawn('screenpipe', ['record'], { detached: true, stdio: 'ignore', shell: true }).unref();
    console.log('  \x1b[32m✓\x1b[0m Screenpipe starting');
  } catch {
    try {
      spawn('npx', ['screenpipe@latest', 'record'], { detached: true, stdio: 'ignore', shell: true }).unref();
      console.log('  \x1b[32m✓\x1b[0m Screenpipe starting (npx)');
    } catch {
      console.log('  \x1b[31m✗\x1b[0m Screenpipe not found. Install: npm i -g screenpipe');
    }
  }
}

// ── 4. API Check ──
try {
  const token = fs.readFileSync(TOKEN_PATH, 'utf8').trim();
  const result = execSync(`curl -s -H "x-api-key: ${token}" https://cognition-api.fly.dev/healthz`, { timeout: 8000, stdio: 'pipe' });
  const health = JSON.parse(result.toString());
  if (health.status === 'ok') console.log('  \x1b[32m✓\x1b[0m API connected');
} catch {
  console.log('  \x1b[33m△\x1b[0m API check skipped');
}

// ── 5. Screenpipe MCP ──
try {
  const mcpList = execSync('claude mcp list 2>&1', { stdio: 'pipe' }).toString();
  if (mcpList.includes('screenpipe')) {
    console.log('  \x1b[32m✓\x1b[0m Screenpipe MCP connected');
  } else {
    execSync('claude mcp add-json screenpipe \'{"command":"cmd","args":["/c","npx","-y","screenpipe-mcp"],"type":"stdio"}\' -s local', { stdio: 'pipe' });
    console.log('  \x1b[32m✓\x1b[0m Screenpipe MCP added');
  }
} catch {
  console.log('  \x1b[33m△\x1b[0m MCP check skipped');
}

console.log(`\n\x1b[38;5;245m  Starting session as ${identity.username}...\x1b[0m\n`);

// ── 6. Launch Claude Code with identity as env var ──
const claude = spawn('claude', ['--plugin-dir', SKILLS_DIR], {
  stdio: 'inherit',
  shell: true,
  env: {
    ...process.env,
    COGNITION_USER_ID: identity.user_id,
    COGNITION_USERNAME: identity.username,
  },
});

claude.on('exit', (code) => process.exit(code || 0));
