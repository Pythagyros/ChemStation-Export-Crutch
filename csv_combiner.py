import glob
import pandas as pd
from tkinter import *


class PlottingWindow:

    # Signal configurations for HPLC-DAD systems

    dad_1260 = ['Time', '210 nm', '230 nm', '260 nm', '280 nm', '330 nm',
                '380 nm', '430 nm', '500 nm', 'ELSD']
    dad_1200 = ['Time', '220 nm', '260 nm', '280 nm', '360 nm', '435 nm']
    dad_1100 = ['Time', '210 nm', '230 nm', '260 nm', '280 nm', '330 nm']

    def __init__(self, master):
        self.master = master
        master.title('csv_combiner v0.1')

        '''Set the variables of the plot'''

        self.path = 'C:\Temp'
        self.data = pd.DataFrame
        self.title = StringVar(master)
        self.title.set('test')

        # Values for selected signals

        self.instrument = StringVar(master)

        self.dad_config = []

        self.instrument_pressure = BooleanVar(master)
        self.instrument_pressure.set(False)
        self.solvent_percent = BooleanVar(master)
        self.solvent_percent.set(False)

        self.toplabel = Label(master, text='Select the Instrument')
        # self.addcurve_label = Label(master, text='Check for additional curves')
        self.title_label = Label(master, text='Filename')

        self.create_button = Button(master, text='Write to .csv',
                                    command=self.create_dataframe)

        self.close_button = Button(master, text='Close', command=master.quit)

        self.title_box = Entry(master, textvariable=self.title)

        self.instrument_select = OptionMenu(master, self.instrument,
                                            'Agilent 1100',
                                            'Agilent 1200',
                                            'Agilent 1260')

        # self.pressure_check = Checkbutton(master, text='Pressure',
        #                                   variable=self.instrument_pressure,
        #                                   onvalue=True, offvalue=False)

        # self.solvent_check = Checkbutton(master, text='%B Solvent',
        #                                  variable=self.solvent_percent,
        #                                  onvalue=True, offvalue=False)

        self.toplabel.pack()
        self.instrument_select.pack()
        # self.addcurve_label.pack()
        # self.solvent_check.pack()
        # self.pressure_check.pack()
        self.title_label.pack()
        self.title_box.pack()
        self.create_button.pack()
        self.close_button.pack()

    def create_dataframe(self):
        chrom = self.data
        signals = []
        i = 0

        # for signal in self.dad_config.get():
        #     dad_list = [dad_1260, dad_1200, dad_1100]

        # if self.solvent_percent.get() is True:
        #     for x in dad_list:
        #         x.append('%%B')
        # else:
        #     pass
        # if self.instrument_pressure.get() is True:
        #     for x in dad_list:
        #         x.append('Pressure')
        # else:
        #     pass

        # Create a list of all .csv files in path folder

        # self.path = askdirectory()

        filenames = glob.glob(self.path + '/Signal*.csv')

        # Iterate filelist and convert the csv files to pandas dataframes

        # try:

        for signal in filenames:

            i += 1
            df = pd.read_csv(signal, encoding='utf-16', sep=';',
                             names=['Time', 'Signal %d' % i])
            signals.append(df)

        # Merge the dataframes into one

        chrom = pd.concat(signals, axis=1)

        # Hack to rename ELSD time until i figure out a more elegant way
        if self.instrument.get() == 'Agilent 1260':
            chrom.columns = ['Time', '210 nm',
                             'Time', '230 nm',
                             'Time', '260 nm',
                             'Time', '280 nm',
                             'Time', '330 nm',
                             'Time', '380 nm',
                             'Time', '430 nm',
                             'Time', '500 nm',
                             'Time_ELSD', 'ELSD']
        # Strip the duplicated time columns

        chrom = chrom.loc[:, ~chrom.columns.duplicated()]

        if self.instrument.get() == 'Agilent 1260':
            self.dad_config = PlottingWindow.dad_1260
        elif self.instrument.get() == 'Agilent 1200':
            self.dad_config = PlottingWindow.dad_1200
        elif self.instrument.get() == 'Agilent 1100':
            self.dad_config = PlottingWindow.dad_1100
        else:
            print('Wat')
            pass
        if self.instrument.get() != 'Agilent 1260':
            chrom.columns = self.dad_config
        self.data = chrom

        self.data.to_csv('C:\Temp\%s.csv' % self.title.get())


if __name__ == '__main__':
    root = Tk()
    app = PlottingWindow(root)
    root.geometry('200x250')
    root.mainloop()
