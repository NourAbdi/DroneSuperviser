import cv2
from tkinter import *
from tkinter import ttk
import drone
from scene import SoftwareRender

target_path = 'main_folder/'


# This func will get the Input (drones statuses and videoCaps) from the destination file and send to the scene to render
def get_drones_from_file(filename, frames_num, drone_name, translations, alpha, videoCaps):
    coordinates = (100, 100)
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    color = (255, 0, 255)
    thickness = 2
    image_num = 0
    with open(filename + drone_name + '/status.txt') as f:
        for line in f:
            if line.startswith('img num:'):
                image_num = [int(i) for i in line.split() if i.isdigit()]
            elif line.startswith('['):
                line = line.replace('[', '')
                line = line.replace(']', '')
                translations.append([float(i) for i in line.split(", ")[0:3]])
                alpha.append([float(i) for i in line.split(", ")[3:4]][0])
    # Reading the frame Images (VideoCaps) for each drone
    # for i in range(frames_num):
    #     img = cv2.imread(filename + drone_name + '/video_cap/' + str(i + 1) + '.jpg')
    #     img = cv2.putText(img, drone_name + ' ,frames_num : ' + str(i+1), coordinates, font, fontScale, color, thickness,
    #                       cv2.LINE_AA)
    #     videoCaps.append(img)


if __name__ == '__main__':
    # Create an instance of tkinter frame or window
    win = Tk()
    # Set the geometry of tkinter frame
    win.geometry("1000x500")


    def reading_drones(drones_num, frames_num):
        # For each drone we will read the status file containing the translations and the rotations per frame

        drones = []
        for i in range(drones_num):
            drone_name = 'drone_name' + str(i + 1)
            translations, alpha, videoCaps = [], [], []
            get_drones_from_file(target_path, frames_num, drone_name, translations,
                                 alpha, videoCaps)
            droneX = drone.Drone()
            droneX.name = 'drone' + str(i + 1)
            droneX.position = translations
            droneX.alpha = alpha
            droneX.videoCaps = videoCaps
            drones.append(droneX)
            win.destroy()

        app = SoftwareRender(drones, drones_num, frames_num)
        app.run()
        cv2.destroyAllWindows()


    def get_value():
        reading_drones(int(entry1.get()), int(entry2.get()))


    # Create a label
    label1 = Label(win, text='Enter the number of drones: ', fg='black', font=('Arial', 14))
    label1.grid(row=0, column=0, padx=50, pady=20)

    entry1 = ttk.Entry(win, font='Century 12', width=40)
    entry1.grid(row=0, column=1)
    # Create a label
    label2 = Label(win, text='Enter the number of frames: ', fg='black', font=('Arial', 14))
    label2.grid(row=1, column=0, padx=50, pady=20)
    # Create an Entry2 Widget
    entry2 = ttk.Entry(win, font='Century 12', width=40)
    entry2.grid(row=1, column=1)
    # Create button
    button = ttk.Button(win, text="Enter", command=get_value)
    button.grid(row=3, column=1, pady=200)
    win.mainloop()
