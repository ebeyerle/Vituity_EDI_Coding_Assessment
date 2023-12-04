import shutil
import os

##
##  Make a copy of the 3 files in a directory Archive/Original
##
def make_backups():

  # Get the directory that has the files
  # -The csv and txt files are stored here
  file_directory = 'Data/'

  # Specify the destination directory
  archive_original_dir = 'Archive/Original/'

  # Create the destination directory if it doesn't exist
  if not os.path.exists(archive_original_dir):
      os.makedirs(archive_original_dir)

  # Get a list of all files in the current directory
  files_to_copy = os.listdir(file_directory)

  # Loop through the files and copy them to the Archive/Original directory
  for file_name in files_to_copy:
    # Construct the source and destination paths
      source_path = os.path.join(file_directory, file_name)
      destination_path = os.path.join(archive_original_dir, file_name)

      # Check if the item is a file (not a directory) before copying
      if os.path.isfile(source_path):
          shutil.copy(source_path, destination_path)
