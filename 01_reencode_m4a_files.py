"""
Script to reencode invalid m4a files, so it creates valid m4a files
"""

import os
import shutil
import subprocess


def copy_invalid_files():
    """
    Copies files from invalid_files.txt to `invalid_files` directory
    """
    invalid_files = []

    # Read invalid_files.txt
    with open("./invalid_files.txt", "r", encoding="utf-8") as f:
        for line in f:
            invalid_files.append(line.strip("\n"))

    # Create invalid_files directory
    if not os.path.exists("./invalid_files"):
        os.makedirs("./invalid_files")

    # Copy files to invalid_files
    for file in invalid_files:
        shutil.copy(file, "./invalid_files")

    print_script_message(
        f"{len(invalid_files)} files copied to invalid_files directory"
    )


def repair_invalid_files():
    """
    Reencodes invalid m4a files to valid m4a files
    """
    # List files in invalid_files
    invalid_files = os.listdir("./invalid_files")
    invalid_file_bitrates = []

    remove_path("./temp")
    os.makedirs("./temp")

    # Reencode files using ffmpeg
    print_script_message("Converting m4a files to wav")
    for file in invalid_files:
        invalid_file_bitrates.append(
            subprocess.check_output(
                f'ffprobe -v error -select_streams a:0 -show_entries stream=bit_rate -of default=noprint_wrappers=1:nokey=1 "./invalid_files/{file}"',
                shell=True,
            )
            .decode("utf-8")
            .strip("\r\n")
        )
        launch_ffmpeg(f"./invalid_files/{file}", f"./temp/{file.strip('.m4a')}.wav")

    wav_files = os.listdir("./temp")

    remove_path("./repaired_files")
    os.makedirs("./repaired_files")

    # Convert wav files to m4a files
    print_script_message("Converting wav files again into m4a")
    for file, bitrate in zip(wav_files, invalid_file_bitrates):
        launch_ffmpeg(
            f"./temp/{file}",
            f"./repaired_files/{file.strip('.wav')}.m4a",
            f"-acodec aac -cutoff 24000 -b:a {bitrate}",
        )

    remove_path("./temp")

    print_script_message(f"{len(invalid_files)} files reencoded to valid m4a files")
    print_script_message("All files copied to `repaired_files`")


def remove_path(path):
    """
    Recreate directory for temporary files
    """
    if os.path.exists(path):
        files_in_directory = os.listdir(path)
        for file in files_in_directory:
            os.remove(f"{path}/{file}")
        os.removedirs(path)


def print_script_message(string):
    """
    Prints script message
    """
    print(f"### {string} ###")


def launch_ffmpeg(input_path, output_path, output_arguments=""):
    """
    Executes an ffmpeg command to process the input file and produce an output file.

    Parameters:
    input_path (str): The path to the input media file.
    output_path (str): The path where the output media file will be saved.
    output_arguments (str, optional): Additional ffmpeg arguments for processing the file.
    """
    os.system(
        f'ffmpeg -v quiet -stats -i "{input_path}" -y {output_arguments} "{output_path}"'
    )


if __name__ == "__main__":
    copy_invalid_files()
    repair_invalid_files()
