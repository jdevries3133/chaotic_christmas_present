import logging

logger = logging.getLogger(__name__)


class SubprocessServerManager:
    """
    Manage many simple TCP servers in subprocesses using instances of
    ./server.Server. Each server will listen on a single port and echo
    a fixed message to any connection. Each server will, on its own or in
    chorus with its peers, be cookie crumbs in the greater scavenger hunt.
    """
