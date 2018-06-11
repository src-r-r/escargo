#!/usr/bin/env python3

import logging


from flask import (
    Flask,
    request,
    Response,
    jsonify,
)

from userless.models import (
    app,
    db,
)

import ssl

from smtplib import (
    SMTP,
    LMTP,
    SMTP_SSL,
)

from email.messgae import (
    EmailMessage
)

from tempfile import (
    NamedTemporaryFile,
)


log = logging.getLogger(__name__)


def write_temp(content):
    """ Write content to a named temporary file.

    :param content: Content to write to a file.

    :return: handle to a NamedTemporaryFile
    """
    tmp_file = NamedTemporaryFile()
    with open(tmp_file, 'w+') as f:
        f.write(content)
    return tmp_file


def write_temp_if_in(data, key, content=None):
    """ Create a temp file only if `key` is in `data`

    :param data: dictionary data.

    :param key: Key to look for in `data`

    :param content: content for the file. If ommitted, defalt to data[key]

    :return: Named temporary file if content is given. `None` otherwise.
    """
    if key not in data:
        return None
    return write_temp(content or data[key])


@app.route('/', methods='POST')
def send_email():
    """ Send an email semi-easily.

    ..

    request:
        method: POST
        mimetype: application/json
        files:
            description: Any attachments to add to the email.
        body:
            'connection':
                'conn_type':
                    type: string
                    description: type of connection
                    choices:
                        - 'smtp'
                        - 'smtp_ssl'
                        - 'lmtp'
                    default: 'smtp'
                'host':
                    type: string
                    required_for: smtp, smtp_ssl, lmtp
                'port':
                    type: int
                    required_for: smtp, smtp_ssl, lmtp
                'local_hostname':
                    type: string
                    optional_for: smtp, smtp_ssl, lmtp
                'source_address':
                    type: string
                    optional_for: smtp, smtp_ssl, lmtp
                'ssl_context':
                    type: dict.
                    'description':
                        `certfile` and `keyfile` will be
                        loaded into a temporary file for passing in to
                        SSLContext.load_cert_chain. If `certificate` is an
                        empty dict but still given, then the default SSL
                        context from the serve will be loaded.
                    optional_for: smtp_ssl
                    body:
                        'cert':
                            type: string
                            description: contents of the cert file
                        'key':
                            type: string
                            description: contents of the key file
                            optional: yes
                        'password':
                            type: string
                            optional: yes
                'timeout':
                    type: int
                    optional_for: smtp, smtp_ssl
            'options':
                'debug_level':
                    type: int
                    description: 1 or 2
                'helo':
                    type: str
                    description: name for `HELO`
                    optional: true
                'ehlo':
                    type: str
                    description: name for `EHLO`
                'verify':
                    type: str
                    description:
                        address on the server to verify. In this case a
                        message will not be sent, and, instead, a status code
                        wil be returned.
                'login':
                    type: dict
                    description:
                        login credentials. If ommited will not be used.
                    body:
                        'user':
                            type: str
                            description: user to log in.
                        'password':
                            type: str
                            description: password for the site.
                'auth':
                    type: dict
                    description:
                        authentication object TODO
                'starttls':
                    type: dict
                    description:
                        start the StartTLS connection
                    body:
                        'key':
                            type: string
                            description:
                                contents of key file
                            optional: yes
                        'cert':
                            type: string
                            description:
                                contents of cert file
            'sending':
                type: dict
                required: true
                body:
                    'from':
                        type: string
                        required: true
                        description:
                            sender's email address
                    'to':
                        type: string
                        required: true
                        description:
                            recipient's address
                    'message':
                        type: dict
                        required: true
                        body:
                            'headers':
                                type: dict
                                body:
                                    'Subject':
                                        type: string
                                        description: subject of message
                                    'From':
                                        type: string
                                        description: optional "from" field.
                                    'To':
                                        type: string
                                        description: optional 'to' field.
                            'text_body':
                                type: string
                                description: text body of message
                            'html_body':
                                type: string
                                description HTML body of message.
                            'attachments':
                                type: list of dicts
                                description:
                                    each dict contains the keys 'name',
                                    'mimetype', 'subtype', correspondiing
                                    to the name associted with the file and
                                    target email's mimetype, subtype,
                    'mail_options':
                        type: dict
    """
    body = request.get_json()

    conn_data = body['connection']
    send_data = body['sending']
    options_data = body.get('options')

    conn_type = conn_data['type'].lower()
    host = conn_data['host']
    port = int(conn_data['port'])
    local_hostname = conn_data.get('local_hostname')
    source_address = conn_data.get('source_address')
    certificate_data = conn_data.get('certificate', None)
    # key_data = conn_data.get('key', None)
    timeout = conn_data.get('timeout')

    debug_level = int(options_data.get('debug_level', 0))
    helo = options_data.get('helo')
    ehlo = options_data.get('ehlo')
    verify = options_data.get('verify')
    login = options_data.get('login')
    starttls = options_data.get('starttls')

    assert conn_type in ('smtp', 'smtp_ssl', 'lmtp')

    log.debug('connection type is [{}]'.format(conn_type.upper()))

    if conn_type == 'smtp':
        conn = SMTP(host=host, port=port, local_hostname=local_hostname,
                    timeout=timeout, source_address=source_address)

    elif conn_type == 'smtp_ssl':
        keyfile = write_temp_if_in(certificate_data, 'keyfile')
        certfile = write_temp_if_in(certificate_data, 'certfile')
        cert_pw = certificate_data.get('password', None)
        ssl_context = None
        if 'certificate' in conn_data:
            ssl_context = ssl.create_default_context()
            if certfile:
                ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile,
                                            password=cert_pw)
            else:
                ssl_context.load_default_certs()
        conn = SMTP_SSL(host=host, port=port, local_hostname=local_hostname,
                        context=ssl_context, source_address=source_address)

    elif conn_type == 'lmtp':
        conn = SMTP_SSL(host=host, port=port, local_hostname=local_hostname,
                        source_address=source_address)

    # Configure options
    if debug_level:
        log.debug('set debug_level={}'.format(debug_level))
        conn.set_debuglevel(debug_level)

    if login:
        log.debug('trying login with user={}'.format(login['user']))
        conn.login(login['user'], login['password'],
                   login['initial_response_ok'])

    if starttls:
        log.debug('initializing STARTTLS')
        keyfile = None
        certfile = None
        if starttls.get('key'):
            keyfile = NamedTemporaryFile()
        if starttls.get('cert'):
            certfile = NamedTemporaryFile()
        log.debug('STARTLS keyfile={}, certfile={}'.format(keyfile.name,
                                                           certfile.name))
        conn.starttls(keyfile=keyfile.name, certfile=certfile.name)

    # If the user just wants to verify, return the result of SMTP.verify()
    if verify:
        log.debug('simply verifying {}'.format(verify))
        (code, message) = conn.verify(verify)
        if code == 404:
            return jsonify({
                'error': {
                    'code': code,
                    'message': message,
                }
            })
        else:
            return jsonify({
                'result': {
                    'code': code,
                    'address': message,
                }
            })

    # Construct the message
    message_data = send_data['message']
    message = EmailMessage()
    for (k, v) in message_data.get('headers', {}):
        message[k] = v
    message.set_content(message_data['text_body'])
    if 'html_body' in message_data:
        message.add_alternative(message_data['html_body'], subtype='html')
    for (name, file) in request.files:
        with open(file) as to_attach:
            message.get_payload()[1].add_related(to_attach.read)

    conn.sendmail(from_addr=send_data['from'], to_addrs=send_data['to'],
                  msg=message)
