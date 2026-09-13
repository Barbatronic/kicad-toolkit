#!/usr/bin/env python3
"""Genere la librairie de blocs de conception Barbatronic.

Chaque bloc est un dossier <Nom>.kicad_block contenant <Nom>.kicad_sch et
<Nom>.json, dans une librairie <Lib>.kicad_blocks, comme attendu par KiCad.
"""
import json, os, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kicad_sch import SymbolCache, Schematic

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(ROOT, "packages/barbatronic-kicad-toolkit/resources/design-blocks",
                   "Barbatronic.kicad_blocks")

FP = {
    "R_0805": "Resistor_SMD:R_0805_2012Metric",
    "R_1206": "Resistor_SMD:R_1206_3216Metric",
    "C_0805": "Capacitor_SMD:C_0805_2012Metric",
    "C_1206": "Capacitor_SMD:C_1206_3216Metric",
    "LED_0805": "LED_SMD:LED_0805_2012Metric",
    "CP_5x5.4": "Capacitor_THT:CP_Radial_D5.0mm_P2.50mm",
    "SOT223": "Package_TO_SOT_SMD:SOT-223-3_TabPin2",
    "SIP3": "Converter_DCDC:Converter_DCDC_RECOM_R-78E-0.5_THT",
    "TERM2": "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2_1x02_P5.00mm_Horizontal",
    "PIN3": "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",
    "PIN4": "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical",
    "SMA": "Diode_SMD:D_SMA",
    "SW_SMD": "Button_Switch_SMD:SW_SPST_B3U-1000P",
}


def bloc_alim_3v3(c):
    """5 V vers 3,3 V par regulateur lineaire."""
    s = Schematic("Alim_LDO_3V3", c)
    u = s.place("Regulator_Linear:AMS1117-3.3", (127, 76.2), value="AMS1117-3.3",
                footprint=FP["SOT223"])
    s.place("power:+5V", (109.22, 68.58))
    s.place("power:+3V3", (144.78, 68.58))
    s.route(u("3"), (109.22, 76.2), (109.22, 68.58))
    s.route(u("2"), (144.78, 76.2), (144.78, 68.58))

    cin = s.place("Device:C_Polarized", (104.14, 83.82), value="10uF", footprint=FP["CP_5x5.4"])
    cout = s.place("Device:C_Polarized", (149.86, 83.82), value="10uF", footprint=FP["CP_5x5.4"])
    cb = s.place("Device:C", (135.89, 83.82), value="100nF", footprint=FP["C_0805"])
    s.route(cin("1"), (104.14, 76.2))
    s.junction((109.22, 76.2)) if False else None
    s.route((104.14, 76.2), (109.22, 76.2))
    s.junction((109.22, 76.2))
    s.route(cout("1"), (149.86, 76.2), (144.78, 76.2))
    s.junction((144.78, 76.2))
    s.route(cb("1"), (135.89, 76.2), (144.78, 76.2))

    gnd = (127, 96.52)
    s.place("power:GND", (127, 96.52))
    s.route(u("1"), (127, 96.52))
    s.route(cin("2"), (104.14, 93.98), (127, 93.98))
    s.route(cout("2"), (149.86, 93.98), (127, 93.98))
    s.route(cb("2"), (135.89, 93.98))
    s.junction((127, 93.98))
    s.junction((135.89, 93.98))
    s.route((127, 93.98), (127, 96.52))
    s.text((101.6, 63.5), "Regulateur 5 V vers 3,3 V, 1 A max, decouplage en entree et en sortie")
    return s, {
        "description": "Regulateur lineaire 5 V vers 3,3 V (AMS1117) avec decouplage",
        "keywords": "alimentation regulateur LDO 3V3 AMS1117 decouplage",
    }


