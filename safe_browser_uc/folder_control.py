import os
import shutil
import tempfile


def make_chrome_tmp_folder():
    """Create the tmp folder for chrome and copy the extension setting to it"""
    folder_path = tempfile.mkdtemp(prefix='uc_chrome_')

    extensions_setting_path = _get_real_path()

    # copy Chrome user data folder to tmp folder
    shutil.copytree(extensions_setting_path, f'{folder_path}\\Default')

    return folder_path


def _get_real_path():
    """Get the real path of the path"""
    current_path = os.path.abspath('.')

    if current_path.endswith('safe_browser_uc'):
        # when debug with __init__.py and folder_control.py
        return f'{current_path}\\Chrome\\UserData\\Default'
    elif current_path.endswith('spiders'):
        # when launch with spiders
        return f'{current_path.replace("spiders", "")}\\safe_browser_uc\\Chrome\\UserData\\Default'
    else:
        # when launch at the root of the project
        return f'{current_path}\\safe_browser_uc\\Chrome\\UserData\\Default'


if __name__ == '__main__':
    path = make_chrome_tmp_folder()
    print(path)