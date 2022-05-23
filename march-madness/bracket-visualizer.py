from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus.frames import Frame
def add_image(image_path):
    c = canvas.Canvas("predictions/test.pdf", pagesize=letter)
    c.drawImage(image_path, 6, -10, width=600, height=800)
    c.setFontSize(16)
    c.drawString(190, 770, "2003")
    c.setFillColorRGB(1, 0, 0)
    c.setFillColorRGB(0, 1, 0)
    c.setFontSize(7)

    text_alignment = {
        "left" : c.drawRightString,
        "right" : c.drawString
    }

    text_location = {
        "left" : lambda x: x+64,
        "right" : lambda x: x
    }

    def draw_round1(x, y, dir):
        for i in range(8):
            text_alignment[dir](text_location[dir](x), y, 'North Carolina Central'[:18])
            text_alignment[dir](text_location[dir](x), y-17, 'North Caroaana Central'[:18])
            y -= 30.5

    def draw_round2(x, y, dir):
        for i in range(4):
            text_alignment[dir](text_location[dir](x), y, 'North Carolina Central'[:18])
            text_alignment[dir](text_location[dir](x), y-17, 'North Carolina Central'[:18])
            y -= 61
    
    def draw_round3(x, y, dir):
        for i in range(2):
            text_alignment[dir](text_location[dir](x), y, 'Miami'[:18])
            text_alignment[dir](text_location[dir](x), y-45, 'North Carolina Central'[:18])
            y -= 123

    def draw_round4(x, y, dir):
            text_alignment[dir](text_location[dir](x), y, 'North Carolina Central'[:18])
            text_alignment[dir](text_location[dir](x), y-105, 'North Carolina Central'[:18])

    def draw_round5():
        c.drawRightString(255, 395, 'Miami'[:18])
        c.drawRightString(255, 350, 'Miami'[:18])
        c.drawString(351, 395, 'Miami'[:18])
        c.drawString(351, 350, 'Miami'[:18])
        
    # draw_round5()

    def draw_round6():
        c.drawString(259, 377, 'Miasdfasdfasdfasdfsadfmi'[:18])
        c.drawRightString(347, 370, 'Miaasfasdfasfasdfmi'[:18])
        c.drawCentredString(303, 400, "Miami")

    draw_round6()

    # # top left
    # draw_round1(20, 655, "left")
    # draw_round2(90, 640, "left")
    # draw_round3(160, 625, "left")
    # draw_round4(230, 595, "left")

    # # bottom left
    # draw_round1(20, 318, "left")
    # draw_round2(90, 303, "left")
    # draw_round3(160, 288, "left")
    # draw_round4(230, 258, "left")

    # # top right
    # draw_round1(528, 655, "right")
    # draw_round2(458, 640, "right")
    # draw_round3(388, 625, "right")
    # draw_round4(318, 595, "right")

    # #bottom right
    # draw_round1(528, 318, "right")
    # draw_round2(458, 303, "right")
    # draw_round3(388, 288, "right")
    # draw_round4(318, 258, "right")



    c.save()
if __name__ == '__main__':
    image_path = 'predictions/empty-bracket.png'
    add_image(image_path)



    '''
    
    def demo1(canvas):

    bodyStyle = ParagraphStyle('Body', fontName=_baseFontName, fontSize=24, leading=28, spaceBefore=6)
    para1 = Paragraph('Spam spam spam spam. ' * 5, bodyStyle)
    para2 = Paragraph('Eggs eggs eggs. ' * 5, bodyStyle)
    mydata = [para1, para2]

    #this does the packing and drawing.  The frame will consume
    #items from the front of the list as it prints them
    frame.addFromList(mydata,canvas) 
    
    '''