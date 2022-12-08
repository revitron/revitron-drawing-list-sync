'Taken from :
'http://stackoverflow.com/questions/1858195/convert-xls-to-csv-on-command-line?noredirect=1&lq=1
'
'xls2csv.vbs [sourcexlsFile].xls [destinationcsvfile].csv

'Erwartet 4 Parameter: XLS-file drawing-list-csv revit-struktur-csv

if WScript.Arguments.Count < 3 Then
    WScript.Echo "Error! Please specify all required arguments."
    Wscript.Quit
End If
Dim excel
Set excel = CreateObject("Excel.Application")
Dim workbook
Set workbook = excel.Workbooks.Open(Wscript.Arguments.Item(0))
Set sheetDrawingList = workbook.Sheets("Sheets")
sheetDrawingList.Activate
workbook.SaveAs WScript.Arguments.Item(1), 6
Set sheetFolders = workbook.Sheets("Groups")
sheetFolders.Activate
workbook.SaveAs WScript.Arguments.Item(2), 6
workbook.Close False
excel.Quit
