#! /bin/bash

export MAIL_PASSWORD=''
export DB_PASSWORD='jrg123'
export TWILIO_SID='AC891972f21eee99d4ed3d325d7528bb53'
export TWILIO_TOKEN='7785a4fc12c49736eacfdd769d6291d5'
source ../env/bin/activate

python devicetableupdate.py

