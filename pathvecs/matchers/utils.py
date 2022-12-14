def getInboundDependencies(span):
    """ Get the set of dependencies from arcs leading into the span """

    inbound_deps = []
    _min, _max = span.start, span.end - 1

    for tok in span:
        if tok.head.i < _min or tok.head.i > _max:
            inbound_deps.append(tok.dep_)

    return inbound_deps


def getOutboundDependencies(span):
    """ Get the set of dependencies from arcs leading out of the span """

    outbound_deps = []
    _min, _max = span.start, span.end - 1

    for tok in span:
        for child in tok.children:
            if child.i < _min or child.i > _max:
                outbound_deps.append(tok.dep_)

    return outbound_deps
