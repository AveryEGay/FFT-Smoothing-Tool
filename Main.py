import csv
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

###################################################
### 1. Change Window Name to include FFT Factor ###
### 2. Add a "Stats" button for smoothed plot   ###
###################################################


class Operations:

    def __init__(self) -> None:
        self.x_axis = []
        self.thc_data = []
        self.x_start = 0
        self.x_end = 0

    def ReadCSV(self,incomingFile):
        fileToRead = incomingFile
        with open(fileToRead, mode='r', encoding='utf-8-sig') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                self.x_axis.append(row[0])
                self.thc_data.append(row[1])

            self.x_start = self.x_axis[0] 
            self.x_end = self.x_axis[-1]
            self.y_data_size = len(self.thc_data)

            return self.thc_data

        
    def SmoothData(self,thc_array, incomingFFTfactor):
        fftFactor = int(incomingFFTfactor)
        y = thc_array
        self.smoothedY = savgol_filter(y, fftFactor, 5)
        return self.smoothedY

    def WriteToCSV(self):
        file = open("SmoothedData.csv", "w", newline='')
        writer = csv.writer(file)

        x_to_start = int(self.x_start)

        for i in range(0,self.y_data_size):
            writer.writerow([x_to_start, self.smoothedY[i]])
            x_to_start = (x_to_start + 1)
        file.close()

    def PlotReadings(self):
        x = np.linspace(int(self.x_start),int(self.x_end),int(self.y_data_size)) #(x_start, x_end, the total number of y points that will be plotted)
        y = self.thc_data
        smoothedYnew = self.smoothedY

        y = [float(i) for i in y]
        smoothedYnew = [float(i) for i in smoothedYnew]

        ax = plt.figure().gca()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.plot(x, y, label="Original", color='red')
        plt.plot(x,smoothedYnew, color='navy', label="Smoothed")

        plt.xlabel("Width (mm)")
        plt.ylabel("Thickness (um)")
        plt.title("Original vs. Smoothed Thickness")
        plt.legend(loc="upper left")
        plt.tight_layout()

        plt.show()