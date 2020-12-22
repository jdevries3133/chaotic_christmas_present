# Orchestrated Multi-Port TCP Server

## Minimum Viable Behavior

It will be necessary to orchestrate many TCP servers. Most importantly, to
assign each server a host, a port, and a message to send to any connector.

## Interprocess Communication

If there is time, it would be great to create a means for servers to communicate
with each other through the parent process. This would make it possible, for
example, for the data sent into one socket to change the data echoed by another.
This obviously opens up a world of possibilities for puzzle design.

# TODO

- [ ] Reach minimum viable behavior
- [ ] Begin designing puzzles, including frontend "documentation"
- [ ] Revisit interprocess communication
