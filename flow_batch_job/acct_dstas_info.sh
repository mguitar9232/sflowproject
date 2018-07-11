#!/bin/bash

USER="testuser"
PASSWORD="password"
DATABASE="pmacct"

TODAY=$(date +%Y%m%d)
echo "$TODAY"

echo "acct_$TODAY"

JOB_QUERY="insert into acct_dstas_info ( as_dst, as_dst_name ) (select as_dst, NULL from pmacct.acct_$TODAY where net_dst != '0.0.0.0' and as_dst != 0 group by as_dst);"
  
JOB_COMMIT="commit;"

# STEP 1
/usr/bin/mysql --user="$USER" --password="$PASSWORD" --database="$DATABASE" --execute="$JOB_QUERY"

# STEP 2
/usr/bin/mysql --user="$USER" --password="$PASSWORD" --database="$DATABASE" --execute="$JOB_COMMIT"
