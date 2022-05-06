from pathlib import Path

BASE_DIR = Path.cwd()


def main():
    with open(BASE_DIR / "requests.txt", "r") as stream:
        requests = stream.read().splitlines()
    with open(BASE_DIR / "experiment3-linearizability.txt", "r") as stream:
        linear = stream.read().splitlines()
    with open(BASE_DIR / "experiment3-eventualconsistency.txt", "r") as stream:
        eventual = stream.read().splitlines()

    for name, replies in [("linear", linear), ("eventual", eventual)]:
        values = {}
        inconsistencies = {}
        if len(requests) > len(replies):
            print("Well I don't have all the replies :(")
            exit(101)
        for i, (request, reply) in enumerate(zip(requests, replies), 1):
            if "insert" in request:
                # _, key, value = map(lambda x: x.strip(), request.split(","))
                [_, key, value] = [x.strip() for x in request.split(",")]
                if "successfully" not in reply:
                    print(f"Not saved successfully (transaction #{i}) :(")
                    exit(102)
                values[key] = value
            if "query" in request:
                # _, key = map(lambda x: x.strip(), request.split(","))
                [_, key] = [x.strip() for x in request.split(",")]
                reply_key = reply.split("key=")[1].split(" -")[0]
                reply_value = reply.split("value=")[1].split(" -")[0]
                if key != reply_key:
                    print(f"Mismatching keys (transaction #{i}) :(")
                    exit(103)
                if str(values.get(reply_key)) != reply_value:
                    print(f"Expected '{reply_key}' to have value {values.get(reply_key)}, got {reply_value} (transaction #{i}) :(")
                    inconsistencies[i] = True
        print(f"Total amount of inconsistencies of {name}: {len(inconsistencies)}")


if __name__ == "__main__":
    main()