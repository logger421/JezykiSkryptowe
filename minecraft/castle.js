// those minus values are due to initial 'Z' axis direction
// please stay still until water around shows up
player.onChat('castle', function() {
    const height = 7;
    const width = 40;
    const houseHeight = height - 2;
    const houseWidth = (width - 16);
    const startPosition = pos(0, -1, -5)

    builder.teleportTo(startPosition)
    builder.mark()
    builder.setOrigin()

    // fill floor
    builder.shift(width, 0, (-width) + 1)
    builder.fill(GRASS_PATH)

    // move position to outer walls
    builder.teleportToOrigin()

    // build outer walls
    builder.mark()
    buildWalls(height, width)

    // move position to inner walls
    builder.teleportToOrigin()
    builder.shift(2, 0, -2)

    // build inner walls
    builder.mark()
    buildWalls(height, width - 4)

    // fill floor between walls
    builder.teleportToOrigin()
    builder.shift(1, height - 2, -1)
    builder.mark()
    for(let i = 0; i < 4; i++) {
        builder.move(FORWARD, width - 2)
        builder.turn(TurnDirection.Right)
    }
    builder.tracePath(PLANKS_DARK_OAK)

    // build towers
    for(let w = 0; w < 4; w++) {
        switch(w) {
            case 0:
                builder.teleportToOrigin()
                break;
            case 1:
                builder.teleportTo(pos(0, -1, -5 - width))
                builder.turn(TurnDirection.Right)
                builder.setOrigin()
                break;
            case 2:
                builder.teleportTo(pos(width, -1, -5 - width))
                builder.turn(TurnDirection.Right)
                builder.setOrigin()
                break;
            case 3:
                builder.teleportTo(pos(width, -1, -5))
                builder.turn(TurnDirection.Right)
                builder.setOrigin()
                break;
        }
        buildTower(height)
    }

    // build center house
    // move to start pos
    builder.teleportTo(startPosition)
    builder.turn(TurnDirection.Right)

    // build floor
    builder.shift(8, 0, -9)
    builder.setOrigin()
    builder.mark()
    builder.shift(width - 16, 1, -width + 16)
    builder.fill(DARK_OAK_WOOD_SLAB)

    builder.teleportToOrigin()
    builder.mark()
    for(let i = 0; i < 4; i++) {
        builder.move(FORWARD, width - 16)
        builder.turn(TurnDirection.Right)
    }
    builder.raiseWall(STONE_BRICKS, houseHeight)

    // add window for left, right and back of the house
    builder.move(UP, 2)
    for(let i = 0; i < 3; i++) {
        builder.move(FORWARD, (width - 16) / 2)
        builder.mark()
        builder.shift(1, 2, 0)
        builder.fill(GLASS)
        builder.move(DOWN, 2)
        builder.move(FORWARD, (width - 16) / 2 - 1)
        builder.turn(TurnDirection.Right)
    }

    // add front windows, doors and path to walls entrance
    // window
    builder.move(FORWARD, (width - 16) / 4)
    builder.mark()
    builder.shift(1, 2, 0)
    builder.fill(GLASS)

    // door
    builder.move(FORWARD, (width - 16) / 4 - 1)
    builder.move(DOWN, 3)
    builder.mark()
    builder.shift(1, 2, 0)
    builder.fill(AIR)
    builder.move(DOWN, 1)
    builder.move(FORWARD, 1)
    builder.place(AIR)
    builder.move(BACK, 3)
    builder.place(AIR)
    builder.move(FORWARD, 2)

    // save position for path and bridge
    let doorPathPos = builder.position()

    // last front window
    builder.move(FORWARD, (width - 16) / 4)
    builder.mark()
    builder.shift(1, 2, 0)
    builder.fill(GLASS)

    // build roof
    builder.teleportToOrigin()
    builder.move(UP, houseHeight)
    builder.mark()
    builder.move(FORWARD, 1)
    builder.turn(TurnDirection.Right)
    builder.move(BACK, 1)
    let roofLayers = 0;

    if (width % 2 == 0) {
        roofLayers = houseWidth / 2 - 1
    } else {
        roofLayers = houseWidth / 2
    }

    for (let layer = 0; layer <= roofLayers + 1; layer++) {
        builder.mark()
        for (let k = 0; k < 4; k++) {
            builder.move(FORWARD, houseWidth + 2 - layer * 2)
            builder.turn(TurnDirection.Right)
        }
        builder.tracePath(PLANKS_OAK)
        builder.shift(1, 1, -1)
    }

    builder.teleportTo(startPosition)
    builder.move(LEFT, 1)
    for(let i = 0; i < 4; i++) {
        builder.mark()
        builder.shift(width + 4, -2, 3)
        builder.fill(WATER)
        builder.shift(-3, 2, -3)
        builder.turn(TurnDirection.Right)
    }

    // entrance path and bridge
    builder.teleportTo(doorPathPos)
    builder.turn(TurnDirection.Left)
    builder.turn(TurnDirection.Left)
    builder.shift(1, -2, -1)
    builder.mark()
    builder.shift(11, 0, 3)
    builder.fill(STONE_BRICKS)

    let bridgeEndPos = builder.position()

    // entrance
    builder.shift(-3, 1, 1)
    builder.mark()
    builder.shift(-3, 3, -5)
    builder.fill(AIR)

    // Left corner
    builder.move(FORWARD, 1)
    builder.move(LEFT, 1)
    let entrancePos = builder.position()
    builder.mark()
    builder.move(RIGHT, 1)
    builder.move(DOWN, 3)
    builder.tracePath(STONE_BRICKS)

    // right corner
    builder.teleportTo(entrancePos)
    builder.move(LEFT, 3)
    builder.mark()
    builder.move(LEFT, 1)
    builder.move(DOWN, 3)
    builder.tracePath(STONE_BRICKS)

    // bridge walls
    // right
    builder.teleportTo(bridgeEndPos)
    builder.move(UP, 1)
    builder.mark()
    builder.move(BACK, 12)
    builder.tracePath(COBBLESTONE_WALL)

    // left
    builder.move(RIGHT, 3)
    builder.mark()
    builder.move(FORWARD, 12)
    builder.tracePath(COBBLESTONE_WALL)
})

