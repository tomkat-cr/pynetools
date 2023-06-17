#!/bin/sh
#
# recycle_hosts_bkp.sh
# /etc/hosts backup recycling
# 2023-06-17 | CR
#
ERROR_MSG=""
cd "`dirname "$0"`" ;
SCRIPTS_DIR="`pwd`" ;

if [ "${ERROR_MSG}" = "" ]; then
	if [ -f "${SCRIPTS_DIR}/.env" ]; then
		echo "Processing ${SCRIPTS_DIR}/.env file..."
		set -o allexport;
		if ! . "${SCRIPTS_DIR}/.env"
		then
			ERROR_MSG="ERROR: could not process .env file."
		fi
		set +o allexport ;
	fi
fi

if [ "${ERROR}" = "" ]; then
	#######################################################
	# GENERAL PARAMETERS
	#######################################################
	source_bkp_pattern="${LOCAL_BACKUP_DIR}";
	par_mtime="${PAR_MTIME}";
	exclude_filenames_with="${EXCLUDE_FILENAMES_WITH}";
	date_time_part="`date +%Y-%m-%d`_`date +%H-%M`";
	#######################################################
	sw_only_report="1";
	if [ "$1" = "-deletion" ]; then
		sw_only_report="0";
	fi
	if [ "${source_bkp_pattern}" = "" ]; then
		source_bkp_pattern="/etc/hosts-*";
	fi
	if [ "${par_mtime}" = "" ]; then
		par_mtime="5";
	fi
	if [ "${exclude_filenames_with}" = "" ]; then
		exclude_filenames_with=".ocrcorp";
	fi
	#
	echo "/etc/hosts Backup Cleaning";
	echo "  Source: ${source_bkp_pattern}";
	echo "  Only Report=${sw_only_report}";
	echo "  Recycle files older than: ${par_mtime} days";
	echo "";
	echo "Files to be deleted today ${date_time_part}:";
	echo "";
    # Report files
    find ${source_bkp_pattern} -mtime +${par_mtime} ! -name *${exclude_filenames_with}* -exec ls -la {} \; ;
    if [ "${sw_only_report}" = "0" ]; then
        # Remove files
        echo "";
        echo "Deleting files...";
        echo "";
        find ${source_bkp_pattern} -mtime +${par_mtime} ! -name *${exclude_filenames_with}* -exec rm {} \; ;
    fi
fi

echo ""
if [ "${ERROR}" = "" ]; then
    echo "Done!"
else
    echo "${ERROR}"
fi
echo ""
