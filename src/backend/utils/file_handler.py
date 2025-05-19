from typing import List
import os
import io
import zipfile
import tempfile
import json


# this method is just a generic way
def create_zip_file(file_paths: List[str]) -> io.BytesIO:
    """
    Creates an in-memory ZIP file from the list of file paths, storing only the basename of each file in the archive.

    Args:
        file_paths (List[str]): A list of file paths to include in the ZIP archive.

    Returns:
        io.BytesIO: A BytesIO object containing the ZIP file data.
    """
    memory_file = io.BytesIO()
    
    with zipfile.ZipFile(memory_file, 'w') as zipf:
        for file_path in file_paths:
            # Write the file to the ZIP, using only the basename
            zipf.write(file_path, arcname=os.path.basename(file_path))
    
    memory_file.seek(0)
    return memory_file

# Save Files via temporary directory
def save_files_temp(folder_name:str, files:dict[str,any]):
    try:
        # Create temp dir
        temp_dir = tempfile.mkdtemp()
        folder_dir = os.path.join(temp_dir, folder_name)
        os.makedirs(folder_dir, exist_ok=True)
        print(f"Temporary directory created: {folder_dir}")
        
        # Save the content 
        for filename,content in files.items():
            filepath = os.path.join(folder_dir, filename)
            with open(filepath, 'w') as file:
                if isinstance(content,dict):
                    file.write(json.dumps(content, indent=4))
                else:
                    file.write(str(content))
            print(f"Saved {filepath}")
            
        return folder_dir
    except Exception as e:
        return "An error occurred while creating the temporary directory: {e}"