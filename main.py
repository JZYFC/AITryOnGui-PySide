import functools
import os
import sys

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QApplication, QFileDialog, QGroupBox, \
    QLineEdit, QMessageBox, QHBoxLayout


class MyWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.time_label = None
        self.generate_button = None
        self.result_image_label = None
        self.result_group_box = None
        self.description = ['人物图片', '衣服图片']
        self.image_group_box = []
        self.image_label = []  # type: [QLabel]
        self.image_file_path_line_edit = []

        self.resize(800, 600)
        # 图片输入
        self.add_image_widgets(0)
        self.add_image_widgets(1)

        # 主界面
        self.input_layout = QVBoxLayout()
        for box in self.image_group_box:
            self.input_layout.addWidget(box)

        self.layout = QHBoxLayout(self)
        self.layout.addLayout(self.input_layout)
        self.add_result_widgets()
        self.layout.addWidget(self.result_group_box)
        self.layout.setStretchFactor(self.input_layout, 1)
        self.layout.setStretchFactor(self.result_group_box, 2)

    def add_result_widgets(self):
        self.result_group_box = QGroupBox("结果")
        result_group_box_layout = QVBoxLayout()
        self.result_group_box.setLayout(result_group_box_layout)
        self.result_image_label = QLabel()
        result_group_box_layout.addWidget(self.result_image_label)
        generate_layout = QHBoxLayout()
        self.generate_button = QPushButton("生成")
        self.time_label = QLabel("生成时间: ")
        self.generate_button.clicked.connect(self.generate)  # type: ignore
        generate_layout.addWidget(self.generate_button)
        generate_layout.addWidget(self.time_label)
        result_group_box_layout.addLayout(generate_layout)
        result_group_box_layout.setStretchFactor(self.result_image_label, 100000)
        result_group_box_layout.setStretchFactor(generate_layout, 1)

    def add_image_widgets(self, number: int):
        self.image_group_box.append(QGroupBox(self.description[number]))
        image_group_box_layout = QVBoxLayout(self.image_group_box[number])
        self.image_group_box[number].setLayout(image_group_box_layout)
        person_layout = QHBoxLayout()
        load_image_button = QPushButton("加载图片")
        load_image_button.clicked.connect(functools.partial(self.load_image, number))  # type: ignore
        self.image_file_path_line_edit.append(QLineEdit())
        self.image_label.append(QLabel())
        self.image_label[number].setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        person_layout.addWidget(self.image_file_path_line_edit[number])
        person_layout.addWidget(load_image_button)
        image_group_box_layout.addLayout(person_layout)
        image_group_box_layout.addWidget(self.image_label[number])

    @Slot()
    def load_image(self, number: int) -> None:
        if len(self.image_file_path_line_edit[number].text()) == 0:
            filepath, _ = QFileDialog.getOpenFileName(
                self,
                "Select one or more files to open",
                str(os.curdir),
                "图片 (*.png *.jpg)"
            )
            self.image_file_path_line_edit[number].setText(filepath)
        else:
            filepath = self.image_file_path_line_edit[number].text()
        if not os.path.exists(filepath):
            QMessageBox.warning(self, '文件不存在', '您所选择的文件不存在')
            self.image_file_path_line_edit[number].setText('')
            return
        self.image_label[number].setPixmap(
            QPixmap(filepath).scaled(self.image_label[number].size(), Qt.AspectRatioMode.KeepAspectRatio,
                                     Qt.TransformationMode.SmoothTransformation)
        )

    @Slot()
    def generate(self):
        if functools.reduce(lambda prev, elem: prev and elem.pixmap() is not None, self.image_label, True):
            self.result_image_label.setPixmap(
                QPixmap(self.image_file_path_line_edit[0].text()).scaled(self.result_image_label.size(),
                                                                  Qt.AspectRatioMode.KeepAspectRatio,
                                                                  Qt.TransformationMode.SmoothTransformation)
            )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())
