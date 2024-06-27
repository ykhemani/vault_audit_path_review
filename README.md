# vault_audit_path_review.py

## Description
[vault_audit_path_review.py](vault_audit_path_review.py) allows you to interrogate a [Vault](https://vaultproject.io) [audit log](https://developer.hashicorp.com/vault/docs/audit) to determine the frequency of interactions with secrets at a specified secret engine mount.

## Prerequisites

* [Python 3](https://www.python.org/) - this script was tested against Python 3.12.3.
* Vault audit log file.

## Usage

```
usage: vault_audit_path_review.py [-h] --audit_log AUDIT_LOG
                                  [--reporting_depth REPORTING_DEPTH]
                                  [--secret_engine_mount SECRET_ENGINE_MOUNT]
                                  [--top TOP]
                                  [--log_level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
                                  [--version]

vault_audit_path_review.py provides a list of the top n paths accessed for a given secret engine mount as identified in the supplied Vault audit log.

options:
  -h, --help
    show this help message and exit
  --audit_log AUDIT_LOG, -audit_log AUDIT_LOG
    Audt log file
  --reporting_depth REPORTING_DEPTH, -reporting_depth REPORTING_DEPTH
    Reporting depth. Default: 6
  --secret_engine_mount SECRET_ENGINE_MOUNT, -secret_engine_mount SECRET_ENGINE_MOUNT
    Secret engine mount. Default: "secret"
  --top TOP, -top TOP
    Show only the top n paths. Default: -1
  --log_level {CRITICAL,ERROR,WARNING,INFO,DEBUG}, -log_level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
    Optional: Log level. Default: INFO.
  --version, -version, -v
    Show version and exit.

Example: 
vault_audit_path_review.py \
    --audit_log vault_audit.log.1 \
    --secret_engine_mount secret \
    --reporting_depth 6 \
    --top 10
```

### Required flags
Use the `audit_log` flag to specify the path to the Vault audit log to interrogate.

### Optional flags
Use the `secret_engine_mount` flag to specify the secret engine mount. Defaults to `secret`.

Use the `reporting_depth` flag to specify reporting depth of the path to the secret. This will be determinted by how you structure secrets at the specified secret engine mount.

Use the `top` flag to specify the top number of paths to output. Should be a positive integer if specified. Defaults to `-1`, which will show all matches.

### Example output

```
$ ./vault_audit_path_review.py --audit_log audit.log --secret_engine_mount vault-ca-imported -top 5
2024-06-27 18:59:08 UTC: [INFO] Starting vault_audit_path_review.py
2024-06-27 18:59:08 UTC: [INFO] Audit log is: audit.log
2024-06-27 18:59:08 UTC: [INFO] Reporting depth is: 6
2024-06-27 18:59:08 UTC: [INFO] Secret engine mount is: vault-ca-imported
2024-06-27 18:59:08 UTC: [INFO] Show top n paths is: 5
2024-06-27 18:59:08 UTC: [INFO] Able to read: audit.log
2024-06-27 18:59:08 UTC: [INFO] Parsing audit log: audit.log
{
  "vault-ca-imported/issue/demo.example.com": 25,
  "vault-ca-imported/config/urls": 2,
  "vault-ca-imported/config/ca": 1,
  "vault-ca-imported/roles/demo.example.com": 1,
  "vault-ca-imported/roles/": 1
}
```

```
$ ./vault_audit_path_review.py --audit_log audit.log --secret_engine_mount mysql-demo
2024-06-27 19:06:57 UTC: [INFO] Starting vault_audit_path_review.py
2024-06-27 19:06:57 UTC: [INFO] Audit log is: audit.log
2024-06-27 19:06:57 UTC: [INFO] Reporting depth is: 6
2024-06-27 19:06:57 UTC: [INFO] Secret engine mount is: mysql-demo
2024-06-27 19:06:57 UTC: [INFO] Show top n paths is: -1
2024-06-27 19:06:57 UTC: [INFO] Able to read: audit.log
2024-06-27 19:06:57 UTC: [INFO] Parsing audit log: audit.log
{
  "mysql-demo/creds/demo-web-role": 133,
  "mysql-demo/creds/demo-dba-role": 34,
  "mysql-demo/config/demodb": 1,
  "mysql-demo/roles/mysql-web-role": 1
}
```
