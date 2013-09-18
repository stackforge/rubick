from ostack_validator.schema import ConfigSchemaRegistry

keystone = ConfigSchemaRegistry.register_schema(project='keystone')

keystone.version('2013.1.3')

keystone.section('DEFAULT')

keystone.section('sql')

keystone.section('identity')

keystone.section('trust')

keystone.section('catalog')

keystone.section('token')

keystone.section('policy')

keystone.section('ec2')

keystone.section('ssl')

keystone.param('enable ', type='string', default=' True')

keystone.param('certfile ', type='string', default=' /etc/keystone/ssl/certs/keystone.pem')

keystone.param('keyfile ', type='string', default=' /etc/keystone/ssl/private/keystonekey.pem')

keystone.param('ca_certs ', type='string', default=' /etc/keystone/ssl/certs/ca.pem')

keystone.param('cert_required ', type='string', default=' True')

keystone.section('signing')

keystone.param('token_format ', type='string', default=' PKI')

keystone.param('certfile ', type='string', default=' /etc/keystone/ssl/certs/signing_cert.pem')

keystone.param('keyfile ', type='string', default=' /etc/keystone/ssl/private/signing_key.pem')

keystone.param('ca_certs ', type='string', default=' /etc/keystone/ssl/certs/ca.pem')

keystone.param('key_size ', type='string', default=' 1024')

keystone.param('valid_days ', type='string', default=' 3650')

keystone.param('ca_password ', type='string', default=' None')

keystone.section('ldap')

keystone.section('auth')

keystone.param('methods ', type='string', default=' password,token')

keystone.param('password ', type='string', default=' keystone.auth.plugins.password.Password')

keystone.param('token ', type='string', default=' keystone.auth.plugins.token.Token')

keystone.section('filter:debug')

keystone.param('paste.filter_factory ', type='string', default=' keystone.common.wsgi:Debug.factory')

keystone.section('filter:token_auth')

keystone.param('paste.filter_factory ', type='string', default=' keystone.middleware:TokenAuthMiddleware.factory')

keystone.section('filter:admin_token_auth')

keystone.param('paste.filter_factory ', type='string', default=' keystone.middleware:AdminTokenAuthMiddleware.factory')

keystone.section('filter:xml_body')

keystone.param('paste.filter_factory ', type='string', default=' keystone.middleware:XmlBodyMiddleware.factory')

keystone.section('filter:json_body')

keystone.param('paste.filter_factory ', type='string', default=' keystone.middleware:JsonBodyMiddleware.factory')

keystone.section('filter:user_crud_extension')

keystone.param('paste.filter_factory ', type='string', default=' keystone.contrib.user_crud:CrudExtension.factory')

keystone.section('filter:crud_extension')

keystone.param('paste.filter_factory ', type='string', default=' keystone.contrib.admin_crud:CrudExtension.factory')

keystone.section('filter:ec2_extension')

keystone.param('paste.filter_factory ', type='string', default=' keystone.contrib.ec2:Ec2Extension.factory')

keystone.section('filter:s3_extension')

keystone.param('paste.filter_factory ', type='string', default=' keystone.contrib.s3:S3Extension.factory')

keystone.section('filter:url_normalize')

keystone.param('paste.filter_factory ', type='string', default=' keystone.middleware:NormalizingFilter.factory')

keystone.section('filter:sizelimit')

keystone.param('paste.filter_factory ', type='string', default=' keystone.middleware:RequestBodySizeLimiter.factory')

keystone.section('filter:stats_monitoring')

keystone.param('paste.filter_factory ', type='string', default=' keystone.contrib.stats:StatsMiddleware.factory')

keystone.section('filter:stats_reporting')

keystone.param('paste.filter_factory ', type='string', default=' keystone.contrib.stats:StatsExtension.factory')

keystone.section('filter:access_log')

keystone.param('paste.filter_factory ', type='string', default=' keystone.contrib.access:AccessLogMiddleware.factory')

keystone.section('app:public_service')

keystone.param('paste.app_factory ', type='string', default=' keystone.service:public_app_factory')

keystone.section('app:service_v3')

keystone.param('paste.app_factory ', type='string', default=' keystone.service:v3_app_factory')

keystone.section('app:admin_service')

keystone.param('paste.app_factory ', type='string', default=' keystone.service:admin_app_factory')

keystone.section('pipeline:public_api')

keystone.param('pipeline ', type='string', default=' access_log sizelimit stats_monitoring url_normalize token_auth admin_token_auth xml_body json_body debug ec2_extension user_crud_extension public_service')

keystone.section('pipeline:admin_api')

keystone.param('pipeline ', type='string', default=' access_log sizelimit stats_monitoring url_normalize token_auth admin_token_auth xml_body json_body debug stats_reporting ec2_extension s3_extension crud_extension admin_service')

keystone.section('pipeline:api_v3')

keystone.param('pipeline ', type='string', default=' access_log sizelimit stats_monitoring url_normalize token_auth admin_token_auth xml_body json_body debug stats_reporting ec2_extension s3_extension service_v3')

keystone.section('app:public_version_service')

keystone.param('paste.app_factory ', type='string', default=' keystone.service:public_version_app_factory')

keystone.section('app:admin_version_service')

keystone.param('paste.app_factory ', type='string', default=' keystone.service:admin_version_app_factory')

keystone.section('pipeline:public_version_api')

keystone.param('pipeline ', type='string', default=' access_log sizelimit stats_monitoring url_normalize xml_body public_version_service')

keystone.section('pipeline:admin_version_api')

keystone.param('pipeline ', type='string', default=' access_log sizelimit stats_monitoring url_normalize xml_body admin_version_service')

keystone.section('composite:main')

keystone.param('use ', type='string', default=' egg:Paste#urlmap')

keystone.param('/v2.0 ', type='string', default=' public_api')

keystone.param('/v3 ', type='string', default=' api_v3')

keystone.param('/ ', type='string', default=' public_version_api')

keystone.section('composite:admin')

keystone.param('use ', type='string', default=' egg:Paste#urlmap')

keystone.param('/v2.0 ', type='string', default=' admin_api')

keystone.param('/v3 ', type='string', default=' api_v3')

keystone.param('/ ', type='string', default=' admin_version_api')

