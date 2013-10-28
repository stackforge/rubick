from rubick.schema import ConfigSchemaRegistry

swift = ConfigSchemaRegistry.register_schema(project='swift')

with swift.version('2013.2') as swift_2013_2:

    swift_2013_2.section('swift-hash')

    swift_2013_2.param('swift_hash_path_suffix',
                       type='string', default='changeme', description="")

    swift_2013_2.param('swift_hash_path_prefix',
                       type='string', default='changeme', description="")

    swift_2013_2.section('swift-constraints')

    swift_2013_2.param(
        'max_file_size', type='string', default='5368709122', description="")

    swift_2013_2.param('max_meta_name_length',
                       type='string', default='128', description="")

    swift_2013_2.param('max_meta_value_length',
                       type='string', default='256', description="")

    swift_2013_2.param(
        'max_meta_count', type='string', default='90', description="")

    swift_2013_2.param('max_meta_overall_size',
                       type='string', default='4096', description="")

    swift_2013_2.param(
        'max_header_size', type='string', default='8192', description="")

    swift_2013_2.param('max_object_name_length',
                       type='string', default='1024', description="")

    swift_2013_2.param('container_listing_limit',
                       type='string', default='10000', description="")

    swift_2013_2.param('account_listing_limit', type='string', default='10000',
                       description="account_listing_limit is the default "
                                   "(and max) number of items returned for an "
                                   "account listing request")

    swift_2013_2.param('max_account_name_length',
                       type='string', default='256', description="")

    swift_2013_2.param('max_container_name_length',
                       type='string', default='256', description="")
