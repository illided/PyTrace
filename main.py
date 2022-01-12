import argparse
from trace import TraceRoute, Hop
from listen import pretty_print


def main():
    parser = argparse.ArgumentParser()
    # Trace route arguments
    parser.add_argument('--address', dest='address', type=str, help='Address to trace')
    parser.add_argument('--timeout', dest='timeout', type=int, default=2,
                        help='Timeout for every request (in seconds).'
                             'Be aware that for every hop multiple requests occur. '
                             'Default: 2s')
    parser.add_argument('--requests-per-hop', dest='req_per_hop', type=int, default=5,
                        help='Number of requests to perform for every hop. Default: 5 requests')
    parser.add_argument('--max-hop', dest='max_ttl', type=int, default=30,
                        help="Maximum number of hops to perform. Default: 30 hops")

    # Pretty printing
    parser.add_argument('--show-time', dest='time', type=bool, default=True,
                        help="Show average time. Default: True")
    parser.add_argument('--show-request-stat', dest="succ", type=bool, default=False,
                        help="Show request successfulness. Default: False")

    args = parser.parse_args()

    if not args.address:
        raise AttributeError

    TraceRoute(
        dest=args.address,
        timeout=args.timeout,
        max_hops=args.max_ttl,
        req_per_hop=args.req_per_hop,
        on_hop=lambda h: print(pretty_print(
            hop=h,
            avg_time=args.time,
            successfulness=args.succ
        ))
    ).start()


if __name__ == '__main__':
    main()
