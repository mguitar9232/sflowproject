#!/bin/bash

USER="testuser"
PASSWORD="password"
DATABASE="pmacct"

TODAY=$(date +%Y%m%d)
echo "$TODAY"

echo "acct_$TODAY"

JOB_QUERY="insert into acct_ifacelist ( select current_date(),a.iface_out, IFNULL(a.iface_out_as, a.iface_out), IFNULL(display_yn, 'Y') from ( select iface_out, iface_out_as, display_yn  FROM acct_ifacelist WHERE date_time = ( select max(date_time) from acct_ifacelist  where date_time >= date_add(current_date(), interval -10 day) ) union ALL SELECT iface_out, '', '' FROM acct_$TODAY WHERE timestamp_start >= date_add(now(), interval -1 minute) AND iface_out != 0   AND net_dst != '0.0.0.0' AND as_dst != 0 GROUP BY iface_out ) a group by a.iface_out );"


JOB_COMMIT="commit;"

# STEP 1
#/usr/bin/mysql --user="$USER" --password="$PASSWORD" --database="$DATABASE" --execute="$JOB1_QUERY"

# STEP 2
/usr/bin/mysql --user="$USER" --password="$PASSWORD" --database="$DATABASE" --execute="$JOB_QUERY"

# STEP 3
/usr/bin/mysql --user="$USER" --password="$PASSWORD" --database="$DATABASE" --execute="$JOB_COMMIT"
