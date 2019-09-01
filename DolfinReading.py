import sys, os, csv, logging, time
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5 import uic
from PyQt5.QtGui import QFont

import numpy as np
sys.dont_write_bytecode = True
from LL_Drives.KineticAssayTools import *
from LL_Drives.dolfinParser import *
from LL_Drives.graphicalInterpretation import *

base_dir = os.getcwd()
LL_dir = os.path.join(base_dir,'LL_drives')
os.chdir(LL_dir)
Ui_MainWindow, QtBaseClass = uic.loadUiType("DolfinInterpreter.ui")


class DIApp(QMainWindow):
    def __init__(self):
        super(DIApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.RunQpb.clicked.connect(self.run_experiments)
        self.ui.ResToDefQpb.clicked.connect(self.reset_defaults)
        self.ui.ResToLasExpQpb.clicked.connect(self.reset_recent_exp)
        self.ui.GetFlu.clicked.connect(self.getFluor)
        self.ui.GetSavLoc.clicked.connect(self.getPath)
        self.ui_list = [self.ui.FluFilQte, self.ui.AbsFilFluSavLocQte, self.ui.StaDroQte, self.ui.EndDroQte, self.ui.BlaLabQte, self.ui.DroLabQte,\
        self.ui.MerDroLabQte, self.ui.Offset1, self.ui.Offset2, self.ui.SavQte, self.ui.NorFacQte, self.ui.KinFilQte]

        with open('defaults.csv', 'wb') as csvfile:
            writer_object = csv.writer(csvfile)
            writer_object.writerow(
                ['N.results.csv', os.path.join(os.getenv('USERPROFILE'), 'Downloads'), 1, 5, 'blank_', 'drop_',
                 'merge_', 1, 10,
                 os.path.join(os.getenv('USERPROFILE'), 'Downloads'), 1.0, 'KineticOverview'])

    def reset_defaults(self):
        """
        Grabs default csv which should be underneath temptext (hardcoded)
        repopulates UI with this information
        """
        os.chdir(LL_dir)
        with open('defaults.csv') as csvfile:
            reader_object = csv.reader(csvfile)
            row_1 = reader_object.next()
            for index,ui_element in enumerate(self.ui_list):
                ui_element.setText(row_1[index])

    def reset_recent_exp(self):
        """
        Grabs reset file and populates all ui Qte objects with previous
        experimental info
        """
        os.chdir(LL_dir)
        with open('recent_exp.csv') as csvfile:
            reader_object = csv.reader(csvfile)
            row_1 = reader_object.next()
            for index ,ui_element in enumerate(self.ui_list):
                ui_element.setText(row_1[index])

    def getFluor(self):
        """
        Utilizes QFileDialog to grab the fluor file and smart populating the labels
        """

        fluor_path = QFileDialog.getOpenFileName(self, 'Open file', \
                          self.ui.FluFilQte.toPlainText(),"CSV files (*.csv)")
        try:
            split_by_path = fluor_path[0].split('/')
            file = split_by_path[-1]
            split_by_path.pop()
            full_path = '\\'.join(split_by_path)
            self.ui.FluFilQte.setText(file)
            self.ui.AbsFilFluSavLocQte.setText(full_path)

            # Filters out default values
            ignore_labels = ['id', 'title', 'description', 'sample_id', 'cartridge_serial', 'user', 'badge', 'start_time', \
                             'end_time', 'controller_version', 'mb_version', 'fl_version', 'fl2_version', 'sp_version', \
                             'fpga_version', 'instrument_name', 'start_temp', 'start_volt', 'end_temp', 'end_volt']
            all_labels, numbers = return_key_labels(file, full_path)
            all_labels = [i for i in all_labels if i not in ignore_labels]

            list_labels = ','.join(all_labels)
            self.ui.BlaLabQte.setText(list_labels)
            self.ui.DroLabQte.setText(list_labels)
            self.ui.StaDroQte.setText(str(min(numbers)))
            self.ui.EndDroQte.setText(str(max(numbers)))
        except:
            pass

    def getPath(self):
        """
        Gets path of the directory the user selects
        """
        fname = QFileDialog.getExistingDirectory(self, 'Select Directory', self.ui.AbsFilFluSavLocQte.toPlainText())
        self.ui.SavQte.setText(fname)

    def run_experiments(self):
        """
        Performs a number of tasks in order as described by the comments

        """
        os.chdir(base_dir)

        #starts time
        time.clock()

        # advanced logger setup
        logger = logging.getLogger('log')
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        log_fh = logging.FileHandler('kinetic.log')
        logger.addHandler(ch)
        logger.addHandler(log_fh)

        # writes data to the local csv file for feature "reset last experiment"
        my_row = []
        os.chdir(LL_dir)
        for index ,ui_element in enumerate(self.ui_list):
            my_row.append(ui_element.toPlainText())
        with open('recent_exp.csv', 'wb') as csvfile:
            csvwriter_object = csv.writer(csvfile)
            csvwriter_object.writerow(my_row)
        os.chdir(base_dir)

        font = QFont()
        font.setPointSize(8)
        self.ui.LogLabQl.setFont(font)

        try:
            # handles user incorrectly typing in information
            if not range(int(self.ui.StaDroQte.toPlainText()), int(self.ui.EndDroQte.toPlainText())+1):
                logger.error('ERROR: Start Drop > End Drop')
                raise ValueError('ERROR: Start Drop > End Drop')
            try:
                directory_list = os.listdir(self.ui.AbsFilFluSavLocQte.toPlainText())
            except WindowsError:
                logger.error('ERROR: Could not find absorbance fluorescence file location')
                raise WindowsError('ERROR: Could not find absorbance fluorescence file location')
            if self.ui.FluFilQte.toPlainText() not in directory_list:
                logger.error('ERROR: Could not identify fluor file in supplied directory')
                raise WindowsError('Please check to make sure the path is correct for the fluor file')

            # Backend calculations
            my_filter = {'Absorbance': [], 'Fluorescence': [], "Time": ['start_time', 'end_time']}
            blank_filter = {}
            for i in range(int(self.ui.StaDroQte.toPlainText()), int(self.ui.EndDroQte.toPlainText())+1):
                my_filter['Time'].extend([self.ui.MerDroLabQte.toPlainText() + str(i)])
                my_filter['Fluorescence'].extend([self.ui.DroLabQte.toPlainText() + str(i), self.ui.BlaLabQte.toPlainText() + str(i)])
                blank_filter[self.ui.DroLabQte.toPlainText() + str(i)] = [self.ui.BlaLabQte.toPlainText() + str(i), self.ui.MerDroLabQte.toPlainText() + str(i)]
            do = dolfinParser(self.ui.FluFilQte.toPlainText(), my_filter, self.ui.AbsFilFluSavLocQte.toPlainText(), np.float64(self.ui.NorFacQte.toPlainText()))
            do.get_id_info()
            logger.info('Process 1 complete, datasets grouped ' + str(time.clock()))
            do.get_blank_subtracted_vals(blank_filter,[int(self.ui.Offset1.toPlainText()), int(self.ui.Offset2.toPlainText())])
            logger.info('Process 2 complete, background subtraction and slopes prepared at ' + str(time.clock()))

            # creates excel file and needed tabs
            gI = GraphInterpreter(do, self.ui.SavQte.toPlainText(), str(self.ui.KinFilQte.toPlainText()))
            gI.plot_spectrums()
            logger.info('Process 3 complete, file written to website ' + str(time.clock()))
            gI.export_data()
            logger.info('Process 4, data report prepared export complete at ' + str(time.clock()))
            # moves data
            os.chdir(base_dir)
            font = QFont()
            font.setPointSize(24)
            self.ui.LogLabQl.setFont(font)
            self.ui.LogLabQl.setText('Success!')
            logger.info('Successfully Processed')
        except:
            logger.error('ERROR: AN ERROR HAS OCCURRED')
            update_log(self.ui, base_dir, os.getcwd())

        # closes logger and moves it to the testing location
        os.chdir(base_dir)
        log_fh.close()
        name_data_file('kinetic.log', base_dir, new_path_location='J:\Users\it_user', rename_flag=True)

        # removes log file for next run
        for item in os.listdir(base_dir):
            if item.endswith('.log'):
                os.remove(os.path.join(base_dir,item))

from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)
window = DIApp()
window.show()
sys.exit(app.exec_())
