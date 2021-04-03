import argparse
import sys
import os
import export.texts
import export.rooms
import patches.chest
import patches.droppedKey
import patches.heartPiece
import patches.health
import patches.overworld
import patches.seashell
import patches.bank3e
import patches.bank3f
import patches.owl
import patches.core
import patches.aesthetics
import assembler
import roomEditor

from romTables import ROMWithTables


def exportRomData(rom, path):
    print("Exporting data")
    export.texts.exportTexts(rom, os.path.join(path, "dialogs.txt"))
    export.rooms.exportRooms(rom, os.path.join(path, "rooms"))


def importRomData(rom, path):
    print("Importing data")
    export.rooms.importRooms(rom, os.path.join(path, "rooms"))


def main(argv):
    parser = argparse.ArgumentParser(description='Toolbox!')
    parser.add_argument('input_filename', metavar='input rom', type=str,
        help="Rom file to use as input.")
    parser.add_argument('--path', dest="path", type=str, required=True,
        help="Path to use to for output or input data.")
    parser.add_argument('--export', dest="export", action="store_true")
    parser.add_argument('--build', dest="build", type=str)
    args = parser.parse_args(argv)

    os.makedirs(args.path, exist_ok=True)

    assembler.resetConsts()
    expanded_inventory = False
    if expanded_inventory:
        assembler.const("INV_SIZE", 16)
        assembler.const("wHasFlippers", 0xDB3E)
        assembler.const("wHasMedicine", 0xDB3F)
        assembler.const("wTradeSequenceItem", 0xDB40)
        assembler.const("wSeashellsCount", 0xDB41)
    else:
        assembler.const("INV_SIZE", 12)
        assembler.const("wHasFlippers", 0xDB0C)
        assembler.const("wHasMedicine", 0xDB0D)
        assembler.const("wTradeSequenceItem", 0xDB0E)
        assembler.const("wSeashellsCount", 0xDB0F)
    assembler.const("wGoldenLeaves", 0xDB42)  # New memory location where to store the golden leaf counter
    assembler.const("wCollectedTunics", 0xDB6D)  # Memory location where to store which tunic options are available
    assembler.const("wCustomMessage", 0xC0A0)

    # We store the link info in unused color dungeon flags, so it gets preserved in the savegame.
    assembler.const("wLinkSyncSequenceNumber", 0xDDF6)
    assembler.const("wLinkStatusBits", 0xDDF7)
    assembler.const("wLinkGiveItem", 0xDDF8)
    assembler.const("wLinkGiveItemFrom", 0xDDF9)
    assembler.const("wLinkSendItemRoomHigh", 0xDDFA)
    assembler.const("wLinkSendItemRoomLow", 0xDDFB)
    assembler.const("wLinkSendItemTarget", 0xDDFC)
    assembler.const("wLinkSendItemItem", 0xDDFD)

    assembler.const("wZolSpawnCount", 0xDE10)
    assembler.const("wCuccoSpawnCount", 0xDE11)

    rom = ROMWithTables(args.input_filename)
    if not patches.bank3e.hasBank3E(rom):
        # Apply early patches that modify things that we need before export
        patches.chest.fixChests(rom)
        patches.droppedKey.fixDroppedKey(rom)
        patches.heartPiece.fixHeartPiece(rom)
        patches.health.upgradeHealthContainers(rom)
        patches.seashell.fixSeashell(rom)
        patches.seashell.upgradeMansion(rom)
        patches.overworld.patchOverworldTilesets(rom)
        patches.bank3e.addBank3E(rom, b'')
        patches.bank3f.addBank3F(rom)
        patches.owl.removeOwlEvents(rom)
        patches.core.bugfixBossroomTopPush(rom)
        patches.core.bugfixWrittingWrongRoomStatus(rom)
        patches.aesthetics.allowColorDungeonSpritesEverywhere(rom)

        # We need to fix up a few vanilla room warp orders, as updating these rooms changes the order of the warps
        re = roomEditor.RoomEditor(rom, 0x0A1)
        re.objects = [obj for obj in re.objects if not isinstance(obj, roomEditor.ObjectWarp)] + list(reversed(re.getWarps()))
        re.store(rom)
        # TODO: room 0x01D

    if args.export:
        exportRomData(rom, args.path)
    if args.build:
        importRomData(rom, args.path)
        patches.aesthetics.updateSpriteData(rom)
        rom.save(args.build)


if __name__ == "__main__":
    main(sys.argv[1:])