function buildWalls(height: number, width: number) {
    for (let h = 0; h < height; h++) {
        for (let wall = 0; wall < 4; wall++) {
            builder.move(FORWARD, width)
            builder.turn(TurnDirection.Right)
        }
        builder.move(UP, 1)
    }
    builder.tracePath(STONE_BRICKS)
    builder.place(AIR)
    placeBricksOnTop(width)
}

function placeBricksOnTop(width: number) {
    for (let i = 0; i < 4; i++) {
        for (let j = 0; j < width / 2; j++) {
            builder.place(MOSSY_STONE_BRICKS)
            builder.move(FORWARD, 2)
        }
        builder.turn(TurnDirection.Right)
    }
}

function buildTower(height: number) {
    builder.mark()
    builder.shift(3, height, -3)
    builder.fill(STONE_BRICKS)
    builder.teleportToOrigin()

    builder.move(UP, height + 1)
    builder.mark()
    for (let h = 0; h < height / 2; h++) {
        for (let i = 0; i < 4; i++) {
            builder.place(STONE_BRICKS)
            builder.move(FORWARD, 3)
            builder.turn(TurnDirection.Right)
        }
        builder.move(UP, 1)
    }
    builder.tracePath(STONE_BRICKS)
    builder.place(AIR)

    // fill tower flor
    builder.shift(1, -2, -1)
    builder.mark()
    builder.shift(1, 0, -1)
    builder.fill(PLANKS_SPRUCE)
    builder.shift(-2, 2, 2)

    // place single bricks on top of tower
    builder.mark()
    for (let i = 0; i < 4; i++) {
        builder.place(MOSSY_STONE_BRICKS)
        builder.move(FORWARD, 3)
        builder.turn(TurnDirection.Right)
    }
}