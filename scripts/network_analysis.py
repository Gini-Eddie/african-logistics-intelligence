import osmnx as ox

PLACE = "Lagos, Nigeria"

print("Downloading Lagos driving network...")

G = ox.graph_from_place(
    PLACE,
    network_type="drive",
    simplify=True
)

print(
    f"Road graph loaded: "
    f"{len(G.nodes):,} nodes, "
    f"{len(G.edges):,} edges"
)