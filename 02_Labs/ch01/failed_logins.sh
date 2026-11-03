#!/usr/bin/env bash
set -euo pipefail
file="${1:?usage: $0 logfile [threshold]}"
threshold="${2:-5}"
grep "Failed password" "$file" | awk '{print $11}' | sort | uniq -c | sort -rn |
while read -r count ip; do
  if [ "$count" -ge "$threshold" ]; then
    echo "ALERT: $ip had $count failed logins"
  fi
done
