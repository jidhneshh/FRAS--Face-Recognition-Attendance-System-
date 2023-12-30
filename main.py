from tkinter import*
from PIL import Image, ImageTk
import cv2
import face_recognition
from datetime import datetime
import numpy as np
import csv
import threading
from tkinter import filedialog
from tkinter import messagebox
import time
import os  
import shutil

def open_file_dialog():
    file_path=str(filedialog.askopenfilename())
    return file_path

class NewStudentWindow:
    def __init__(self, root):

        self.root = root

        self.new_student_window = Toplevel(self.root)
        self.new_student_window.title("Add New Student")

        self.new_student_window.attributes("-topmost", True)

        window_width = 400
        window_height = 300
        screen_width = self.new_student_window.winfo_screenwidth()
        screen_height = self.new_student_window.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.new_student_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.name_label = Label(self.new_student_window, text="Student Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=10)

        self.name_entry = Entry(self.new_student_window)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.image_path_label = Label(self.new_student_window, text="Image Path:")
        self.image_path_label.grid(row=1, column=0, padx=10, pady=10)

        self.image_path_entry = Entry(self.new_student_window)
        self.image_path_entry.grid(row=1, column=1, padx=10, pady=10)

        self.browse_button = Button(self.new_student_window, text="Browse", command=self.browse_image)
        self.browse_button.grid(row=1, column=2, padx=10, pady=10)

        self.save_button = Button(self.new_student_window, text="save in file", command=self.save_student)
        self.save_button.grid(row=2, column=1, padx=10, pady=10)
        self.done_button = Button(self.new_student_window, text="Done", command=self.done)
        self.done_button.grid(row=4, column=1, padx=10, pady=10)
        self.capture_button = Button(self.new_student_window, text="Capture Photo", command=self.capture_photo)
        self.capture_button.grid(row=3, column=1, padx=10, pady=10)

    def capture_photo(self):
        video_capture = cv2.VideoCapture(0)

        _, frame = video_capture.read()

        photo_filename = f"captured_photos/{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"

        cv2.imwrite(photo_filename, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        self.image_path_entry.delete(0, END)
        self.image_path_entry.insert(0, photo_filename)

        
        video_capture.release()


    def browse_image(self):
        file_path = filedialog.askopenfilename()
        self.image_path_entry.delete(0, END)
        self.image_path_entry.insert(0, file_path)

    def save_student(self):
        name = self.name_entry.get()
        image_path = self.image_path_entry.get()
        self.new_student_window.destroy()
        if name and image_path:
            with open(str(filedialog.askopenfilename()), 'a', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([name, image_path])
                messagebox.showinfo("Success", "Student details saved successfully!")
        else:
            messagebox.showerror("Error", "Please enter both name and image path.")
        
    def done(self):
        self.new_student_window.destroy()


class FRAS:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1550x790+0+0")
        self.root.title ("FRAS:-Face Recognition Attendence System")
        
        #bg_image
        bg_img=Image.open(r"gui images\bg.jpg")
        bg_img=bg_img.resize((1550,800),Image.ADAPTIVE)
        self.bgimg=ImageTk.PhotoImage(bg_img)

        bglabel=Label(self.root,image=self.bgimg)
        bglabel.place(x=0,y=0,width=1550,height=800)

       
        #button
        img3=Image.open(r"gui images\open file.png")
        img3=img3.resize((100,100),Image.ADAPTIVE)
        self.pimg3=ImageTk.PhotoImage(img3)

        b1=Button(bglabel,image=self.pimg3,command=lambda:FaceRecognition(root),cursor="hand2")
        b1.place(x=200,y=100,width=200,height=200)

        b11=Button(bglabel,text="open your excel file",font=("calibri",11,"bold"),command=lambda:FaceRecognition(root),cursor="hand2")
        b11.place(x=200,y=300,width=200,height=40)

        #button for start recognition
        img4=Image.open(r"gui images\openfile.jpg")
        img4=img4.resize((100,100),Image.ADAPTIVE)
        self.pimg4=ImageTk.PhotoImage(img4)

        b4=Button(bglabel,image=self.pimg4,command=self.download_attendance,cursor="hand2")
        b4.place(x=1100,y=100,width=200,height=200)

        b41=Button(bglabel,text="attendance file",font=("calibri",11,"bold"),command=self.download_attendance,cursor="hand2")
        b41.place(x=1100,y=300,width=200,height=40)

        #labels for clock
        self.clock_label = Label(bglabel, font=('calibri', 20))
        self.clock_label.place(x=1480, y=750, anchor='se',width=300,height=60)  
        self.update_clock()

        img5=Image.open(r"gui images\newimage.jpg")
        img5=img5.resize((100,100),Image.ADAPTIVE)
        self.pimg5=ImageTk.PhotoImage(img5)

        self.b5=Button(bglabel,image=self.pimg5,cursor="hand2", command=self.open_new_student_window)
        self.b5.place(x=1100,y=400,width=200,height=200)
        self.new_student_button = Button(bglabel, text="Add New Student", font=("calibri",11,"bold"),command=self.open_new_student_window)
        self.new_student_button.place(x=1100, y=600, width=200, height=40)
        

    def open_new_student_window(self):
        new_student_window = NewStudentWindow(self.root)
 

    def update_clock(self):
            current_time = time.strftime('%H:%M:%S')
            self.clock_label.config(text=current_time)
            self.clock_label.after(1000, self.update_clock)

    def download_attendance(self):
        filename = datetime.now().strftime("%Y-%m-%d") + '.csv'
        try:
            source_path = os.path.abspath(filename)
            destination_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        
            if destination_path:
                shutil.copyfile(source_path, destination_path)
                messagebox.showinfo("Download Successful", f"Attendance file downloaded to {destination_path}")
            else:
                messagebox.showinfo("Download Cancelled", "Attendance file download was cancelled.")
        except FileNotFoundError:
                messagebox.showerror("File Not Found", f"Attendance file not found for {filename}")


class FaceRecognition:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.capture_thread = None
        self.recognize_faces = False
        self.known_face_encodings = []
        self.known_faces_names = []
        self.detected_name_label = Label(root, text="", font=('calibri', 20), background='white', foreground='black')
        self.detected_name_label.place(x=100,y=600,width=400,height=50)

        with open(str(filedialog.askopenfilename()), 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                name = row[0]
                image1 = row[1]
                name_image = face_recognition.load_image_file(image1)
                name_encoding = face_recognition.face_encodings(name_image)[0]
                self.known_face_encodings.append(name_encoding)
                self.known_faces_names.append(name)
                self.students=self.known_faces_names.copy()
        messagebox.showinfo("successful","data entered successfully")

        self.start_button = Button(root, text="Start Recognition", command=self.start_recognition)
        self.start_button.place(x=650,y=600,width=150,height=30)

        self.stop_button = Button(root, text="Stop Recognition", command=self.stop_recognition)
        self.stop_button.place(x=650,y=660,width=150,height=30)
        self.stop_button["state"] = "disabled"
               
    def start_recognition(self):
        self.start_button["state"] = "disabled"
        self.stop_button["state"] = "active"
        self.recognize_faces = True
        self.capture_thread = threading.Thread(target=self.capture_and_recognize)
        self.capture_thread.start()


    def stop_recognition(self):
        self.start_button["state"] = "active"
        self.stop_button["state"] = "disabled"
        self.recognize_faces = False

    def capture_and_recognize(self):
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")

        f = open(current_date + '.csv', 'w+', newline='')
        lnwriter = csv.writer(f)

        video_capture = cv2.VideoCapture(0)

        while self.recognize_faces:
            _, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = ""
                face_distance = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distance)

                if matches[best_match_index]:
                    name = self.known_faces_names[best_match_index]

                face_names.append(name)

                if name:
                    self.detected_name_label.config(text=f"Detected: {name}")



                if name in self.known_faces_names:
                    if name in self.students:
                        self.students.remove(name)
                        print(self.students)
                        current_time=now.strftime("%H-%M-%S")
                        lnwriter.writerow([name,current_time,current_date])

            cv2.imshow("FRAS", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()
        f.close()
   

if __name__ == "__main__":
    if not os.path.exists("captured_photos"):
        os.makedirs("captured_photos")

    root=Tk()
    obj=FRAS(root)
    root.mainloop()  
