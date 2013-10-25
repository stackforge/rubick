from rubick.schema import ConfigSchemaRegistry

keystone = ConfigSchemaRegistry.register_schema(project='keystone')

with keystone.version('2013.1.4') as keystone_2013_1_4:

    keystone_2013_1_4.section('ssl')

    keystone_2013_1_4.param('enable', type='boolean', default=True)

    keystone_2013_1_4.param('certfile', type='string',
                            default='/etc/keystone/pki/certs/ssl_cert.pem')

    keystone_2013_1_4.param('keyfile', type='string',
                            default='/etc/keystone/pki/private/ssl_key.pem')

    keystone_2013_1_4.param('ca_certs', type='string',
                            default='/etc/keystone/pki/certs/cacert.pem')

    keystone_2013_1_4.param('ca_key', type='string',
                            default='/etc/keystone/pki/private/cakey.pem')

    keystone_2013_1_4.param('key_size', type='integer', default=1024)

    keystone_2013_1_4.param('valid_days', type='integer', default=3650)

    keystone_2013_1_4.param('cert_required', type='boolean', default=False)

    keystone_2013_1_4.param('cert_subject', type='string',
                            default='/CUS/STUnset/LUnset/OUnset/CNlocalhost')

    keystone_2013_1_4.section('signing')

    keystone_2013_1_4.param(
        'token_format', type='string', default='',
        description="Deprecated in favor of provider in the [token] "
        "section Allowed values are PKI or UUID")

    keystone_2013_1_4.param('certfile', type='string',
                            default='/etc/keystone/pki/certs/signing_cert.pem')

    keystone_2013_1_4.param(
        'keyfile', type='string',
        default='/etc/keystone/pki/private/signing_key.pem')

    keystone_2013_1_4.param('ca_certs', type='string',
                            default='/etc/keystone/pki/certs/cacert.pem')

    keystone_2013_1_4.param('ca_key', type='string',
                            default='/etc/keystone/pki/private/cakey.pem')

    keystone_2013_1_4.param('key_size', type='integer', default=2048)

    keystone_2013_1_4.param('valid_days', type='integer', default=3650)

    keystone_2013_1_4.param(
        'cert_subject', type='string',
        default='/CUS/STUnset/LUnset/OUnset/CNwww.example.com')

    keystone_2013_1_4.section('auth')

    keystone_2013_1_4.param('methods', type='string',
                            default='external,password,token,oauth1')

    keystone_2013_1_4.param(
        'external', type='string',
        default='keystone_2013_1_4.auth.plugins.external.ExternalDefault')

    keystone_2013_1_4.param(
        'password', type='string',
        default='keystone_2013_1_4.auth.plugins.password.Password')

    keystone_2013_1_4.param(
        'token', type='string',
        default='keystone_2013_1_4.auth.plugins.token.Token')

    keystone_2013_1_4.param(
        'oauth1', type='string',
        default='keystone_2013_1_4.auth.plugins.oauth1.OAuth')

    keystone_2013_1_4.section('paste_deploy')

    keystone_2013_1_4.param(
        'config_file', type='string',
        default='keystone-paste.ini',
        description="Name of the paste configuration file that defines "
        "the available pipelines")
