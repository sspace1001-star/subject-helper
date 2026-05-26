#!/usr/bin/env bash
# oci-vm-1-6 (152.69.239.29) 배포
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOST="${DEPLOY_HOST:-oci-vm-1-6}"
REMOTE_DIR="${DEPLOY_DIR:-~/subject-helper}"

rsync -avz \
  --exclude '.git' --exclude '.venv' --exclude '.agent' \
  --exclude '__pycache__' --exclude '.DS_Store' --exclude '~$*' \
  "$ROOT/" "$HOST:$REMOTE_DIR/"

ssh "$HOST" "set -e
cd $REMOTE_DIR
python3 -m venv .venv 2>/dev/null || true
.venv/bin/pip install -q -U pip
.venv/bin/pip install -q -r requirements.txt
sudo systemctl restart subject-helper
sleep 2
curl -sS -o /dev/null -w 'local %{http_code}\n' http://127.0.0.1:5001/"

echo "배포 완료: http://univref.152-69-239-29.sslip.io/"
