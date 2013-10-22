from rubick.schema import ConfigSchemaRegistry

keystone = ConfigSchemaRegistry.register_schema(project='keystone')

keystone.version('2013.1.4')

keystone.section('DEFAULT')

keystone.section('sql')

keystone.section('identity')

keystone.section('credential')

keystone.section('trust')

keystone.section('os_inherit')

keystone.section('catalog')

keystone.section('endpoint_filter')

keystone.section('token')

keystone.section('cache')

keystone.section('policy')

keystone.section('ec2')

keystone.section('assignment')

keystone.section('oauth1')

keystone.section('ssl')

keystone.param('enable', type='string', default='True', description="")

keystone.param('certfile', type='string',
               default='/etc/keystone/pki/certs/ssl_cert.pem', description="")

keystone.param('keyfile', type='string',
               default='/etc/keystone/pki/private/ssl_key.pem', description="")

keystone.param('ca_certs', type='string',
               default='/etc/keystone/pki/certs/cacert.pem', description="")

keystone.param('ca_key', type='string',
               default='/etc/keystone/pki/private/cakey.pem', description="")

keystone.param('key_size', type='string', default='1024', description="")

keystone.param('valid_days', type='string', default='3650', description="")

keystone.param('cert_required', type='string', default='False', description="")

keystone.param('cert_subject', type='string',
               default='/CUS/STUnset/LUnset/OUnset/CNlocalhost',
               description="")

keystone.section('signing')

keystone.param('token_format', type='string', default='',
               description="Deprecated in favor of provider in the [token] "
                           "section Allowed values are PKI or UUID")

keystone.param('certfile', type='string',
               default='/etc/keystone/pki/certs/signing_cert.pem',
               description="")

keystone.param('keyfile', type='string',
               default='/etc/keystone/pki/private/signing_key.pem',
               description="")

keystone.param('ca_certs', type='string',
               default='/etc/keystone/pki/certs/cacert.pem', description="")

keystone.param('ca_key', type='string',
               default='/etc/keystone/pki/private/cakey.pem', description="")

keystone.param('key_size', type='string', default='2048', description="")

keystone.param('valid_days', type='string', default='3650', description="")

keystone.param('cert_subject', type='string',
               default='/CUS/STUnset/LUnset/OUnset/CNwww.example.com',
               description="")

keystone.section('ldap')

keystone.section('auth')

keystone.param('methods', type='string',
               default='external,password,token,oauth1', description="")

keystone.param('external', type='string',
               default='keystone.auth.plugins.external.ExternalDefault',
               description="")

keystone.param('password', type='string',
               default='keystone.auth.plugins.password.Password',
               description="")

keystone.param('token', type='string',
               default='keystone.auth.plugins.token.Token', description="")

keystone.param('oauth1', type='string',
               default='keystone.auth.plugins.oauth1.OAuth', description="")

keystone.section('paste_deploy')

keystone.param('config_file', type='string', default='keystone-paste.ini',
               description="Name of the paste configuration file that defines "
                           "the available pipelines")

keystone.commit()
