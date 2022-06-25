import configparser
import os

write_config = configparser.ConfigParser()
write_config.add_section('Section1')
file_path = os.path.join('SimpleStorage/Storage/' 'config.ini')
cfgfile = open(file_path, 'w')
write_config.write(cfgfile)
cfgfile.close()
# ROOT_PROJECT = os.getcwd().replace("\\", "/")
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
# ROOT_FOLDER = os.path.basename(ROOT_DIR)

# print(ROOT_PROJECT)
# print(ROOT_DIR)
# print(ROOT_FOLDER)

# os.chdir("..")

# ROOT_PROJECT = os.getcwd().replace("\\", "/")
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
# ROOT_FOLDER = os.path.basename(ROOT_DIR)
# print(ROOT_PROJECT)
# print(ROOT_DIR)
# print(ROOT_FOLDER)