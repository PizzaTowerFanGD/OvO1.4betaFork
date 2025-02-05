# Selenium firefox

from selenium import webdriver
import chromedriver_autoinstaller
import threading
import urllib.request
import urllib.parse
import shutil
import os

chromedriver_autoinstaller.install()

VERSIONS = {
    "1.3.2": "https://dedragames.com/games/ovo/1.3.2/",
    "1.3": "https://dedragames.com/games/ovo/1.3/",
    "1.2": "https://dedragames.com/games/ovo/1.2/",
    "1.1": "https://dedragames.com/games/ovo/1.1/",
    "feedback": "https://ovofeedback.surge.sh/",
    "devovo": "https://devovo.surge.sh/",
    "itch": "https://html-classic.itch.zone/html/789098/",
    "procanim": "https://procanim.surge.sh/"
}

for version, base_url in VERSIONS.items():
    URL = urllib.parse.urlparse(base_url)
    OUTPUT_DIR = f"versions/{version}/"

    driver = webdriver.Chrome()
    driver.get(URL.geturl())

    timings = []

    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)

    def download_file_process(url, path):
        print("Downloading", url, "to", path)
        urllib.request.urlretrieve(url, path)

    def download_file(url, path):
        p = threading.Thread(target=download_file_process, args=(url, path))
        p.start()

    while True:
        new_timings = driver.execute_script("return window.performance.getEntriesByType('resource')")

        for timing in new_timings:
            if timing not in timings:
                timings.append(timing)
                url = urllib.parse.urlparse(timing["name"])
                path = OUTPUT_DIR + url.path[len(URL.path):]

                if url.netloc != URL.netloc:
                    print("Skipping", timing["name"])
                    continue

                dirs = os.path.dirname(path)
                if dirs:
                    os.makedirs(dirs, exist_ok=True)

                print("Downloading", timing["name"], "to", path)
                download_file(timing["name"], path)

    driver.quit()
