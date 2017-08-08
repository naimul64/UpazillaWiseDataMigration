# parent, payment, pespapp_historicalparent, session, school_session, student, student_stipend, upazilla,

# !/usr/bin/python

import sys
import datetime
import os
import MySQLdb
import sys
import os
import csv
import datetime


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

def get_src_db_connection():
    return MySQLdb.connect(src_ip,
                           src_user_name,
                           src_pwd,
                           src_schema)


def get_dest_db_connection():
    return MySQLdb.connect(dest_ip,
                           dest_user_name,
                           dest_pwd,
                           dest_schema)


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


def export_upazilla(upazilla_list, db_con):
    with open('ExportUpazilla.sql', 'r') as myfile:
        data = myfile.read()
    query = data % upazilla_list

    export(db_con=db_con, query=query, export_entity="upazilla")

def import_upazilla(dest_db_con):
    export_entity = "upazilla"
    cursor = dest_db_con.cursor()
    query = """
        SELECT * FROM upazilla LIMIT 1
    """
    cursor.execute(query)
    if len(cursor.fetchall()) > 1:
        choise = raw_input('Clear upazilla table?(y/n): ')
        if choise in ['y', 'Y']:
            cursor.execute("TRUNCATE TABLE upazilla")
            dest_db_con.commit()
            print("Upazilla table cleared")
        else:
            return

    csv_data = csv.reader(file(os.path.join(export_folder_name, export_entity + "_" + time_stamp, export_entity + ".csv")))

    for row in csv_data:
        cursor.execute(""" INSERT INTO %s """)


    


def create_export_dir():
    create_dir_if_not_exist(export_folder_name)


def export(db_con, query, export_entity):
    cursor = db_con.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    description = cursor.description
    header = ()
    for desc in description:
        header = header + (desc[0],)
    cursor.close()

    if not os.path.exists('export'):
        os.makedirs(os.path.join(export_folder_name, export_entity + "_" + time_stamp))

    fp = open(os.path.join(export_folder_name, export_entity + "_" + time_stamp, export_entity + ".csv"), 'wb')
    myFile = csv.writer(fp)
    myFile.writerow(header)
    myFile.writerows(rows)
    fp.close()

    print "\n" + export_entity + " exported to CSV."


def main():
    create_export_dir()
    check_args(sys.argv)
    src_db_con = get_src_db_connection()
    dest_db_con = get_dest_db_connection()

    export_upazilla(sys.argv[2], src_db_con)
    import_upazilla(dest_db_con)


main()
