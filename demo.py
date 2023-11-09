import marshal
import sys
import json

def write_file(file_path, content, encoding='utf-8'):
    """
    Writes content to a file.

    Parameters:
    file_path (str): The path to the file to write to.
    content (str or dict): The content to write to the file. If encoding is 'JSON', content is expected to be a dictionary.
    encoding (str, optional): The encoding to use when writing the file. 'utf-8' is used by default. If set to 'JSON', content is expected to be a dictionary and will be JSON-encoded.

    Returns:
    dict: A dictionary with an 'error' key (True if there was an error, False otherwise) and an 'exception' key (containing an error message if an error occurred).
    """
    try:
        if encoding == 'JSON':
            if not isinstance(content, dict):
                return {'error': True, 'exception': "Content must be a dictionary when encoding is set to 'JSON'"}
            content = json.dumps(content)
        
        with open(file_path, 'w', encoding=encoding) as file:
            file.write(content)
        
        return {'error': False}
    except Exception as e:
        return {'error': True, 'exception': f"An error occurred while writing to the file: {e}"}

def read_file(file_path, encoding='utf-8'):
    """
    Reads the contents of a file.

    Parameters:
    file_path (str): The path to the file to read.
    encoding (str, optional): The encoding to use when reading the file. 'utf-8' is used by default. If set to 'JSON', the file contents are expected to be JSON-encoded.

    Returns:
    dict: A dictionary with an 'error' key (True if there was an error, False otherwise), a 'content' key (containing the file contents if no error occurred), and an 'exception' key (containing an error message if an error occurred).
    """
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            file_contents = file.read()

        if encoding == 'JSON':
            try:
                file_contents = json.loads(file_contents)
            except json.JSONDecodeError:
                return {'error': True, 'exception': "JSON decoding error. The file may not contain valid JSON data."}

        return {'error': False, 'content': file_contents}
    except FileNotFoundError as e:
        return {'error': True, 'exception': f"File not found: {file_path}"}
    except Exception as e:
        return {'error': True, 'exception': f"An error occurred while reading the file: {e}"}

def compile_file(source_file, output_file):
    """
    Compiles the contents of a source file and saves it to an output file.

    Parameters:
    source_file (str): The path to the source file to compile.
    output_file (str): The path to the output file to save the compiled code.

    Returns:
    dict: A dictionary with an 'error' key (True if there was an error, False otherwise) and an 'exception' key (containing an error message if an error occurred).
    """
    
    # Retrieve the file
    readed  = read_file(source_file)
    if readed['error'] :
        return readed

    # compile
    return  compile_str(readed['content'], output_file)

def compile_str(source_code, output_file):
    """
    Compiles the provided source code and saves it to an output file.

    Parameters:
    source_code (str): The Python source code to compile.
    output_file (str): The path to the output file to save the compiled code.

    Returns:
    dict: A dictionary with an 'error' key (True if there was an error, False otherwise) and an 'exception' key (containing an error message if an error occurred).
    """
    try:
        
        compiled_code = compile(source_code,output_file , 'exec')
        with open(output_file, 'wb') as file:
            marshal.dump(compiled_code, file)
        return {'error': False}
    except Exception as e:
        return {'error': True, 'exception': f"An error occurred while compiling to the file: {e}"} 

def execute_compiled_file(input_file,local_namespace={}):
    """
    Executes a compiled file and retrieves the response.

    Parameters:
    input_file (str): The path to the compiled file to execute.
    local_namespace (dict): The dict passed to local_namespace
    Returns:
    dict: A dictionary with an 'error' key (True if there was an error, False otherwise), a 'response' key (containing the response from the executed code if no error occurred), and an 'exception' key (containing an error message if an error occurred).
    """
  
    try:
         
        # Put more variables to compiled context by local_namespace
        #local_namespace['bar'] ='foo'
 
        with open(input_file, 'rb') as file:
            compiled_code = marshal.load(file)
        exec(compiled_code, globals(), local_namespace)
         
        # Access variables from the compiled context after execution
        response = local_namespace.get('__response__', None)


        if response is not None:
            return {'error': False, 'response': response}
        else:
            return {'error': False, 'response': None}
    except SystemExit as e:  # Handles sys.exit of the compiled content
        response = local_namespace.get('__response__', None)
        return {'error': False, 'response': response}
    except Exception as e:
        return {'error': True, 'exception': f"An error occurred while executing the compiled file: {e}"}

 
 

def neorun(file_path,output_path,compile=False):


    compiled = compile_file(file_path,output_path)
    if  compiled['error'] : 
            return compiled
 
    

    return execute_compiled_file(output_path)
 



response = neorun('demo_input_file.py','build/demo_output_file.pyc',compile=True)
print(response)