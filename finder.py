import concurrent.futures

value_to_find = "184;29;2.98;211"
value_to_find = "184;29;2.98;211\n"


def search(batch, value):
    with open(f"batch_{batch}.txt", "r") as f:
        for line in f:
            if line.endswith(value):
                print(batch)
                return batch
    return None

def main():
    with concurrent.futures.ProcessPoolExecutor(max_workers=32) as executor:
        futures = [executor.submit(search, batch, value_to_find) for batch in range(32)]
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

if __name__ == '__main__':
    main()