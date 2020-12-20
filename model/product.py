class Product:
    def __init__(self, name: str, categories: list, online_status: str, long_description: str, long_description_mm: str,
                 marketing_text_mm: str, short_description: str, short_description_mm: str, categories_predicted: list):
        self.name: str = self.convert_nan_to_empty_string(name)
        self.online_status: str = self.convert_nan_to_empty_string(online_status)
        self.long_description: str = self.convert_nan_to_empty_string(long_description)
        self.long_description_mm: str = self.convert_nan_to_empty_string(long_description_mm)
        self.marketing_text_mm: str = self.convert_nan_to_empty_string(marketing_text_mm)
        self.short_description: str = self.convert_nan_to_empty_string(short_description)
        self.short_description_mm: str = self.convert_nan_to_empty_string(short_description_mm)

        self.categories: list = categories
        self.categories_predicted = categories_predicted
        self.categories_id = []
        self.categories_names = []
        self.categories_parent_id = []
        self.categories_parent_name = []

        self.id_2_name = {'': "NO_CATEGORY_FOUND", '202': 'TV & Audio', '203': 'Fernseher', '204': '3D-Fernseher',
                          '205': 'LED- & LCD-Fernseher',
                          '206': 'Plasma Fernseher', '213': 'LÖSCHEN - Heimkino Leinwände', '696': 'QLED',
                          '898': 'OLED-TVs', '789': 'Curved-TVs', '20566': 'Zubehör TV',
                          '207': 'TV-Kabel & Stromversorgung', '208': 'Universalfernbedienungen',
                          '209': 'Pflege & Schutz', '210': 'Netzwerke & CI-Module', '211': 'LED-Beleuchtung',
                          '212': 'TV-Tastaturen & USB-Zubehör', '691': 'Wandhalterungen', '3678': 'TV-Festplatten',
                          '3122': 'TV-Karten', '6557': 'DVB-T Stick', '4500': '3D-Brillen',
                          '1815': 'Professional Shop Display', '4888': 'LÖSCHEN - Überspannungsschutz',
                          '214': 'TV- & Multimediamöbel', '215': 'Decken- & Wandhalterungen',
                          '216': 'Stand- & Tischfüße', '217': 'Drehteller', '218': 'Multimedia-Möbel',
                          '219': 'Heimkino Leinwände', '220': 'Kabelkanäle', '221': 'Fernseher LED-Beleuchtung',
                          '222': 'Heimkino Systeme', '223': '2.1 Systeme', '224': '5.1 Systeme', '225': 'Soundbars',
                          '226': 'Heimkino Kompaktanlagen', '227': 'Funk Heimkinosystem', '228': 'Jukeboxen',
                          '787': 'Soundbase', '229': 'DVD-Player & Blu-ray-Player',
                          '230': 'LÖSCHEN - 3D-Blu-ray-Player', '231': 'Blu-ray-Player', '232': 'DVD-Player',
                          '233': 'Blu-ray-Recorder', '234': 'DVD-Recorder', '235': 'Tragbarer DVD-Player',
                          '236': 'Tragbarer DVD-/Blu-ray-Player', '237': 'Multimedia-Player',
                          '240': 'Tastaturen & USB-Zubehör', '692': 'UHD-Blu-ray-Recorder',
                          '2850': 'LÖSCHEN - Videokassetten', '11234': 'UHD-Blu-ray-Player',
                          '2567': 'Zubehör DVD-/Blu-ray-Player', '238': 'HDMI Kabel & Zubehör',
                          '239': 'Universalfernbedienungen', '10040': '3D-Brillen', '241': 'Beamer', '242': '3D-Beamer',
                          '243': 'Full HD-Beamer', '244': 'HD ready-Beamer', '245': 'Mini-Beamer',
                          '246': 'Multifunktions-Beamer', '3501': 'Zubehör Beamer', '247': 'Heimkino Leinwände',
                          '248': 'Kabel & Stromversorgung', '249': 'Universalfernbedienungen', '250': 'Halterungen',
                          '3500': '3D-Brillen', '4300': 'UHD 4K-Beamer', '251': 'HiFi Komponenten & Anlagen',
                          '252': 'AV-Receiver', '253': 'Netzwerk-Player', '254': 'HiFi-Tuner', '255': 'Vollverstärker',
                          '256': 'Kassettendeck', '257': 'Plattenspieler & Tonabnehmersysteme',
                          '258': 'Hifi Kabel & Steckdosen', '788': 'Kompaktanlagen & Audiosysteme', '765': 'Jukeboxen',
                          '4561': 'HiFi-CD-Player', '259': 'Lautsprecher', '260': 'Funklautsprecher',
                          '261': 'Regallautsprecher', '262': 'Standlautsprecher', '263': 'Lautsprecher-Sets',
                          '264': 'Subwoofer', '265': 'Outdoorlautsprecher', '266': 'Center Lautsprecher',
                          '267': 'Wandlautsprecher', '268': 'Adapter & Kabel', '269': 'Halterungen & Ständer',
                          '784': 'Streaming Lautsprecher', '270': 'SAT, Kabel & DVB-T',
                          '271': 'Satellitenanlagen Single', '272': 'Satellitenanlagen Twin',
                          '273': 'Satellitenanlagen Quad', '274': 'SAT Receiver Single', '275': 'SAT Receiver Twin',
                          '276': 'Festplatten-Receiver', '277': 'DVB-T', '278': 'Zimmerantennen',
                          '279': 'Kabel Receiver', '280': 'Mobile SAT-Anlagen', '281': 'SAT-IP Receiver',
                          '283': 'CI-Module & Netzwerke', '290': 'Zubehör SAT/Kabel/DVB-T', '282': 'Adapter & Kabel',
                          '284': 'Antennen- & TV-Zubehör', '1629': 'HD DVB-T2 Receiver',
                          '285': 'Mp3-Player & Mp4-Player', '286': 'Mp3-Player & Mp4-Player', '287': 'Apple iPod',
                          '289': 'CD-Player & Discmans', '292': 'Halterungen & Ständer',
                          '4211': 'Zubehör Mp3-/Mp4-Player', '288': 'App-Zubehör',
                          '291': 'Taschen, Cover & Cases (MP3)', '293': 'Schutzfolien', '294': 'Stromversorgung',
                          '295': 'HiFi-Adapter & Spezialzubehör', '296': 'Docking-Stations',
                          '297': 'Airplay Docking-Stations', '298': 'Wireless WiFi',
                          '299': 'Bluetooth Docking-Stations', '300': 'Klinkenstecker Docking-Stations',
                          '301': 'Apple Docking-Stations', '302': 'Android Docking-Stations', '303': 'Radios',
                          '304': 'Internetradios', '305': 'Radiowecker & Uhrenradios', '306': 'Weltempfänger',
                          '307': 'Radiorecorder', '308': 'DAB+ Radios', '309': 'Küchenradios', '310': 'Radiogeräte',
                          '311': 'Kopfhörer', '312': 'Bluetooth-Kopfhörer', '313': 'Funk-Kopfhörer',
                          '314': 'HiFi-Kopfhörer', '315': 'In-Ear-Kopfhörer', '749': 'Sport-Kopfhörer',
                          '750': 'Kinderkopfhörer', '5698': 'True Wireless Kopfhörer', '1993': 'Kopfhörer-Zubehör',
                          '316': 'DJ Equipment & Musikinstrumente', '317': 'Audio Interfaces', '318': 'DJ CD-Player',
                          '319': 'Plattenspieler', '320': 'Effektgeräte', '321': 'Kopfhörer',
                          '322': 'Studio-/PA-Monitore', '323': 'Recording', '324': 'DJ-Mixer & DJ-Konsolen',
                          '325': 'Keyboards', '326': 'DJ-Controller', '327': 'Jukebox', '328': 'Musikinstrumente',
                          '329': 'DJ-Zubehör', '330': 'Car Hifi', '331': 'Autoradios & Moniceiver',
                          '332': 'Auto Lautsprecher', '333': 'Adapter & Kabel', '10039': 'Verstärker',
                          '334': 'Apple & Zubehör', '335': 'App-Zubehör',
                          '336': 'Taschen, Cover & Cases (Apple - TV&Audio)', '337': 'Halterungen & Ständer',
                          '338': 'Headsets & Kopfhörer', '340': 'Schutzfolien', '342': 'Spezialzubehör',
                          '810': 'Apple iPod', '1476': 'Apple Originalzubehör', '343': 'Vorbestellungen - zu löschen',
                          '802': 'Tragbare Lautsprecher', '8021': 'Airplay', '8022': 'Bluetooth-Lautsprecher',
                          '8023': 'Outdoor-Lautsprecher', '8024': 'Kabelgebundene Lautsprecher',
                          '4036': 'Akkus, Batterien & Steckdosenleisten', '777': 'Ladegeräte', '2668': 'Batterien',
                          '2669': 'Akkus', '779': 'Steckdosenleisten & Stecker', '4100': 'Knopfzellen',
                          '4200': 'Hörgeräte-Batterien', 'MediaMarkt_DE': 'MediaMarkt_DE'}
        self.children = [202, 203, 204, 205, 206, 213, 696, 898, 789, 20566, 207, 208, 209, 210, 211, 212, 691, 3678,
                         3122, 6557, 4500, 1815, 4888, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226,
                         227, 228, 787, 229, 230, 231, 232, 233, 234, 235, 236, 237, 240, 692, 2850, 11234, 2567, 238,
                         239, 10040, 241, 242, 243, 244, 245, 246, 3501, 247, 248, 249, 250, 3500, 4300, 251, 252, 253,
                         254, 255, 256, 257, 258, 788, 765, 4561, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269,
                         784, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 283, 290, 282, 284, 1629, 285,
                         286, 287, 289, 292, 4211, 288, 291, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304,
                         305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 749, 750, 5698, 1993, 316, 317, 318,
                         319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 10039, 334, 335,
                         336, 337, 338, 340, 342, 810, 1476, 343, 802, 8021, 8022, 8023, 8024, 4036, 777, 2668, 2669,
                         779, 4100, 4200]
        self.parents = ['MediaMarkt_DE', '202', '203', '203', '203', '203', '203', '203', '203', '203', '20566',
                        '20566', '20566', '20566', '20566', '20566', '20566', '20566', '20566', '20566', '20566', '203',
                        '203', '202', '214', '214', '214', '214', '214', '214', '214', '202', '222', '222', '222',
                        '222', '222', '222', '222', '202', '229', '229', '229', '229', '229', '229', '229', '229',
                        '229', '229', '229', '229', '229', '2567', '2567', '229', '202', '241', '241', '241', '241',
                        '241', '241', '3501', '3501', '3501', '3501', '3501', '241', '202', '251', '251', '251', '251',
                        '251', '251', '251', '251', '251', '251', '202', '259', '259', '259', '259', '259', '259',
                        '259', '259', '259', '259', '259', '202', '270', '270', '270', '270', '270', '270', '270',
                        '270', '270', '270', '270', '270', '270', '290', '290', '270', '202', '285', '285', '285',
                        '285', '285', '4211', '4211', '4211', '4211', '4211', '202', '296', '296', '296', '296', '296',
                        '296', '202', '303', '303', '303', '303', '303', '303', '303', '202', '311', '311', '311',
                        '311', '311', '311', '311', '311', '202', '316', '316', '316', '316', '316', '316', '316',
                        '316', '316', '316', '316', '316', '316', '202', '330', '330', '330', '330', '202', '334',
                        '334', '334', '334', '334', '334', '334', '334', '202', '202', '802', '802', '802', '802',
                        '202', '4036', '4036', '4036', '4036', '4036', '4036']

    @staticmethod
    def convert_nan_to_empty_string(input_to_check):
        if type(input_to_check) == float:
            return "NO_TEXT"
        to_delete = ["<body>", "</body>", "<header>", "</header>"]
        for str_to_delete in to_delete:
            input_to_check = input_to_check.replace(str_to_delete, "")
        return input_to_check.replace("\n", "")

    def get_category_parent(self, child, parent_list):
        if child == "MediaMarkt_DE" or child == "":
            return parent_list
        child = int(child)
        for p, ch in zip(self.parents, self.children):
            if child == ch:
                parent_list.append(p)
                return self.get_category_parent(p, parent_list)

    def get_categories_parents(self):
        for category in self.categories_id:
            self.categories_parent_id.append(self.get_category_parent(category, [category]))
        return self.categories_parent_id

    def convert_id_2_categories(self, categories):
        print(categories)
        return [self.id_2_name[category] for category in categories]

    def convert_id_parents_2_name(self):
        for parent in self.categories_parent_id:
            self.categories_parent_name.append(self.convert_id_2_categories(parent))
        return self.categories_parent_name
