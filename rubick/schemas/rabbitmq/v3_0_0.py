from rubick.schema import ConfigSchemaRegistry

rabbitmq = ConfigSchemaRegistry.register_schema(project='rabbitmq')

with rabbitmq.version('3.0.0', checkpoint=True) as cfg:
    cfg.param(
        'tcp_listeners', type='rabbitmq_bind_list', default=[5672],
        description="List of ports on which to listen for AMQP connections (without SSL)")

    cfg.param(
        'ssl_listeners', type='rabbitmq_bind_list', default=[],
        description="List of ports on which to listen for AMQP connections (SSL)")

    cfg.param('ssl_options', type='string_list', default=[])

    cfg.param('vm_memory_high_watermark', type='float', default=0.4)

    cfg.param('vm_memory_high_watermark_paging_ratio',
              type='float', default=0.5)

    cfg.param('disk_free_limit', type='integer', default='50000000')
    cfg.param('log_levels', type='string_list', default=['{connection, info}'])
    cfg.param('frame_max', type='integer', default=131072)
    cfg.param('heartbeat', type='integer', default=600)
    cfg.param('default_vhost', type='string', default='/')
    cfg.param('default_user', type='string', default='guest')
    cfg.param('default_pass', type='string', default='guest')
