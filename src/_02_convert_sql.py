def sql_to_string(sql_file_name):
    """Converts given SQL file contents to Python string."""
    with open('sql/{}'.format(sql_file_name), 'r') as file:
        sql_script = file.read()
    
    sql_string = '''\n{}\n'''.format(sql_script)
    return sql_string