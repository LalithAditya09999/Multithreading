import os
import time
import threading
import shutil
import urllib.request
from urllib.parse import urlparse

def download_file(url, output_dir="downloads"):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filename = os.path.basename(urlparse(url).path)
        if not filename:
            filename = f"file_{int(time.time())}.dat"

        filepath = os.path.join(output_dir, filename)

        start_time = time.time()
        with urllib.request.urlopen(url) as response:
            content_length = response.getheader('Content-Length')
            file_size = int(content_length) if content_length else 0

            with open(filepath, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

        end_time = time.time()
        print(f"Downloaded {filename} ({file_size / 1024:.1f} KB) in {end_time - start_time:.2f} seconds")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return False

def seq_download(urls, output_dir="downloads"):
    print("\nInitiating sequential downloads...")
    start_time = time.time()
    success_count = 0

    for url in urls:
        if download_file(url, output_dir):
            success_count += 1

    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nSequential download finished: {success_count}/{len(urls)} files in {total_time:.2f} seconds")
    return total_time

def threaded_download(urls, output_dir="downloads", max_threads=5):
    print("\nInitiating threaded downloads with", max_threads, "threads...")
    start_time = time.time()
    threads = []
    success_count = [0]

    def download_and_count(url):
        if download_file(url, output_dir):
            success_count[0] += 1

    for url in urls:
        thread = threading.Thread(target=download_and_count, args=(url,))
        threads.append(thread)
        thread.start()

        while threading.active_count() > max_threads:
            time.sleep(0.1)

    for thread in threads:
        thread.join()

    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nThreaded download completed: {success_count[0]}/{len(urls)} files in {total_time:.2f} seconds")
    return total_time

def get_urls(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return []

def main():
    print("Concurrent File Downloader")
    
    while True:
        print("\nHow would you like to provide URLs?")
        print("1. Enter URLs manually")
        print("2. Load URLs from a text file")
        print("3. Use sample URLs")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == '1':
            print("\nPlease enter URLs one per line (press Enter on a blank line to finish):")
            urls = []
            while True:
                url = input()
                if not url:
                    break
                urls.append(url)

        elif choice == '2':
            file_path = input("\nPlease provide the path to the text file containing URLs: ")
            urls = get_urls(file_path)

        elif choice == '3':
            urls = [
                "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                "https://file-examples-com.github.io/uploads/2017/10/file-sample_150kB.pdf"
            ]
            print("\nUsing the following sample URLs:")
            for url in urls:
                print(f"- {url}")

        elif choice == '4':
            print("Goodbye!")
            break

        else:
            print("Invalid selection. Please try again.")
            continue

        if not urls:
            print("No URLs provided for download. Please try again.")
            continue

        output_dir = input("\nSpecify the download directory (default: downloads): ") or "downloads"

        try:
            max_threads = int(input("\nSpecify the maximum number of concurrent downloads (default: 5): ") or "5")
        except ValueError:
            max_threads = 5
            print("Invalid input, defaulting to 5 threads.")

        sequential_time = seq_download(urls, output_dir)
        threaded_time = threaded_download(urls, output_dir, max_threads)

        speedup = sequential_time / threaded_time if threaded_time > 0 else 0
        print(f"\nPerformance comparison:")
        print(f"- Sequential: {sequential_time:.2f} seconds")
        print(f"- Threaded:   {threaded_time:.2f} seconds")
        print(f"- Speedup:    {speedup:.2f}x")

        print("\nWould you like to download more files? (y/n)")
        if input().lower() != 'y':
            print("Goodbye!")
            break

main()
