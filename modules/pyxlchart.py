from win32com.client import Dispatch
import os
import pythoncom



class Pyxlchart(object):
    """
    This class exports charts in an Excel Spreadsheet to the FileSystem
    win32com libraries are required.
    """
    

    def __init__(self):
        pythoncom.CoInitialize()
        self.WorkbookDirectory = ''
        self.WorkbookFilename = ''
        self.GetAllWorkbooks = False
        self.SheetName = ''
        self.ChartName = ''
        self.GetAllWorkbookCharts = False
        self.GetAllWorksheetCharts = False
        self.ExportPath = ''
        self.ImageFilename = ''
        self.ReplaceWhiteSpaceChar = '_'
        self.ImageType = 'jpg'
        self.ChartDetail = []
    def __del__(self):
        pass
    def start_export(self):
        if self.WorkbookDirectory == '':
            return "WorkbookDirectory not set"
        else:
            self._export()    
        return self.ChartDetail
    
    def _export(self):
        """
        Exports Charts as determined by the settings in class variabels.
        """
        excel = Dispatch("excel.application")
        excel.Visible = False
        wb = excel.Workbooks.Open(os.path.join(self.WorkbookDirectory ,self.WorkbookFilename))
        self._get_Charts_In_Worksheet(wb,self.SheetName,self.ChartName)
        wb.Close(False)
        excel.Quit()


    def _get_Charts_In_Worksheet(self,wb,worksheet = "", chartname = ""):
        
        if worksheet != "" and chartname != "":
            sht = self._change_sheet(wb,worksheet)
            cht = sht.ChartObjects(chartname)
            self._save_chart(cht)
            return
        
        if worksheet == "":
            for sht in wb.Worksheets:
                for cht in sht.ChartObjects():
                    if chartname == "":
                        ImageName = self._save_chart(sht.Name,cht)
                    else:
                        if chartname == cht.Name:
                            ImageName = self._save_chart(sht.Name,cht)
                    self.ChartDetail.append(dict(workbookpath = self.WorkbookDirectory,workbookfile = self.WorkbookFilename, sheetname = sht.Name, chartname = cht.Name, imagename = ImageName))
        else:
            sht = wb.Worksheets(worksheet)
            for cht in sht.ChartObjects():
                if chartname == "":
                    ImageName = self._save_chart(sht.Name,cht)
                else:
                    if chartname == cht.Name:
                        ImageName = self._save_chart(sht.Name,cht)
                self.ChartDetail.append(dict(workbookpath = self.WorkbookDirectory,workbookfile = self.WorkbookFilename, sheetname = sht.Name, chartname = cht.Name, imagename = ImageName))
        

    def _change_sheet(self,wb,worksheet):
        try:
            return wb.Worksheets(worksheet)
        except:
            raise NameError('Unable to Select Sheet: ' + worksheet + ' in Workbook: ' + wb.Name)
        


    def _save_chart(self,sheetname,chartObject):
        imagename = sheetname + '-' + self._get_filename(chartObject.Name)
        savepath = os.path.join(self.ExportPath,imagename)
        print savepath
        chartObject.Chart.Export(savepath,self.ImageType)
        return imagename


    

    def _get_filename(self,chartname):
        """
        Replaces white space in self.WorkbookFileName with the value given in self.ReplaceWhiteSpaceChar
        If self.ReplaceWhiteSpaceChar is an empty string then self.WorkBookFileName is left as is
        """
        
        if self.ImageFilename == '':
            self.ImageFilename == chartname

        if self.ReplaceWhiteSpaceChar != '':
            chartname = chartname.replace(' ',self.ReplaceWhiteSpaceChar)
        
        
        if self.ImageFilename != "":
            return self.ImageFilename + "_" + chartname + "." + self.ImageType
        else:
            return chartname + '.' + self.ImageType

    
        

if __name__ == "__main__":
    xl = Pyxlchart()
    xl.WorkbookDirectory = "\\\\maawtns01\\discipline\\procurement\\MATERIEL\\Raw Material\\Data Management\\Hawk"
    xl.WorkbookFilename = "Hawk Workability KPI.xlsm"
    xl.SheetName = ""
    xl.ImageFilename = "MyChart1"
    xl.ExportPath = "d:\\pycharts"
    xl.ChartName = ""
    xl.start_export()
    
    print "This file does not currently allow direct access"
    print "Please import PyXLChart and run start_export()"
    
