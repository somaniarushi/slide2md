import os

def clear_tmp():
    """
    Clears all the files in the tmp folder.
    """
    # Ask yes/no confirmation
    print("Are you sure you want to clear the tmp folder? (y/n)")
    answer = input()
    if answer != "y" or answer != "Y":
        print("Aborting...")
        return

    files = os.listdir("tmp")
    for file in files:
        os.remove(os.path.join("tmp", file))


if __name__ == "__main__":
    clear_tmp()