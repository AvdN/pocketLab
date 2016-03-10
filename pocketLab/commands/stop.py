__author__ = 'rcj1492'
__created__ = '2016.03'

_cmd_details_stop = {
    'command': 'stop',
    'usage': 'stop [options]',
    'description': 'terminates container running a project component',
    'brief': 'terminates container running a project component',
    'defaults': { },
    'options': [
        {   'args': [ '-a', '--alias' ],
            'kwargs': {
                'type': str,
                'default': '',
                'metavar': 'ALIAS',
                'dest': 'containerAlias',
                'help': 'name of container ALIAS (default: "container_alias" value in local lab-component.json)'
            }
        },
        {   'args': [ '-b', '--box' ],
            'kwargs': {
                'type': str,
                'default': 'default',
                'metavar': 'VBOX',
                'dest': 'virtualbox',
                'help': 'name of docker virtualbox (default: %(default)s)' }
        }
    ]
}

def stop(**kwargs):

# import dependencies
    from pocketLab.importers.config_file import configFile
    from pocketLab.importers.local_os import localOS
    from pocketLab.clients.docker_session import dockerSession
    from pocketLab.validators.config_model import configModel
    from pocketLab.exceptions.lab_exception import labException

# determine system properties
    local_os = localOS()

# ingest & validate virtualbox property
    vbox_name = kwargs['virtualbox']
    if not local_os in ('Windows','Mac'):
        vbox_name = ''

# check for docker installation
    docker_session = dockerSession(kwargs, vbox_name)

# retrieve list of container aliases
    container_list = docker_session.containers()
    alias_list = []
    for container in container_list:
        alias_list.append(container['NAMES'])

# ingest & validate alias name
    alias_name = kwargs['containerAlias']
    if alias_name == '':
        comp_details = configFile('lab-component.json', kwargs)
        comp_details = configModel(comp_details, 'rules/lab-component-model.json', kwargs, 'component settings')
        alias_name = comp_details['container_alias']

# check that container exists
    if not alias_name in alias_list:
        from pocketLab.compilers.table_print import tablePrint
        header_list = [ 'NAMES', 'STATUS', 'IMAGE', 'PORTS']
        error = {
            'kwargs': kwargs,
            'message': 'Container "%s" does not exist. Containers currently active: \n\n%s' % (alias_name, tablePrint(header_list, container_list)),
            'error_value': alias_name,
            'failed_test': 'required_resource'
        }
        raise labException(**error)

# remove container
    end_command = docker_session.remove(alias_name)
    start_text = 'Sweet! Container "%s" stopped.' % alias_name
    print(start_text)

    return end_command