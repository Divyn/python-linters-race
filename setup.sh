set -e
export DEBIAN_FRONTEND=noninteractive
apt-get update -q
apt-get install -yq --no-install-recommends python3-venv python3-dev build-essential ca-certificates
python3 -m venv /root/v
/root/v/bin/pip install -q --upgrade pip
/root/v/bin/pip install -q ruff flake8 pylint
/root/v/bin/pip freeze > /root/exp/versions.txt
mkdir -p /root/exp/target /tmp/sdists
/root/v/bin/pip download -q --no-binary :all: -d /tmp/sdists \
  requests==2.32.3 urllib3==2.3.0 idna==3.10 charset-normalizer==3.4.1 \
  httpx==0.28.1 httpcore==1.0.7 anyio==4.8.0 certifi==2024.12.14
cd /tmp/sdists
for f in *.tar.gz; do
  tar -xzf "$f" -C /root/exp/target
done
find /root/exp/target -name '*.py' | wc -l > /root/exp/file_count.txt
