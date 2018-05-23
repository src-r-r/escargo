#!/usr/bin/env python3

from smtplib import (
    SMTP,
    LMTP,
    SMTP_SSL,
)

PROTOCOL_SMTP_SSL = 'smtp_ssl'
PROTOCOL_SMTP = 'smtp'
PROTOCOL_LMTP = 'lmtp'
CONN_PROTOCOLS = (PROTOCOL_SMTP, PROTOCOL_SMTP_SSL, PROTOCOL_LMTP)

def send_email(conn_host, conn_port,
               conn_protocol=PROTOCOL_SMTP,
               conn_source_address=None,
               conn_local_hostname=None,
               conn_timeout=None,
               smtp_ssl_keyfile=None,
               smtp_ssl_certfile=None,
               smtp_ssl_context=None,
               login_username=None,
               login_password=None,
               auth_mechanism=None,
               auth_object=None,
               auth_args=[],
               auth_initial_response_ok=True,
               starttls_keyfile=None,
               starttls_certfile=None,
               startls_context=None):
    assert conn_protocol in CONN_PROTOCOLS
    conn = None
    if conn_protocol == PROTOCOL_SMTP_SSL:
        conn = SMTP_SSL(host=conn_host, port=conn_port,
                        local_hostname=conn_local_hostname,
                        keyfile=smtp_ssl_keyfile,
                        certfile=smtp_ssl_certfile,
                        timeout=conn_timeout,
                        context=smtp_ssl_context,
                        source_address=conn_source_address)
    elif conn_protocol == PROTOCOL_SMTP:
        conn = SMTP(host=conn_host, conn_port,
                    local_hostname=conn_local_hostname,
                    timeout=conn_timeout,
                    source_address=conn_source_address)
    elif conn_protocol == PROTOCOL_
