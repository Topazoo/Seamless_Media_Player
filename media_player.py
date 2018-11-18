import vlc
import os
import Tkinter as tk
from PIL import ImageTk, Image

class Video_Window(object):
    ''' Window to display videos '''

    def __init__(self, path):
        '''@path - The path of the file to load '''

        # Instantiate video player
        vlc_root = vlc.Instance()
        self.player = vlc_root.media_player_new()

        # Load video
        video = vlc_root.media_new(path)
        video.get_mrl()
        self.player.set_media(video)

    def play(self, loop=False):
        ''' Open the video player and play video
            @loop - True if player should loop the video '''

        # Create a fullscreen video window
        window = tk.Toplevel()
        window.wm_attributes('-fullscreen', 'true')

        # Add the video to the window
        video_label = tk.Label(window)
        video_label.configure(bg='black')

        # The Pack geometry manager packs widgets in rows or columns.
        video_label.pack(side="bottom", fill="both", expand="yes")

        # Set focus on the window
        window.focus_set()

        # Bind escape key to quit the window
        window.bind("<Escape>", self.video_exit_callback)

        # Assign to window
        if os.name == "nt":
            self.player.set_hwnd(video_label.winfo_id())
        elif os.name == "posix":
            self.player.set_xwindow(video_label.winfo_id())

        # Play video
        self.player.play()

        # Start the GUI
        window.mainloop()

    def video_exit_callback(self, event):
        ''' Callback when window is destroyed '''

        # Stop the playing video
        self.player.stop()

        # Quit the window
        event.widget.destroy()

class Media_Player(object):
    ''' Media player '''

    def resize_image(self, raw_image, base_width, base_height):
        ''' Resize an image to fit a width and height maintaining aspect-ratio
            @raw_image - The image to resize
            @base_width - The width to resize to
            @base_height - The height to resize to '''

        # If the original image is too wide
        if base_width < raw_image.size[0]:
            # Get the percentage to scale the width down by
            width_percentage = base_width / float(raw_image.size[0])
            # Get the height scaled down by that percentage
            new_height = int(width_percentage * float(raw_image.size[1]))
            # Resize the image
            raw_image = raw_image.resize((base_width, new_height), Image.ANTIALIAS)

        # If the original image or new image is too tall
        if base_height < raw_image.size[1]:
            # Get the percentage to scale the height down by
            height_percentage = base_height / float(raw_image.size[1])
            # Get the width scaled down by that percentage
            new_width = int(height_percentage * float(raw_image.size[0]))
            # Resize the image
            raw_image = raw_image.resize((new_width, base_height), Image.ANTIALIAS)

        return raw_image

    def display_image(self, path):
        ''' Display an image in fullscreen
            @path - The path to the image '''

        # Create a fullscreen image window
        window = tk.Toplevel()
        window.wm_attributes('-fullscreen', 'true')

        # Load the image with tk
        raw_image = Image.open(path)
        raw_image = self.resize_image(raw_image, window.winfo_screenwidth(), window.winfo_screenheight())
        img = ImageTk.PhotoImage(raw_image)

        # Add the image to the window
        image_label = tk.Label(window, image=img)
        image_label.configure(bg='black')

        # The Pack geometry manager packs widgets in rows or columns.
        image_label.pack(side="bottom", fill="both", expand="yes")

        # Set focus on the window
        window.focus_set()

        # Bind escape key to quit the window
        window.bind("<Escape>", lambda quit_window: quit_window.widget.destroy())

        # Start the GUI
        window.mainloop()

    def play_video(self, path, loop=True):
        ''' Play a video in fullscreen
            @path - The path to the video
            @loop - Loop video if True'''

        # Create the wideo window
        window = Video_Window(path)

        # Play media
        window.play(loop)


