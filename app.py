import PySimpleGUI as sg
import Main


# Setting up layout
fullPage = [
    [
        sg.Text("Select the CSV File: ", size =(18, 1)),
        sg.In(size=(15,1), enable_events=True, key="-User_File_Input-"),
        sg.FileBrowse(),
    ],
    [

        sg.Text("FFT Smoothing Factor: ", size =(18, 1)),
        sg.InputText(key='-FFT_Factor-', size =(15, 1)),
    ],
    [
        sg.Button("Submit"),
        sg.Button("Exit"),
    ],
]

layout = [
    [
        sg.Column(fullPage),
    ]
]

window = sg.Window("Auto FFT Smoothing", layout)

# Loop for any events from the user
while True:
    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == "Submit":
        requestedFile = values['-User_File_Input-']
        requestedFFTfactor = values['-FFT_Factor-']

        if (requestedFile == "" or requestedFFTfactor == ""):
            sg.popup("Fields cannot be left blank", keep_on_top=True)
        elif (not requestedFile.endswith('.csv')):
            sg.popup("Imported File Must Be A .CSV", keep_on_top=True)
        elif(int(requestedFFTfactor) <= 5):
            sg.popup("FFT Factor Must Be Greater Than 5", keep_on_top=True)
        else:
            obj = Main.Operations()

            originalThc = obj.ReadCSV(requestedFile)

            if(int(requestedFFTfactor) > int(obj.y_data_size)):
                sg.popup("FFT Factor Is Greater Than Num of Y Values", keep_on_top=True)
            else:
                smoothedThc = obj.SmoothData(originalThc, requestedFFTfactor)
                obj.WriteToCSV()
                obj.PlotReadings(requestedFFTfactor)

window.close()