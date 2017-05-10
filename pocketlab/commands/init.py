__author__ = 'rcj1492'
__created__ = '2017.05'
__license__ = 'MIT'

_init_schema = {
    'title': 'init',
    'description': 'Adds lab configuration files to the current directory.',
    'metadata': {
        'cli_help': 'creates a lab framework in workdir',
        'docs_benefit': 'Init adds the config files for other lab commands.',
        'docs_description': 'Init adds a number of files to the working directory which are required for other lab processes. If not present, it will create a ```lab.yaml``` file in the root directory to manage various configuration options. It will also create, if missing, ```cred/``` and ```data/``` folders to store sensitive information outside version control along with a ```.gitignore``` (or ```.hgignore```) file to escape out standard non-VCS files.'
    },
    'schema': {
        'container_alias': '',
        'image_name': '',
        'vcs_service': ''
    },
    'components': {
        '.vcs_service': {
            'field_description': 'Version control system used by project',
            'default_value': '',
            'discrete_values': [ '', 'git', 'Git', 'mercurial', 'Mercurial' ],
            'field_metadata': {
                # 'cli_group': 'A',
                'cli_flags': [ '--vcs' ],
                'cli_help': 'VCS service to generate ignore file',
                'cli_metavar': 'SERVICE'
            }
        }
    }
}

def init(container_alias='', image_name='', vcs_service=''):

    '''
        a method to add lab framework files to the current directory
        
    :param container_alias: [optional] string with alias for project's docker container
    :param image_name: [optional] string with name for project's docker image
    :param vcs_service: [optional] string with name of version control service
    :return: string with success exit message
    '''

    title = 'init'

# validate inputs
    from jsonmodel.validators import jsonModel
    input_model = jsonModel(_init_schema)
    input_map = {
        'vcs_service': vcs_service
    }
    for key, value in input_map.items():
        object_title = '%s(%s=%s)' % (title, key, str(value))
        input_model.validate(value, '.%s' % key, object_title)

# import dependencies
    from os import path

# determine version control service
    if not vcs_service:
        vcs_service = '.git'
        if path.exists('.git'):
            if path.isdir('.git'):
                vcs_service = 'git'
        elif path.exists('.hg'):
            if path.isdir('.hg'):
                vcs_service = 'mercurial'
    else:
        vcs_service = vcs_service.lower()

# add a vcs ignore file
    from pocketlab.methods.vcs import load_ignore
    if vcs_service == 'git':
        vcs_path = '.gitignore'
        vcs_type = 'git'
    else:
        vcs_path = '.hgignore'
        vcs_type = 'mercurial'
    if not path.exists(vcs_path):
        file_text = load_ignore(vcs=vcs_type)
        with open(vcs_path, 'wt') as f:
            f.write(file_text)
            f.close()

# add a lab config file
    config_path = 'lab.yaml'
    if not path.exists(config_path):
        from pocketlab import __module__
        from jsonmodel.loader import jsonLoader
        from labpack.records.settings import save_settings
        config_schema = jsonLoader(__module__, 'models/lab-config.json')
        config_model = jsonModel(config_schema)
        config_details = config_model.ingest(**{})
        save_settings(config_path, config_details)

# add a data folder
    data_path = 'data'
    from os import makedirs
    if not path.exists(data_path):
        makedirs(data_path)

# add a credential folder
    cred_path = 'cred'
    notes_path = 'notes'
    if not path.exists(cred_path):
        makedirs(cred_path)
        if path.exists(notes_path):
            if path.isdir(notes_path):
                src_list = []
                dst_list = []
                from os import listdir
                from shutil import copyfile
                for file_name in listdir(notes_path):
                    file_path = path.join(notes_path, file_name)
                    if path.isfile(file_path):
                        if file_name.find('.json') > -1 or file_name.find('.yaml') > -1 or file_name.find('.yml') > -1:
                            src_list.append(file_path)
                            dst_list.append(path.join(cred_path, file_name))
                for i in range(len(src_list)):
                    copyfile(src_list[i], dst_list[i])

    msg_insert = ''
    if container_alias:
        msg_insert = ' for "%s"' % container_alias
    exit_msg = 'Lab framework%s setup in current directory.' % msg_insert

    return exit_msg

if __name__ == "__main__":

    from labpack.records.settings import load_settings
    from jsonmodel.validators import jsonModel
    config_path = '../models/lab-config.json'
    config_model = jsonModel(load_settings(config_path))
    print(config_model.ingest(**{}))