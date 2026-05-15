param(
    [string]$ServerIp = "",
    [string]$SshUser = "",
    [string]$SshTarget = ""
)

$ErrorActionPreference = "Stop"

if ($SshTarget) {
    if ($SshTarget -notmatch "^(?<user>[^@]+)@(?<host>.+)$") {
        throw "SshTarget must look like user@host"
    }

    if (-not $SshUser) {
        $SshUser = $Matches.user
    }

    if (-not $ServerIp) {
        $ServerIp = $Matches.host
    }
}

if (-not $ServerIp) {
    throw "Specify -ServerIp or -SshTarget"
}

if (-not $SshUser) {
    throw "Specify -SshUser or -SshTarget"
}

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Require-Command {
    param([string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $Name"
    }
}

function ConvertTo-PlainText {
    param([Security.SecureString]$SecureString)
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureString)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    }
    finally {
        if ($bstr -ne [IntPtr]::Zero) {
            [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
        }
    }
}

function Invoke-Ssh {
    param(
        [string]$Command,
        [switch]$AllowFailure
    )

    & ssh -o StrictHostKeyChecking=no "$SshUser@$ServerIp" $Command
    if (-not $AllowFailure -and $LASTEXITCODE -ne 0) {
        throw "SSH command failed."
    }
}

function Invoke-RemoteScript {
    param([string]$ScriptText)

    $tempScript = Join-Path $env:TEMP ("urfu-remote-{0}.sh" -f ([guid]::NewGuid().ToString("N")))
    try {
        [System.IO.File]::WriteAllText($tempScript, $ScriptText, [System.Text.UTF8Encoding]::new($false))
        Get-Content -Raw $tempScript | & ssh -o StrictHostKeyChecking=no "$SshUser@$ServerIp" "bash -s"
        if ($LASTEXITCODE -ne 0) {
            throw "Remote deployment script failed."
        }
    }
    finally {
        if (Test-Path $tempScript) {
            Remove-Item -LiteralPath $tempScript -Force
        }
    }
}

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$archivePath = Join-Path $env:TEMP "urfu-innovation-deploy.tgz"
$remoteArchive = "~/urfu-innovation-deploy.tgz"

Require-Command ssh
Require-Command scp
Require-Command tar

Write-Step "Checking SSH access to $SshUser@$ServerIp"
Invoke-Ssh "echo connected"

Write-Step "Checking remote sudo mode"
& ssh -o StrictHostKeyChecking=no "$SshUser@$ServerIp" 'sudo -n true >/dev/null 2>&1'
$sudoPassword = ""
if ($LASTEXITCODE -ne 0) {
    $securePassword = Read-Host "Enter sudo password for $SshUser@$ServerIp" -AsSecureString
    $sudoPassword = ConvertTo-PlainText -SecureString $securePassword
}

Write-Step "Building deploy archive"
if (Test-Path $archivePath) {
    Remove-Item -LiteralPath $archivePath -Force
}