def bloc_entree_alim(c):
    """Entree d'alimentation protegee contre l'inversion de polarite."""
    s = Schematic("Entree_Alim_Protegee", c)
    j = s.place("Connector:Screw_Terminal_01x02", (99.06, 78.74), value="Entree 7-24 V",
                footprint=FP["TERM2"])
    f = s.place("Device:Fuse", (114.3, 78.74), value="2 A", angle=90,
                footprint="Fuse:Fuse_1206_3216Metric")
    d = s.place("Device:D_Schottky", (129.54, 78.74), value="SS34", footprint=FP["SMA"])
    cbulk = s.place("Device:C_Polarized", (142.24, 86.36), value="100uF/35V",
                    footprint=FP["CP_5x5.4"])

    s.route(j("1"), (110.49, 78.74))
    s.route((118.11, 78.74), (125.73, 78.74))
    s.route(d("2"), (142.24, 78.74))
    s.route(cbulk("1"), (142.24, 78.74))
    s.junction((142.24, 78.74))
    s.route((142.24, 78.74), (152.4, 78.74))
    s.label((152.4, 78.74), "VIN", glob=True)

    s.place("power:GND", (142.24, 96.52))
    s.route(cbulk("2"), (142.24, 96.52))
    s.route(j("2"), (104.14, 81.28), (104.14, 93.98), (142.24, 93.98))
    s.junction((142.24, 93.98))
    s.text((96.52, 66.04), "Entree d'alimentation : fusible, diode anti-inversion, condensateur reservoir")
    return s, {
        "description": "Entree d'alimentation protegee : fusible, diode anti-inversion, reservoir",
        "keywords": "alimentation entree protection fusible diode polarite inversion bornier",
    }


def bloc_i2c(c):
    """Bus I2C avec resistances de tirage et connecteur."""
    s = Schematic("Bus_I2C", c)
    r1 = s.place("Device:R", (121.92, 78.74), value="4k7", footprint=FP["R_0805"])
    r2 = s.place("Device:R", (132.08, 78.74), value="4k7", footprint=FP["R_0805"])
    s.place("power:+3V3", (127, 66.04))
    s.route(r1("1"), (121.92, 71.12), (127, 71.12), (127, 66.04))
    s.route(r2("1"), (132.08, 71.12), (127, 71.12))
    s.junction((127, 71.12))

    s.route(r1("2"), (121.92, 88.9), (109.22, 88.9))
    s.label((109.22, 88.9), "SDA", glob=True)
    s.route(r2("2"), (132.08, 93.98), (109.22, 93.98))
    s.label((109.22, 93.98), "SCL", glob=True)

    j = s.place("Connector_Generic:Conn_01x04", (149.86, 88.9), value="I2C", footprint=FP["PIN4"])
    s.route(j("1"), (139.7, 86.36), (139.7, 71.12), (127, 71.12))
    s.route(j("2"), (144.78, 88.9), (139.7, 88.9))
    s.junction((139.7, 88.9)) if False else None
    s.route(j("3"), (144.78, 93.98), (132.08, 93.98))
    s.junction((132.08, 93.98))
    s.place("power:GND", (144.78, 101.6))
    s.route(j("4"), (144.78, 96.52), (144.78, 101.6))
    s.text((106.68, 63.5), "Bus I2C : tirages 4k7 vers 3,3 V et connecteur 4 points")
    return s, {
        "description": "Bus I2C avec resistances de tirage 4k7 et connecteur 4 points",
        "keywords": "I2C SDA SCL bus tirage pullup connecteur capteur",
    }


def bloc_servos(c):
    """Quatre sorties servomoteur sur alimentation dediee."""
    s = Schematic("Servos_x4", c)
    cbulk = s.place("Device:C_Polarized", (104.14, 88.9), value="470uF/16V",
                    footprint=FP["CP_5x5.4"])
    s.route(cbulk("1"), (104.14, 78.74), (111.76, 78.74))
    s.label((111.76, 78.74), "V_SERVO", glob=True)
    s.place("power:GND", (104.14, 99.06))
    s.route(cbulk("2"), (104.14, 99.06))

    y = 78.74
    for i in range(4):
        j = s.place("Connector_Generic:Conn_01x03", (149.86, y + 2.54), value=f"Servo {i + 1}",
                    footprint=FP["PIN3"])
        s.route(j("1"), (137.16, y), (129.54, y))
        s.label((129.54, y), f"SERVO{i + 1}", glob=True)
        s.route(j("2"), (142.24, y + 2.54), (137.16, y + 2.54))
        s.label((137.16, y + 2.54), "V_SERVO", glob=True)
        g = s.place("power:GND", (142.24, y + 10.16))
        s.route(j("3"), (142.24, y + 5.08), (142.24, y + 10.16))
        y += 20.32
    s.text((101.6, 68.58), "Quatre sorties servomoteur, alimentation dediee et reservoir commun")
    return s, {
        "description": "Quatre sorties servomoteur avec alimentation dediee et condensateur reservoir",
        "keywords": "servo servomoteur sortie PWM robotique connecteur alimentation",
    }


