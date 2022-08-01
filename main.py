# [01] GUI LIB
import dearpygui.dearpygui as dpg
import array
import numpy as np
import cv2

# [02] SCREAN INFO LIB
import ctypes

# Cache Screen info
user32 = ctypes.windll.user32

# Get Screen Size
screensize = {
    "width":user32.GetSystemMetrics(78),
    "height":user32.GetSystemMetrics(79)
}


# To access any DPG commands
dpg.create_context()

# Define the application viewport
dpg.create_viewport(
    title='Elsherbiniy Image Box', 
    max_width=screensize["width"], max_height=screensize["height"],
    min_width= screensize["width"], min_height= screensize["height"],
    width=screensize["width"], height= screensize["height"],
    x_pos=0, y_pos=0,
    resizable= True,
    always_on_top= False,
    decorated= True
    )


w,h,d = 1280 ,536 ,3
raw_data = np.zeros((h,w,d), dtype=np.float32)

def update_dynamic_texture(new_frame):
    global raw_data, w, h, d

    h, w, d = new_frame.shape

    # print("=" * 50)
    # print(new_frame[:d2])
    # print("=" * 50)

    # raw_data[:h2] = new_frame[:h2] / 255
    # raw_data[:w2] = new_frame[:w2] / 255
    # raw_data[:d2] = new_frame[:d2] / 255
    raw_data[:h, :w] = new_frame[:, :] / 255




# Button Call Back Function
def button_call_back():
    global raw_data, h, w, d
    print("Video Execute")

    
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        #  cv2.imwrite('frame.png', frame)
        # print("-" * 50)
        # print(frame.astype(np.float32) / 255)
        # print("-" * 50)
        # print(np.float32(frame))

        # Get the current frame height
        height, width, depth = frame.shape

        if dpg.is_dearpygui_running():
            
            # Check Frame Comptability
            if height != h or width != w or depth != d:

                # Update Frame
                h = height
                w = width
                d = depth

                print("Frame Updated")

                # Re render the dpg
                dpg.render_dearpygui_frame()
                
            update_dynamic_texture(frame)
        else:
            break


        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

# Define Form
with dpg.window(label="Video", width=300, height=100, pos=(0, 0), autosize=True, no_move=True, no_close=True, no_collapse=True):
    dpg.add_button(label="Start Video Streaming!", callback= button_call_back)


with dpg.texture_registry(show=True):
    dpg.add_raw_texture(width=w, height=h, default_value=raw_data, format=dpg.mvFormat_Float_rgb, tag="texture_tag")

with dpg.window(label="Tutorial"):
    dpg.add_image("texture_tag")

# Initialize the GUI
dpg.setup_dearpygui()

# Displayt the viewport
dpg.show_viewport()

# Display the GUI
dpg.start_dearpygui()

# Proper clean up of DPG
dpg.destroy_context()

