import datetime
import calendar
import os
from dataclasses import dataclass
from typing import Dict, List, Tuple


IDCOLNAME = 'ID'
FATHERIDCOL = 'father\'s ID'
MOTHERIDCOL = 'mother\'s ID'

HEADER = '''0 HEAD
1 SOUR XLSTOGEDCOM
1 DATE {}
2 TIME {}
1 SUBM @SUBM@
1 GEDC
2 VERS 5.5.1
2 FORM LINEAGE-LINKED
1 CHAR UTF-8
1 LANG English
0 @SUBM@ SUBM
1 NAME {} /{}/'''

TRAILER = '0 TRLR'

def convertDate(d):
    """Return the Gedcom date format of an excel date format like 08/04/1931 -> 08 APR 1931."""
    if isinstance(d, int): return d  # year only
    res = d.split('/')
    if len(res) == 1: return int(res[0])
    res[-2] = calendar.month_name[int(res[-2])][:3].upper()
    return ' '.join(res).strip()

def getSurNameWithPrefix(row):
    if row['title']: return row['title'] + ' ' + row['last name']
    return row['last name']    

def getFirstNameWithMidName(row):
    if row['midname']: return row['midname'] + ' ' + row['first name']
    return row['first name']

def printPlace(place):
    if place:
        address = place.split()
        city = address[1][1:-1]
        print('2 PLAC {}'.format(city))
        print('2 ADDR')            
        print('3 CITY {}'.format(city))
        print('3 CTRY {}'.format(address[0][1:-1]))      

@dataclass
class Family:
    id: int
    children: List[str]
        
    def addChildren(self, child):
        self.children.append(child)

@dataclass
class FamilyMapping:
    parentToFamily: Dict[Tuple[str, str],  Family]         # excel ID of father, mother pair -> Family
    
    def __init__(self):
        self.parentToFamily = {}

    def addChildren(self, fatherID, motherID, childID):
        if (fatherID, motherID) in self.parentToFamily:
            self.parentToFamily[(fatherID, motherID)].addChildren(childID)
        else:
            self.parentToFamily[(fatherID, motherID)] = Family(len(self.parentToFamily) + 1, [childID])
    
    def getSpouseMap(self):
        res = {}
        for k, v in self.parentToFamily.items():
            if k[0]:    # father might be missing
                res.setdefault(k[0], []).append(v.id)     
            if k[1]:    # mother might be missing
                res.setdefault(k[1], []).append(v.id)
        return res

    def printGedcom(self, ID2GedcomID):
        for k, v in self.parentToFamily.items():
            print('0 @F{}@ FAM'.format(v.id))
            if k[0]: print('1 HUSB @I{}@'.format(ID2GedcomID[k[0]]))
            if k[1]: print('1 WIFE @I{}@'.format(ID2GedcomID[k[1]]))
            for child in v.children:
                print('1 CHIL @I{}@'.format(child))            

hasKnownParent = lambda row: row[FATHERIDCOL] or row[MOTHERIDCOL]

class FamilyTreeMapping:
    __ID2GedcomID = {}     # excel ID -> Gedcom ID
    __famMap = FamilyMapping()
    __famSMap = {}         # Gedcom ID -> list of family ID in which he/she is a spouse
    
    def __init__(self, t, picdir):
        """Create a FamilyTreeMapping object that supports printing a Gedcom file.

        arguments:
        t      -- the family tree data in a table-like format, i.e. each person is a map and people are contained in a list. This format is returned by function pyexcel.get_records.
        picdir -- directory that stores pictores of the family members
        """
        self.t = t.copy()  
        self.picdir = picdir
        self.__ID2GedcomID = {row[IDCOLNAME]: idx + 1 for idx, row in enumerate(t)}
        self.trantab = str.maketrans("éáűúüőöóí", "eauuuoooi")

        for row in t:
            if not hasKnownParent(row): continue
            self.__famMap.addChildren(row[FATHERIDCOL], row[MOTHERIDCOL], self.__ID2GedcomID[row[IDCOLNAME]])
                                           
        self.__famSMap = self.__famMap.getSpouseMap()
    
    def __getFAMC(self, row):
        if hasKnownParent(row):
            return self.__famMap.parentToFamily[(row[FATHERIDCOL], row[MOTHERIDCOL])].id
        return None 

    def __getPicName(self, ID): 
        return os.path.join(self.picdir, ID.lower().translate(self.trantab) + '.jpg')

    def printGedcom(self, submitter_firstname, submitter_last_name):
        """Prints Gedcom content to the standard output"""
        picList= []
        print(HEADER.format(datetime.datetime.now().strftime("%d %b %Y").upper(), datetime.datetime.now().strftime("%H:%M:%S"), 
            submitter_firstname, submitter_last_name))
        for row in self.t:
            print('0 @I{}@ INDI'.format(self.__ID2GedcomID[row[IDCOLNAME]]))    
            print('1 NAME {} /{}/'.format(getFirstNameWithMidName(row), getSurNameWithPrefix(row)))
            print('2 GIVN {}'.format(row['first name'].encode().decode()))
            print('2 SURN {}'.format(row['last name']))
            if row['nickname']:
                print('2 NICK {}'.format(row['nickname']))
            print('1 SEX {}'.format('M' if row['gender'] == 0 else 'F'))
            if row['email']:
                print('1 EMAIL {}'.format(row['email']))
            if row['webpage']:
                print('1 WWW {}'.format(row['webpage']))        
        
            if row['date of birth']:
                print('1 BIRT')
                print('2 DATE {}'.format(convertDate(row['date of birth'])))
                printPlace(row['place of birth'])
                
            if row['date of death']:
                print('1 DEAT')
                print('2 DATE {}'.format(convertDate(row['date of death'])))
                printPlace(row['place of death'])                

            elif row['is living?'] == 0:
                print('1 DEAT Y')
        
            famc = self.__getFAMC(row)
            if not famc == None:
                print('1 FAMC @F{:,.0f}@'.format(famc))
            if row[IDCOLNAME] in self.__famSMap:
                for fmas in self.__famSMap[row[IDCOLNAME]]:
                    print('1 FAMS @F{}@'.format(fmas))
            if os.path.isfile(self.__getPicName(row[IDCOLNAME])):
                print('1 OBJE @O{}@'.format(len(picList)))
                picList.append(self.__getPicName(row[IDCOLNAME]))

        self.__famMap.printGedcom(self.__ID2GedcomID)
        for idx, p in enumerate(picList):
            print('0 @O{}@ OBJE'.format(idx))
            print('1 FILE {}'.format(p))
            print('2 FORM jpg')
        print(TRAILER)            
             

    
