from fnmatch import fnmatch
from http.client import HTTPSConnection
import io
import json
from os import path
import os
import subprocess
import time
from urllib import request
import zipfile
import shutil

ENGINE_REPO = "MechMania-30/engine"
USER_AGENT = "MechMania-30"
FORMAT_ASSET_NAME = lambda version: f"engine-{version}.zip"
GITHUB_RELEASE_CHECK_DELAY = 60
MIN_NPM_MAJOR_VERSION = 10
NODE_JS_DOWNLOAD_URL = "https://nodejs.org/en/download"
NPM_UPDATE_COMMAND = "npm install -g npm@latest"
ENGINE_DIR = "engine"
DATAFILE_NAME = "data.txt"
DATAFILE_PATH = path.join(ENGINE_DIR, DATAFILE_NAME)


def __get_current_data():
    if path.exists(DATAFILE_PATH):
        with open(DATAFILE_PATH) as file:
            data = file.read().strip()

            if data:
                data = data.split(";")

            return data


def __get_latest_release_data():
    try:
        conn = HTTPSConnection("api.github.com")
        path = f"/repos/{ENGINE_REPO}/releases/latest"
        conn.request(
            "GET",
            path,
            headers={"User-Agent": USER_AGENT},
        )

        response = conn.getresponse()

        if response.status == 200:
            data = response.read().decode("utf-8")
            release_data = json.loads(data)

            return release_data
        else:
            print(f"`api.github.com{path}` returned status code {response.status}")
            exit(1)
    except Exception as e:
        print(f"Error: Failed to connect GitHub API, {e}")
        exit(1)


def __download(url):
    if not path.exists(ENGINE_DIR):
        os.makedirs(ENGINE_DIR, exist_ok=True)

    for filename in os.listdir(ENGINE_DIR):
        filepath = path.join(ENGINE_DIR, filename)
        if filename == DATAFILE_NAME:
            continue
        if path.isfile(filepath):
            os.remove()
        elif path.isdir(filepath):
            shutil.rmtree(path.join(ENGINE_DIR, filename))

    print(f"Downloading engine from `{url}`...")

    try:
        with request.urlopen(url) as response:
            with io.BytesIO(response.read()) as zip_buffer:
                with zipfile.ZipFile(zip_buffer, "r") as zip_file:
                    zip_file.extractall(ENGINE_DIR)
    except Exception as e:
        print(f"Error downloading: {e}")
        exit(1)

    for filename in os.listdir(ENGINE_DIR):
        if filename != DATAFILE_NAME:
            os.rename(
                os.path.join(ENGINE_DIR, filename),
                os.path.join(ENGINE_DIR, "engine"),
            )

    print("Saved to `engine/engine`")

def __install():
    print("Checking for npm installation...")
    check_npm = subprocess.run(
        ["npm", "--version"],
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if check_npm.returncode != 0:
        print(check_npm.stderr)
        print("Failed to check npm. Make sure you install node!\n" +
              f"You can update node here: {NODE_JS_DOWNLOAD_URL}\n" +
              f"And you can update npm by running: {NPM_UPDATE_COMMAND}")
        exit(1)

    version = check_npm.stdout.strip()
    print(f"Current installed NPM version: v{version}")
    major = int(version.split(".")[0])

    if major < MIN_NPM_MAJOR_VERSION:
        print("Your node/npm version is out of date! Please install the latest version!\n" +
              f"You can do so here: {NODE_JS_DOWNLOAD_URL}\n" +
              f"And you can update npm by running: {NPM_UPDATE_COMMAND}")
        exit(1)

    print("Is sufficiently up to date!")

    print("Installing node_modules (npm install)...")

    install = subprocess.run(
        ["npm", "install"],
        cwd=f"{ENGINE_DIR}/engine/",
        shell=True,
        text=True,
    )

    if install.returncode != 0:
        print("Failed to install")
        exit(1)

    print("Installed successfully!")


def __mark_checked(checked, version):
    if not path.exists(ENGINE_DIR):
        os.makedirs(ENGINE_DIR, exist_ok=True)

    with open(DATAFILE_PATH, "w") as file:
        file.write(f"{checked};{version}")


def update_if_not_latest():
    print("Checking for latest engine...")
    data = __get_current_data()

    last_checked = float(data[0]) if data else 0
    current_version = data[1] if data else None

    checked = time.time()
    if checked - last_checked < GITHUB_RELEASE_CHECK_DELAY:
        print("Already checked recently")
        return

    release = __get_latest_release_data()
    latest_version = release["tag_name"]

    if latest_version == current_version:
        __mark_checked(checked, latest_version)
        print("Latest engine already downloaded")
        return

    print(f"New engine is available ({current_version}->{latest_version})")

    asset_url = f"https://github.com/{ENGINE_REPO}/releases/latest/download/{FORMAT_ASSET_NAME(latest_version)}"

    if not path.exists(ENGINE_DIR):
        os.makedirs(ENGINE_DIR, exist_ok=True)

    __download(asset_url)
    __install()
    __mark_checked(checked, latest_version)


if __name__ == "__main__":
    update_if_not_latest()
