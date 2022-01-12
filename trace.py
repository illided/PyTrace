import socket
from dataclasses import dataclass, field
from os import getpid
from typing import List, Callable, Optional

from icmplib import ICMPRequest, ICMPv6Socket, ICMPv4Socket, is_ipv4_address, is_ipv6_address
from icmplib.exceptions import *
from icmplib.sockets import ICMPSocket


@dataclass
class Hop:
    successful: bool
    final: bool
    address: str
    times: List[Optional[int]] = field(default_factory=list)

    @property
    def failed_requests(self) -> int:
        return self.times.count(None)

    @property
    def successful_requests(self) -> int:
        return len(self.times) - self.failed_requests


class TraceRoute:
    def __init__(self, dest: str, timeout: int = 2,
                 max_hops: int = 30, req_per_hop: int = 3,
                 on_hop: Callable[[Hop], None] = None):
        self.dest = dest
        self.ip_address = socket.gethostbyname(dest)

        self.timeout = timeout
        self.max_hops = max_hops
        self.req_per_hop = req_per_hop
        self.on_hop = on_hop

        self.hops: List[Hop] = []
        self.ended_successfully = False
        self.error: Optional[Exception] = None

        self.unique_id = getpid()

    def start(self):
        try:
            self.hops = self.trace()
            self.ended_successfully = True
        except ICMPError as err:
            self.error = err
            self.ended_successfully = False

    def trace(self) -> List[Hop]:
        ttl = 1
        with self.initialize_socket() as sock:
            route = [self.try_reach(sock, ttl)]
            while not route[-1].final:
                if len(route) >= self.max_hops:
                    break
                ttl += 1
                hop = self.try_reach(sock, ttl)
                self.on_hop(hop)
                route.append(hop)
        return route

    def initialize_socket(self):
        if is_ipv4_address(self.ip_address):
            return ICMPv4Socket()
        elif is_ipv6_address(self.ip_address):
            return ICMPv6Socket()
        else:
            raise SocketAddressError

    def try_reach(self, sock: ICMPSocket, ttl: int) -> Hop:
        hop = Hop(False, False, "", [])
        for i in range(self.req_per_hop):
            icmp_id = self.generate_icmp_id()
            request = ICMPRequest(
                destination=self.ip_address,
                sequence=i,
                id=icmp_id,
                ttl=ttl
            )

            try:
                sock.send(request)
                reply = sock.receive(request, self.timeout)

                hop.times.append((reply.time - request.time) * 1000)
                hop.address = reply.source
                hop.successful = True

                if reply.type == 0:
                    hop.final = True
            except TimeoutExceeded:
                hop.times.append(None)
        return hop

    def generate_icmp_id(self):
        self.unique_id += 1
        self.unique_id &= 0xffff
        return self.unique_id