Push-Location $projectRoot
try {
    & tar -czf $archivePath `
        --exclude=.git `
        --exclude=.idea `
        --exclude=.venv `
        --exclude=.vite `
        --exclude=frontend/frontend-vue/node_modules `
        --exclude=frontend/frontend-vue/dist `
        --exclude=backend/data `
        --exclude=urfu-innovation-deploy.tgz `
        -C $projectRoot .
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to build deploy archive."
    }
}
finally {
    Pop-Location
}

Write-Step "Uploading archive to server"
& scp -o StrictHostKeyChecking=no $archivePath "${SshUser}@${ServerIp}:$remoteArchive"
if ($LASTEXITCODE -ne 0) {
    throw "Failed to upload deploy archive."
}

$sudoPasswordB64 = ""
if ($sudoPassword) {
    $sudoPasswordB64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($sudoPassword))
}

$remoteScript = @'
set -euo pipefail

APP_DIR="$HOME/URFU-Innovation"
ARCHIVE_PATH="$HOME/urfu-innovation-deploy.tgz"
PRESERVE_ENV_REL="backend/app/.env"
PRESERVE_DB_REL="backend/app/data/innovate.db3"
SUDO_PASSWORD_B64="__SUDO_PASSWORD_B64__"

log() {
  printf '\n==> %s\n' "$1"
}

have_sudo_nopass() {
  sudo -n true >/dev/null 2>&1
}

run_sudo() {
  if have_sudo_nopass; then
    sudo "$@"
    return
  fi

  if [ -z "$SUDO_PASSWORD_B64" ]; then
    echo "sudo password is required but was not provided" >&2
    exit 1
  fi

  local sudo_password
  sudo_password="$(printf '%s' "$SUDO_PASSWORD_B64" | base64 -d)"
  printf '%s\n' "$sudo_password" | sudo -S -p '' "$@"
}

http_status() {
  python3 - "$1" <<'PY'
import sys
import urllib.request

url = sys.argv[1]
with urllib.request.urlopen(url, timeout=20) as response:
    print(response.status)
PY
}

wait_for_http_status() {
  local url="$1"
  local expected_status="$2"
  local attempts="${3:-30}"
  local sleep_seconds="${4:-2}"
  local status=""

  for _ in $(seq 1 "$attempts"); do
    status="$(http_status "$url" 2>/dev/null || true)"
    if [ "$status" = "$expected_status" ]; then
      return 0
    fi
    sleep "$sleep_seconds"
  done

  echo "Timed out waiting for $url to return HTTP $expected_status" >&2
  return 1
}

wait_for_docker() {
  local attempts="${1:-30}"
  local sleep_seconds="${2:-2}"

  for _ in $(seq 1 "$attempts"); do
    if run_sudo docker info >/dev/null 2>&1; then
      return 0
    fi
    sleep "$sleep_seconds"
  done

  echo "Timed out waiting for Docker daemon" >&2
  run_sudo systemctl status docker --no-pager -l || true
  return 1
}

log "Installing Docker if needed"
if ! command -v docker >/dev/null 2>&1; then
  run_sudo apt-get update
  run_sudo apt-get install -y docker.io docker-compose-v2
fi

run_sudo systemctl reset-failed docker docker.socket || true
run_sudo systemctl enable --now containerd docker.socket docker
wait_for_docker

db_backup=""
env_backup=""

if [ -f "$APP_DIR/$PRESERVE_DB_REL" ]; then
  db_backup="$(mktemp)"
  cp "$APP_DIR/$PRESERVE_DB_REL" "$db_backup"
fi

if [ -f "$APP_DIR/$PRESERVE_ENV_REL" ]; then
  env_backup="$(mktemp)"
  cp "$APP_DIR/$PRESERVE_ENV_REL" "$env_backup"
fi

log "Refreshing application directory"
rm -rf "$APP_DIR"
mkdir -p "$APP_DIR"
tar -xzf "$ARCHIVE_PATH" -C "$APP_DIR"

if [ -n "$env_backup" ]; then
  mkdir -p "$APP_DIR/backend/app"
  cp "$env_backup" "$APP_DIR/$PRESERVE_ENV_REL"
fi

if [ -n "$db_backup" ]; then
  mkdir -p "$APP_DIR/backend/app/data"
  cp "$db_backup" "$APP_DIR/$PRESERVE_DB_REL"
fi

log "Starting containers"
cd "$APP_DIR"
run_sudo docker compose up -d --build

log "Container status"
run_sudo docker compose ps

log "Verifying local HTTP"
wait_for_http_status "http://127.0.0.1" "200"

log "Verifying API proxy"
wait_for_http_status "http://127.0.0.1/api/get-all-test" "200"

log "Cleaning up archive"
rm -f "$ARCHIVE_PATH"

log "Remote deploy finished"
'@

$remoteScript = $remoteScript.Replace("__SUDO_PASSWORD_B64__", $sudoPasswordB64)

Write-Step "Running remote deploy"
Invoke-RemoteScript -ScriptText $remoteScript

Write-Step "Verifying public HTTP from Windows"
& curl.exe -fsSI "http://$ServerIp" | Out-Host
if ($LASTEXITCODE -ne 0) {
    throw "Public HTTP check failed."
}

if (Test-Path $archivePath) {
    Remove-Item -LiteralPath $archivePath -Force
}

Write-Host ""
Write-Host "Deploy finished successfully." -ForegroundColor Green
Write-Host "App URL: http://$ServerIp"
