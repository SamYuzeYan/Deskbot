from deskbot import constant as cs, controller as ctr, processor as ps
import time


def test_match(controller):
    controller.screen_shot()
    match = ps.match_all(threshold=0.15)
    print(match)


def test_diff(controller):
    controller.screen_shot()
    time.sleep(0.5)
    ps.difference(cs.CURRENT_FRAME, "image_cache/test2.png")


def run():
    controller = ctr.Controller(cs.DUEL_LINKS)
    processor = ps.Processor(controller)
    # test_diff(controller)
    test_match(controller)





