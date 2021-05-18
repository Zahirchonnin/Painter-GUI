import sys, os, re
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget, 
    QTableWidgetItem,
    QWidget,
    QLabel,
    QAction,
    QSlider,
    QFileDialog,
    QMessageBox,
    QToolBar,
    QStatusBar,
    QSizePolicy,
    QTabWidget,
    QDockWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QCheckBox,
    QButtonGroup,
    QSpinBox,
    QComboBox,
    QColorDialog,
    QTabWidget
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QImage, QColor, qRgb, QCursor
from PyQt5.QtCore import Qt, QSize, QThread
from painter import GETDATA


class SAVE(QThread):
    def __init__(self, src, colors, new_colors, bg_color, size, options):
        save = GETDATA()
        save.get_position(
            src, 
            colors, 
            new_colors,
            bg_color,
            size,
            options[0], 
            options[1]
            )

class PAINTER(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.initalizeUI()
    
    def initalizeUI(self):

        self.setGeometry(200, 100, 600, 600)
        self.setWindowTitle("PAINTER")
        self.setWindowIcon(QIcon("logo.png"))

        self.colors = {}
        self.createToolBar()
        self.setupTab()
    
    def setupTab(self):
        self.tab_bar = QTabWidget(self)

        self.draw = QLabel()
        self.info = QLabel()

        self.tab_bar.addTab(self.draw, 'Draw')
        self.tab_bar.addTab(self.info, 'informations')

        self.tab1_h_box = QHBoxLayout()
        self.drawTab()
        self.infoTab()
        self.draw.setLayout(self.tab1_h_box)

        self.addToolBar(self.tool_bar)
        self.setCentralWidget(self.tab_bar)
    
    def drawTab(self):
        self.createToolsDockWidget()
        self.createPhotoWidgets()
        self.setStatusBar(QStatusBar(self))
    
    def infoTab(self):
        self.table_widget = QTableWidget(0, 5)
        items = [
            'Selected color', 'New color', 'background color',
            'color option', 'range'
            ]
        
        for col, item in enumerate(items):
            self.table_widget.setHorizontalHeaderItem(col, QTableWidgetItem(item))
        self.insert_row = QPushButton()
        self.insert_row.setIcon(QIcon('insert.webp'))
        self.insert_row.setIconSize(QSize(32, 32))
        self.insert_row.setShortcut('Ctrl+I')
        self.insert_row.setDisabled(True)
        self.insert_row.clicked.connect(self.insertRow)
        self.tab2_h_box = QHBoxLayout()
        self.tab2_h_box.addWidget(self.table_widget)
        self.tab2_h_box.addWidget(self.insert_row)
        self.info.setLayout(self.tab2_h_box)

    def createToolsDockWidget(self):

        self.dock_tools = QDockWidget()
        self.dock_tools.setObjectName('tools')
        self.dock_tools.setWindowTitle('add data | draw')
        self.dock_tools.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.tools_contents = QWidget()

        self.color_picker = QPushButton()
        self.color_picker.setCursor(QCursor(Qt.PointingHandCursor))
        self.color_picker.setIcon(QIcon('picker.png'))
        self.color_picker.setIconSize(QSize(50, 50))
        self.color_picker.setStatusTip('Color picker')
        self.color_picker.clicked.connect(self.pickColor)

        range_h_box = QHBoxLayout()
        range_h_box.addWidget(QLabel('Range:'))
        self.range = QSpinBox()
        self.range.setCursor(QCursor(Qt.PointingHandCursor))
        self.range_slider = QSlider(Qt.Horizontal)
        self.range_slider.setCursor(QCursor(Qt.PointingHandCursor))
        self.range_slider.setMaximum(255)
        self.range_slider.valueChanged['int'].connect(self.updateRange)
        self.range.valueChanged['int'].connect(self.updateRange)
        self.range.setStatusTip("Choose a range to select color.")
        self.range.setRange(1, 255)
        self._range = []
        range_h_box.addWidget(self.range_slider)
        range_h_box.addWidget(self.range)

        option_h_box = QHBoxLayout()
        color_option = QButtonGroup(self)
        self.skip_draw = []
        self.skip_color = QCheckBox('Skip')
        self.skip_color.setStatusTip('Skip choosed color.')
        option_h_box.addWidget(self.skip_color)

        self.draw_color = QCheckBox('Draw')
        self.draw_color.setStatusTip('Draw choosed color.')
        self.draw_color.setChecked(True)

        option_h_box.addWidget(self.draw_color)
        color_option.addButton(self.skip_color)
        color_option.addButton(self.draw_color)


        self.change_color = QPushButton()
        self.change_color.setCursor(QCursor(Qt.PointingHandCursor))
        self.change_color.setIcon(QIcon('change.png'))
        self.change_color.setIconSize(QSize(50, 50))
        self.change_color.setStatusTip("Change color")
        self.change_color.clicked.connect(self.changeColor)

        self.add_color = QPushButton()
        self.add_color.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_color.setIcon(QIcon('add.png'))
        self.add_color.setIconSize(QSize(50, 50))
        self.add_color.setStatusTip('add selected color.')
        self.add_color.clicked.connect(self.addColor)
        self.add_color.setDisabled(True)

        self.bg_color_b = QPushButton()
        self.bg_color_b.setCursor(QCursor(Qt.PointingHandCursor))
        self.bg_color_b.setIcon(QIcon('bg.png'))
        self.bg_color_b.setIconSize(QSize(50, 50))
        self.bg_color_b.setStatusTip("Select background color.")
        self.bg_color_b.clicked.connect(self.selectBgColor)
        self.bg_color = (255, 255, 255)

        self.choose_draw = QComboBox()
        self.choose_draw.setStatusTip("Choose a item to draw")
        self.choose_draw.setMaximumSize(QSize(100, 25))
        for data in os.listdir('.\\data'):
            if data.endswith('.json'):
                try:
                    data = re.compile(r'(.*)\..*\.json', re.DOTALL).findall(data)[0]
                except:
                    data = re.compile(r'(.*)\.json', re.DOTALL).findall(data)[0]
                self.choose_draw.addItem(data)

        

        self.start_draw = QPushButton()
        self.start_draw.setCursor(QCursor(Qt.PointingHandCursor))
        self.start_draw.setShortcut('Ctrl+D')
        self.start_draw.setIcon(QIcon('start.png'))
        self.start_draw.setIconSize(QSize(50, 50))
        self.start_draw.setStatusTip('Start drawing selected.')
        self.start_draw.setToolTip('Start drawing the selected colors')
        self.start_draw.clicked.connect(self.startDrawing)
        self.start_draw.setDisabled(True)
        if self.choose_draw.currentText(): self.start_draw.setEnabled(True)

        dock_v_box = QVBoxLayout()
        dock_v_box.addWidget(self.color_picker)
        dock_v_box.addLayout(range_h_box)
        dock_v_box.addLayout(option_h_box)
        dock_v_box.addWidget(self.change_color)
        dock_v_box.addWidget(self.add_color)
        dock_v_box.addSpacing(3)
        dock_v_box.addWidget(self.bg_color_b)
        dock_v_box.addStretch(1)
        dock_v_box.addWidget(self.choose_draw)
        dock_v_box.addWidget(self.start_draw)

        self.tools_contents.setLayout(dock_v_box)
        self.dock_tools.setWidget(self.tools_contents)
        
        self.dock_tools.setMaximumWidth(200)
        self.tab1_h_box.addWidget(self.dock_tools)
    

    def createToolBar(self):
        self.tool_bar = QToolBar("Painter Toolbar")
        self.tool_bar.setIconSize(QSize(24, 24))

        open_act = QAction(QIcon('open.png'), 'Open', self)
        open_act.setShortcut('Ctrl+O')
        open_act.setStatusTip("Open image")
        open_act.triggered.connect(self.openImage)

        clear_act = QAction(QIcon('clear.png'), 'Clear', self)
        clear_act.setShortcut('Ctrl+N')
        clear_act.setStatusTip("clear image")
        clear_act.triggered.connect(self.clearImage)

        self.save_act = QAction(QIcon('save.png'), 'Save', self)
        self.save_act.setShortcut('Ctrl+S')
        self.save_act.setStatusTip("save entred data")
        self.save_act.setDisabled(True)
        self.save_act.triggered.connect(self.saveDraw)

        exit_act = QAction(QIcon('exit.png'), 'Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip("Quit the program")
        exit_act.triggered.connect(self.close)

        self.tool_bar.addActions([open_act, clear_act, self.save_act, exit_act])
        
    
    def createPhotoWidgets(self):

        self.image = QPixmap()
        self.image_label = QLabel("Image")
        self.image_label.setAlignment(Qt.AlignCenter)

        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        self.image_label.setFont(QFont("Arial", 20))

        self.image_label.setObjectName("image_label")
        self.tab1_h_box.addWidget(self.image_label)

    
    def pickColor(self):
        self.color = QColorDialog.getColor()
        self.color = self.color.getRgb()
        self.add_color.setEnabled(True)

    def insertRow(self):
        self.table_widget.insertRow(self.table_widget.rowCount())

    def changeColor(self):
        self.new_color = QColorDialog.getColor()
        self.new_color = self.new_color.getRgb()
        

    def addColor(self):
        self.save_act.setEnabled(True)
        self.colors[self.color] = self.color
        try:
            self.colors[self.color] = self.new_color
            del self.new_color
        
        except:
            pass

        if self.draw_color.isChecked():
            self.skip_draw.append('draw')
        
        elif self.skip_color.isChecked():
            self.skip_draw.append('skip')
        
        self._range.append(int(self.range.text()))

        index = self.table_widget.rowCount()
        self.table_widget.insertRow(index)
        self.table_widget.setItem(index, 0, QTableWidgetItem(str(self.color)))
        self.table_widget.setItem(index, 1, QTableWidgetItem(str(self.colors[self.color])))
        self.table_widget.setItem(index, 2, QTableWidgetItem(str(self.bg_color)))
        self.table_widget.setItem(index, 3, QTableWidgetItem(self.skip_draw[-1]))
        self.table_widget.setItem(index, 4, QTableWidgetItem(self.range.text()))

    
    def selectBgColor(self):
        self.bg_color = QColorDialog.getColor()
        self.bg_color = self.bg_color.getRgb()
        for bg_row in range(self.table_widget.rowCount()):
            self.table_widget.setItem(bg_row, 2, QTableWidgetItem(str(self.bg_color)))
        

    def updateRange(self, value):
        self.range.setValue(value)
        self.range_slider.setValue(value)

    def saveDraw(self):
        colors = []
        new_colors = []
        bg_color = eval(self.table_widget.item(0, 2).text())
        skip_draw = []
        _range = []
        for row in range(self.table_widget.rowCount()):
            try:
                colors.append(eval(self.table_widget.item(row, 0).text()))
                new_colors.append(eval(self.table_widget.item(row, 1).text()))
                skip_draw.append(self.table_widget.item(row, 3).text())
                _range.append(int(self.table_widget.item(row, 4).text()))
            
            except AttributeError:
                break

        size = (self.image_label.width(), self.image_label.height())
        SAVE(
            self.image_file,
            colors,
            new_colors,
            bg_color,
            size,
            [skip_draw, _range] # Options
        )

        available_draw = [self.choose_draw.itemText(i) for i in range(self.choose_draw.count())]
        for data in os.listdir('..\\data'):
            if data.endswith('.json'):
                data = data.replace('.json', '')
                if data not in available_draw:
                    self.choose_draw.addItem(data)

        self.start_draw.setEnabled(True)

    def startDrawing(self):
        way = QMessageBox.question(
            self, 'way', 'Do you want to draw with paint??', QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No)
        
        if way == QMessageBox.Yes: way = True
        else: way = False
        
        start = GETDATA()
        
        self.image = QPixmap(start.draw_image(
            self.choose_draw.currentText() + '.json',
            way
        ))
        self.image_label.setPixmap(
                self.image.scaled(
                    self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
                            )
                        )

    def openImage(self):
        self.insert_row.setEnabled(True)
        self.image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
        "JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;Bitmap Files (*.bmp)")
        
        if self.image_file:
            cursor = QPixmap('.\\cursor.png')
            cursor_scaled_pix = cursor.scaled(QSize(20, 20), Qt.KeepAspectRatio)
            self.image_label.setCursor(QCursor(cursor_scaled_pix, 1, 1))
            try:
                self.color
                self.add_color.setEnabled(True)
            except:
                pass
        
            self.image = QPixmap(self.image_file)
            self.image_label.setPixmap(
                self.image.scaled(
                    self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
                            )
                        )

    def clearImage(self):
        self.image_label.clear()
        self.image_label.setText("Image")
        self.save_act.setDisabled(True)
        self.add_color.setDisabled(True)

        self.colors = []
        self.new_colors = []
        self.table_widget.clear()
        items = [
            'Selected color', 'New color', 'background color',
            'color option', 'range'
            ]
        
        for col, item in enumerate(items):
            self.table_widget.setHorizontalHeaderItem(col, QTableWidgetItem(item))

def main():
    app = QApplication(sys.argv)
    editor = PAINTER()
    style_sheet = """

        QMainWindow {
            background-color: #98b2db
        }

        #image_label {
            border: 5px solid black;
            border-radius: 1px;
        }

        QStatusBar {
            background-color: #bfb8b7;
            border: 1px solid white;
            color: black
        }

        QPushButton {
            background-color: #623580;
            border-radius: 4px;
            padding: 6px;
            color: #DFD8D7
        }

        QPushButton:hover {
            background-color: #AB88C3
        }

        QPushButton:pressed {
            background-color: #280D3A
        }

        QToolBar {
            background-color: #cc98db
        }

        QSlider:groove:horizontal{
            border: 1px solid #000000;
            background: white;
            height: 10 px;
            border-radius: 4px
        }
        
        QSlider::add-page:horizontal {
            background: #FFFFFF;
            border: 1px solid #4C4B4B;
            height: 10px;
            border-radius: 4px;
        }

        QSlider::handle:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #EEEEEE, stop:1 #CCCCCC);
            border: 1px solid #4C4B4B;
            width: 13px;
            margin-top: -3px;
            margin-bottom: -3px;
            border-radius: 4px;
        }

        QSlider::handle:horizontal:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #FFFFFF, stop:1 #DDDDDD);border: 1px solid #393838;
            border-radius: 4px;
        }

        QSlider:sub-page:horizontal{
        background: qlineargradient(x1: 1, y1: 0, x2: 0, y2: 1,
        stop: 0 #FF4242, stop: 1 #1C1C1C);
        background: qlineargradient(x1: 0, y1: 1, x2: 1, y2: 1,
        stop: 0 #1C1C1C, stop: 1 #00FF00);
        border: 1px solid #4C4B4B;
        height: 10px;
        border-radius: 4px;
        }

        QTableWidget {
            background-color: #C1BEBE;
            border: 6px dashed black;
        
        }
        QTabBar::tab:: {
            width: 0; height: 0; margin: 0; padding: 0; border: none;
        }

    """
    editor.setStyleSheet(style_sheet)
    editor.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()