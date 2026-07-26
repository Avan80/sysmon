# sysmon
 
A lightweight Linux systems monitor. A Python service polls host metrics (CPU, memory, disk, network) every 30 seconds, writes them as JSON lines to a local log file, and separately logs any threshold breaches. On AWS, infrastructure is provisioned via Terraform and the CloudWatch Agent ships both logs to CloudWatch Logs.
 
## How it works
 
1. **`systems_monitor.py`** loops forever. Every 30s it collects a metrics snapshot via `psutil` and appends it as one JSON line to `metrics.log`. It also checks each snapshot against fixed thresholds and logs any breach to `warn.log`.
2. **`sysmon.service`** (systemd unit) runs the script as a dedicated unprivileged `sysmon` user, restarting it on failure.
3. **Terraform** (`terraform/`) provisions an EC2 instance, IAM role, and security group. `user_data.sh` runs once at boot: installs dependencies, creates the `sysmon` user, clones this repo, installs the CloudWatch Agent, and starts the service.
4. **The CloudWatch Agent** tails `metrics.log` and `warn.log` and ships both to the `sysmon/metrics` log group in CloudWatch Logs, with per-instance log streams.
5. **CI** (GitHub Actions) lints with ruff, runs the pytest suite, and validates the Terraform on every push/PR to `master`.
## Thresholds

CPU usage > 80% 
Memory used > 90%
Swap used > 35% 
Disk usage (per mount) > 80% 
Network errors / drops > 0 
 
## Repo layout
 
```
systems_monitor.py     # the monitor itself
sysmon.service          # systemd unit
cw-agent.json            # CloudWatch Agent config
requirements.txt        # psutil, ruff, boto3
Dockerfile               # containerized run (local/dev use)
pytest.ini
tests/test_smoke.py     # unit tests for metrics() and check_thresholds()
terraform/
  main.tf                # EC2 instance, IAM role, security group
  user_data.sh           # instance bootstrap script
.github/workflows/ci.yml
```
 
## Running locally
 
**Directly:**
```bash
pip install -r requirements.txt
python3 systems_monitor.py
```
Logs go to `/var/log/sysmon/` by default, or set `SYSMON_LOG_DIR` to override.
 
**Via Docker:**
```bash
docker build -t sysmon .
docker run sysmon
```
 
## Deploying to AWS
 
Requires an AWS CLI profile named `sysmon-test` and an existing EC2 key pair named `sysmon-key`.
 
```bash
cd terraform/
terraform init
terraform apply
```
 
This provisions a `t3.micro` EC2 instance running Ubuntu 24.04. The security group only allows SSH from the IP you apply from (auto-detected at apply time). Once up:
 
```bash
terraform output instance_public_ip
ssh -i <path_to_sysmon-key.pem> ubuntu@<instance_public_ip>
```
 
The service starts automatically via `user_data.sh` on boot, bit `apply` finishes before connecting.
 
## Testing
 
```bash
pip install -r requirements.txt pytest
PYTHONPATH=. pytest tests/
```
 
## Design decisions
 
- **CloudWatch Agent over boto3-in-script**: the agent tails local log files independently of the monitor process, so log shipping doesn't share fate with the collector loop.
- **Dedicated `sysmon` system user**: the service runs without privilages, not as root, to limit blast radius if the process or a dependency is ever compromised. See [RUNBOOK.md](RUNBOOK.md) for details on why this matters and how it's enforced.
- **Single `main.tf`**: infrastructure is small enough that splitting into multiple files isn't worth the indirection yet.
## Known issues / in progress
 
See [RUNBOOK.md](RUNBOOK.md) for current known issues, troubleshooting steps, and operational notes.
