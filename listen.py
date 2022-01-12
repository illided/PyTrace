import statistics

from trace import Hop


def pretty_print(hop: Hop, ip=True, avg_time=True, successfulness=False) -> str:
    s = []
    if not hop.successful:
        return "No reply"
    if ip:
        s.append(f"{hop.address}")
    if avg_time:
        mean = statistics.mean([t for t in hop.times if t is not None])
        ms = round(mean, 2)
        s.append(f"Time: {ms} ms")
    if successfulness:
        s.append(f"Requests: Successful = {hop.successful_requests} Failed = {hop.failed_requests}")
    if hop.final:
        s.append("Destination reached")
    return " ".join(s)

