from panda3d.core import CollisionNode, CollisionBox

def update_terrain(loaded_chunks, planeModel, loader, render):
    plane_pos = planeModel.getPos()
    chunk_x = int(plane_pos.x // 1000)
    chunk_y = int(plane_pos.y // 1000)

    for cx in range(chunk_x - 1, chunk_x + 2):
        for cy in range(chunk_y - 1, chunk_y + 2):
            if (cx, cy) not in loaded_chunks:
                load_chunk(cx, cy, loader, render, loaded_chunks)

    chunks_to_remove = []
    for (cx, cy) in loaded_chunks.keys():
        if abs(cx - chunk_x) > 1 or abs(cy - chunk_y) > 1:
            chunks_to_remove.append((cx, cy))

    for chunk_coord in chunks_to_remove:
        remove_chunk(chunk_coord, loaded_chunks)

def load_chunk(cx, cy, loader, render, loaded_chunks):
    chunk = loader.loadModel("models/environment")
    chunk.setPos(cx * 1000, cy * 1000, 0)
    chunk.reparentTo(render)
    
    cnode = CollisionNode('terrain')
    cnode.addSolid(CollisionBox((0, 0, 0), 500, 500, 10))

    cnodepath = chunk.attachNewNode(cnode)

    loaded_chunks[(cx, cy)] = chunk

def remove_chunk(coord, loaded_chunks):
    # Remove the chunk from render
    loaded_chunks[coord].removeNode()
    del loaded_chunks[coord]