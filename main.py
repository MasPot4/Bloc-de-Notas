import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QMessageBox, QLabel, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QMenu, QAction, QFileDialog, QLineEdit
import tkinter

root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

class textEdit(QTextEdit):
	def __init__(self):
		super(textEdit, self).__init__()

		self.cursor = self.textCursor()

class gotolineWin(QMainWindow):
	def __init__(self):
		super(gotolineWin, self).__init__()
		self.main = textEdit()
		self.label = QLabel(self)
		self.go_line = QLineEdit(self)
		self.buttonGoto = QPushButton("Go to...", self)
		self.buttonCancel = QPushButton("Cancel", self)

		self.initUi()

	def initUi(self):
		self.label.setText("Go to...")
		self.label.move(20, 0)

		self.go_line.move(20, 25)
		self.go_line.resize(260, 20)

		self.buttonGoto.move(20, 60)
		self.buttonGoto.resize(100, 30)
		self.buttonGoto.clicked.connect(lambda: self.GoToLine(int(self.go_line.text())))

		self.buttonCancel.clicked.connect(self.cancel)
		self.buttonCancel.move(180, 60)

		self.setGeometry((width / 2) - 150, (height / 2) - 50, 300, 100)
		self.setWindowTitle("Go to...")

	def GoToLine(self, line):
		# self.main.cursor = self.main.textCursor()
		# self.main.cursor.movePosition(self.main.cursor.Left, self.main.cursor.KeepAnchor, 3)
		# self.main.setTextCursor(self.main.cursor)

		ln = int(line)
		linecursor = QTextCursor(self.main.document().findBlockByLineNumber(ln - 1))
		self.main.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)
		self.main.setTextCursor(linecursor)
		
		self.close()

	def cancel(self):
		self.close()

