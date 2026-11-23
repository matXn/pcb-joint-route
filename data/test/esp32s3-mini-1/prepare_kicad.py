"""Rebuild the physical GPIO routing input from Espressif's published PADS archive."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.request import urlopen
from zipfile import ZipFile

import pcbnew as pcb


HERE = Path(__file__).resolve().parent
ARCHIVE_URL = 'https://raw.githubusercontent.com/espressif/esp-hardware-design-guidelines/f048d20be54bbd2546af3d83deaec84c95916b12/docs/_static/esp32s3/esp32-s3-mini-1_reference_design.zip'
ASCII_MEMBER = 'ESP32-S3-MINI-1_V1.1_Reference_Design/02_PCB/PCB_ESP32-S3-MINI-1_V1.1_20220704.asc'


def rebuild(archive, directory, cli, case, reference_drc=False):
    if hashlib.sha256(archive.read_bytes()).hexdigest() != case['source_archive_sha256']:
        raise ValueError('Expected the ESP32-S3-MINI-1 V1.1 archive identified in case.json')
    outputs = ['board.kicad_pcb', 'board.kicad_pro']
    if reference_drc:
        outputs.append('reference-drc.json')
    if any((directory / name).exists() for name in outputs):
        raise FileExistsError('Choose a new output directory to avoid replacing an existing board')
    with TemporaryDirectory() as working:
        tmp = Path(working)
        source = tmp/'module.asc'
        with ZipFile(archive) as z:
            source.write_bytes(z.read(ASCII_MEMBER))
        board_path = tmp/'board.kicad_pcb'
        subprocess.run([str(cli),'pcb','import','--format','pads','-o',str(board_path),str(source)],check=True)
        shutil.copyfile(HERE/'board.kicad_pro',tmp/'board.kicad_pro')
        board = pcb.LoadBoard(str(board_path))
        if board.GetCopperLayerCount() != 4:
            raise ValueError('Expected a four-layer module')
        targets = set(case['targets'])
        pads = [p for p in board.GetPads() if p.GetNetname() in targets]
        observed = {(p.GetNetname(), p.GetParentFootprint().GetReference(), p.GetNumber()) for p in pads}
        expected = {(p['net'],p['ref'],p['pad']) for p in case['terminals']}
        if observed != expected or len(pads) != len(expected):
            raise ValueError('The imported pad inventory does not match the published test case')
        if not any(d.GetLayer()==pcb.Edge_Cuts for d in board.GetDrawings()):
            # KiCad 10.0.6 omits the PADS layer-0 BOARD rectangle at U2's origin.
            origin = next(f.GetPosition() for f in board.GetFootprints() if f.GetReference()=='U2')
            w,h = case['board_size_mm']
            corners = [(0,0),(0,-h),(w,-h),(w,0),(0,0)]
            for start,end in zip(corners,corners[1:]):
                line=pcb.PCB_SHAPE(board)
                line.SetShape(pcb.SHAPE_T_SEGMENT)
                line.SetLayer(pcb.Edge_Cuts)
                line.SetWidth(0)
                line.SetStart(origin+pcb.VECTOR2I(*(pcb.FromMM(v) for v in start)))
                line.SetEnd(origin+pcb.VECTOR2I(*(pcb.FromMM(v) for v in end)))
                board.Add(line)
        if reference_drc:
            board.BuildConnectivity()
            pcb.ZONE_FILLER(board).Fill(board.Zones())
            if pcb.SaveBoard(str(board_path),board) is False:
                raise OSError('KiCad could not prepare the reference DRC baseline')
            subprocess.run([str(cli),'pcb','drc','--refill-zones','--format','json',
                            '--severity-error','--severity-warning','-o',str(tmp/'reference-drc.json'),str(board_path)],check=True)
        for item in list(board.GetTracks()):
            if item.GetNetname() in targets:
                board.Delete(item)
        board.BuildConnectivity()
        pcb.ZONE_FILLER(board).Fill(board.Zones())
        if pcb.SaveBoard(str(board_path),board) is False:
            raise OSError('KiCad could not save the blank test board')
        check=pcb.LoadBoard(str(board_path))
        if any(item.GetNetname() in targets for item in check.GetTracks()):
            raise ValueError('The rebuilt board contains target copper')
        directory.mkdir(parents=True,exist_ok=True)
        for name in outputs:
            shutil.copyfile(tmp/name,directory/name)
    print(directory/'board.kicad_pcb')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive',type=Path,help='Use a locally downloaded official ZIP')
    parser.add_argument('--out',type=Path,required=True,help='Output directory for the blank KiCad project')
    parser.add_argument('--kicad-cli',type=Path,help='KiCad 10 CLI executable')
    parser.add_argument('--reference-drc',action='store_true',help='Also export the original DRC report for evaluation only')
    args=parser.parse_args()
    cli=args.kicad_cli or shutil.which('kicad-cli')
    if not cli:
        bin_dir=Path(sys.executable).parent
        cli=next((p for p in (bin_dir/'kicad-cli.exe',bin_dir/'kicad-cli') if p.is_file()),None)
    if not cli:
        parser.error('Pass --kicad-cli or add kicad-cli to PATH')
    case=json.loads((HERE/'case.json').read_text(encoding='utf8'))
    with TemporaryDirectory() as tmp:
        archive=args.archive
        if archive is None:
            archive=Path(tmp)/'esp32-s3-mini-1.zip'
            with urlopen(ARCHIVE_URL,timeout=60) as response, archive.open('wb') as target:
                shutil.copyfileobj(response,target)
        rebuild(archive,args.out,cli,case,args.reference_drc)


if __name__=='__main__':
    main()
