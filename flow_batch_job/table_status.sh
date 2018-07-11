#!/bin/bash

USER="testuser"
PASSWORD="password"
DATABASE="pmacct"

JOB_QUERY="show table status"

/usr/bin/mysql --user="$USER" --password="$PASSWORD" --database="$DATABASE" --execute="$JOB_QUERY"