class writter(QMainWindow):
	def __init__(self):
		super().__init__()
		
		self.textEdit = textEdit()
		self.lineWin = gotolineWin()
		self.setCentralWidget(self.textEdit)

		self.file_name = None

		self.initUi()

	def initUi(self):
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('File')
		editMenu = menubar.addMenu('Edit')
		formatMenu = menubar.addMenu('Format')
		viewMenu = menubar.addMenu("View")
		
		# File Menu		
		new_file = QAction('New', self)
		new_file.setShortcut("Ctrl+N")
		new_file.triggered.connect(self.newfile)

		open_file = QAction('Open...', self)
		open_file.setShortcut("Ctrl+O")
		open_file.triggered.connect(self.openfile)

		save_file = QAction('Save', self)
		save_file.setShortcut("Ctrl+S")
		save_file.triggered.connect(self.savefile)

		save_as_file = QAction('Save As...', self)
		save_as_file.setShortcut("Ctrl+Shift+S")
		save_as_file.triggered.connect(self.saveasfile)

		exit = QAction("Exit", self)
		exit.triggered.connect(self.quit)

		# Edit Menu
		undo_edit = QAction("Undo", self)
		undo_edit.setShortcut("Ctrl+Z")
		undo_edit.triggered.connect(self.undo)

		cut_edit = QAction("Cut", self)
		cut_edit.setShortcut("Ctrl+X")
		cut_edit.triggered.connect(self.cut)

		copy_edit = QAction("Copy", self)
		copy_edit.setShortcut("Ctrl+C")
		copy_edit.triggered.connect(self.copy)

		paste_edit = QAction("Paste", self)
		paste_edit.setShortcut("Ctrl+V")
		paste_edit.triggered.connect(self.paste)

		delete_edit = QAction("Delete", self)
		delete_edit.setShortcut("Supr")
		delete_edit.triggered.connect(self.delete)

		goto_edit = QAction("Go To...", self)
		goto_edit.setShortcut("Ctrl+T")
		goto_edit.triggered.connect(self.gotoline)

		find_editor = QAction("Find", self)
		find_editor.setShortcut("Ctrl+F")

		select_all_edit = QAction("Select All", self)
		select_all_edit.setShortcut("Ctrl+E")

		time_edit = QAction("Date and Time", self)
		time_edit.setShortcut("F5")

		# Format Menu
		font_format = QAction("Font", self)

		# View Menu
		zoom_view = QMenu("Zoom", self)
		zoom_mas_view = QAction("Zoom In", self)
		zoom_mas_view.setShortcut("Ctrl++")
		zoom_menos_view = QAction("Ward Off", self)
		zoom_menos_view.setShortcut("Ctrl+-")
		zoom_pre_view = QAction("Restore Default Zoom", self)
		zoom_pre_view.setShortcut("Ctrl+0")
		zoom_view.addAction(zoom_mas_view)
		zoom_view.addAction(zoom_menos_view)
		zoom_view.addAction(zoom_pre_view)

		statusbar_view = QAction("Status Bar", self)
		
		fileMenu.addAction(new_file)
		fileMenu.addAction(open_file)
		fileMenu.addAction(save_file)
		fileMenu.addAction(save_as_file)
		fileMenu.addSeparator()
		fileMenu.addAction(exit)

		editMenu.addAction(undo_edit)
		editMenu.addSeparator()
		editMenu.addAction(cut_edit)
		editMenu.addAction(copy_edit)
		editMenu.addAction(paste_edit)
		editMenu.addAction(delete_edit)
		editMenu.addSeparator()
		editMenu.addAction(goto_edit)
		editMenu.addAction(find_editor)
		editMenu.addSeparator()
		editMenu.addAction(select_all_edit)
		editMenu.addAction(time_edit)

		viewMenu.addMenu(zoom_view)
		viewMenu.addAction(statusbar_view)

		self.setGeometry((width / 2) - 300, (height / 2) - 250, 600, 500)
		self.setWindowTitle("NotePad 2.0")
		self.show()

	def newfile(self):
		if self.textEdit.toPlainText() != "":
			buttonReply = QMessageBox.question(self, 'Bloc de Notas 2.0', f"You want to save changes to Sin Titulo?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if buttonReply == QMessageBox.Yes:
				self.saveasfile()
			else:
				try:
					name, _ = QFileDialog.getSaveFileName(self, "New File", "New File.txt", "All Files (*.*)")
					url = QUrl.fromLocalFile(name)
					name = url.fileName()
					with open(name, "w") as f:
						f.write("")
					self.textEdit.clear()
					self.file_name = name
				except FileNotFoundError:
					pass
		else:
			try:
				name, _ = QFileDialog.getSaveFileName(self, "New File", "New File.txt", "All Files (*.*)")
				url = QUrl.fromLocalFile(name)
				name = url.fileName()
				with open(name, "w") as f:
					f.write("")
				self.textEdit.clear()
				self.file_name = name
			except FileNotFoundError:
				pass

	def openfile(self):
		if self.textEdit.toPlainText() != "":
			buttonReply = QMessageBox.question(self, 'Bloc de Notas 2.0', f"You want to save changes to Sin Titulo?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if buttonReply == QMessageBox.Yes:
				self.saveasfile()				
			else:
				try:
					name, _ = QFileDialog.getOpenFileName(self, "New File", "New File.txt", "All Files (*.*)")
					url = QUrl.fromLocalFile(name)
					name = url.fileName()
					with open(name, "r") as f:
						content = f.read()
					self.textEdit.setText(content)
				except FileNotFoundError:
					pass
		else:
			try:
				name, _ = QFileDialog.getOpenFileName(self, "New File", "New File.txt", "All Files (*.*)")
				url = QUrl.fromLocalFile(name)
				name = url.fileName()
				with open(name, "r") as f:
					content = f.read()
				self.textEdit.setText(content)
			except FileNotFoundError:
				pass

	def savefile(self):
		if self.textEdit.toPlainText() == "":
			self.newfile()
		elif self.textEdit.toPlainText() != "":
			if self.file_name == None:
				self.saveasfile()
			else:
				with open(self.file_name, "w") as f:
					f.write(self.textEdit.toPlainText())
		elif self.file_name == None:
			self.saveasfile()

	def saveasfile(self):
		try:
			name, _ = QFileDialog.getSaveFileName(self,'Save File', "New File.txt", "All Files (*.*)")
			with open(name, "w") as f:
				f.write(self.textEdit.toPlainText())
			self.file_name = name
		except FileNotFoundError:
			pass

	def quit(self):
		sys.exit()

	def undo(self):
		self.textEdit.undo()

	def cut(self):
		self.textEdit.copy()
		self.textEdit.insertPlainText("")

	def copy(self):
		self.textEdit.copy()

	def paste(self):
		text = QApplication.clipboard().text()
		self.textEdit.insertPlainText(text)

	def delete(self):
		self.textEdit.insertPlainText("")

	def gotoline(self):
		self.lineWin.show()

app = QApplication(sys.argv)
Window = writter()
sys.exit(app.exec_())