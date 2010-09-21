#!/usr/bin/env python

import os.path
import subprocess

working_surveys = [
    ( "Fiets- en Bromfietsbedrijf", "Ambachten", "Hoofdbedrijfschap Ambachten (HBA)", 19, True),
    ( "Algemene MKB RI&E", "MKB", "MKB", 1, True),
    ( "Betonmortelfabrikanten", "Betonmortelfabrikanten", "VOBN", 89, True),
    ( "Openbare Bibliotheken", "Bibliotheken", "Werkgeversvereniging Openbare Bibliotheken", 53, True),
    ( "Boekhandel en Kantoorvakhandel", "Boekhandel", "NBB, Nederlandse Boekverkopers Bond en Novaka Organisatie Kantoorbranche", 48, True),
    ( "Handel in bouwmaterialen", "Bouwmaterialen", "HIBIN", 58, True),
    ( "Autoverhuurbedrijf", "Bovag", "Bovag", 80, False),
    ( "Autowasbedrijf", "Bovag", "Bovag", 75, False),
    ( "Caravanbedrijf", "Bovag", "Bovag", 81, False),
    ( "Fietsbedrijf", "Bovag", "Bovag", 82, False),
    ( "Motorenrevisiebedrijf", "Bovag", "Bovag", 83, False),
    ( "Motorfietsbedrijf", "Bovag", "Bovag", 84, False),
    ( "Truckerdealerbedrijf", "Bovag", "Bovag", 78, False),
    ( "Conferentiecentra Facilities", "Conferentiecentra", "Kasteel De Vanenburg", 99, True),
    ( "Dranken en wijn", "Dranken", "Productschap Dranken en Productschap Wijn", 33, True),
    ( "Fitnesscentra", "Fitnesscentra", "Fitvak", 9, True),
    ( "Fotovakhandel", "Fotovakhandel", "Stichting Nederlandse Fotovakhandel", 107, True),
    ( "Fysiotherapiepraktijken", "Fysiotherapie", "Koninklijk Nederlands Genootschap voor Fysiotherapie (KNGF)", 31, True),
    ( "Houtverwerkende Industrie", "Houtverwerking", "Sociaal Fonds voor de Houtverwerkende Industrie", 61, True),
    ( "Banden en wielenbranche", "banden-wielen", "Vereniging VACO ism CNV Dienstenbond, FNV Bondgenoten en De Unie", 51, True),
    ( "Groothandel in Bloemen en Planten", "bloemen-planten", "VGB", 109, True),
    ( "Binnenscheepvaart", "Binnenscheepvaart", "Kantoor binnenvaart en Centraal Bureau voor de Rijn- en Binnenvaart", 39, True),
    ( "Checklist gezondheidsrisicos", "Checklist", "SZW", 10, True),
    ( "Marktonderzoek", "Marktonderzoek", "Markt Onderzoek Associatie", 54, True),
    ( "Meubel en Houtsector", "meubel-hout", "Centrale Bond van Meubelfabrikanten (CBM)", 55, True),
    ( "Mode, Schoenen en sportdetailhandel", "Mitex", "Mitex", 3, True),
    ( "Mode en Interieurindustrie", "Modint", "Modint", 50, True),
    ( "Ontwerpers", "Ontwerpers", "BNO", 106, True),
    ( "Optiekbedrijven", "Optiekbedrijven", "NUVO", 4, True),
    ( "Reisbranche", "Reisbranche", "ANVR", 14, True),
    ( "Reprobedrijven", "Reprobedrijven", "Vereniging Repro Nederland", 59, True),
    ( "Slagerbedrijf", "Slagerbedrijf", "Koninklijke Nederlandse Slagersorganisatie", 69, True),
    ( "Sloopaannemers", "Sloopaannemers", "Vereniging van Sloopaannemers", 57, True),
    ( "Akkerbouw en Vollegrondsgroenteteelt", "Stigas", "Stigas", 30, True),
    ( "Bloembollenteelt, -handel en -broeierij", "Stigas", "Stigas / LTO", 46, True),
    ( "Bomen en vaste planten teelt", "Stigas", "Stigas", 65, True),
    ( "Bos en Natuur", "Stigas", "Stigas", 66, True),
    ( "Fruitteelt", "Stigas", "Stigas", 64, True),
    ( "Glastuinbouw", "Stigas", "Stigas", 16, True),
    ( "Hoveniers en Groenvoorzieners", "Stigas", "Stigas", 15, True),
    ( "Mechanisch Loonwerk", "Stigas", "Stigas", 20, True),
    ( "Melkveehouderij", "Stigas", "Stigas", 28, True),
    ( "Pluimveehouderij", "Stigas", "Stigas", 37, True),
    ( "Varkenshouderij", "Stigas", "Stigas", 29, True),
    ( "Tabaksdetailhandel", "Tabaksdetailhandel", "NSO", 11, True),
    ( "Tankstations Beta", "Tankstations", "BETA", 7, True),
    ( "Timmerfabrieken (Tifa)", "Timmerindustrie", "Sociaal fonds voor de timmerindustrie", 94, True),
    ( "Visverwerkende industrie", "Vis", "Productschap Vis", 77, True),
    ( "Vlakglasbranche", "Vlakglas", "Glas Branche Organisatie (GBO)", 104, True),
    ( "Vrijwilligers", "Vrijwilligers", "CIVIQ/ NOV", 47, True),
    ( "Zorgboerderijen", "Zorgboerderijen", "Steunpunt Landbouw & Zorg", 45, True),
    ( "Uitvaartondernemingen", "Uitvaartondernemingen", "NUVU", 5, True),
    ( "Takel en Bergingsbedrijf", "takel-berging", "VBS", 100, True),
    ( "Rijscholen", "Bovag", "Bovag", 79, True),
    ( "Conferentiecentra Hospitality", "Conferentiecentra", "Kasteel De Vanenburg", 101, True),
    ( "Dierenartsen", "Dierenartsen", "Koninklijke Nederlandse Maatschappij voor Dierengeneeskunde", 103, True),
    ( "Dierenpensions", "Divebo", "Divebo", 108, True),
    ( "Uitgeverijen", "Uitgeverijen", "BTB Uitgeverijen", 44, True),
    ( "Groothandel in Levensmiddelen", "Levensmiddelen", "Vakcentrum Levensmiddelen", 88, True),
    ( "Horeca", "Horeca", "Bedrijfschap Horeca en Catering", 13, True),
    ( "Groen en Tuinbranche", "Tuinbranche", "Tuinbranche Nederland", 93, True),
    ( "Autobedrijf-Algemeen", "Bovag", "Bovag", 22, True),
    ( "Autodealerbedrijven", "Bovag", "Bovag", 23, True),
    ( "Recycling Breken en Sorteren", "Recycling", "Branchevereniging Recycling Breken en Sorteren (BRBS)", 67, True),
    ( "Paardenhouderij", "Paardenhouderij", "Federatie van Nederlandse Ruitersportcentra (FNRS)", 85, True),
    ( "Drogisterij en Parfumeriedetailhandel", "Drogisterij", "KNDB & CBD", 12, True),
    ( "Ambulante Handel", "Detailhandel", "CVAH/ Hoofdbedrijfschap Detailhandel (HBD)", 70, True),
    ( "Bakkerijen", "Akkerbouw", "Hoofd Productschap Akkerbouw", 92, True),
    ( "Elektrotechnische detailhandel", "Elektrotechnisch", "Uneto VNI", 111, True),
    ( "Houthandel VVNH", "Houthandel", "Vereniging Van Nederlandse Houtondernemingen (VVNH)", 90, True),
    ( "Taxibedrijven", "Taxi", "Sociaal Fonds Taxi", 42, True),
    ( "Voertuigdemontagebedrijven", "Voertuigdemontage", "Stiba", 105, True),
    ( "Timmerindustrie", "Timmerindustrie", "Sociaal fonds voor de timmerindustrie", 95, True),
    ( "Paddenstoelenteelt", "Stigas", "Stigas", 63, True),
    ( "Dierenspeciaalzaken", "Divebo", "Divebo", 110, True),
    ( "Gewasbeschermingsmiddelen", "Gewasbescherming", "Vereniging AGRODIS", 52, True),
    ( "Universitair Medische Centra / Academische Ziekenhuizen", "NFU", "NFU, Arboconvenant Academische Ziekenhuizen", 35, True),
    ( "Verloskundigen", "knov", "KNOV",  113, False ),
    ]

