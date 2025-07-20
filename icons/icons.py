from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QColor, QPen, QPolygonF
from PySide6.QtCore import Qt, QRectF, QPointF
from theme.theme import get_app_primary_color, get_app_secondary_color

class IconLabel(QLabel):
    """Custom icon label that creates simple geometric icons when files are missing"""
    def __init__(self, icon_type="default", size=20, parent=None):
        super().__init__(parent)
        self.icon_type = icon_type
        self.icon_size = size
        self.setFixedSize(size, size)
        
        # Make the QLabel itself transparent
        self.setStyleSheet("background-color: transparent;")
        
        self.create_icon()
    
    def create_icon(self):
        if self.icon_type == "logo":
            self.create_app_icon()
            return
        
        pixmap = QPixmap(self.icon_size, self.icon_size)
        pixmap.fill(Qt.transparent)  # Ensure transparent background
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        primary_color = get_app_primary_color()
        secondary_color = get_app_secondary_color()
        
        if self.icon_type == "home":
            self.draw_home_icon(painter, primary_color)
        elif self.icon_type == "image":
            self.draw_image_icon(painter, primary_color)
        elif self.icon_type == "pdf":
            self.draw_pdf_icon(painter, primary_color)
        elif self.icon_type == "pdf_compress":
            self.draw_pdf_compress_icon(painter, primary_color)
        elif self.icon_type == "image_to_pdf":
            self.draw_image_to_pdf_icon(painter, primary_color)
        elif self.icon_type == "pdf_to_image":
            self.draw_pdf_to_image_icon(painter, primary_color)
        elif self.icon_type == "upload":
            self.draw_upload_icon(painter, secondary_color)
        elif self.icon_type == "success_tick":
            self.draw_success_tick_icon(painter, primary_color)
        else:
            self.draw_default_icon(painter, secondary_color)
        
        painter.end()
        self.setPixmap(pixmap)

    def create_app_icon(self):
        """Create green document compression icon"""
        size = self.icon_size
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        margin = size * 0.1
        main_rect = QRectF(margin, margin, size - 2*margin, size - 2*margin)
        painter.setBrush(QColor("#ffffff"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(main_rect, size * 0.15, size * 0.15)

        # Document shape
        doc_top_width = size * 0.35
        doc_bottom_width = size * 0.25
        doc_height = size * 0.45
        doc_center_x = size * 0.5
        doc_top_y = size * 0.15
        doc_bottom_y = doc_top_y + doc_height
        
        doc_path = QPainterPath()
        doc_path.moveTo(doc_center_x - doc_top_width/2, doc_top_y)
        doc_path.lineTo(doc_center_x + doc_top_width/2, doc_top_y)
        doc_path.lineTo(doc_center_x + doc_bottom_width/2, doc_bottom_y)
        doc_path.lineTo(doc_center_x - doc_bottom_width/2, doc_bottom_y)
        doc_path.closeSubpath()
        
        painter.setBrush(QColor("#10b981"))
        painter.drawPath(doc_path)
        
        # Text lines
        painter.setPen(QPen(QColor("#ffffff"), size * 0.008))
        for i in range(3):
            y_pos = doc_top_y + (i + 1) * (doc_height / 5)
            progress = (y_pos - doc_top_y) / doc_height
            line_width = doc_top_width - progress * (doc_top_width - doc_bottom_width)
            line_width *= 0.7
            painter.drawLine(
                QPointF(doc_center_x - line_width/2, y_pos),
                QPointF(doc_center_x + line_width/2, y_pos)
            )
        
        # Compression arrows
        arrow_size = size * 0.08
        left_arrow_x = size * 0.20
        right_arrow_x = size * 0.78
        arrow_y = size * 0.5
        painter.setBrush(QColor("#10b981"))
        
        # Left arrow (points right, toward document)
        left_arrow = QPolygonF([
            QPointF(left_arrow_x, arrow_y - arrow_size),
            QPointF(left_arrow_x + arrow_size, arrow_y),
            QPointF(left_arrow_x, arrow_y + arrow_size)
        ])
        painter.drawPolygon(left_arrow)

        # Right arrow (points left, toward document)
        right_arrow = QPolygonF([
            QPointF(right_arrow_x, arrow_y - arrow_size),
            QPointF(right_arrow_x - arrow_size, arrow_y),
            QPointF(right_arrow_x, arrow_y + arrow_size)
        ])
        painter.drawPolygon(right_arrow)

        # Text label
        painter.setPen(QColor("#10b981"))
        font = painter.font()
        font.setPixelSize(max(12, size // 8))
        font.setBold(True)
        painter.setFont(font)
        text_rect = QRectF(size * 0.2, size * 0.7, size * 0.6, size * 0.2)
        painter.drawText(text_rect, Qt.AlignCenter, "FILE")

        # Compression indicator lines
        painter.setPen(QPen(QColor("#10b981"), size * 0.01, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(QPointF(size * 0.25, size * 0.25), QPointF(size * 0.75, size * 0.25))
        painter.drawLine(QPointF(size * 0.25, size * 0.65), QPointF(size * 0.75, size * 0.65))
        
        painter.end()
        self.setPixmap(pixmap)

    def draw_pdf_compress_icon(self, painter, color):
        size = self.icon_size
        painter.setRenderHint(QPainter.Antialiasing)
        green_color = QColor("#10b981")

        # Document shape with rounded corners
        painter.setPen(Qt.NoPen)
        painter.setBrush(green_color)
        painter.drawRoundedRect(QRectF(0, 0, size, size), size * 0.1, size * 0.1)

        # Folded top-right corner
        fold_color = QColor("#34d399")  # lighter green for fold
        fold_path = QPainterPath()
        fold_size = size * 0.25
        fold_path.moveTo(size, 0)
        fold_path.lineTo(size - fold_size, 0)
        fold_path.lineTo(size, fold_size)
        fold_path.closeSubpath()
        painter.setBrush(fold_color)
        painter.drawPath(fold_path)

        # Horizontal white lines (like "=" symbol)
        line_width = size * 0.6
        line_height = size * 0.06
        line_x = (size - line_width) / 2

        painter.setBrush(Qt.white)
        line1_y = size * 0.35
        line2_y = size * 0.5
        painter.drawRect(QRectF(line_x, line1_y, line_width, line_height))
        painter.drawRect(QRectF(line_x, line2_y, line_width, line_height))

        # "PDF" text
        font = painter.font()
        font.setPixelSize(size * 0.2)
        font.setBold(True)
        font.setFamily("Arial")
        painter.setFont(font)
        painter.setPen(Qt.white)
        painter.drawText(QRectF(0, size * 0.65, size, size * 0.25), Qt.AlignCenter, "PDF")

    def draw_image_to_pdf_icon(self, painter, color):    
        size = self.icon_size
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        
        # Draw the source image (left side) - using your image compression style
        image_size = size * 0.4
        image_x = size * 0.05
        image_y = size * 0.3
        
        # Main image frame with shadow (from your image compress icon)
        painter.setBrush(QColor(0, 0, 0, 30))  # Shadow
        painter.drawRoundedRect(image_x + size * 0.02, image_y + size * 0.02, image_size, image_size * 0.8, 3, 3)
        
        # Image background (blue from your theme)
        painter.setBrush(QColor("#4A90E2"))  # Blue for image
        painter.drawRoundedRect(image_x, image_y, image_size, image_size * 0.8, 3, 3)
        
        # Image content - sky
        painter.setBrush(QColor("#87CEEB"))  # Sky
        painter.drawRect(image_x + image_size * 0.08, image_y + image_size * 0.08, 
                        image_size * 0.84, image_size * 0.4)
        
        # Mountains/landscape
        painter.setBrush(QColor("#228B22"))
        landscape = QPainterPath()
        landscape.moveTo(image_x + image_size * 0.08, image_y + image_size * 0.48)
        landscape.lineTo(image_x + image_size * 0.25, image_y + image_size * 0.25)
        landscape.lineTo(image_x + image_size * 0.5, image_y + image_size * 0.35)
        landscape.lineTo(image_x + image_size * 0.75, image_y + image_size * 0.2)
        landscape.lineTo(image_x + image_size * 0.92, image_y + image_size * 0.48)
        landscape.closeSubpath()
        painter.drawPath(landscape)
        
        # Sun
        painter.setBrush(QColor("#FFD700"))
        painter.drawEllipse(image_x + image_size * 0.7, image_y + image_size * 0.15, 
                        image_size * 0.15, image_size * 0.15)
        
        # Draw curved arrow from image to PDF - using a different color for visibility
        painter.setPen(QPen(QColor("#6b7280"), size * 0.025))  # Gray color for arrow
        painter.setBrush(QColor("#6b7280"))
        
        # Create curved arrow path
        arrow_path = QPainterPath()
        start_x = image_x + image_size + size * 0.01
        start_y = image_y + image_size * 0.4
        end_x = size * 0.52
        end_y = size * 0.48
        
        # Control points for the curve
        control1_x = start_x + size * 0.08
        control1_y = start_y - size * 0.08
        control2_x = end_x - size * 0.05
        control2_y = end_y - size * 0.05
        
        arrow_path.moveTo(start_x, start_y)
        arrow_path.cubicTo(control1_x, control1_y, control2_x, control2_y, end_x, end_y)
        
        painter.drawPath(arrow_path)
        
        # Draw arrow head
        arrow_head_size = size * 0.04
        arrow_head_path = QPainterPath()
        arrow_head_path.moveTo(end_x, end_y)
        arrow_head_path.lineTo(end_x - arrow_head_size, end_y - arrow_head_size * 0.8)
        arrow_head_path.lineTo(end_x - arrow_head_size * 0.5, end_y)
        arrow_head_path.lineTo(end_x - arrow_head_size, end_y + arrow_head_size * 0.8)
        arrow_head_path.closeSubpath()
        
        painter.drawPath(arrow_head_path)
        
        # Draw the PDF document (right side) - using your PDF compression style
        pdf_width = size * 0.4
        pdf_height = size * 0.5
        pdf_x = size * 0.52
        pdf_y = size * 0.25
        
        # Document shape with rounded corners (green from your PDF theme)
        green_color = QColor("#10b981")
        painter.setBrush(green_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRectF(pdf_x, pdf_y, pdf_width, pdf_height), 
                            pdf_width * 0.08, pdf_width * 0.08)
        
        # Folded top-right corner (lighter green)
        fold_color = QColor("#34d399")  # lighter green for fold
        fold_size = pdf_width * 0.2
        fold_path = QPainterPath()
        fold_path.moveTo(pdf_x + pdf_width, pdf_y)
        fold_path.lineTo(pdf_x + pdf_width - fold_size, pdf_y)
        fold_path.lineTo(pdf_x + pdf_width, pdf_y + fold_size)
        fold_path.closeSubpath()
        painter.setBrush(fold_color)
        painter.drawPath(fold_path)
        
        # Horizontal white lines (like "=" symbol from your PDF icon)
        line_width = pdf_width * 0.7
        line_height = pdf_height * 0.05
        line_x = pdf_x + (pdf_width - line_width) / 2
        
        painter.setBrush(Qt.white)
        line1_y = pdf_y + pdf_height * 0.35
        line2_y = pdf_y + pdf_height * 0.45
        painter.drawRect(QRectF(line_x, line1_y, line_width, line_height))
        painter.drawRect(QRectF(line_x, line2_y, line_width, line_height))
        
        # "PDF" text
        font = painter.font()
        font.setPixelSize(size * 0.12)
        font.setBold(True)
        font.setFamily("Arial")
        painter.setFont(font)
        painter.setPen(Qt.white)
        painter.drawText(QRectF(pdf_x, pdf_y + pdf_height * 0.6, pdf_width, pdf_height * 0.3), Qt.AlignCenter, "PDF")

    def draw_pdf_to_image_icon(self, painter, color):
        size = self.icon_size
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        
        # Improved color scheme
        pdf_color = QColor("#E74C3C")  # Vibrant red for PDF
        fold_color = QColor("#EC7063")  # Lighter red for fold
        image_bg_color = QColor("#3498DB")  # Blue for image
        arrow_color = QColor("#7F8C8D")  # Neutral gray for arrow
        
        # Draw the PDF document (left side) - cleaner design
        pdf_width = size * 0.4
        pdf_height = size * 0.55
        pdf_x = size * 0.05
        pdf_y = size * 0.2
        
        # Document shape with subtle shadow
        painter.setBrush(QColor(0, 0, 0, 20))
        painter.drawRoundedRect(QRectF(pdf_x + 2, pdf_y + 2, pdf_width, pdf_height), 
                            pdf_width * 0.08, pdf_width * 0.08)
        
        # Main document
        painter.setBrush(pdf_color)
        painter.drawRoundedRect(QRectF(pdf_x, pdf_y, pdf_width, pdf_height), 
                            pdf_width * 0.08, pdf_width * 0.08)
        
        # Folded corner - more subtle
        fold_size = pdf_width * 0.15
        fold_path = QPainterPath()
        fold_path.moveTo(pdf_x + pdf_width, pdf_y)
        fold_path.lineTo(pdf_x + pdf_width - fold_size, pdf_y)
        fold_path.lineTo(pdf_x + pdf_width, pdf_y + fold_size)
        fold_path.closeSubpath()
        painter.setBrush(fold_color)
        painter.drawPath(fold_path)
        
        # Document lines - fewer and more spaced
        line_width = pdf_width * 0.7
        line_height = pdf_height * 0.04
        line_x = pdf_x + (pdf_width - line_width) / 2
        
        painter.setBrush(Qt.white)
        line_spacing = pdf_height * 0.15
        for i in range(3):
            line_y = pdf_y + pdf_height * 0.3 + (i * line_spacing)
            painter.drawRoundedRect(QRectF(line_x, line_y, line_width, line_height), 
                                line_height/2, line_height/2)
        
        # "PDF" text - more prominent
        font = painter.font()
        font.setPixelSize(size * 0.14)
        font.setBold(True)
        font.setFamily("Arial")
        painter.setFont(font)
        painter.setPen(Qt.white)
        painter.drawText(QRectF(pdf_x, pdf_y + pdf_height * 0.7, pdf_width, pdf_height * 0.3), 
                        Qt.AlignCenter, "PDF")
        
        # Draw elegant arrow from PDF to image
        arrow_width = size * 0.02
        painter.setPen(QPen(arrow_color, arrow_width))
        painter.setBrush(arrow_color)
        
        # Curved arrow path with better flow
        arrow_path = QPainterPath()
        start_x = pdf_x + pdf_width + size * 0.01
        start_y = pdf_y + pdf_height * 0.5
        end_x = size * 0.55
        end_y = size * 0.45
        
        # Smooth bezier curve
        control_offset = size * 0.15
        arrow_path.moveTo(start_x, start_y)
        arrow_path.cubicTo(
            start_x + control_offset, start_y - control_offset*0.7,
            end_x - control_offset*0.7, end_y - control_offset,
            end_x, end_y)
        
        painter.drawPath(arrow_path)
        
        # Arrow head - more elegant
        arrow_head_size = size * 0.045
        arrow_head = QPolygonF()
        arrow_head.append(QPointF(end_x, end_y))
        arrow_head.append(QPointF(end_x - arrow_head_size*1.5, end_y - arrow_head_size))
        arrow_head.append(QPointF(end_x - arrow_head_size, end_y))
        arrow_head.append(QPointF(end_x - arrow_head_size*1.5, end_y + arrow_head_size))
        painter.drawPolygon(arrow_head)
        
        # Draw the target image (right side) - more modern
        image_width = size * 0.38
        image_height = size * 0.5
        image_x = size * 0.55
        image_y = size * 0.25
        
        # Image shadow
        painter.setBrush(QColor(0, 0, 0, 25))
        painter.drawRoundedRect(image_x + 3, image_y + 3, image_width, image_height, 5, 5)
        
        # Image frame with border
        painter.setBrush(image_bg_color)
        painter.setPen(QPen(Qt.white, size * 0.008))
        painter.drawRoundedRect(image_x, image_y, image_width, image_height, 5, 5)
        
        # Image content - simplified landscape
        # Sky
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#87CEEB"))
        painter.drawRect(image_x, image_y, image_width, image_height * 0.6)
        
        # Mountains
        mountain_path = QPainterPath()
        mountain_path.moveTo(image_x, image_y + image_height * 0.6)
        mountain_path.lineTo(image_x + image_width * 0.3, image_y + image_height * 0.3)
        mountain_path.lineTo(image_x + image_width * 0.5, image_y + image_height * 0.4)
        mountain_path.lineTo(image_x + image_width * 0.7, image_y + image_height * 0.25)
        mountain_path.lineTo(image_x + image_width, image_y + image_height * 0.6)
        mountain_path.closeSubpath()
        painter.setBrush(QColor("#27AE60"))
        painter.drawPath(mountain_path)
        
        # Sun with rays
        painter.setBrush(QColor("#F1C40F"))
        sun_size = image_width * 0.15
        painter.drawEllipse(QPointF(image_x + image_width * 0.75, image_y + image_height * 0.2), 
                        sun_size/2, sun_size/2)
        
        # "IMG" text at bottom
        font.setPixelSize(size * 0.12)
        painter.setFont(font)
        painter.setPen(Qt.white)
        painter.drawText(QRectF(image_x, image_y + image_height * 0.7, image_width, image_height * 0.3), Qt.AlignCenter, "IMG")
        
    def draw_image_compress_icon(self, painter, color):
        size = self.icon_size
        painter.setPen(Qt.NoPen)
        
        # Main image frame with shadow
        painter.setBrush(QColor(0, 0, 0, 30))  # Shadow
        painter.drawRoundedRect(size * 0.22, size * 0.17, size * 0.56, size * 0.66, 3, 3)
        
        painter.setBrush(QColor("#4A90E2"))  # Blue for image
        painter.drawRoundedRect(size * 0.2, size * 0.15, size * 0.56, size * 0.66, 3, 3)
        
        # Image content - photo-like
        painter.setBrush(QColor("#87CEEB"))  # Sky
        painter.drawRect(size * 0.23, size * 0.18, size * 0.5, size * 0.35)
        
        # Mountains/landscape
        painter.setBrush(QColor("#228B22"))
        landscape = QPainterPath()
        landscape.moveTo(size * 0.23, size * 0.45)
        landscape.lineTo(size * 0.35, size * 0.3)
        landscape.lineTo(size * 0.5, size * 0.38)
        landscape.lineTo(size * 0.65, size * 0.25)
        landscape.lineTo(size * 0.73, size * 0.45)
        landscape.closeSubpath()
        painter.drawPath(landscape)
        
        # Sun
        painter.setBrush(QColor("#FFD700"))
        painter.drawEllipse(size * 0.6, size * 0.2, size * 0.08, size * 0.08)
        
        # Compression arrows
        painter.setBrush(QColor("#FF6B6B"))  # Red for compression
        
        # Left arrow
        left_arrow = QPainterPath()
        left_arrow.moveTo(size * 0.05, size * 0.5)
        left_arrow.lineTo(size * 0.15, size * 0.45)
        left_arrow.lineTo(size * 0.12, size * 0.47)
        left_arrow.lineTo(size * 0.12, size * 0.53)
        left_arrow.lineTo(size * 0.15, size * 0.55)
        left_arrow.closeSubpath()
        painter.drawPath(left_arrow)
        
        # Right arrow
        right_arrow = QPainterPath()
        right_arrow.moveTo(size * 0.95, size * 0.5)
        right_arrow.lineTo(size * 0.85, size * 0.45)
        right_arrow.lineTo(size * 0.88, size * 0.47)
        right_arrow.lineTo(size * 0.88, size * 0.53)
        right_arrow.lineTo(size * 0.85, size * 0.55)
        right_arrow.closeSubpath()
        painter.drawPath(right_arrow)
        
        # Size indicator
        painter.setPen(Qt.white)
        font = painter.font()
        font.setPixelSize(max(6, size // 10))
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(QRectF(size * 0.2, size * 0.65, size * 0.56, size * 0.12), Qt.AlignCenter, "COMPRESS")

    def draw_home_icon(self, painter, color):
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)

        size = self.icon_size
        w, h = size, size

        path = QPainterPath()

        # House roof (triangle)
        path.moveTo(w * 0.2, h * 0.5)
        path.lineTo(w * 0.5, h * 0.2)
        path.lineTo(w * 0.8, h * 0.5)
        
        # House body (rectangle)
        path.lineTo(w * 0.8, h * 0.85)
        path.lineTo(w * 0.2, h * 0.85)
        path.lineTo(w * 0.2, h * 0.5)
        path.closeSubpath()

        painter.drawPath(path)

        # Draw a door (smaller rectangle)
        painter.setBrush(Qt.white)  # or a contrasting color
        door_width = w * 0.15
        door_height = h * 0.25
        door_x = w * 0.5 - door_width / 2
        door_y = h * 0.85 - door_height

        painter.drawRect(door_x, door_y, door_width, door_height)
    
    def draw_image_icon(self, painter, color):
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        
        size = self.icon_size
        # Image frame
        painter.drawRoundedRect(size * 0.1, size * 0.1, size * 0.8, size * 0.8, 2, 2)
        
        # Mountain and sun
        painter.setBrush(Qt.white)
        # Sun
        painter.drawEllipse(size * 0.65, size * 0.25, size * 0.2, size * 0.2)
        # Mountain
        path = QPainterPath()
        path.moveTo(size * 0.2, size * 0.7)
        path.lineTo(size * 0.4, size * 0.45)
        path.lineTo(size * 0.6, size * 0.55)
        path.lineTo(size * 0.8, size * 0.7)
        path.closeSubpath()
        painter.drawPath(path)
    
    def draw_pdf_icon(self, painter, color):
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        
        size = self.icon_size
        # Document shape
        painter.drawRoundedRect(size * 0.2, size * 0.1, size * 0.6, size * 0.8, 2, 2)
        
        # Lines representing text
        painter.setBrush(Qt.white)
        for i in range(3):
            y = size * (0.3 + i * 0.15)
            painter.drawRect(size * 0.3, y, size * 0.4, size * 0.05)
    
    def draw_upload_icon(self, painter, color):
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        
        size = self.icon_size
        # Arrow pointing up
        path = QPainterPath()
        path.moveTo(size * 0.5, size * 0.2)
        path.lineTo(size * 0.3, size * 0.4)
        path.lineTo(size * 0.45, size * 0.4)
        path.lineTo(size * 0.45, size * 0.7)
        path.lineTo(size * 0.55, size * 0.7)
        path.lineTo(size * 0.55, size * 0.4)
        path.lineTo(size * 0.7, size * 0.4)
        path.closeSubpath()
        
        painter.drawPath(path)
        
        # Base line
        painter.drawRect(size * 0.2, size * 0.8, size * 0.6, size * 0.1)

    def draw_success_tick_icon(self, painter, color):
        size = self.icon_size
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        # Circle background
        painter.setBrush(color)
        painter.drawEllipse(0, 0, size, size)

        # White tick mark
        tick_pen = QPen(QColor("#ffffff"), size * 0.15, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(tick_pen)

        # Coordinates for the check mark
        start = QPointF(size * 0.28, size * 0.55)
        mid = QPointF(size * 0.45, size * 0.7)
        end = QPointF(size * 0.75, size * 0.35)

        painter.drawLine(start, mid)
        painter.drawLine(mid, end)

    
    def draw_default_icon(self, painter, color):
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        
        size = self.icon_size
        painter.drawEllipse(size * 0.2, size * 0.2, size * 0.6, size * 0.6)