def bloc_led_etat(c):
    """LED d'etat sur sortie logique."""
    s = Schematic("LED_Etat", c)
    r = s.place("Device:R", (127, 76.2), value="1k", angle=90, footprint=FP["R_0805"])
    d = s.place("Device:LED", (139.7, 76.2), value="Verte", footprint=FP["LED_0805"])
    s.route((111.76, 76.2), r("1"))
    s.label((111.76, 76.2), "LED_ETAT", glob=True)
    s.route(r("2"), d("1"))
    s.place("power:GND", (149.86, 83.82))
    s.route(d("2"), (149.86, 76.2), (149.86, 83.82))
    s.text((109.22, 68.58), "LED d'etat : 1 k pour environ 2 mA sous 3,3 V")
    return s, {
        "description": "LED d'etat avec resistance de limitation, pilotee par une sortie logique",
        "keywords": "LED etat temoin indicateur resistance sortie logique",
    }


def bloc_bouton(c):
    """Bouton poussoir avec tirage et filtrage anti-rebond."""
    s = Schematic("Bouton_Poussoir", c)
    r = s.place("Device:R", (127, 71.12), value="10k", footprint=FP["R_0805"])
    sw = s.place("Switch:SW_Push", (127, 88.9), value="Bouton", footprint=FP["SW_SMD"])
    cd = s.place("Device:C", (139.7, 86.36), value="100nF", footprint=FP["C_0805"])

    s.place("power:+3V3", (127, 60.96))
    s.route(r("1"), (127, 60.96))
    s.route(r("2"), (127, 83.82))
    s.route(sw("1"), (121.92, 88.9), (121.92, 83.82), (127, 83.82))
    s.junction((127, 83.82))
    s.route((127, 83.82), (147.32, 83.82))
    s.label((147.32, 83.82), "BOUTON", glob=True)
    s.route(cd("1"), (139.7, 83.82))
    s.junction((139.7, 83.82))

    s.place("power:GND", (132.08, 99.06))
    s.route(sw("2"), (132.08, 88.9), (132.08, 96.52))
    s.route(cd("2"), (139.7, 96.52), (132.08, 96.52))
    s.junction((132.08, 96.52))
    s.route((132.08, 96.52), (132.08, 99.06))
    s.text((119.38, 55.88), "Bouton poussoir : tirage 10 k et filtrage anti-rebond 100 nF")
    return s, {
        "description": "Bouton poussoir avec resistance de tirage et filtrage anti-rebond",
        "keywords": "bouton poussoir interrupteur tirage pullup anti-rebond debounce",
    }


BLOCS = [bloc_alim_3v3, bloc_entree_alim, bloc_i2c, bloc_servos, bloc_led_etat, bloc_bouton]


def main():
    cache = SymbolCache()
    if os.path.isdir(LIB):
        shutil.rmtree(LIB)
    os.makedirs(LIB)
    for fn in BLOCS:
        sch, meta = fn(cache)
        d = os.path.join(LIB, sch.name + ".kicad_block")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, sch.name + ".kicad_sch"), "w", encoding="utf-8") as f:
            f.write(sch.render())
        meta["fields"] = {}
        with open(os.path.join(d, sch.name + ".json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=1)
        print(f"  {sch.name}")
    print(f"{len(BLOCS)} blocs ecrits dans {os.path.relpath(LIB, ROOT)}")


if __name__ == "__main__":
    main()
