# Project Athena
'''
Owner: Efstratios Pahis
Contributors:
Description: Various Helpermethods and Attributes specicific to Bayerischer Rundfunk
'''

import re

departments_bayerischer_rundfunk = {"Hauptabteilungen": {
    "HA IT und Medientechnik": {"Abteilungen": {"IT-Basis und Infrastruktur": {"Fachgruppen": ["Server und Basisdienste", "Hardware und Datenspeicherung", "Netwerk und Systemsicherheit", "Enterprise Workplace Solutions", "Energieanlagetechnik", "Asset & Configuration Management"]},
                                                "Mediensysteme": {"Fachgruppen": ["Außentechnik", "FS-Studios und Systeme", "Zentrale AV-Technik", "Trimediale Studios und Systeme", "Zentrale Mediensysteme", "Regionale Studios und Systeme", "Redaktionssysteme"]},
                                                "Businesssysteme und -lösungen": {"Fachgruppen": ["Planungs- und Standardapplikationen", "Businessapplikationen", "IT Solutions"]},
                                                "Planung Infrastrukturtechnologie": {"Fachgruppen": ["Planung Verbreitungstechnik"]}
                                                }},
    "HA Programmdirektion Information": {"Abteilungen": {"Softwareentwicklung und Plattformen (SEP)": {"Fachgruppen": []},
                                                         }},
    "HA Produktionsservice": {"Abteilungen": {"Veranstaltungsservice": {"Fachgruppen": ["Veranstaltungstechnik", "Veranstaltungssicherheit", "Ausstattungsservice"]},
                                              "Kamera": {"Fachgruppen": ["Kamera 1", "Kamera 2"]},
                                              "Audio/Video Engineering": {"Fachgruppen": ["Audio Engineering", "Video Engineering"]},
                                              "Design - und Editingservice": {"Fachgruppen": ["Video- und Grafikdesign", "Editing", "Sounddesign"]},
                                              "Audio/Video Operating": {"Fachgruppen": ["Audio Operating", "Video Operating", "Multimedia Operating"]}
                                              }},
    "HA Verbreitung und Controlling": {"Abteilungen": {"Controlling": {"Fachgruppen": ["Produktionswirtschaft", "Technisches Controlling und Haushalt"]},
                                                       "Senderbetrieb": {"Fachgruppen": ["Betrieb Terrestrik", "Infrastruktur Senderstandorte"]},
                                                       "Entwicklung Programmverbreitung": {"Fachgruppen": ["Systementwicklung"]},
                                                       "Rundfunkversorgung u. Frequenzmanagement": {"Fachgruppen": ["Rundfunkvertriebssysteme", "Rechnertechnik", "Neue Übertragungstechniken"]},
                                                       "Zentrale Betriebstechnik": {"Fachgruppen": ["Internetverbreitung und Multiplexing", "Netzmanagement", "Leitungsnetze und Richtfunk"]}
                                                       }},
    "HA Personal": {"Abteilungen": {"Kein Eintrag": {"Fachgruppen": []}}},
    "HA Planung": {"Abteilungen": {"Investitionsstrategie": {"Fachgruppen": ["Projektportfoliomanagement"]},
                                   "Planung Produktionstechnologie": {"Fachgruppen": ["Planung Zentrale Broadcastsysteme", "Planung Produktionstechnick"]},
                                   "Planung Systemtechnologie": {"Fachgruppen": ["Enterprise Architecture Management"]},
                                   "Planung Infrastrukturtechnologie": {"Fachgruppen": ["Planung Verbreitungstechnik"]}
                                   }},
    "HA Produktionstechnologie": {"Abteilungen": {"Produktionszentren": {"Fachgruppen": ["MCR / SAW", "Wellenhaus", "Aktualitätenzentrum", "Sendeleitung"]},
                                                  "Audio/Video Editing Infrastruktur": {"Fachgruppen": ["A/V Schnittsysteme", "Grafiksysteme"]},
                                                  "Studios und Mobile Produktion": {"Fachgruppen": ["Studios", "Mobile Produktion", "Materialmanagement"]},
                                                  "Dezentrale Produktionsstandorte": {"Fachgruppen": ["Regionen und Ausland", "Produktionsservice Franken"]}
                                                  }},
}}


def clean_department_from_dataset(department: str):
    return "".join(re.findall(r"(.*?)(?:\(.*?\)|$)", department.replace("Abt. ", "").replace("FG ", "").replace(" (Organisationseinheit)", ""))).rstrip()


def get_departments_bayerischer_rundfunk_list():
    list_tmp = list(__get_departments_bayerischer_rundfunk_list_helper(
        departments_bayerischer_rundfunk))
    return [val for val in ([item for sublist in list_tmp for item in sublist if isinstance(sublist, list)] + [val for val in list_tmp if isinstance(val, str)]) if not val == "Hauptabteilungen" and not val == "Abteilungen" and not val == "Fachgruppen"]


def __get_departments_bayerischer_rundfunk_list_helper(_dict):
    for k, v in _dict.items():
        yield k
        if isinstance(v, dict):
            yield from __get_departments_bayerischer_rundfunk_list_helper(v)
        else:
            yield v
