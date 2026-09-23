def log_filter(filepath):
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            received = yield line

            if isinstance(received, dict) and "level" in received:
                level = received["level"]
                continue

            if level in line:
                print("[FILTERED]", line)


f = log_filter("log.txt")

line = next(f)
print(line)

f.send({"level": "INFO"})

while True:
    try:
        line = f.send(None)
    except StopIteration:
        break
