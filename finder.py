import concurrent.futures
import sys

"162;31;3.07;51"

def search(batch, value):
    with open(f"logs/batch_{batch}.txt", "r") as f:

        for line in f:
            if value in line:
                print(batch)
                return batch
    return None

def main():
    value_to_find = sys.argv[1]
    with concurrent.futures.ProcessPoolExecutor(max_workers=32) as executor:
        futures = [executor.submit(search, batch, value_to_find) for batch in range(32)]
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

if __name__ == '__main__':
    main()