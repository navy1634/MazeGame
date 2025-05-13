from tkinter import Frame, Label, LabelFrame, Tk


class OperationView(Frame):
    def __init__(self, parent: Tk | Frame) -> None:
        super().__init__(parent)
        self.parent = parent
        self.widget_width = 30
        self.widget_height = 3
        self.set_frame()

    def set_frame(self) -> None:
        frame_2D = self.set_2D_frame()
        frame_3D = self.set_3D_frame()
        frame_common = self.set_common_frame()
        frame_2D.grid(row=0, column=0)
        frame_3D.grid(row=0, column=1)
        frame_common.grid(row=1, column=0, columnspan=2)
        # 四隅に寄せる
        self.grid_rowconfigure(0, weight=2, pad=0)
        self.grid_columnconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=2)
        self.grid_columnconfigure(1, weight=2)

    def set_common_frame(self) -> LabelFrame:
        frame = LabelFrame(self, text="操作方法 共通")

        Label(frame, text="スタート画面に戻る", width=self.widget_width, height=self.widget_height).grid(row=0, column=0)
        Label(frame, text="迷路を開く", width=self.widget_width, height=self.widget_height).grid(row=1, column=0)
        Label(frame, text="操作方法を確認する", width=self.widget_width, height=self.widget_height).grid(row=2, column=0)
        Label(frame, text="アプリを閉じる", width=self.widget_width, height=self.widget_height).grid(row=3, column=0)

        Label(frame, text="Ctrl + H", width=self.widget_width, height=self.widget_height).grid(row=0, column=1)
        Label(frame, text="Ctrl + D", width=self.widget_width, height=self.widget_height).grid(row=1, column=1)
        Label(frame, text="Ctrl + C", width=self.widget_width, height=self.widget_height).grid(row=2, column=1)
        Label(frame, text="Ctrl + Q", width=self.widget_width, height=self.widget_height).grid(row=3, column=1)

        Label(frame, text="Reset ボタン", width=self.widget_width, height=self.widget_height).grid(row=0, column=2)
        Label(frame, text="Restart ボタン", width=self.widget_width, height=self.widget_height).grid(row=1, column=2)
        Label(frame, text="Solve ボタン", width=self.widget_width, height=self.widget_height).grid(row=2, column=2)
        Label(frame, text="Close ボタン", width=self.widget_width, height=self.widget_height).grid(row=3, column=2)

        Label(frame, text="スタートに戻る", width=self.widget_width, height=self.widget_height).grid(row=0, column=3)
        Label(frame, text="別の迷路を始める", width=self.widget_width, height=self.widget_height).grid(row=1, column=3)
        Label(frame, text="解答を表示する", width=self.widget_width, height=self.widget_height).grid(row=2, column=3)
        Label(frame, text="アプリを閉じる", width=self.widget_width, height=self.widget_height).grid(row=3, column=3)

        return frame

    def set_2D_frame(self) -> LabelFrame:
        frame = LabelFrame(self, text="操作方法 2D", padx=1, pady=10)

        Label(frame, text="上に進む", width=self.widget_width, height=self.widget_height).grid(row=0, column=0)
        Label(frame, text="右に進む", width=self.widget_width, height=self.widget_height).grid(row=1, column=0)
        Label(frame, text="左に進む", width=self.widget_width, height=self.widget_height).grid(row=2, column=0)
        Label(frame, text="下に進む", width=self.widget_width, height=self.widget_height).grid(row=3, column=0)

        Label(frame, text="↑", width=self.widget_width, height=self.widget_height).grid(row=0, column=1)
        Label(frame, text="→", width=self.widget_width, height=self.widget_height).grid(row=1, column=1)
        Label(frame, text="←", width=self.widget_width, height=self.widget_height).grid(row=2, column=1)
        Label(frame, text="↓", width=self.widget_width, height=self.widget_height).grid(row=3, column=1)

        return frame

    def set_3D_frame(self) -> LabelFrame:
        frame = LabelFrame(self, text="操作方法 3D", padx=1, pady=10)

        Label(frame, text="前に進む", width=self.widget_width, height=self.widget_height).grid(row=0, column=0)
        Label(frame, text="右を向く", width=self.widget_width, height=self.widget_height).grid(row=1, column=0)
        Label(frame, text="左を向く", width=self.widget_width, height=self.widget_height).grid(row=2, column=0)
        Label(frame, text="後ろを向く", width=self.widget_width, height=self.widget_height).grid(row=3, column=0)

        Label(frame, text="↑", width=self.widget_width, height=self.widget_height).grid(row=0, column=1)
        Label(frame, text="→", width=self.widget_width, height=self.widget_height).grid(row=1, column=1)
        Label(frame, text="←", width=self.widget_width, height=self.widget_height).grid(row=2, column=1)
        Label(frame, text="↓", width=self.widget_width, height=self.widget_height).grid(row=3, column=1)

        return frame
