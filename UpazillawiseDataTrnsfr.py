# parent, payment, pespapp_historicalparent, session, school_session, student, student_stipend, upazilla,

# !/usr/bin/python

import sys
import datetime
import os
import subprocess


## important variable
##########
src_ip = "192.168.1.56"
dest_ip = "localhost"
src_user_name = 'nayan'
dest_user_name = 'root'
src_pwd = 'PSL_n@y@n#pr0g0t1!!56'
dest_pwd = '123456'
src_schema = "pesp_q3_nayan_desk"
dest_schema = "djangoDb"
time_stamp = datetime.datetime.now().strftime("%y%m%d%H%M%S")
export_folder_name = "EXPORT"


###########


def connect_to_db():
    command = """ mysql --host="192.168.1.56" --user="nayan" --password="PSL_n@y@n#pr0g0t1!!56" """
    os.system(command)


def check_args(args):
    if len(args) < 3:
        print "NOT NOUGH ARGUMENT"
        return False

    if args[1] not in ['u', "U", 's', "S"]:
        print "INVALID ARGUMENT"
        return False

    return True


def create_dir_if_not_exist(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def create_file(file_with_path):
    with open(file_with_path, 'a'):
        os.utime(file_with_path, None)


def export_upazilla(upazilla_list):
    with open('ExportUpazilla.sql', 'r') as myfile:
        data = myfile.read()
    query = data % upazilla_list
    print query
    create_dir_if_not_exist(os.path.join(export_folder_name, "upazilla_" + time_stamp))

    command = 'mysql -h %s -u %s -p -sN -e "%s" %s > %s' % (src_ip,
                                                            src_user_name,
                                                            query,
                                                            src_schema,
                                                            os.path.join(export_folder_name, "upazilla_" + time_stamp,
                                                                         "upazilla"))
    create_file(os.path.join(export_folder_name, "upazilla_" + time_stamp, "upazilla"))
    os.system(command)
    print "Upazilla exported".upper()


def create_export_dir():
    create_dir_if_not_exist(export_folder_name)


def export(table_name, query):
    dir_path = os.path.join(export_folder_name, table_name + "_" + time_stamp)
    create_dir_if_not_exist(dir_path)

    command = 'mysql -h %s -u %s -p -sN -e "%s" %s > %s' % (src_ip,
                                                            src_user_name,
                                                            query,
                                                            src_schema,
                                                            os.path.join(dir_path, table_name))
    create_file(os.path.join(dir_path, table_name))
    os.system(command)
    print (table_name + " exported").upper()


def main():
    create_export_dir()
    check_args(sys.argv)

    export_upazilla(sys.argv[2])


main()
