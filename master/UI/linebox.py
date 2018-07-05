"""line box class"""
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets


class LineNumberArea(QtWidgets.QWidget):


    def __init__(self, editor):
        super().__init__(editor)
        self.myeditor = editor


    def sizeHint(self):
        return QtCore.Qsize(self.editor.lineNumberAreaWidth(), 0)


    def paintEvent(self, event):
        self.myeditor.lineNumberAreaPaintEvent(event)


class CodeEditor(QtWidgets.QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.lineNumberArea = LineNumberArea(self)

        # self.connect(self, QtCore.SIGNAL('blockCountChanged(int)'), self.updateLineNumberAreaWidth)
        # self.connect(self, QtCore.SIGNAL('updateRequest(QRect,int)'), self.updateLineNumberArea)
        # self.connect(self, QtCore.SIGNAL('cursorPositionChanged()'), self.highlightCurrentLine)
        # pyQt5使用下面的方法
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        
        self.updateLineNumberAreaWidth(0)

        self.font_size = 9


    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space


    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)


    def updateLineNumberArea(self, rect, dy):

        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),
                       rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)


    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect();
        self.lineNumberArea.setGeometry(QtCore.QRect(cr.left(), cr.top(),
                    self.lineNumberAreaWidth(), cr.height()))


    def lineNumberAreaPaintEvent(self, event):
        mypainter = QtGui.QPainter(self.lineNumberArea)

        mypainter.fillRect(event.rect(), QtCore.Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                mypainter.setPen(QtCore.Qt.black)
                mypainter.drawText(0, top, self.lineNumberArea.width(), height, QtCore.Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1


    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QtWidgets.QTextEdit.ExtraSelection()

            lineColor = QtGui.QColor(QtCore.Qt.yellow).lighter(160)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)


    def set_font_size(self, font_size):
        """set font size"""
        self.font_size = font_size
        font = QtGui.QFont("Courier", self.font_size)
        self.setFont(font)


    def get_font_size(self):
        """get font size"""
        return self.font_size


    def zoomOut(self):
        """change font"""
        self.font_size = max(self.font_size - 1, 1)
        font = QtGui.QFont("Courier", self.font_size)
        self.setFont(font)


    def zoomIn(self):
        """change font"""
        self.font_size = min(self.font_size + 1, 30)
        font = QtGui.QFont("Courier", self.font_size)
        self.setFont(font)
