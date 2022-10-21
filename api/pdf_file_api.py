from flask_restful import Resource


class PdfFileManager(Resource):
    """
    Класс-менеджер для создания и отправки pdf-файла с заключением в виде цены и форматированным стилем
    Как я посмотрел, можно использовать библиотеку ptext
    {@link https://habr.com/ru/company/skillfactory/blog/556936/}
    """

    def post(self):
        pass

    def get(self):
        pass


class PDFCreator(object):
    def __int__(self):
        pass

    def create(self):
        """
        Функция заглушка
        :return: pdf файл
        """
        from borb.pdf import Document
        from borb.pdf import Page
        from borb.pdf import MultiColumnLayout
        from borb.pdf import Paragraph
        from borb.pdf import PDF
        from borb.io.read.types import Decimal

        pdf = Document()

        page = Page()
        pdf.add_page(page)

        # use a PageLayout (SingleColumnLayout in this case)
        layout = MultiColumnLayout(page)

        # add a Paragraph object
        layout.add(Paragraph("Hello World!", font_size=Decimal(20), font="Helvetica"))

        # store the PDF
        # print(pdf.get_page(0))
        with open("output.pdf", "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)


if __name__ == "__main__":
    p = PDFCreator()
    p.create()
