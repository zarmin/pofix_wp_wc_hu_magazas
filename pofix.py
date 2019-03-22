#!/usr/bin/env python3

DICT_WHITESPACE = [
  ['kosaradból', 'kosarából'],
  ['rakhatod', 'rakhatja'],
  ['kattintsunk', 'kattintson'],
  ['kattints', 'kattintson'],
  ['böngésződ', 'böngszője'],
  ['rendelésed', 'rendelését'],
  ['jelszavad   jelszava'],
  ['véleményed', 'véleménye'],
  ['üzleted', 'üzlete'],
  ['elérted', 'elérte'],
  ['veheted', 'veheti'],
  ['elmented', 'elmenti'],
  ['elhagyod', 'elhagyja'],
  ['adhatsz', 'adhat'],
  ['add', 'adja'],
  ['adj', 'adjon'],
  ['törölj', 'töröljön'],
  ['címed', 'címét'],
  ['emlékezz', 'emlékezzen'],
  ['állítottál', 'állított'],
  ['hagyd', 'hagyja'],
  ['kérlek', 'kérjük'],
  ['találtál', 'talált'],
  ['vagy benne', 'benne'],
  ['hagyd', 'hagyja'],
  ['választod', 'válsztja'],
  ['választhatsz', 'választhat'],
  ['szeretnéd', 'szeretné'],
  ['írd', 'írja'],
  ['írj', 'írjon'],
  ['jogosultságod', 'jogosultsága'],
  ['kaptad', 'kapta'],
  ['jogos', 'joga'],
  ['fiókod', 'fiókja'],
  ['visszaállítanod', 'visszaállítani'],
  ['termékeid', 'termékei'],
  ['vedd', 'vegye'],
  ['mondd', 'mondja'],
  ['próbáld', 'próbálja'],
  ['kapcsold', 'kapcsolja'],
  ['használod', 'használja'],
  ['eltávolítod', 'eltávolítja']
]

DICT_EXACT = [
  [' vagy?', '?']
]


import argparse
import polib # external
import re

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--dry-run", help="Do not modify the file only print the changes", action='store_true')
parser.add_argument("files", nargs='*', help='files to process')
args = parser.parse_args()

WHITESPACE_BEGIN = r'(^|\s|[\x00-\x2F:;<=>?@\[\]\\_\{|}])'
WHITESPACE_END = r'($|\s|[\x00-\x2F:;<=>?@\[\]\\_\{|}])'

for file_entry in args.files:
  po = polib.pofile(file_entry)
  for po_entry in po:
    msgstr = po_entry.msgstr
    original_msgstr = msgstr + r''
    for ds in DICT_WHITESPACE:
      re_search = WHITESPACE_BEGIN + r'(' + str(ds[0]).strip() + r')' + WHITESPACE_END
      m = re.search(re_search, msgstr, re.IGNORECASE)
      if m:
        mid = m.groups()[1]
        newstring = str(ds[1]).strip()
        if mid[0].istitle():
          newstring = newstring[0].upper() + newstring[1:]
        new_msgstr = re.sub(re_search, r'\1' + newstring + r'\3', msgstr, flags=re.IGNORECASE)
        msgstr = new_msgstr
    for ds in DICT_EXACT:
      ds_search = str(ds[0])
      if ds_search in msgstr:
        new_msgstr = msgstr.replace(ds_search, str(ds[1]))
        msgstr = new_msgstr
    if original_msgstr != msgstr:
      print("CHANGED >> " + original_msgstr + "  -->  " + msgstr)
      po_entry.msgstr = msgstr

  if not args.dry_run:
    po.save(file_entry + '_new_.po')
    po.save_as_mofile(file_entry + '_new_.mo')




