# Escargo

Escargo is a zero-configuration REST API for email. Just spin up the vagrant
machine and you can being sending email easily using the endpoint.

# Installation

Firstly, ensure [Vagrant is installed](https://www.vagrantup.com/docs/installation/).

# Endpoint

There's really only 1 endpoint for this service:

    POST /

However, the power of the request comes from the JSON data in the POST. Since
each email server is different, there are are a lot of configuration options.
It's recommended to keep the configuration in a file, and pass it in with the
rest of the request.

Documetation copied from the source:

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

# Testing

In order to test, we'll need to spin up at least 2 vagrant instances.
