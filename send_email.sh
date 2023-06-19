#!/bin/sh
#
# send_email.sh
# 2023-06-18 | CR
#
ERROR_MSG=""
cd "`dirname "$0"`" ;
SCRIPTS_DIR="`pwd`" ;

if [ "${ERROR_MSG}" = "" ]; then
	if [ -f "${SCRIPTS_DIR}/.env" ]; then
		# echo "Processing ${SCRIPTS_DIR}/.env file..."
		set -o allexport;
		if ! . "${SCRIPTS_DIR}/.env"
		then
			ERROR_MSG="ERROR: could not process .env file."
		fi
		set +o allexport ;
	fi
fi

if [ "${ERROR}" = "" ]; then
	if ! python3 -m src.send_email $1 $2 $3 $4 $5 $6 $7 $8 $9${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} ${18} ${19} ${20} ${21} ${22} ${23} ${24} ${25} ${26} ${27} ${28} ${29} ${30}
	then
		ERROR="ERROR: running send_email module."
	fi
fi

echo ""
if [ "${ERROR}" = "" ]; then
    echo "Done!"
else
    echo "${ERROR}"
fi
echo ""
