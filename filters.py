import os
import mimetypes
import arrow                    #Filters for jinja2 template

additional_file_types = {
    '.md': 'text/markdown'
}

#Creates human-readable date time
def datetimeformat(date_str):
    dt = arrow.get(date_str)    #Creates arrow object
    return dt.humanize()        #Translates the string

#Displays file type
def file_type(key):
    file_info = os.path.splitext(key)   #Splits the file extension tuple
    file_extension = file_info[1]       
    try:        
        return mimetypes.types_map[file_extension]  #Checks that there's a file extension
    except KeyError:
        filetype = 'Unknown'
        if file_info[0].startswith('.') and file_extension == '':
            filetype = 'text'
        elif file_info[0].endswith('/') and file_extension == '':
            filetype = 'folder'
        
        if file_extension in additional_file_types.keys():
            filetype = additional_file_types[file_extension]
            
        return filetype

#Displays file name
def file_name(key):
    file_info = os.path.splitext(key)
    return file_info[0][1:]