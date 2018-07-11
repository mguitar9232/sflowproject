#!/bin/bash

WTIME=`date +%Y%m%d-%H%M%S`
#echo $WTIME

REST_MEMORY_SIZE=`free -m | awk '{print $4}' | tail -n 2 | head -1`

############################
# function : email_send()
############################
email_send() {
        echo | mutt  -s "[RXN_SERVER-MEMORY-WARN]192.168.1.1(${WTIME})" testtest@gmail.com -c testtest@gmail.com -i /opt/flow_batch_job/mail_body2
}

############################
# function : proc_restart()
############################
proc_restart() {
        echo "process kill and restart";

        if [ "" !=  "$ASR_PID" ]; then
                echo "killing $ASR_PID";
                /bin/kill -9 $ASR_PID
        fi

        #ASR_CHECK_PID=`ps -ef | grep "xxxxxx -Dvertx" | grep -v grep | awk '{print $2}'`

        #if [ "" ==  "$ASR_CHECK_PID" ]; then
        #        echo "Process Not Found :: Start ASR Process";

        #       #cd /data/asr_srv/bin
        #        #/data/asr_srv/bin/vertx runmod com.systran~asr~3.87.00-final -conf /data/asr_srv/conf/conf.json
        #fi
}

if [ $# -eq 0 ]; then
        echo "";
        echo "Please... Input Arguments!!";
        echo "=========================================================";
        echo "Usage:";
        echo "  option : 0 - just mail send"
        echo "  option : 1 - mail send & process ( job )";
        echo "=========================================================";
        exit
fi

if [ $1 -eq 0 ]; then
        echo "Just Email Send Option"

        if [ $REST_MEMORY_SIZE < 200 ]; then
				rm -f /opt/flow_batch_job/mail_body2
				cp /opt/flow_batch_job/mail_body /opt/flow_batch_job/mail_body2
				echo "======================================================================================" >> /opt/flow_batch_job/mail_body2
                free -m >> /opt/flow_batch_job/mail_body2
                echo $REST_MEMORY_SIZE
                echo "MEMORY SIZE WARNNING"
                echo "CURRENT MEMORY SIZE is $REST_MEMORY_SIZE"
        else
                echo $PCHECK_NUM
                echo "SERVER NOT ACTIVE"
                echo "Email Send";
                email_send
        fi
elif [ $1 -eq 1 ]; then
        echo "Email Send & restart Process Option";

        if [ $PCHECK_NUM -eq 1 ]; then
                echo $PCHECK_NUM
                echo "STATUS SUCCESS"
        else
                echo  "###### RESTART #######"
                echo $PCHECK_NUM
                echo "SERVER NOT ACTIVE"
                echo "Process Restart";
                proc_restart
                echo "Email Send";
                email_send
        fi
else
        echo "ELSE";
fi

