import configparser


write_config = configparser.ConfigParser()
write_config.add_section('Section1')
cfgfile = open('config.ini', 'w')
write_config.write(cfgfile)
cfgfile.close()
