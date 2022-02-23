import arcade


class FadingText():
    def __init__(self, amount: int, x: int, y:int, is_damage: bool):
        """
        This deals with damage or healing text being removed or added.

        :param amount: The number that's to be displayed
        :param x: X-Coord of the Parent
        :param y: y-Coord of the Parent
        :param is_damage: True if its damage, false if its healing
        """
        self.__amount = str(amount)
        self.__is_damage = is_damage
        if self.__is_damage is True:
            self.__color = [255, 0, 0, 255]
        else:
            self.__color = [0, 255, 0, 255]

        self.__y_offset = 20
        self.__transparency = 255
        # self.__text_object = arcade.Text(text=self.__amount,
        #                  start_x=x,
        #                  start_y=(y + self.__y_offset),
        #                  color=self.__color)

    def draw(self, x, y):
        """
        This draws the text.

        :param x: X-coord of parent
        :param y: Y-coord of parent
        :return: Returns true if the transparency is <=0 and should stop being drawed
        :rtype: bool
        """
        # self.__color[3] = self.__transparency
        # self.__text_object.color = self.__color
        # self.__text_object.position = (x, (y+self.__y_offset))
        # self.__text_object.draw()
        # self.__y_offset += 1
        # self.__transparency -= 5
        # if self.__transparency > 0:
        #     return False
        # else:
        #     return True

        self.__color[3] = self.__transparency

        arcade.draw_text(text=self.__amount,
                         start_x=x,
                         start_y=y + self.__y_offset,
                         color=self.__color)
        self.__y_offset += 2
        self.__transparency -= 3

        if self.__transparency <= 0:
            return True
        else:
            return False
