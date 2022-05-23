from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import pandas as pd

games = pd.read_csv("brackets/2022-bracket.csv")
regions = games[-1:]
regions = list(regions.iloc[0])[:-1]
games = games[:-1]
positions = ["top left", "bottom left", "top right", "bottom right"]
games["prediction"] = games["winner"]

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

    def draw_round1(x, y, dir, df):
        df = df[df["round"] == 1]
        games = list(zip(df["winner"], df["loser"], df["prediction"]))
        print(games)

        c.setFontSize(7)
        for i in range(8):
            winner, loser, prediction = games.pop(0)
            text_alignment[dir](text_location[dir](x), y, 'North Carolina Central'[:18])
            text_alignment[dir](text_location[dir](x), y-17, 'North Caroaana Central'[:18])
            y -= 30.5

    def draw_round2(x, y, dir, df):
        c.setFontSize(7)
        for i in range(4):
            text_alignment[dir](text_location[dir](x), y, 'North Carolina Central'[:18])
            text_alignment[dir](text_location[dir](x), y-17, 'North Carolina Central'[:18])
            y -= 61
    
    def draw_round3(x, y, dir, df):
        c.setFontSize(7)
        for i in range(2):
            text_alignment[dir](text_location[dir](x), y, 'Miami'[:18])
            text_alignment[dir](text_location[dir](x), y-45, 'North Carolina Central'[:18])
            y -= 123

    def draw_round4(x, y, dir, df):
        c.setFontSize(7)
        text_alignment[dir](text_location[dir](x), y, 'North Carolina Central'[:18])
        text_alignment[dir](text_location[dir](x), y-105, 'North Carolina Central'[:18])

    def draw_round5():
        c.setFontSize(7)
        c.drawRightString(255, 395, 'Miami'[:18])
        c.drawRightString(255, 350, 'Miami'[:18])
        c.drawString(351, 395, 'Miami'[:18])
        c.drawString(351, 350, 'Miami'[:18])

    def draw_round6():
        c.setFontSize(7)
        c.drawString(259, 377, 'Miasdfasdfasdfasdfsadfmi'[:18])
        c.drawRightString(347, 370, 'Miaasfasdfasfasdfmi'[:18])
        c.drawCentredString(303, 400, "Miami")

    def draw_region(name, position):
        df = games[games["region"] == name]            
        if position == "top left":
            # draw the region name
            c.setFontSize(20)
            c.setFillColorRGB(0, 0, 0)
            c.drawCentredString(160, 683, name)

            # draw the teams
            draw_round1(20, 655, "left", df)
            draw_round2(90, 640, "left", df)
            draw_round3(160, 625, "left", df)
            draw_round4(230, 595, "left", df)
        elif position == "bottom left":
            # bottom left
            c.setFontSize(20)
            c.setFillColorRGB(0, 0, 0)
            c.drawCentredString(160, 50, name)
            draw_round1(20, 318, "left")
            draw_round2(90, 303, "left")
            draw_round3(160, 288, "left")
            draw_round4(230, 258, "left")
        elif position == "top right":
            # top right
            c.setFontSize(20)
            c.setFillColorRGB(0, 0, 0)
            c.drawCentredString(452, 683, name)
            draw_round1(528, 655, "right")
            draw_round2(458, 640, "right")
            draw_round3(388, 625, "right")
            draw_round4(318, 595, "right")
        elif position == "bottom right":
            #bottom right
            c.setFontSize(20)
            c.drawCentredString(452, 50, name)
            draw_round1(528, 318, "right")
            draw_round2(458, 303, "right")
            draw_round3(388, 288, "right")
            draw_round4(318, 258, "right")
        else:
            print("Invalid position")
            exit(1)
    for name, position in zip(regions, positions):
        if position == "top left":
            draw_region(name, position)

    c.save()
    
if __name__ == '__main__':
    image_path = 'predictions/empty-bracket.png'
    add_image(image_path)