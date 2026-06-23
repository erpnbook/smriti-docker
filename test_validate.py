import json
from smriti_retail_os.item_master_api import validate_import_rows

rows = [{
    'BARCODE NO': '7007007007001',
    'PRODUCT STYLE CODE': 'CH-01-A',
    'ITEM DESCRIPTION': 'BASIC',
    'BRAND NAME': 'TATTLY THREADS',
    'COLOR': 'CREAM',
    'SIZE': '35',
    'PLANNED MRP': '1899',
    'COST PRICE': '375',
    'PRODUCT TAX': '5',
    'HSN CODE': '',
    'GENDER': 'LADIES',
    'VENDOR CODE': 'A',
    'PURCHASE CLASS': 'SIS',
    'DEPARTMENT': 'LADIES FTW',
    'MERCHANDISE CATEGORY': 'CHAPPAL',
    'Sub category': 'CROSS',
    'HEELS': 'SMALL PLATFORM',
    'UPPER MATERIAL': 'SYNTHETIC',
    'OUTSOLE': 'PU',
    'IMAGE LINK': 'CH-01-A'
}]

result = validate_import_rows(json.dumps(rows))
print(json.dumps(result, indent=2))
