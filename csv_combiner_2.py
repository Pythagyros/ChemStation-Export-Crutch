import glob
import pandas as pd
from tkinter import *


class PlottingWindow:

    '''
    The PlottingWindow class contains all the buttons and labels for the
    user interface. It creates an instance of the Chromatogram class and calls
    its functions through buttons.
    '''

    def __init__(self, master, path):

        # Chromatogram contains the functions to read the data
        self.data = Chromatogram(path)
        # Allows the user to switch between three different configurations
        self.instrument = StringVar()
        # Some tkinter stuff
        self.master = master
        # Window title
        master.title('csv_combiner v0.1')
        # Name of the exported file
        self.title = StringVar(master)
        self.title.set('test')

        # Create UI elements
        self.toplabel = Label(master, text='Select the Instrument')
        self.title_label = Label(master, text='Filename')

        self.create_button = Button(master, text='Write to .csv',
                                    command=self.data.create_dataframe)
        self.close_button = Button(master, text='Close', command=master.quit)
        self.title_box = Entry(master, textvariable=self.title)
        self.instrument_select = OptionMenu(master, self.instrument,
                                            'Agilent 1100',
                                            'Agilent 1200',
                                            'Agilent 1260')

        # pack UI elements
        self.toplabel.pack()
        self.instrument_select.pack()
        self.title_label.pack()
        self.title_box.pack()
        self.create_button.pack()
        self.close_button.pack()


class Chromatogram:

    ''' This class contains the functions to read the exported signal files
    in .csv format, combine them into a pandas DataFrame object and name the
    columns based on the selected instrument. The DataFrame is exported to a
    new .csv file
    '''

    # Set the three different configurations as immutable tuples
    dad_1260 = ('Time', '210 nm', '230 nm', '260 nm', '280 nm', '330 nm',
                '380 nm', '430 nm', '500 nm', 'ELSD')
    dad_1200 = ('Time', '220 nm', '260 nm', '280 nm', '360 nm', '435 nm')
    dad_1100 = ('Time', '210 nm', '230 nm', '260 nm', '280 nm', '330 nm')

    def __init__(self, path):
        # set up the variables
        self.path = path
        self.data = pd.DataFrame
        self.instrument = None
        self.dad_config = []

    def create_dataframe(self):
        ''' This function reads the information in the .csv files and converts
        them to DataFrame objects. These are subsequently concatenated to a
        single object and renamed.
        '''
        chrom = pd.DataFrame
        signals = []
        i = 0

        # create a list of .csv files in the path which begin with "signal"
        filenames = glob.glob(self.path + '/Signal*.csv')

        # Iterate through the filelist and convert them to dataframes.
        # The generated dataframes are stored in a list.
        for signal in filenames:
            i += 1
            df = pd.read_csv(signal, encoding='utf-16', sep=';',
                             names=['Time', 'Signal %d' % i])
            signals.append(df)

        # Combine all dataframes in the list into a single one
        chrom = pd.concat(signals, axis=1)

        # Retrieves the instrument setting from the PlottingWindow class.
        # Renaming of the columns is depended on it.
        self.instrument = app.instrument.get()

        # Hack to rename ELSD time until i figure out a more elegant way.
        # The timescale is different here and the next line would delete all
        # time data but the first. With this, the time belonging to the ELSD
        # signal is renamed and stored alongside the rest.

        if self.instrument == 'Agilent 1260':
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

        # Choose the dad config from the tuples depending on the selected
        # instrument configuration.
        if self.instrument == 'Agilent 1260':
            self.dad_config = Chromatogram.dad_1260
        elif self.instrument == 'Agilent 1200':
            self.dad_config = Chromatogram.dad_1200
        elif self.instrument == 'Agilent 1100':
            self.dad_config = Chromatogram.dad_1100
        else:
            print('Wat')
            pass
        # Exception for the Agilent 1260 variant, which contains the modified
        # ELSD timeline. It has already been renamed in line 103
        if self.instrument != 'Agilent 1260':
            chrom.columns = self.dad_config
        # Store the dataframe in the class variable
        self.data = chrom
        # Export the dataframe to a new .csv file in the same folder.
        self.data.to_csv('C:\Temp\%s.csv' % app.title.get())

if __name__ == '__main__':
    root = Tk()
    app = PlottingWindow(root, 'C:\Temp')
    root.geometry('200x250')
    root.mainloop()
