import configparser

# read_config = configparser.ConfigParser()
# read_config.read('config.ini')
# print(read_config['Section1']['username'])

update_config = configparser.ConfigParser()
update_config.read('SimpleStorage/Storage/config.ini')
update_config['Section1']['username'] = "coba"
update_config['Section1']['user'] = "coba1"
with open ('SimpleStorage/Storage/config.ini', 'w') as configfile:
    update_config.write(configfile)
