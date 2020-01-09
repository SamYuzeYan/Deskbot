from deskbot import constant as cs, controller as ctr, processor as ps


def run():
    controller = ctr.Controller(cs.DUEL_LINKS)
    processor = ps.Processor(controller)
    # processor.parse_text()
    controller.screen_shot("image_cache/test.png")
    match = ps.match("templates/initiate_button.png", "image_cache/test.png")
    print(match)




