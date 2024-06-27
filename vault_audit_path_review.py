#!/usr/bin/env python3

import json
import argparse
import logging
import sys
import os
from os import path, access
from EnvDefault import env_default
from itertools import islice

version = '0.0.1'

help_indent_formatter = lambda prog: argparse.RawTextHelpFormatter(
  prog,
  max_help_position=4, 
  indent_increment=2,
  width=80
)

if __name__ == '__main__':
  
  # parse arguments
  parser = argparse.ArgumentParser(
    formatter_class=help_indent_formatter,
    description = 'vault_audit_path_review.py provides a list of the top n paths accessed for a given secret engine mount as identified in the supplied Vault audit log.',
    epilog = "Example: \n" + 
             "vault_audit_path_review.py \\\n" + 
             "    --audit_log vault_audit.log.1 \\\n" +
             "    --secret_engine_mount secret \\\n" +
             "    --reporting_depth 6 \\\n" +
             "    --top 10"
  )

  parser.add_argument(
    '--audit_log', '-audit_log',
    action = env_default('AUDIT_LOG'),
    help = 'Audt log file',
    required = True,
  )

  parser.add_argument(
    '--reporting_depth', '-reporting_depth',
    action = env_default('REPORTING_DEPTH'),
    help = 'Reporting depth. Default: 6',
    default = '6',
    required = True,
  )

  parser.add_argument(
    '--secret_engine_mount', '-secret_engine_mount',
    action = env_default('SECRET_ENGINE_MOUNT'),
    help = 'Secret engine mount. Default: "secret"',
    default = 'secret',
    required = True,
  )

  parser.add_argument(
    '--top', '-top',
    help = 'Show only the top n paths. Default: -1',
    default = -1,
    required = False,
  )

  parser.add_argument(
    '--log_level', '-log_level',
    action = env_default('LOG_LEVEL'),
    help = 'Optional: Log level. Default: INFO.',
    choices = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
    required = False
  )

  parser.add_argument(
    '--version', '-version', '-v',
    help='Show version and exit.',
    action='version',
    version=f"{version}"
  )
  
  args = parser.parse_args()
  
  audit_log = args.audit_log
  reporting_depth = int(args.reporting_depth)
  secret_engine_mount = args.secret_engine_mount
  top = int(args.top)
  if top < -1:
    logging.error("top must be a positive integer")
    sys.exit(1)

  # logging
  format = "%(asctime)s: [%(levelname)s] %(message)s"
  date_format = "%Y-%m-%d %H:%M:%S %Z"
  logging.basicConfig(format=format, level=logging.INFO, datefmt=date_format)

  if args.log_level == 'CRITICAL':
    logging.getLogger().setLevel(logging.CRITICAL)
  elif args.log_level == 'ERROR':
    logging.getLogger().setLevel(logging.ERROR)
  elif args.log_level == 'WARNING':
    logging.getLogger().setLevel(logging.WARNING)
  elif args.log_level == 'INFO':
    logging.getLogger().setLevel(logging.INFO)
  elif args.log_level == 'DEBUG':
    logging.getLogger().setLevel(logging.DEBUG)
  
  # what are we doing here?
  logging.debug("Log level set to %s", args.log_level)
  logging.info("Starting %s", path.basename(__file__))
  logging.info("Audit log is: %s", audit_log)
  logging.info("Reporting depth is: %s", reporting_depth)
  logging.info("Secret engine mount is: %s", secret_engine_mount)
  logging.info("Show top n paths is: %s", top)

  # read json
  if access(audit_log, os.R_OK):
    logging.info("Able to read: %s", audit_log)
  else:
    logging.error("Unable to read: %s", audit_log)
    sys.exit(1)

  logging.info("Parsing audit log: %s", audit_log)

  audit_log_dict = {}
  audit_log_list = []
  #audit_log_csv = 

  with open(audit_log, 'r') as f:
    i = 0
    for line in f:
      i += 1
      audit_log_entry = json.loads(line)
      #logging.info("Audit log entry: ")
      if audit_log_entry['type'] == 'request':
        logging.debug("audit log entry is a request")
        logging.debug(json.dumps(audit_log_entry, indent=2))
        path = audit_log_entry['request']['path']
        #logging.info("Path is %s", path)
        #print(path)
        separator = '/'
        path_list = path.split(separator)
        if path_list[0] == secret_engine_mount:
          reporting_path = separator.join(path_list[slice(reporting_depth)])
          logging.debug(reporting_path)
          
          audit_log_dict[reporting_path] = audit_log_dict.get(reporting_path,0)+1
      else:
        if audit_log_entry['type'] == 'response':
          logging.debug("audit log entry is a response")
        else:
          logging.error("is a %s", audit_log_entry['type'])
          exit(1)
      if i == 10000:
        break
  f.close()

  if top > 0:
    print(json.dumps(dict(islice(
      {k: v for k, v in sorted(audit_log_dict.items(), key=lambda item: item[1], reverse=True)}.items()
      , top)), indent=2))
  else:
    print(json.dumps({k: v for k, v in sorted(audit_log_dict.items(), key=lambda item: item[1], reverse=True)}, indent=2))
  
  sys.exit(0)
