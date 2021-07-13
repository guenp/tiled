import io

from ..client import from_config


def serialize_xdi(dataframe, metadata):
    output = io.StringIO()
    output.write("# XDI/1.0 tiled/0.1.0a20\n")
    # TODO validation/formatting of metadata
    for k, v in metadata.items():
        output.write(f"# {k}: {v}\n")
    output.write("# /////////////\n")
    output.write("# generated by tiled\n")
    output.write("# -------------\n")

    # write column labels
    # TODO should we expect the index to be set?
    columns = [dataframe.index.name] + list(dataframe.columns)
    print(columns)
    output.write("# ")
    output.write(" ".join(columns))
    output.write("\n")

    # write data
    dataframe.to_csv(output, header=False)
    return output.getvalue()


def test_xdi_example():
    config = {
        "trees": [
            {
                "tree": "tiled.examples.xas:tree",
                "path": "/",
            },
        ],
        "media_types": {
            "dataframe": {
                "application/x-xdi": "tiled._tests.test_custom_format:serialize_xdi"
            },
        },
        "file_extensions": {"xdi": "application/x-xdi"},
    }
    client = from_config(config)
    buffer = io.BytesIO()
    client["example"].export(buffer, format="xdi")
    actual = bytes(buffer.getbuffer()).decode()
    # TODO A literal character-for-character comparison may be stricter than we
    # want here.
    assert actual == EXPECTED


EXPECTED = """# XDI/1.0 tiled/0.1.0a20
# Column.1: energy eV
# Column.2: i0
# Column.3: itrans
# Column.4: mutrans
# Element.edge: K
# Element.symbol: Cu
# Scan.edge_energy: 8980.0
# Mono.name: Si 111
# Mono.d_spacing: 3.13553
# Beamline.name: 13ID
# Beamline.collimation: none
# Beamline.focusing: yes
# Beamline.harmonic_rejection: rhodium-coated mirror
# Facility.name: APS
# Facility.energy: 7.0
# Facility.xray_source: APS Undulator A
# Scan.start_time: 2001-06-26T22:27:31
# Detector.I0: 10cm  N2
# Detector.I1: 10cm  N2
# Sample.name: Cu
# Sample.prep: Cu metal foil
# GSE.EXTRA: config 1
# /////////////
# generated by tiled
# -------------
# energy i0 itrans mutrans
8779.0,149013.7,550643.089065,-1.3070486
8789.0,144864.7,531876.119084,-1.3006104
8799.0,132978.7,489591.10592,-1.3033816
8809.0,125444.7,463051.104096,-1.3059724
8819.0,121324.7,449969.103983,-1.3107085
8829.0,119447.7,444386.117562,-1.3138152
8839.0,119100.7,440176.091039,-1.3072055
8849.0,117707.7,440448.106567,-1.3195882
8859.0,117754.7,442302.10637,-1.3233895
8869.0,117428.7,441944.116528,-1.3253521
8879.0,117383.7,442810.120466,-1.327693
8889.0,117185.7,443658.11566,-1.3312944
"""
