import pandas as pd
from barcode import Code128
from barcode.writer import ImageWriter
import pyodbc


#file = "C:\\Users\\twatki21\\Desktop\\testFiles.xlsx"
conn_str  = 'DRIVER={SQL Server};SERVER={ESMHCANDBP3};DATABASE={AnalyticsSource};Trusted_Connection=yes'
conn = pyodbc.connect(conn_str)
query = 'SELECT * FROM [inv].[Equip_Action_Barcode_Source_vw]'

#frame = pd.read_excel(file)
sql_frame = pd.read_sql(query,conn)
columnData = sql_frame['Equip_Barcode']
        

print(columnData)
"""""
for value in columnData:
    barcodeName = value
    barcode = Code128(barcodeName, ImageWriter())
    barcode.save(barcodeName)
"""""