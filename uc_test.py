import os
import shutil
import tempfile


def mk_chrome_tmp_folder():
    """Create the tmp folder for chrome and copy the extension setting to it"""
    folder_path = tempfile.mkdtemp(prefix='uc_chrome_')

    extensions_setting_path = get_real_path()

    # extensions_setting_path = 'C:\\Users\\admin\\PycharmProjects\\feapder_init_spider\\safe_browser_uc\\Chrome\\UserData\\Default'

    # copy Chrome user data folder to tmp folder
    shutil.copytree(extensions_setting_path, f'{folder_path}\\Default')

    return folder_path


def get_real_path():
    """Get the real path of the path"""
    current_path = os.path.abspath('spiders')

    if current_path.endswith('safe_browser_uc'):
        return f'{current_path}\\Chrome\\UserData'
    elif current_path.endswith('spiders'):
        return f'{current_path.replace("spiders", "")}safe_browser_uc\\Chrome\\UserData'
    else:
        return f'{current_path}\\safe_browser_uc\\Chrome\\UserData'


if __name__ == '__main__':
    path = mk_chrome_tmp_folder()
    path = 'launch'
    print(path)