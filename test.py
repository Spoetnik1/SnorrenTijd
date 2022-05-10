import configparser


## Read configurations
config = configparser.ConfigParser()
config.read('config.ini')

job_section = 'DEFAULT'

print(config.get(job_section, 'image_file_path'))

print(config.get('SOME_OTHER_SITUATION', 'image_file_path'))