pending_surveys = [
    ( "Contractcatering", "Contractcatering", "Stichtingen ContractCatering", 71, True),
    ( "Home Entertainment Retailers", "Entertainment", "Nederlandse Vereniging van Entertainment Retailers (NVER)", 86, True),
    ( "Levensmiddelendetailhandel", "Levensmiddelen", "Vakcentrum Levensmiddelen", 72, True),
    ( "Kottervisserij", "Vis", "Productschap Vis", 34, True),
    ( "Visdetailhandel", "Vis", "Productschap Vis", 2, True),
    ]

colours = {
        'ambachten': ('#e5efff', '#b86400'),
        'banden-wielen': ('#ffffff', '#ffffff'),
        'bloemen-planten': ('#ffffff', '#aac52b'),
        'boekhandel': ('#c4c4c4', '#d25bb8'),
        'bovag': ('#ffffff', '#ffc814'),
        'checklist': ('#ffffff', '#ff5c5c'),
        'dierenartsen': ('#ffffff', '#3a0094'),
        'divebo': ('#ffcccc', '#ff0f43'),
        'dranken': ('#ffffff', '#bababa'),
        'drogisterij': ('#ffe8b8', '#2d8795'),
        'fotovakhandel': ('#ffffff', '#ff6c24'),
        'meubel-hout': ('#f5f5f5', '#a61717'),
        'modint': ('#f5f6ff', '#ff813d'),
        'optiekbedrijven': ('#ffffff', '#b4e4e2'),
        'reisbranche': ('#e9edfb', '#ff1105'),
        'slagerbedrijf': ('#f0f1ff', '#ff8733'),
        'stigas': ('#f7ffd6', '#573400'),
        'takel-berging': ('#ffffff', '#ffffff'),
        'tuinbranche': ('#ffffff', '#14d600'),
        'uitvaartondernemingen': ('#f5f5f5', '#286234'),
        'vlakglas': ('#ebecff', '#ffe829'),
        'vrijwilligers': ('#e2f4fd', '#902761'),
        }

surveys = working_surveys + pending_surveys

devnull=open("/dev/null", "w")

for (name, login, sector, index, publish) in working_surveys:
    login=login.lower()
    logo="data/%s.png" % index
    input="data/%s.xml" % index
    command=["bin/instance", "run", "src/Euphorie/euphorie/deployment/commands/xmlimport.py",
            "--country=nl", "--login=%s" % login, "--sector=%s" % sector,
            "--name=%s" % name, "--version-name=Standaard",
            ]
    print "Importing %s - %s" % (index, name)
    if os.path.isfile(logo):
        print "  with logo"
        command.append("--logo=%s" % logo)
    if login in colours:
        print "  with colours"
        command.append("--main-colour=%s" % colours[login][0])
        command.append("--support-colour=%s" % colours[login][1])
    if publish:
        print "  and publishing"
        command.append("--publish")
    command.append(input)

    popen=subprocess.Popen(command, stderr=devnull)
    popen.wait()

